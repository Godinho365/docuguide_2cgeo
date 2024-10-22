# recursos/views.py
from django.shortcuts import render, redirect, get_object_or_404
from .models import DevProject, Mensagem
from .forms import DevProjectForm, MensagemForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages

def list_projects(request):
    projects = DevProject.objects.all()
    return render(request, 'projectdev/project_list.html', {'projects': projects})

def cria_projeto(request):
    if request.method == 'POST':
        form = DevProjectForm(request.POST)
        if form.is_valid():
            form.save()  # Salva o projeto no banco de dados
            return redirect('list_projects')  # Redireciona para a lista de projetos após salvar
    else:
        form = DevProjectForm()
    
    return render(request, 'projectdev/create_project.html', {'form': form})

def edita_projeto(request, id):
    projeto = get_object_or_404(DevProject, pk=id)  # Busca o projeto pelo ID

    if request.method == 'POST':
        # Preenche o formulário com os dados do projeto existente
        form = DevProjectForm(request.POST, instance=projeto)  
        if form.is_valid():
            form.save()  # Salva as alterações no banco de dados
            return redirect('list_projects')  # Redireciona para a lista de projetos após salvar
    else:
        # Cria um formulário preenchido com os dados do projeto existente
        form = DevProjectForm(instance=projeto)  
    
    # Renderiza o template com o formulário
    return render(request, 'projectdev/create_project.html', {'form': form})

def view_observacoes(request, projeto_id):
    projeto = get_object_or_404(DevProject, id=projeto_id)
    mensagens = Mensagem.objects.filter(projeto=projeto).order_by('-data')  # Obter mensagens do projeto
    form_mensagem = MensagemForm()  # Instanciar o formulário de Mensagem

    if request.method == 'POST':
        form_mensagem = MensagemForm(request.POST)  # Reinstanciar o formulário de mensagem
        if form_mensagem.is_valid():
            mensagem = form_mensagem.save(commit=False)
            mensagem.projeto = projeto
            mensagem.integrante = request.user
            mensagem.save()
            return redirect('view_observacoes', projeto_id=projeto.id)

    return render(request, 'projectdev/view_observacoes.html', {
        'projeto': projeto,
        'form_mensagem': form_mensagem,
        'mensagens': mensagens,  # Adiciona mensagens ao contexto
    })

@login_required
def excluir_mensagem(request, pk):
    mensagem = get_object_or_404(Mensagem, pk=pk)

    # Verifica se o usuário tem permissão para excluir a mensagem (autor ou superuser)
    if request.user != mensagem.integrante and not request.user.is_superuser:
        messages.error(request, 'Você não tem permissão para excluir esta mensagem.')
        return redirect('view_observacoes', projeto_id=mensagem.projeto.id)  # Incluindo projeto_id

    if request.method == 'POST':
        mensagem.delete()
        messages.success(request, 'Mensagem excluída com sucesso.')
        return redirect('view_observacoes', projeto_id=mensagem.projeto.id)  # Incluindo projeto_id

    return render(request, 'projectdev/excluir_mensagem.html', {'mensagem': mensagem})



@login_required
def editar_mensagem(request, pk):
    mensagem = get_object_or_404(Mensagem, pk=pk)

    # Verifica se o usuário tem permissão para editar a mensagem (autor ou superuser)
    if request.user != mensagem.integrante and not request.user.is_superuser:
        messages.error(request, 'Você não tem permissão para editar esta mensagem.')
        return redirect('view_observacoes', projeto_id=mensagem.projeto.id)  # Incluindo projeto_id

    if request.method == 'POST':
        form = MensagemForm(request.POST, instance=mensagem)
        if form.is_valid():
            form.save()
            messages.success(request, 'Mensagem atualizada com sucesso.')
            return redirect('view_observacoes', projeto_id=mensagem.projeto.id)  # Incluindo projeto_id
    else:
        form = MensagemForm(instance=mensagem)

    return render(request, 'projectdev/editar_mensagem.html', {'form': form, 'mensagem': mensagem})

def user_project_list(request):
    # Lista os projetos em que o usuário é o responsável ou integrante
    projects = DevProject.objects.filter(responsavel=request.user) | DevProject.objects.filter(demais_integrantes=request.user)
    return render(request, 'projectdev/user_project_list.html', {'projects': projects})

@login_required
def delete_projeto(request, pk):
    projeto = get_object_or_404(DevProject, id=pk)  # Obtém o projeto ou retorna 404 se não existir

    # Verifica se o usuário tem permissão para excluir o projeto (responsável ou superuser)
    if request.user != projeto.responsavel and not request.user.is_superuser:
        messages.error(request, 'Você não tem permissão para excluir este projeto.')
        return redirect('list_projects')  # Redireciona para a lista de projetos se não tiver permissão

    if request.method == 'POST':
        projeto.delete()  # Deleta o projeto
        messages.success(request, 'Projeto excluído com sucesso.')
        return redirect('list_projects')  # Redireciona para a lista de projetos após a exclusão

    # Renderiza um template de confirmação (opcional)
    return render(request, 'projectdev/confirm_delete.html', {'projeto': projeto})
# users/views.py
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login as auth_login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import user_passes_test
from .forms import GroupForm
from .forms import CustomUserCreationForm
from django.contrib import messages
from .forms import RedefinirEmailForm
from django.contrib.auth.models import User
from .forms import UserGroupForm
from instructions.models import Instruction

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)  # Loga o usuário automaticamente após o registro
            return redirect('profile')  # Redireciona para a página de perfil ou outra página
    else:
        form = CustomUserCreationForm()
    return render(request, 'users/register.html', {'form': form})

@login_required
def update_profile(request):
    if request.method == 'POST':
        form = RedefinirEmailForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'E-mail alterado com sucesso.')
            return redirect('profile')  # Redirecione para uma página de perfil, por exemplo
    else:
        form = RedefinirEmailForm(instance=request.user)

    return render(request, 'users/update_profile.html', {'form': form})

def login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            auth_login(request, user)  # Faz o login do usuário
            return redirect('profile')  # Redireciona para a página de perfil após o login
    else:
        form = AuthenticationForm()
    return render(request, 'users/login.html', {'form': form})

def logout(request):
    auth_logout(request)  # Faz o logout do usuário
    return redirect('login')  # Redireciona para a página de login após o logout

@login_required
def profile(request):
    return render(request, 'users/profile.html')

@user_passes_test(lambda u: u.is_superuser)
def create_group(request):
    if request.method == 'POST':
        form = GroupForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('list_groups')
    else:
        form = GroupForm()
    return render(request, 'users/create_group.html', {'form': form})

@user_passes_test(lambda u: u.is_superuser)
def list_groups(request):
    groups = Group.objects.all().order_by('id')  # Ordena os grupos por ID
    return render(request, 'users/list_groups.html', {'groups': groups})

@user_passes_test(lambda u: u.is_superuser)
def edit_group(request, pk):
    group = get_object_or_404(Group, pk=pk)
    if request.method == 'POST':
        form = GroupForm(request.POST, instance=group)
        if form.is_valid():
            form.save()
            return redirect('list_groups')
    else:
        form = GroupForm(instance=group)
    return render(request, 'users/edit_group.html', {'form': form, 'group': group})

@user_passes_test(lambda u: u.is_superuser)
def delete_group(request, pk):
    group = get_object_or_404(Group, pk=pk)
    if request.method == 'POST':
        group.delete()
        return redirect('list_groups')
    return render(request, 'users/delete_group.html', {'group': group})



@user_passes_test(lambda u: u.is_superuser)
def list_users_and_groups(request):
    query = request.GET.get('search', '')  # Obtém a busca do GET
    if query:
        users = User.objects.filter(username__icontains=query).order_by('date_joined')  # Filtra os usuários
    else:
        users = User.objects.all().order_by('date_joined')  # Obtém todos os usuários se não houver busca

    groups = Group.objects.all()  # Obtém todos os grupos
    context = {
        'users': users,
        'groups': groups,
        'search_query': query  # Passa a consulta de busca para o template
    }
    return render(request, 'users/list_users_and_groups.html', context)




def update_user_groups(request, user_id):
    user = get_object_or_404(User, id=user_id)
    groups = Group.objects.all()

    if request.method == "POST":
        # Obtém os grupos selecionados no formulário
        selected_groups = request.POST.getlist('groups')
        
        # Atualiza os grupos do usuário
        user.groups.set(selected_groups)
        user.save()
        
        messages.success(request, f'Grupos do usuário {user.username} foram atualizados.')
        return redirect('list_users_and_groups')

    return render(request, 'users/update_user_groups.html', {
        'user': user,
        'groups': groups,
    })

@user_passes_test(lambda u: u.is_superuser)
def create_user(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Usuário criado com sucesso!')
            return redirect('list_users_and_groups')
    else:
        form = CustomUserCreationForm()

    context = {
        'form': form
    }
    return render(request, 'users/create_user.html', context)

@user_passes_test(lambda u: u.is_superuser)
def delete_user(request, user_id):
    if not request.user.is_superuser:
        messages.error(request, "Você não tem permissão para excluir usuários.")
        return redirect('list_users_and_groups')
    
    user = get_object_or_404(User, id=user_id)
    
    if request.method == "POST":
        user.delete()
        messages.success(request, f'O usuário {user.username} foi deletado com sucesso.')
        return redirect('list_users_and_groups')
    
    return redirect('list_users_and_groups')

@user_passes_test(lambda u: u.is_superuser)
def toggle_superuser(request, user_id):
    if not request.user.is_superuser:
        messages.error(request, "Você não tem permissão para modificar o status de superusuário.")
        return redirect('list_users_and_groups')
    
    user = get_object_or_404(User, id=user_id)
    
    if request.method == "POST":
        user.is_superuser = not user.is_superuser
        user.save()
        status = "concedido" if user.is_superuser else "removido"
        messages.success(request, f'O status de superusuário foi {status} para o usuário {user.username}.')
        return redirect('list_users_and_groups')
    
    return redirect('list_users_and_groups')


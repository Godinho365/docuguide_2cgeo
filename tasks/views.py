# tasks/views.py
from django.http import HttpResponseForbidden
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Task
from .forms import TaskForm, TaskUpdateFormAssigne  # Assumindo que você criará um formulário
from django.db.models import Q
from django.utils import timezone
from django.contrib import messages

@login_required
def task_detail(request, task_id):
    task = get_object_or_404(Task, id=task_id)

    # Verifica se o usuário é o criador ou o delegado da tarefa
    if task.creator != request.user and task.assignee != request.user:
        return HttpResponseForbidden("Você não tem permissão para ver esta tarefa.")

    return render(request, 'tasks/task_detail.html', {'task': task})

@login_required
def create_task(request):
    if request.method == 'POST':
        form = TaskForm(request.POST, request.FILES)
        if form.is_valid():
            task = form.save(commit=False)
            task.creator = request.user  # Supondo que você tenha um campo para o criador
            task.save()
            return redirect('task_list')  # Redirecione para a lista de tarefas após salvar
    else:
        form = TaskForm()

    return render(request, 'tasks/create_task.html', {'form': form})

@login_required
def task_list(request):
    # Obtém o parâmetro de filtro de status e de data da requisição
    status_filter = request.GET.get('status', '')
    start_date = request.GET.get('start_date', '')
    due_date = request.GET.get('due_date', '')

    # Aplica o filtro de status às tarefas criadas e atribuídas ao usuário
    created_tasks = Task.objects.filter(creator=request.user)
    assigned_tasks = Task.objects.filter(assignee=request.user)

    # Filtragem condicional para status
    if status_filter:
        created_tasks = created_tasks.filter(status=status_filter)
        assigned_tasks = assigned_tasks.filter(status=status_filter)

    # Filtragem condicional para a data de início
    if start_date:
        created_tasks = created_tasks.filter(start_date__gte=start_date)
        assigned_tasks = assigned_tasks.filter(start_date__gte=start_date)

    # Filtragem condicional para a data de vencimento
    if due_date:
        # Usando due_date para filtrar tarefas com vencimento até a data selecionada
        created_tasks = created_tasks.filter(due_date__lte=due_date)
        assigned_tasks = assigned_tasks.filter(due_date__lte=due_date)

    # Contexto para o template
    context = {
        'created_tasks': created_tasks,
        'assigned_tasks': assigned_tasks,
        'status_filter': status_filter,
        'start_date': start_date,
        'due_date': due_date,
    }

    return render(request, 'tasks/task_list.html', context)


def update_task_assigne(request, pk):
    task = get_object_or_404(Task, pk=pk)

    # Verifica se o usuário logado é o responsável pela tarefa
    if request.user != task.assignee:
        messages.error(request, 'Você não tem permissão para atualizar esta tarefa.')
        return redirect('task_detail', task_id=task.pk)  # Redireciona para os detalhes da tarefa

    if request.method == 'POST':
        form = TaskUpdateFormAssigne(request.POST, instance=task)
        if form.is_valid():
            form.save()  # Salva a instância com o novo status e observação
            return redirect('task_detail', task_id=task.pk)  # Redireciona para os detalhes da tarefa após a atualização
    else:
        form = TaskUpdateFormAssigne(instance=task)

    return render(request, 'tasks/update_task_assigne.html', {'form': form, 'task': task})


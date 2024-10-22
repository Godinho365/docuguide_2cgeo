# insumos/views.py
from django.shortcuts import render, redirect, get_object_or_404
from .models import Insumo
from .forms import InsumoForm

def list_insumos(request):
    # Recupera todos os insumos do banco de dados
    insumos = Insumo.objects.all()
    
    # Verifica se o usuário é superusuário ou pertence ao grupo "Insumos"
    is_insumo_group_member = request.user.is_superuser or request.user.groups.filter(name='Insumos').exists()
    
    # Renderiza o template com os insumos e a verificação de grupo
    return render(request, 'insumos/list_insumos.html', {
        'insumos': insumos,
        'is_insumo_group_member': is_insumo_group_member,
    })

def create_insumo(request):
    if request.method == 'POST':
        form = InsumoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('list_insumos')  # Redireciona para a lista de insumos após a criação
    else:
        form = InsumoForm()
    return render(request, 'insumos/insumo_form.html', {'form': form})

def edit_insumo(request, pk):
    insumo = get_object_or_404(Insumo, pk=pk)
    if request.method == 'POST':
        form = InsumoForm(request.POST, instance=insumo)
        if form.is_valid():
            form.save()
            return redirect('list_insumos')  # Redireciona para a lista de insumos após a edição
    else:
        form = InsumoForm(instance=insumo)
    return render(request, 'insumos/insumo_form.html', {'form': form})

def delete_insumo(request, pk):
    insumo = get_object_or_404(Insumo, pk=pk)
    if request.method == 'POST':
        insumo.delete()
        return redirect('list_insumos')  # Redireciona para a lista de insumos após a exclusão
    return render(request, 'insumos/insumo_confirm_delete.html', {'insumo': insumo})

# servers/views.py
from django.shortcuts import render, redirect, get_object_or_404
from .models import Server
from .forms import ServerForm

def list_servers(request):
    servers = Server.objects.all()
    is_server_group_member = request.user.is_superuser or request.user.groups.filter(name='Servidor').exists()
    
    return render(request, 'servers/list_servers.html', {
        'servers': servers,
        'is_server_group_member': is_server_group_member,
    })

def create_server(request):
    if request.method == 'POST':
        form = ServerForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('list_servers')
    else:
        form = ServerForm()
    return render(request, 'servers/server_form.html', {'form': form})

def edit_server(request, pk):
    server = get_object_or_404(Server, pk=pk)
    if request.method == 'POST':
        form = ServerForm(request.POST, instance=server)
        if form.is_valid():
            form.save()
            return redirect('list_servers')
    else:
        form = ServerForm(instance=server)
    return render(request, 'servers/server_form.html', {'form': form})

def delete_server(request, pk):
    server = get_object_or_404(Server, pk=pk)
    if request.method == 'POST':
        server.delete()
        return redirect('list_servers')
    return render(request, 'servers/server_confirm_delete.html', {'server': server})

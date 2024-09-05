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
            return redirect('profile')
    else:
        form = GroupForm()
    return render(request, 'users/create_group.html', {'form': form})

# Verifica se o usuário é superusuário
def is_superuser(user):
    return user.is_superuser

@user_passes_test(is_superuser)
def list_groups(request):
    groups = Group.objects.all()
    return render(request, 'users/list_groups.html', {'groups': groups})

@user_passes_test(is_superuser)
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

@user_passes_test(is_superuser)
def delete_group(request, pk):
    group = get_object_or_404(Group, pk=pk)
    if request.method == 'POST':
        group.delete()
        return redirect('list_groups')
    return render(request, 'users/delete_group.html', {'group': group})
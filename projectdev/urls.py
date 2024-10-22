# recursos/urls.py
from django import views
from django.urls import path
from .views import list_projects, cria_projeto, edita_projeto, view_observacoes, editar_mensagem, excluir_mensagem, user_project_list, delete_projeto

urlpatterns = [
    path('', list_projects, name='list_projects'),
    path('criar/', cria_projeto, name='cria_projeto'),
    path('editar/<int:id>/', edita_projeto, name='edita_projeto'),
    path('projeto/<int:projeto_id>/observacoes/', view_observacoes, name='view_observacoes'),
    path('mensagem/<int:pk>/editar/', editar_mensagem, name='editar_mensagem'),
    path('mensagem/<int:pk>/excluir/', excluir_mensagem, name='excluir_mensagem'),
    path('meus-projetos/', user_project_list, name='user_project_list'),
    path('projeto/<int:pk>/delete/', delete_projeto, name='delete_projeto'),
    
]

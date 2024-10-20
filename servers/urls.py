# servers/urls.py
from django.urls import path
from .views import list_servers, create_server, edit_server, delete_server

urlpatterns = [
    path('', list_servers, name='list_servers'),
    path('add/', create_server, name='create_server'),
    path('edit/<int:pk>/', edit_server, name='edit_server'),
    path('delete/<int:pk>/', delete_server, name='delete_server'),
]

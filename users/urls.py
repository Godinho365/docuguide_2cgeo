# users/urls.py
from django.urls import path
from .views import register, login, logout, profile, create_group, list_groups, edit_group, delete_group

urlpatterns = [
    path('register/', register, name='register'),
    path('login/', login, name='login'),
    path('logout/', logout, name='logout'),
    path('profile/', profile, name='profile'),
    path('create-group/', create_group, name='create_group'),
    path('list-groups/', list_groups, name='list_groups'),
    path('edit-group/<int:pk>/', edit_group, name='edit_group'),
    path('delete-group/<int:pk>/', delete_group, name='delete_group'),
]

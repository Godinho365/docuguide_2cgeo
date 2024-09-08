# users/urls.py
from django.urls import path
from .views import register, login, logout, profile, create_group, list_groups, edit_group, delete_group , update_profile, list_users_and_groups, update_user_groups, create_user, delete_user,toggle_superuser

urlpatterns = [
    path('register/', register, name='register'),
    path('login/', login, name='login'),
    path('logout/', logout, name='logout'),
    path('profile/', profile, name='profile'),
    path('update-profile/', update_profile, name='update_profile'),
    path('create-group/', create_group, name='create_group'),
    path('list-groups/', list_groups, name='list_groups'),
    path('edit-group/<int:pk>/', edit_group, name='edit_group'),
    path('delete-group/<int:pk>/', delete_group, name='delete_group'),
    path('list-users-and-groups/', list_users_and_groups, name='list_users_and_groups'),
    path('update-user-groups/<int:user_id>/', update_user_groups, name='update_user_groups'),
    path('create-user/', create_user, name='create_user'),
    path('delete_user/<int:user_id>/', delete_user, name='delete_user'),
    path('toggle_superuser/<int:user_id>/', toggle_superuser, name='toggle_superuser'),
    
]

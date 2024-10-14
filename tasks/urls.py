# tasks/urls.py
from django.urls import path
from .views import task_list, create_task, task_detail, update_task_assigne


urlpatterns = [
    path('', task_list, name='task_list'),
    path('create/', create_task, name='create_task'),
    path('tasks/<int:task_id>/', task_detail, name='task_detail'),
     path('tasks/<int:pk>/update-assigne/', update_task_assigne, name='update_task_assigne'),
]


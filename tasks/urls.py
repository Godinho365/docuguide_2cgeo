# tasks/urls.py
from django.urls import path
from .views import task_list, create_task, task_detail, update_task_assigne, update_task_creator, delete_task_creator


urlpatterns = [
    path('', task_list, name='task_list'),
    path('create/', create_task, name='create_task'),
    path('tasks/<int:task_id>/', task_detail, name='task_detail'),
    path('tasks/<int:pk>/update-assigne/', update_task_assigne, name='update_task_assigne'),
    path('task/update/<int:task_id>/', update_task_creator, name='update_task_created'),
     path('tasks/<int:pk>/delete/', delete_task_creator, name='delete_task_created'),
]


# tasks/models.py
from django.contrib.auth.models import User
from django.db import models

class Task(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    creator = models.ForeignKey(User, related_name='created_tasks', on_delete=models.CASCADE)  # Quem passou a tarefa
    assignee = models.ForeignKey(User, related_name='assigned_tasks', on_delete=models.CASCADE)  # Quem vai realizar a tarefa
    start_date = models.DateTimeField(null=True, blank=True)
    due_date = models.DateTimeField(null=True, blank=True)
    completion_date = models.DateTimeField(null=True, blank=True)
    observation = models.TextField(blank=True, null=True)
    status = models.CharField(
        max_length=50, 
        choices=[
            ('pending', 'Pendente'), 
            ('in_progress', 'Em Progresso'), 
            ('completed', 'Concluída')
        ],
        default='pending'
    )
    file_attachment = models.FileField(upload_to='task_attachments/', null=True, blank=True)

    def __str__(self):
        return self.title

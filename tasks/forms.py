# tasks/forms.py
from django import forms
from django.core.exceptions import ValidationError
from .models import Task

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description', 'assignee', 'start_date', 'due_date', 'file_attachment', 'status', 'observation']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['title'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Digite o título da tarefa'})
        self.fields['description'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Digite a descrição da tarefa'})
        self.fields['assignee'].widget.attrs.update({'class': 'form-control'})
        # Adiciona o tipo datetime-local aos campos de data
        self.fields['start_date'].widget.attrs.update({'class': 'form-control', 'type': 'datetime-local'})  
        self.fields['due_date'].widget.attrs.update({'class': 'form-control', 'type': 'datetime-local'})    
        self.fields['file_attachment'].widget.attrs.update({'class': 'form-control'})
        self.fields['status'].widget.attrs.update({'class': 'form-control'})
        self.fields['observation'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Digite observações adicionais'})

    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get('start_date')
        due_date = cleaned_data.get('due_date')

        if start_date and due_date:
            if due_date < start_date:
                raise ValidationError("A data de vencimento não pode ser anterior à data de início.")

        return cleaned_data

class TaskUpdateFormAssigne(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['status', 'observation']  # Adiciona o campo de observação

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['status'].widget.attrs.update({'class': 'form-control'})
        self.fields['observation'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Digite observações adicionais'})
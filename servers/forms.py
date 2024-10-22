# servers/forms.py
from django import forms
from .models import Server

class ServerForm(forms.ModelForm):
    class Meta:
        model = Server
        fields = ['name', 'ip_address', 'link', 'username', 'password']
        
        # Customizando os widgets dos campos
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nome do Servidor',
                'required': 'required'
            }),
            'ip_address': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Endereço IP',
                'required': 'required'
            }),
            'link': forms.URLInput(attrs={
                'class': 'form-control',
                'placeholder': 'URL de Acesso',
                'required': 'required'
            }),
            'username': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nome de Usuário',
                'required': 'required'
            }),
            'password': forms.PasswordInput(attrs={
                'class': 'form-control',
                'placeholder': 'Senha',
                'required': 'required'
            }),
        }

# insumos/forms.py
from django import forms
from .models import Insumo

class InsumoForm(forms.ModelForm):
    class Meta:
        model = Insumo
        fields = ['nome', 'tipo', 'local', 'observacao', 'link']
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nome do Insumo'}),
            'tipo': forms.Select(attrs={'class': 'form-control'}),
            'local': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Local'}),
            'observacao': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Observações', 'rows': 3}),
            'link': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'Link'}),
        }

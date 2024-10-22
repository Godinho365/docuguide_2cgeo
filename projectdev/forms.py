# recursos/forms.py
from django import forms
from .models import DevProject
from .models import Mensagem
from ckeditor.widgets import CKEditorWidget

class DevProjectForm(forms.ModelForm):
    class Meta:
        model = DevProject
        fields = [
            'nome',
            'descricao',
            'categoria',
            'principal_requisito',
            'status',
            'responsavel',
            'dificuldade',
            'demais_integrantes',
            'data_inicio',
            'data_finalizada',
        ]
        widgets = {
            'demais_integrantes': forms.CheckboxSelectMultiple(),
        }

class MensagemForm(forms.ModelForm):
    class Meta:
        model = Mensagem
        fields = ['conteudo']
        widgets = {
            'conteudo': CKEditorWidget(),  # Usando o CKEditor para o campo de conteúdo
        }
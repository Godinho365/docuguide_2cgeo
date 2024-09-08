from django import forms
from ckeditor.widgets import CKEditorWidget
from .models import Instruction, Section, Category, Subcategory

class InstructionForm(forms.ModelForm):
    class Meta:
        model = Instruction
        fields = ['title', 'content', 'section', 'category', 'subcategory']
        widgets = {
            'content': CKEditorWidget(),
        }

class SectionForm(forms.ModelForm):
    class Meta:
        model = Section
        fields = ['title', 'media']
        widgets = {
            'content': CKEditorWidget(),  # Usando CKEditorWidget para o campo 'content'
        }

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'section']  # Inclua apenas os campos que existem no modelo
        widgets = {
            'section': forms.Select(attrs={'class': 'form-control'}),
        }

class SubcategoryForm(forms.ModelForm):
    class Meta:
        model = Subcategory
        fields = ['name', 'category', 'section']  # Campos ajustados conforme o modelo Subcategory
        widgets = {
            'section': forms.Select(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-control'}),

        }

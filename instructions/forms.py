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
        fields = ['title', 'imagem']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Digite o Nome'}),
            'imagem': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name','section','imagem']  # Inclua apenas os campos que existem no modelo
        widgets = {
            'section': forms.Select(attrs={'class': 'form-control'}),
            'imagem': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }

class SubcategoryForm(forms.ModelForm):
    class Meta:
        model = Subcategory
        fields = ['name', 'category', 'section', 'imagem']  # Campos ajustados conforme o modelo Subcategory
        widgets = {
            'section': forms.Select(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'imagem': forms.ClearableFileInput(attrs={'class': 'form-control'}),

        }

from django.contrib import admin
from .models import Instruction, Section, Category, Subcategory, Tag

@admin.register(Instruction)
class InstructionAdmin(admin.ModelAdmin):
    list_display = ('title', 'section', 'category', 'subcategory')
    list_filter = ('section', 'category', 'subcategory')  # Adiciona filtros para facilitar a busca
    search_fields = ('title', 'section__title', 'category__name', 'subcategory__name')  # Adiciona campos de pesquisa

@admin.register(Section)
class SectionAdmin(admin.ModelAdmin):
    list_display = ('title', 'order')
    list_filter = ('order',)  # Adiciona filtro por ordem
    search_fields = ('title',)  # Adiciona campo de pesquisa

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'section')
    list_filter = ('section',)  # Adiciona filtro por seção
    search_fields = ('name', 'section__title')  # Adiciona campo de pesquisa

@admin.register(Subcategory)
class SubcategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'category')
    list_filter = ('category',)  # Adiciona filtro por categoria
    search_fields = ('name', 'category__name')  # Adiciona campo de pesquisa

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)  # Adiciona campo de pesquisa

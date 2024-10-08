from django.shortcuts import render, get_object_or_404, redirect
from .models import Instruction, Section, Category, Subcategory
from .forms import InstructionForm, SectionForm, CategoryForm, SubcategoryForm
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.contrib.auth.decorators import user_passes_test
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
import json

 #  INSTRUCTION
@login_required
def create_instruction(request):
    if request.method == 'POST':
        form = InstructionForm(request.POST, request.FILES)
        if form.is_valid():
            instruction = form.save(commit=False)  # Não salva ainda
            instruction.author = request.user  # Atribui o usuário logado como autor
            instruction.save()  # Agora salva com o autor
            return redirect('list_instructions')
    else:
        form = InstructionForm()
    return render(request, 'instructions/create_instruction.html', {'form': form})

@login_required
def delete_instruction(request, pk):
    instruction = get_object_or_404(Instruction, pk=pk)
    if request.user.is_superuser or request.user == instruction.author:
        if request.method == 'POST':
            instruction.delete()
            return redirect('list_instructions')
    return redirect('detail_instruction', pk=pk)

import logging
logger = logging.getLogger(__name__)

@login_required
def update_instruction(request, pk):
    instruction = get_object_or_404(Instruction, pk=pk)

    logger.info(f"Usuário atual: {request.user}")
    logger.info(f"Autor da instrução: {instruction.author}")

    # Permitir edição se o usuário for superuser ou o autor da instrução
    if not (request.user.is_superuser or request.user == instruction.author):
        return HttpResponseForbidden("Você não tem permissão para editar esta instrução.")

    if request.method == 'POST':
        form = InstructionForm(request.POST, instance=instruction)
        if form.is_valid():
            form.save()
            return redirect('detail_instruction', pk=instruction.pk)
    else:
        form = InstructionForm(instance=instruction)

    return render(request, 'instructions/update_instruction.html', {'form': form})

@login_required
def list_instructions(request):
    sections = Section.objects.all()
    categories = Category.objects.all()
    subcategories = Subcategory.objects.all()

    section_id = request.GET.get('section')
    category_id = request.GET.get('category')
    subcategory_id = request.GET.get('subcategory')

    instructions = Instruction.objects.all()

    if section_id:
        instructions = instructions.filter(section_id=section_id)
    if category_id:
        instructions = instructions.filter(category_id=category_id)
    if subcategory_id:
        instructions = instructions.filter(subcategory_id=subcategory_id)

    return render(request, 'instructions/list_instructions.html', {
        'instructions': instructions,
        'sections': sections,
        'categories': categories,
        'subcategories': subcategories
    })

def list_user_instructions(request):
    # Filtra instruções pelo usuário autenticado
    instructions = Instruction.objects.filter(author=request.user)
    return render(request, 'instructions/list_user_instructions.html', {'instructions': instructions})

def detail_instruction(request, pk):
    instruction = get_object_or_404(Instruction, pk=pk)
    return render(request, 'instructions/detail_instruction.html', {'instruction': instruction})

#SEÇÕES

def create_section(request):
    if request.method == 'POST':
        form = SectionForm(request.POST, request.FILES)  # Inclua request.FILES para o upload de imagem
        if form.is_valid():
            # Verifica se já existe uma seção com o mesmo título
            title = form.cleaned_data.get('title')
            if Section.objects.filter(title=title).exists():
                form.add_error('title', 'Uma seção com este título já existe.')
            else:
                form.save()
                return redirect('list_sections')  # Ajuste o redirecionamento conforme necessário
    else:
        form = SectionForm()
    
    return render(request, 'instructions/create_section.html', {'form': form})


def is_superuser(user):
    return user.is_superuser

@user_passes_test(is_superuser, login_url='login')  # Use o nome da URL de login
def delete_section(request, pk):
    section = get_object_or_404(Section, pk=pk)
    
    if not request.user.is_superuser:
        messages.error(request, 'Você não tem permissão para acessar esta página.')
        return redirect('list_sections')  # Redireciona para a página inicial ou qualquer outra página apropriada

    if request.method == 'POST':
        section.delete()
        messages.success(request, 'Seção deletada com sucesso.')
        return redirect('list_sections')
    
    return render(request, 'instructions/delete_section.html', {'section': section})

def update_section(request, pk):
    section = get_object_or_404(Section, pk=pk)
    if request.method == 'POST':
        form = SectionForm(request.POST, instance=section)
        if form.is_valid():
            form.save()
            return redirect('list_sections')
    else:
        form = SectionForm(instance=section)
    return render(request, 'instructions/update_section.html', {'form': form, 'section': section})

def list_sections(request):
    sections = Section.objects.all().order_by('id')
    return render(request, 'instructions/list_sections.html', {
        'sections': sections,
    })


# CATEGORIAS

def list_categories(request, section_id):
    # Verifica se a seção existe
    section = get_object_or_404(Section, pk=section_id)
    # Filtra as categorias associadas à seção
    categories = Category.objects.filter(section=section)
    return render(request, 'instructions/list_categories.html', {'section': section, 'categories': categories})

def list_subcategories(request, category_id):
    # Obtenha a categoria usando o ID fornecido
    category = get_object_or_404(Category, id=category_id)
    subcategories = Subcategory.objects.filter(category=category)
    return render(request, 'instructions/list_subcategories.html', {'subcategories': subcategories, 'category': category})


def load_categories(request):
    section_id = request.GET.get('section_id')
    categories = Category.objects.filter(section_id=section_id).all()
    return JsonResponse(list(categories.values('id', 'name')), safe=False)

def load_subcategories(request):
    category_id = request.GET.get('category_id')
    subcategories = Subcategory.objects.filter(category_id=category_id).all()
    return JsonResponse(list(subcategories.values('id', 'name')), safe=False)



def create_category(request, section_id=None):
    section = None
    if section_id:
        section = get_object_or_404(Section, id=section_id)  # Obtém a seção se um ID for fornecido

    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data.get('name')
            # Verifica se já existe uma categoria com o mesmo nome
            if Category.objects.filter(name=name).exists():
                form.add_error('name', 'Uma categoria com este nome já existe.')
            else:
                category = form.save(commit=False)  # Não salva ainda
                if section:
                    category.section = section  # Define a seção se existir
                category.save()  # Agora salva a categoria
                return redirect('list_categories_for_section', section_id=section.id)  # Redirecione para a lista de categorias da seção
    else:
        form = CategoryForm()

    return render(request, 'instructions/create_category.html', {'form': form, 'section': section})

def update_category(request, pk):
    # Lógica para atualizar a categoria
    category = get_object_or_404(Category, pk=pk)

    if request.method == 'POST':
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            return redirect('list_categories_for_section', section_id=category.section.id)  # Redireciona para a lista de categorias da seção
    else:
        form = CategoryForm(instance=category)  # Preenche o formulário com os dados existentes da categoria

    return render(request, 'instructions/update_categories.html', {'form': form, 'category': category})


def delete_categories(request, category_id):
    # Obtém a categoria ou retorna um 404 se não encontrada
    category = get_object_or_404(Category, id=category_id)
    
    # Se o método da requisição for POST, exclua a categoria
    if request.method == 'POST':
        category.delete()
        messages.success(request, 'Categoria excluída com sucesso!')
        return redirect('list_categories', section_id=category.section.id)  # Redireciona para a lista de categorias da seção

    # Se não for um POST, renderiza um template de confirmação
    return render(request, 'instructions/list_categories.html', {'category': category})

def create_subcategory(request):
    if request.method == 'POST':
        form = SubcategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('create_instruction')  # Redirecione para uma página de sucesso ou lista de subcategorias
    else:
        form = SubcategoryForm()
    return render(request, 'instructions/create_subcategory.html', {'form': form})

def ajax_load_categories(request):
    section_id = request.GET.get('section_id')
    if section_id:
        categories = Category.objects.filter(section_id=section_id).values('id', 'name')
        return JsonResponse(list(categories), safe=False)
    return JsonResponse([], safe=False)

def ajax_load_subcategories(request):
    category_id = request.GET.get('category_id')
    if category_id:
        subcategories = Subcategory.objects.filter(category_id=category_id).values('id', 'name')
        return JsonResponse(list(subcategories), safe=False)
    return JsonResponse([], safe=False)


import logging

logger = logging.getLogger(__name__)

@csrf_exempt
def update_order(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        
        # Atualizar a ordem das seções
        for index, section_id in enumerate(data.get('sections', [])):
            Section.objects.filter(id=section_id).update(order=index)
        
        # Atualizar a ordem das categorias
        for index, category_id in enumerate(data.get('categories', [])):
            Category.objects.filter(id=category_id).update(order=index)
        
        # Atualizar a ordem das subcategorias
        for index, subcategory_id in enumerate(data.get('subcategories', [])):
            Subcategory.objects.filter(id=subcategory_id).update(order=index)
        
        # Atualizar a ordem das instruções (se aplicável)
        for index, instruction_id in enumerate(data.get('instructions', [])):
            Instruction.objects.filter(id=instruction_id).update(order=index)
        
        return JsonResponse({'status': 'success'})
    
    return JsonResponse({'status': 'error'}, status=400)


@csrf_exempt
@require_POST
def create_item(request):
    try:
        data = json.loads(request.body)
        name = data.get('name')
        item_type = data.get('type')  # 'section', 'category', or 'subcategory'
        section_id = data.get('section_id')
        category_id = data.get('category_id')

        if item_type == 'section':
            item = Section.objects.create(title=name)
        elif item_type == 'category':
            if not section_id:
                return JsonResponse({'status': 'error', 'message': 'Section ID required'}, status=400)
            item = Category.objects.create(name=name, section_id=section_id)
        elif item_type == 'subcategory':
            if not section_id or not category_id:
                return JsonResponse({'status': 'error', 'message': 'Section ID and Category ID required'}, status=400)
            item = Subcategory.objects.create(name=name, section_id=section_id, category_id=category_id)
        else:
            return JsonResponse({'status': 'error', 'message': 'Invalid type'}, status=400)

        return JsonResponse({'status': 'success', 'id': item.id})
    except json.JSONDecodeError:
        return JsonResponse({'status': 'error', 'message': 'Invalid JSON'}, status=400)

@csrf_exempt
@require_POST
def update_item(request):
    try:
        data = json.loads(request.body)
        item_id = data.get('id')
        new_name = data.get('name')
        item_type = data.get('type')  # 'section', 'category', or 'subcategory'

        if item_type == 'section':
            item = Section.objects.get(id=item_id)
            item.title = new_name
        elif item_type == 'category':
            item = Category.objects.get(id=item_id)
            item.name = new_name
        elif item_type == 'subcategory':
            item = Subcategory.objects.get(id=item_id)
            item.name = new_name
        else:
            return JsonResponse({'status': 'error', 'message': 'Invalid type'}, status=400)

        item.save()
        return JsonResponse({'status': 'success'})
    except (Section.DoesNotExist, Category.DoesNotExist, Subcategory.DoesNotExist):
        return JsonResponse({'status': 'error', 'message': 'Item not found'}, status=404)
    except json.JSONDecodeError:
        return JsonResponse({'status': 'error', 'message': 'Invalid JSON'}, status=400)

@csrf_exempt
@require_POST
def delete_item(request):
    try:
        data = json.loads(request.body)
        item_id = data.get('id')
        item_type = data.get('type')  # 'section', 'category', or 'subcategory'

        if item_type == 'section':
            item = Section.objects.get(id=item_id)
        elif item_type == 'category':
            item = Category.objects.get(id=item_id)
        elif item_type == 'subcategory':
            item = Subcategory.objects.get(id=item_id)
        else:
            return JsonResponse({'status': 'error', 'message': 'Invalid type'}, status=400)

        item.delete()
        return JsonResponse({'status': 'success'})
    except (Section.DoesNotExist, Category.DoesNotExist, Subcategory.DoesNotExist):
        return JsonResponse({'status': 'error', 'message': 'Item not found'}, status=404)
    except json.JSONDecodeError:
        return JsonResponse({'status': 'error', 'message': 'Invalid JSON'}, status=400)
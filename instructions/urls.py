from django.urls import path
from . import views
from .views import update_item, update_order, create_item, delete_item, list_subcategories


urlpatterns = [
    path('', views.list_instructions, name='list_instructions'),
    path('instruction/create/', views.create_instruction, name='create_instruction'),
    path('instruction/<int:pk>/update/', views.update_instruction, name='update_instruction'),
    path('instruction/<int:pk>/delete/', views.delete_instruction, name='delete_instruction'),
    path('create-section/', views.create_section, name='create_section'),
    path('create-category/', views.create_category, name='create_category'),
    path('create-subcategory/', views.create_subcategory, name='create_subcategory'),
    path('ajax/load-categories/', views.ajax_load_categories, name='ajax_load_categories'),
    path('ajax/load-subcategories/', views.ajax_load_subcategories, name='ajax_load_subcategories'),
    path('detail_instruction/<int:pk>/', views.detail_instruction, name='detail_instruction'),
    path('minhas-instrucoes/', views.list_user_instructions, name='list_user_instructions'),
    path('categories/', views.list_categories, name='list_categories'),  # Esta URL pode ser removida se não for necessária
    path('subcategories/', views.list_subcategories, name='list_subcategories'),
    path('sections/', views.list_sections, name='list_sections'),
    path('sections/create/', views.create_section, name='create_section'),
    path('sections/<int:pk>/update/', views.update_section, name='update_section'),
    path('sections/<int:pk>/delete/', views.delete_section, name='delete_section'),
    path('sections/<int:section_id>/categories/', views.list_categories, name='list_categories_for_section'),  # Nova URL
    path('categories/<int:category_id>/subcategories/', list_subcategories, name='list_subcategories_for_category'),
    path('instructions/subcategory/<int:subcategory_id>/', views.list_instructions, name='list_instructions_for_subcategory'),
    path('instructions/subcategory/<int:subcategory_id>/details/', views.list_instructions_for_subcategory, name='list_instructions_for_subcategories'),
    path('categories/<int:pk>/update/', views.update_category, name='update_categories'),  # Adicione esta linha
    path('categories/<int:pk>/delete/', views.delete_category, name='delete_categories'),
    path('update-order/', update_order, name='update_order'),
    path('update-item/', update_item, name='update_item'),
    path('create-item/', create_item, name='create_item'),
    path('delete-item/', delete_item, name='delete_item'),
    path('subcategories/update/<int:pk>/', views.update_subcategory, name='update_subcategory'),
    path('subcategories/delete/<int:pk>/', views.delete_subcategory, name='delete_subcategory'),
    path('instruction/<int:pk>/pdf/', views.generate_pdf, name='generate_pdf'),
    path('search/', views.search_instructions, name='search_instructions'),
    
    
] 

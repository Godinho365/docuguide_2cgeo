# insumos/urls.py
from django.urls import path
from .views import list_insumos, create_insumo, edit_insumo, delete_insumo

urlpatterns = [
    path('', list_insumos, name='list_insumos'),
    path('criar/', create_insumo, name='create_insumo'),
    path('editar/<int:pk>/', edit_insumo, name='edit_insumo'),
    path('excluir/<int:pk>/', delete_insumo, name='delete_insumo'),
]

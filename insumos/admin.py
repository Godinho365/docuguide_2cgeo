# insumos/admin.py
from django.contrib import admin
from .models import Insumo, TipoInsumo

admin.site.register(Insumo)
admin.site.register(TipoInsumo)


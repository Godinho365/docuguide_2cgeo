# insumos/models.py
from django.db import models

class TipoInsumo(models.Model):
    nome = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.nome

class Insumo(models.Model):
    nome = models.CharField(max_length=100)
    tipo = models.ForeignKey(TipoInsumo, on_delete=models.CASCADE)
    local = models.CharField(max_length=100)
    observacao = models.TextField(blank=True, null=True)
    link = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.nome

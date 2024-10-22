# recursos/models.py
from django.db import models
from django.contrib.auth.models import User
from ckeditor.fields import RichTextField


class DevProject(models.Model):
    # Definindo as categorias
    CATEGORIA_CHOICES = [
        ('infraestrutura', 'Infraestrutura'),
        ('capacitação', 'Capacitação'),
        ('gestao', 'Gestão'),
        ('tecnico', 'Técnico'),
    ]

    STATUS_CHOICES = [
        ('em_execucao', 'Em Execução'),
        ('nao_iniciada', 'Não Iniciada'),
        ('bloqueada', 'Bloqueada'),
        ('finalizada', 'Finalizada'),
    ]

    DIFICULDADE_CHOICES = [
        ('facil', 'Fácil'),
        ('medio', 'Médio'),
        ('dificil', 'Difícil'),
        ('bizarro', 'Bizarro'),
    ]

    nome = models.CharField(max_length=255)
    descricao = models.TextField(blank=True, null=True)  # Campo de descrição
    categoria = models.CharField(max_length=20, choices=CATEGORIA_CHOICES, default='infraestrutura')  # Campo de categoria
    principal_requisito = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='nao_iniciada')
    responsavel = models.ForeignKey(User, on_delete=models.CASCADE)
    dificuldade = models.CharField(max_length=20, choices=DIFICULDADE_CHOICES, default='medio')
    demais_integrantes = models.ManyToManyField(User, related_name='dev_projects', blank=True)
    
    # Campos de data
    data_inicio = models.DateField(blank=True, null=True)  # Data de início
    data_finalizada = models.DateField(blank=True, null=True)  # Data de finalização

    def get_status_display(self):
        status_dict = dict(self.STATUS_CHOICES)  # Cria um dicionário a partir das opções de status
        return status_dict.get(self.status, self.status)

    def __str__(self):
        return self.nome

class Mensagem(models.Model):
    projeto = models.ForeignKey(DevProject, on_delete=models.CASCADE)
    integrante = models.ForeignKey(User, on_delete=models.CASCADE)
    conteudo = RichTextField()
    data = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.integrante.username}: {self.conteudo[:20]}"
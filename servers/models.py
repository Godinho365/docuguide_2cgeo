# servers/models.py
from django.db import models

class Server(models.Model):
    name = models.CharField(max_length=255)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    link = models.URLField(max_length=200)
    username = models.CharField(max_length=100)
    password = models.CharField(max_length=100)  # Use um gerenciador de senhas apropriado em produção

    def __str__(self):
        return self.name

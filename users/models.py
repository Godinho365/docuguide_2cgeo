from django.contrib.auth.models import User
from django.db import models

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # Campos adicionais
    image = models.ImageField(upload_to='image/', blank=True, null=True)
    
    def __str__(self):
        return self.user.username

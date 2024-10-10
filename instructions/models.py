from django.db import models
from ckeditor.fields import RichTextField  # Se estiver usando o CKEditor
from django.contrib.auth.models import User

class Instruction(models.Model):
    title = models.CharField(max_length=255)
    content = RichTextField()  # Usando CKEditor para o conteúdo
    section = models.ForeignKey('Section', on_delete=models.CASCADE, related_name='instructions')
    category = models.ForeignKey('Category', on_delete=models.CASCADE, related_name='instructions')
    subcategory = models.ForeignKey('Subcategory', on_delete=models.CASCADE, related_name='instructions')
    tags = models.ManyToManyField('Tag', blank=True, related_name='instructions')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class Section(models.Model):
    title = models.CharField(max_length=255, unique=True)
    content = RichTextField(blank=True, null=True)  # Permite conteúdo vazio ou nulo
    order = models.PositiveIntegerField(default=0)
    imagem = models.ImageField(upload_to='section_imagens/', blank=True, null=True)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.title

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    section = models.ForeignKey(Section, on_delete=models.CASCADE, related_name='categories')
    order = models.PositiveIntegerField(default=0)  # Novo campo para a ordem

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.name

class Subcategory(models.Model):
    name = models.CharField(max_length=100)  
    section = models.ForeignKey(Section, on_delete=models.CASCADE, related_name='subcategories')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='subcategories')
    order = models.PositiveIntegerField(default=0)  # Novo campo para a ordem

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.name

class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name

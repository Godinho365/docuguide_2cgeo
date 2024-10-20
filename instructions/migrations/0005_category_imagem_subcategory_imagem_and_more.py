# Generated by Django 5.1.1 on 2024-10-11 21:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('instructions', '0004_remove_section_media_section_imagem'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='imagem',
            field=models.ImageField(blank=True, null=True, upload_to='categories_imagens/'),
        ),
        migrations.AddField(
            model_name='subcategory',
            name='imagem',
            field=models.ImageField(blank=True, null=True, upload_to='subcategory_imagens/'),
        ),
        migrations.AlterField(
            model_name='section',
            name='imagem',
            field=models.ImageField(blank=True, null=True, upload_to='section_imagens/'),
        ),
    ]

# Generated by Django 5.1.1 on 2024-10-20 04:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('servers', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='server',
            name='ip_address',
            field=models.GenericIPAddressField(blank=True, null=True),
        ),
    ]

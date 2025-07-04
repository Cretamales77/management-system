# Generated by Django 4.2.7 on 2025-06-22 21:56

from django.db import migrations
from django.contrib.auth.hashers import make_password

def crear_usuario_custom(apps, schema_editor):
    Usuario = apps.get_model('usuario', 'Usuario')
    if not Usuario.objects.filter(nombre_usuario='admin').exists():
        # Usamos make_password para hashear la contraseña, igual que en tu modelo
        hashed_password = make_password('admin123')
        Usuario.objects.create(
            nombre_usuario='admin',
            correo='admin@example.com',
            contraseña=hashed_password
        )

def reverse_crear_usuario_custom(apps, schema_editor):
    Usuario = apps.get_model('usuario', 'Usuario')
    Usuario.objects.filter(nombre_usuario='admin').delete()


class Migration(migrations.Migration):

    dependencies = [
        ('usuario', '0003_usuario_correo'),
    ]

    operations = [
        migrations.RunPython(crear_usuario_custom, reverse_crear_usuario_custom),
    ]

# Generated by Django 5.2.1 on 2025-06-14 22:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("venta", "0005_remove_configuracionboleta_mostrar_codigo_and_more"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="configuracionboleta",
            name="mostrar_descuento",
        ),
    ]

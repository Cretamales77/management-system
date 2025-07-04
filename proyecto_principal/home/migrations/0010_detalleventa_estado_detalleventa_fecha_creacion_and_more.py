# Generated by Django 5.2.1 on 2025-06-14 19:43

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("home", "0009_remove_venta_cantidad_remove_venta_id_producto_and_more"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name="detalleventa",
            name="estado",
            field=models.CharField(
                choices=[
                    ("ACTIVO", "Activo"),
                    ("REEMBOLSADO", "Reembolsado"),
                    ("PARCIALMENTE_REEMBOLSADO", "Parcialmente Reembolsado"),
                ],
                default="ACTIVO",
                max_length=30,
            ),
        ),
        migrations.AddField(
            model_name="detalleventa",
            name="fecha_creacion",
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="detalleventa",
            name="fecha_modificacion",
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="detalleventa",
            name="subtotal",
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
        ),
        migrations.AddField(
            model_name="venta",
            name="estado",
            field=models.CharField(
                choices=[
                    ("COMPLETADA", "Completada"),
                    ("REEMBOLSADA", "Reembolsada"),
                    ("PARCIALMENTE_REEMBOLSADA", "Parcialmente Reembolsada"),
                    ("ANULADA", "Anulada"),
                ],
                default="COMPLETADA",
                max_length=30,
            ),
        ),
        migrations.AddField(
            model_name="venta",
            name="fecha_modificacion",
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="venta",
            name="total_venta",
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
        ),
        migrations.AddField(
            model_name="venta",
            name="usuario",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AlterField(
            model_name="detalleventa",
            name="producto",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.PROTECT, to="home.producto"
            ),
        ),
    ]

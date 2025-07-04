# Generated by Django 5.2.1 on 2025-06-14 05:13

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("home", "0009_remove_venta_cantidad_remove_venta_id_producto_and_more"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Reembolso",
            fields=[
                ("id_reembolso", models.AutoField(primary_key=True, serialize=False)),
                ("fecha_hora", models.DateTimeField(auto_now_add=True)),
                ("observaciones", models.TextField(blank=True, null=True)),
                (
                    "total_devuelto",
                    models.DecimalField(decimal_places=2, max_digits=10),
                ),
                (
                    "usuario",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "venta",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="home.venta"
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="ReembolsoDetalle",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("cantidad", models.IntegerField()),
                ("monto", models.DecimalField(decimal_places=2, max_digits=10)),
                (
                    "producto",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="home.producto"
                    ),
                ),
                (
                    "reembolso",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="detalles",
                        to="venta.reembolso",
                    ),
                ),
            ],
        ),
    ]

# Generated by Django 5.0.6 on 2025-06-14 23:22

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0011_update_venta_totals'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='ConfiguracionBoleta',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(default='Ferretería El Ingeniero', max_length=100)),
                ('direccion', models.CharField(default='Av. Principal 123, Ciudad', max_length=200)),
                ('fono', models.CharField(default='Fono: +56 9 1234 5678', max_length=50)),
                ('rut', models.CharField(default='RUT: 12.345.678-9', max_length=20)),
                ('logo', models.ImageField(blank=True, null=True, upload_to='boleta_logos/')),
                ('fecha_modificacion', models.DateTimeField(auto_now=True)),
                ('correo', models.CharField(blank=True, default='', max_length=100)),
                ('sitio_web', models.CharField(blank=True, default='', max_length=100)),
                ('mensaje_pie', models.CharField(blank=True, default='¡Gracias por su compra!', max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Reembolso',
            fields=[
                ('id_reembolso', models.AutoField(primary_key=True, serialize=False)),
                ('fecha_hora', models.DateTimeField(auto_now_add=True)),
                ('observaciones', models.TextField(blank=True, null=True)),
                ('total_devuelto', models.DecimalField(decimal_places=2, max_digits=10)),
                ('usuario', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
                ('venta', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reembolsos', to='home.venta')),
            ],
        ),
        migrations.CreateModel(
            name='ReembolsoDetalle',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cantidad', models.IntegerField()),
                ('monto', models.DecimalField(decimal_places=2, max_digits=10)),
                ('producto', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='home.producto')),
                ('reembolso', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='detalles', to='home.reembolso')),
            ],
        ),
    ]

from django.db import migrations
from django.utils import timezone

def actualizar_totales(apps, schema_editor):
    DetalleVenta = apps.get_model('home', 'DetalleVenta')
    Venta = apps.get_model('home', 'Venta')
    
    # Actualizar subtotales y fechas en DetalleVenta
    for detalle in DetalleVenta.objects.all():
        detalle.subtotal = detalle.cantidad * detalle.precio_unitario
        detalle.fecha_creacion = timezone.now()
        detalle.fecha_modificacion = timezone.now()
        detalle.save()
    
    # Actualizar totales y fechas en Venta
    for venta in Venta.objects.all():
        venta.total_venta = sum(detalle.subtotal for detalle in venta.detalles.all())
        venta.fecha_modificacion = timezone.now()
        venta.save()

def reverse_actualizar_totales(apps, schema_editor):
    # No necesitamos revertir los cambios ya que son datos calculados
    pass

class Migration(migrations.Migration):
    dependencies = [
        ('home', '0010_detalleventa_estado_detalleventa_fecha_creacion_and_more'),
    ]

    operations = [
        migrations.RunPython(actualizar_totales, reverse_actualizar_totales),
    ] 
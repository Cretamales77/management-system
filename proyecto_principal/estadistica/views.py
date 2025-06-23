from django.shortcuts import render
from django.db.models import Sum, F, FloatField
from django.http import JsonResponse
from home.models import Venta, Compra, DetalleVenta, DetalleCompra
from datetime import datetime, date

def estadisticas(request):
    # Verificar si es una petición AJAX para el resumen del día
    if request.GET.get('ajax') == 'resumen_dia':
        fecha_actual = date.today()
        
        # Filtros específicos para el día actual
        filtro_ventas_hoy = {'venta__fecha__date': fecha_actual}
        filtro_compras_hoy = {'compra__fecha__date': fecha_actual}

        # Totales específicos del día actual
        totales_ventas_hoy = DetalleVenta.objects.filter(**filtro_ventas_hoy).aggregate(
            total_cant=Sum('cantidad'),
            total_monto=Sum(F('cantidad') * F('precio_unitario'), output_field=FloatField())
        )

        totales_compras_hoy = DetalleCompra.objects.filter(**filtro_compras_hoy).aggregate(
            total_cant=Sum('cantidad'),
            total_monto=Sum(F('cantidad') * F('precio_compra'), output_field=FloatField())
        )

        # Producto más vendido del día actual
        producto_mas_vendido_hoy = (
            DetalleVenta.objects.filter(**filtro_ventas_hoy)
            .values('producto__nombre')
            .annotate(total_vendido=Sum('cantidad'))
            .order_by('-total_vendido')
            .first()
        )

        # Producto más comprado del día actual
        producto_mas_comprado_hoy = (
            DetalleCompra.objects.filter(**filtro_compras_hoy)
            .values('producto__nombre')
            .annotate(total_comprado=Sum('cantidad'))
            .order_by('-total_comprado')
            .first()
        )

        # Producto con mayor gasto del día actual
        mayor_gasto_hoy = (
            DetalleCompra.objects.filter(**filtro_compras_hoy)
            .values('producto__nombre')
            .annotate(monto_gastado=Sum(F('cantidad') * F('precio_compra'), output_field=FloatField()))
            .order_by('-monto_gastado')
            .first()
        )

        return JsonResponse({
            'totales_ventas_hoy': {
                'total_cant': totales_ventas_hoy['total_cant'] or 0,
                'total_monto': float(totales_ventas_hoy['total_monto'] or 0)
            },
            'totales_compras_hoy': {
                'total_cant': totales_compras_hoy['total_cant'] or 0,
                'total_monto': float(totales_compras_hoy['total_monto'] or 0)
            },
            'producto_mas_vendido_hoy': producto_mas_vendido_hoy,
            'producto_mas_comprado_hoy': producto_mas_comprado_hoy,
            'mayor_gasto_hoy': mayor_gasto_hoy,
        })

    # Verificar si es una petición AJAX para los datos del día del gráfico
    if request.GET.get('ajax') == 'datos_dia':
        fecha_actual = date.today()
        top = request.GET.get('top', 10)
        
        try:
            top = int(top)
            if top < 1:
                top = 10
        except ValueError:
            top = 10

        # Filtros específicos para el día actual
        filtro_ventas_hoy = {'venta__fecha': fecha_actual}

        # Productos vendidos del día actual para el gráfico
        productos_vendidos_hoy = (
            DetalleVenta.objects.filter(**filtro_ventas_hoy)
            .values('producto__nombre')
            .annotate(total_vendido=Sum('cantidad'))
            .order_by('-total_vendido')[:top]
        )

        return JsonResponse({
            'productos_vendidos_hoy': list(productos_vendidos_hoy),
        })

    top = request.GET.get('top', 10)
    fecha_inicio_str = request.GET.get('fecha_inicio')
    fecha_fin_str = request.GET.get('fecha_fin')

    advertencia_fecha = False

    try:
        top = int(top)
        if top < 1:
            top = 10
    except ValueError:
        top = 10

    def parse_fecha(fecha_str):
        try:
            return datetime.strptime(fecha_str, '%Y-%m-%d').date()
        except:
            return None

    fecha_inicio = parse_fecha(fecha_inicio_str)
    fecha_fin = parse_fecha(fecha_fin_str)

    if fecha_inicio and fecha_fin and fecha_inicio > fecha_fin:
        fecha_inicio, fecha_fin = fecha_fin, fecha_inicio
        advertencia_fecha = True

    # Obtener la fecha actual para el resumen del día
    fecha_actual = date.today()
    
    filtro_ventas = {}
    filtro_compras = {}

    if fecha_inicio:
        filtro_ventas['venta__fecha__date__gte'] = fecha_inicio
        filtro_compras['compra__fecha__date__gte'] = fecha_inicio
    if fecha_fin:
        filtro_ventas['venta__fecha__date__lte'] = fecha_fin
        filtro_compras['compra__fecha__date__lte'] = fecha_fin

    # Filtros específicos para el día actual (resumen general)
    filtro_ventas_hoy = {'venta__fecha__date': fecha_actual}
    filtro_compras_hoy = {'compra__fecha__date': fecha_actual}

    productos_vendidos = (
        DetalleVenta.objects.filter(**filtro_ventas)
        .values('producto__nombre', 'producto__id_categoria__nombre', 'precio_unitario')
        .annotate(
            total_vendido=Sum('cantidad'),
            monto_generado=Sum(F('cantidad') * F('precio_unitario'), output_field=FloatField())
        )
        .order_by('-total_vendido')[:top]
    )

    productos_comprados = (
        DetalleCompra.objects.filter(**filtro_compras)
        .values('producto__nombre', 'compra__proveedor__nombre')
        .annotate(
            total_comprado=Sum('cantidad'),
            monto_gastado=Sum(F('cantidad') * F('precio_compra'), output_field=FloatField())
        )
        .order_by('-total_comprado')[:top]
    )

    compras_por_proveedor = (
        DetalleCompra.objects.filter(**filtro_compras)
        .values('compra__proveedor__nombre')
        .annotate(
            total_cant=Sum('cantidad'),
            total_monto=Sum(F('cantidad') * F('precio_compra'), output_field=FloatField())
        )
        .order_by('-total_monto')
    )

    totales_ventas = DetalleVenta.objects.filter(**filtro_ventas).aggregate(
        total_cant=Sum('cantidad'),
        total_monto=Sum(F('cantidad') * F('precio_unitario'), output_field=FloatField())
    )

    totales_compras = DetalleCompra.objects.filter(**filtro_compras).aggregate(
        total_cant=Sum('cantidad'),
        total_monto=Sum(F('cantidad') * F('precio_compra'), output_field=FloatField())
    )

    # Totales específicos del día actual para el resumen general
    totales_ventas_hoy = DetalleVenta.objects.filter(**filtro_ventas_hoy).aggregate(
        total_cant=Sum('cantidad'),
        total_monto=Sum(F('cantidad') * F('precio_unitario'), output_field=FloatField())
    )

    totales_compras_hoy = DetalleCompra.objects.filter(**filtro_compras_hoy).aggregate(
        total_cant=Sum('cantidad'),
        total_monto=Sum(F('cantidad') * F('precio_compra'), output_field=FloatField())
    )

    # Producto más vendido del día actual
    producto_mas_vendido_hoy = (
        DetalleVenta.objects.filter(**filtro_ventas_hoy)
        .values('producto__nombre')
        .annotate(total_vendido=Sum('cantidad'))
        .order_by('-total_vendido')
        .first()
    )

    # Producto más comprado del día actual
    producto_mas_comprado_hoy = (
        DetalleCompra.objects.filter(**filtro_compras_hoy)
        .values('producto__nombre')
        .annotate(total_comprado=Sum('cantidad'))
        .order_by('-total_comprado')
        .first()
    )

    # Producto con mayor gasto del día actual
    mayor_gasto_hoy = (
        DetalleCompra.objects.filter(**filtro_compras_hoy)
        .values('producto__nombre')
        .annotate(monto_gastado=Sum(F('cantidad') * F('precio_compra'), output_field=FloatField()))
        .order_by('-monto_gastado')
        .first()
    )

    # Categorías más vendidas
    categorias_vendidas = (
        DetalleVenta.objects.filter(**filtro_ventas)
        .values('producto__id_categoria__nombre')
        .annotate(
            total_vendido=Sum('cantidad'),
            monto_generado=Sum(F('cantidad') * F('precio_unitario'), output_field=FloatField())
        )
        .order_by('-total_vendido')
    )

    # Categorías más compradas
    categorias_compradas = (
        DetalleCompra.objects.filter(**filtro_compras)
        .values('producto__id_categoria__nombre')
        .annotate(
            total_comprado=Sum('cantidad'),
            monto_gastado=Sum(F('cantidad') * F('precio_compra'), output_field=FloatField())
        )
        .order_by('-total_comprado')
    )

    # Ventas por día
    ventas_por_dia = (
        DetalleVenta.objects.filter(**filtro_ventas)
        .values('venta__fecha__date')
        .annotate(
            total_cant=Sum('cantidad'),
            total_monto=Sum(F('cantidad') * F('precio_unitario'), output_field=FloatField())
        )
        .order_by('venta__fecha__date')
    )

    # Compras por día
    compras_por_dia = (
        DetalleCompra.objects.filter(**filtro_compras)
        .values('compra__fecha__date')
        .annotate(
            total_cant=Sum('cantidad'),
            total_monto=Sum(F('cantidad') * F('precio_compra'), output_field=FloatField())
        )
        .order_by('compra__fecha__date')
    )

    context = {
        'productos_vendidos': productos_vendidos,
        'productos_comprados': productos_comprados,
        'compras_por_proveedor': compras_por_proveedor,
        'totales_ventas': totales_ventas,
        'totales_compras': totales_compras,
        'totales_ventas_hoy': totales_ventas_hoy,
        'totales_compras_hoy': totales_compras_hoy,
        'producto_mas_vendido_hoy': producto_mas_vendido_hoy,
        'producto_mas_comprado_hoy': producto_mas_comprado_hoy,
        'mayor_gasto_hoy': mayor_gasto_hoy,
        'categorias_vendidas': categorias_vendidas,
        'categorias_compradas': categorias_compradas,
        'ventas_por_dia': ventas_por_dia,
        'compras_por_dia': compras_por_dia,
        'fecha_inicio': fecha_inicio_str,
        'fecha_fin': fecha_fin_str,
        'top': top,
        'advertencia_fecha': advertencia_fecha,
    }

    return render(request, 'estadistica/estadisticas.html', context)

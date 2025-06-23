from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import JsonResponse, HttpResponse, FileResponse
from home.models import Venta, Producto, Codigo, DetalleVenta, Categoria, Reembolso, ReembolsoDetalle, ConfiguracionBoleta
from .forms import VentaForm, DetalleVentaForm
from decimal import Decimal
from django.db import transaction
from django.forms import modelformset_factory
from django.views.decorators.http import require_POST, require_GET, require_http_methods
from django.core.paginator import Paginator
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import get_user_model
from django.db.models import Q
from io import BytesIO
import xlsxwriter
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
from datetime import datetime
from django.db import models
from usuario.models import Usuario
from reportlab.lib.units import mm
from django.urls import reverse

# --- Utilidades de carrito en sesión ---
def get_cart(request):
    return request.session.get('carrito_venta', [])

def save_cart(request, cart):
    request.session['carrito_venta'] = cart
    request.session.modified = True

def clear_cart(request):
    if 'carrito_venta' in request.session:
        del request.session['carrito_venta']
        request.session.modified = True

def get_producto_or_none(producto_id):
    try:
        return Producto.objects.get(id_producto=producto_id)
    except Producto.DoesNotExist:
        return None

# --- Vistas de Carrito ---
def ventas(request):
    mostrar = int(request.GET.get('mostrar', 5))
    orden = request.GET.get('orden', 'desc')
    if orden == 'asc':
        lista_ventas = Venta.objects.all().order_by('fecha', 'id_venta')
    else:
        lista_ventas = Venta.objects.all().order_by('-fecha', '-id_venta')
    nombre_usuario = request.session.get('usuario_nombre', 'Invitado')

    # Carrito actual en sesión
    carrito = get_cart(request)
    productos_carrito = []
    total_carrito = Decimal('0.00')
    for item in carrito:
        try:
            producto = Producto.objects.get(id_producto=item['producto_id'])
            subtotal = producto.precio_unitario * item['cantidad']
            productos_carrito.append({
                'producto': producto,
                'cantidad': item['cantidad'],
                'subtotal': subtotal
            })
            total_carrito += subtotal
        except Producto.DoesNotExist:
            continue

    # Obtener todos los productos disponibles para el formulario
    productos = Producto.objects.all()
    categorias = Categoria.objects.all()

    # Obtener detalles de cada venta (agrupados)
    ventas_con_detalles = []
    for venta in lista_ventas:
        detalles = []
        total_venta = 0
        # Solo incluir detalles con cantidad > 0
        for d in venta.detalles.select_related('producto').all():
            if d.cantidad > 0:
                subtotal = d.cantidad * d.precio_unitario
                detalles.append({
                    'producto': d.producto,
                    'cantidad': d.cantidad,
                    'precio_unitario': d.precio_unitario,
                    'subtotal': subtotal,
                })
                total_venta += subtotal
        ventas_con_detalles.append({
            'venta': venta,
            'detalles': detalles,
            'total_venta': total_venta,
        })

    # Paginación: ventas por página según 'mostrar'
    page_number = request.GET.get('page', 1)
    paginator = Paginator(ventas_con_detalles, mostrar)
    page_obj = paginator.get_page(page_number)

    return render(request, 'venta/ventas.html', {
        'ventas': lista_ventas,
        'ventas_con_detalles': page_obj.object_list,
        'page_obj': page_obj,
        'paginator': paginator,
        'nombre_usuario': nombre_usuario,
        'carrito': productos_carrito,
        'total_carrito': total_carrito,
        'productos': productos,
        'categorias': categorias,
        'mostrar': mostrar,
        'orden': orden,
    })

@require_POST
def agregar_a_carrito(request):
    if request.method == 'POST':
        producto_id = request.POST.get('producto_id')
        if not producto_id or not producto_id.isdigit():
            messages.error(request, 'Debes seleccionar un producto válido.')
            return redirect('ventas')
        try:
            cantidad = int(request.POST.get('cantidad', 1))
        except (TypeError, ValueError):
            messages.error(request, 'Cantidad inválida.')
            return redirect('ventas')
        if cantidad <= 0:
            messages.error(request, 'La cantidad debe ser mayor a cero.')
            return redirect('ventas')
        producto = get_producto_or_none(producto_id)
        if not producto:
            messages.error(request, 'Producto no encontrado.')
            return redirect('ventas')
        if producto.stock_actual < cantidad:
            messages.error(request, 'Stock insuficiente para el producto.')
            return redirect('ventas')
        carrito = get_cart(request)
        for item in carrito:
            if item['producto_id'] == producto.id_producto:
                item['cantidad'] += cantidad
                break
        else:
            carrito.append({'producto_id': producto.id_producto, 'cantidad': cantidad})
        save_cart(request, carrito)
        messages.success(request, f'{producto.nombre} agregado al carrito.')
    return redirect('ventas')

@require_POST
def eliminar_de_carrito(request, producto_id):
    carrito = get_cart(request)
    carrito = [item for item in carrito if item['producto_id'] != int(producto_id)]
    save_cart(request, carrito)
    messages.success(request, 'Producto eliminado del carrito.')
    return redirect('ventas')

@require_POST
def editar_carrito(request, producto_id):
    if request.method == 'POST':
        try:
            nueva_cantidad = int(request.POST.get('cantidad', 1))
        except (TypeError, ValueError):
            messages.error(request, 'Cantidad inválida.')
            return redirect('ventas')
        if nueva_cantidad <= 0:
            messages.error(request, 'La cantidad debe ser mayor a cero.')
            return redirect('ventas')
        producto = get_producto_or_none(producto_id)
        if not producto:
            messages.error(request, 'Producto no encontrado.')
            return redirect('ventas')
        if producto.stock_actual < nueva_cantidad:
            messages.error(request, f'Stock insuficiente para {producto.nombre}.')
            return redirect('ventas')
        carrito = get_cart(request)
        for item in carrito:
            if item['producto_id'] == int(producto_id):
                item['cantidad'] = nueva_cantidad
                break
        save_cart(request, carrito)
        messages.success(request, 'Cantidad actualizada en el carrito.')
    return redirect('ventas')

@require_POST
def finalizar_venta(request):
    carrito = get_cart(request)
    if not carrito:
        clear_cart(request)
        messages.error(request, 'El carrito está vacío.')
        return redirect('ventas')
    
    # Validación anticipada de stock
    productos_faltantes = []
    total_venta = Decimal('0.00')
    for item in carrito:
        producto = get_producto_or_none(int(item['producto_id']))
        if not producto:
            productos_faltantes.append(f"ID {item['producto_id']}")
        elif producto.stock_actual < item['cantidad']:
            productos_faltantes.append(producto.nombre)
        else:
            total_venta += producto.precio_unitario * item['cantidad']
    
    if productos_faltantes:
        clear_cart(request)
        messages.error(request, f"Stock insuficiente o producto no encontrado para: {', '.join(productos_faltantes)}.")
        return redirect('ventas')
    
    observaciones = request.POST.get('observaciones', '').strip() or '---'
    
    with transaction.atomic():
        # Crear la venta con los nuevos campos
        venta = Venta.objects.create(
            observaciones=observaciones,
            total_venta=total_venta,
            estado='Completada',
            usuario=request.user if request.user.is_authenticated else None
        )
        
        # Crear los detalles de venta
        for item in carrito:
            producto = get_producto_or_none(int(item['producto_id']))
            cantidad = item['cantidad']
            precio_unitario = producto.precio_unitario
            subtotal = precio_unitario * cantidad
            
            DetalleVenta.objects.create(
                venta=venta,
                producto=producto,
                cantidad=cantidad,
                precio_unitario=precio_unitario,
                subtotal=subtotal,
                estado='Completado'
            )
            
            # Actualizar stock
            producto.stock_actual -= cantidad
            producto.save()
    
    clear_cart(request)
    messages.success(request, 'Venta registrada exitosamente.')
    return redirect('ventas')

def agregar_venta(request):
    if request.method == 'POST':
        form = VentaForm(request.POST)
        if form.is_valid():
            producto = form.cleaned_data['producto']
            cantidad = form.cleaned_data['cantidad']
            observaciones = form.cleaned_data.get('observaciones', '')

            if producto.stock_actual < cantidad:
                return redirect('ventas')

            Venta.objects.create(
                id_producto=producto,
                cantidad=cantidad,
                observaciones=observaciones,
            )
            producto.stock_actual -= cantidad
            producto.save()

            request.session['detalle_venta'] = {'producto_id': producto.id_producto, 'cantidad': cantidad}
            messages.success(request, "Venta registrada exitosamente.")
        else:
            return redirect('ventas')

    return redirect('ventas')

def eliminar_venta(request, id):
    if request.method == 'POST':
        venta = get_object_or_404(Venta, id_venta=id)
        with transaction.atomic():
            venta.detalles.all().delete()
            venta.delete()
        messages.success(request, "Venta eliminada correctamente.")
    return redirect('ventas')

def validar_producto(request):
    nombre_o_codigo = request.GET.get('producto', '').strip()
    producto = Producto.objects.filter(nombre__iexact=nombre_o_codigo).first()
    if not producto:
        codigo_obj = Codigo.objects.filter(codigo__iexact=nombre_o_codigo).first()
        if codigo_obj:
            producto = Producto.objects.filter(id_producto=codigo_obj.id_producto.id_producto).first()
    if producto:
        return JsonResponse({
            'existe': True, 
            'stock': producto.stock_actual,
            'stock_minimo': producto.stock_minimo if producto.stock_minimo is not None else None
        })
    return JsonResponse({'existe': False})

def editar_venta(request, id):
    venta = get_object_or_404(Venta, id_venta=id)
    detalles = venta.detalles.select_related('producto').all()
    
    if request.method == 'POST':
        with transaction.atomic():
            total_reembolso = Decimal('0.00')
            venta_modificada = False
            reembolso_items = []
            for detalle in detalles:
                nueva_cantidad = int(request.POST.get(f'cantidad_{detalle.id_detalle}', 0))
                if nueva_cantidad < 0:
                    messages.error(request, 'La cantidad no puede ser negativa.')
                    return redirect('ventas')
                if nueva_cantidad != detalle.cantidad:
                    venta_modificada = True
                    cantidad_reembolso = detalle.cantidad - nueva_cantidad
                    if cantidad_reembolso > 0:  # Hay reembolso
                        # Actualizar stock
                        detalle.producto.stock_actual += cantidad_reembolso
                        detalle.producto.save()
                        # Calcular monto reembolsado
                        monto_reembolso = cantidad_reembolso * detalle.precio_unitario
                        total_reembolso += monto_reembolso
                        # Guardar para crear el registro de reembolso
                        reembolso_items.append({
                            'producto': detalle.producto,
                            'cantidad': cantidad_reembolso,
                            'monto': monto_reembolso
                        })
                        # Actualizar detalle
                        detalle.cantidad = nueva_cantidad
                        detalle.subtotal = nueva_cantidad * detalle.precio_unitario
                        detalle.estado = 'Parcialmente Reembolsado' if nueva_cantidad > 0 else 'Reembolsado'
                        detalle.save()
                    elif nueva_cantidad > detalle.cantidad:  # Aumentar cantidad
                        if detalle.producto.stock_actual < (nueva_cantidad - detalle.cantidad):
                            messages.error(request, f'Stock insuficiente para {detalle.producto.nombre}.')
                            return redirect('ventas')
                        # Actualizar stock
                        detalle.producto.stock_actual -= (nueva_cantidad - detalle.cantidad)
                        detalle.producto.save()
                        # Actualizar detalle
                        detalle.cantidad = nueva_cantidad
                        detalle.subtotal = nueva_cantidad * detalle.precio_unitario
                        detalle.estado = 'Completado'
                        detalle.save()
            if venta_modificada:
                # Crear registro de reembolso si corresponde
                if reembolso_items:
                    usuario_id = request.session.get('usuario_id')
                    usuario = Usuario.objects.filter(id_usuario=usuario_id).first() if usuario_id else None
                    reembolso = Reembolso.objects.create(
                        venta=venta,
                        usuario=usuario,
                        observaciones=request.POST.get('observaciones', ''),
                        total_devuelto=total_reembolso
                    )
                    for item in reembolso_items:
                        ReembolsoDetalle.objects.create(
                            reembolso=reembolso,
                            producto=item['producto'],
                            cantidad=item['cantidad'],
                            monto=item['monto']
                        )
                # Actualizar total de la venta
                venta.total_venta = sum(detalle.subtotal for detalle in detalles)
                # Actualizar estado de la venta
                if all(detalle.estado == 'Reembolsado' for detalle in detalles):
                    venta.estado = 'Reembolsada'
                elif any(detalle.estado == 'Parcialmente Reembolsado' for detalle in detalles):
                    venta.estado = 'Parcialmente Reembolsada'
                else:
                    venta.estado = 'Completada'
                venta.save()
                if total_reembolso > 0:
                    messages.success(request, f'Venta actualizada. Reembolso total: ${total_reembolso:.2f}')
                else:
                    messages.success(request, 'Venta actualizada exitosamente.')
            else:
                messages.info(request, 'No se realizaron cambios en la venta.')
            return redirect('ventas')
    return render(request, 'venta/editar_venta.html', {
        'venta': venta,
        'detalles': detalles,
    })

@csrf_exempt
@require_POST
def editar_venta_ajax(request, id):
    import json
    venta = get_object_or_404(Venta, id_venta=id)
    try:
        data = json.loads(request.body)
        cantidades = data.get('cantidades', [])
        observaciones = data.get('observaciones', '')
        fecha = data.get('fecha', None)
        detalles = list(venta.detalles.select_related('producto').all())
        if len(cantidades) != len(detalles):
            return JsonResponse({'success': False, 'error': 'Cantidad de productos no coincide.'})
        # Validar stock
        for idx, detalle in enumerate(detalles):
            nueva_cantidad = int(cantidades[idx])
            producto = detalle.producto
            stock_disponible = producto.stock_actual + detalle.cantidad
            if nueva_cantidad > stock_disponible:
                return JsonResponse({'success': False, 'error': f'Stock insuficiente para {producto.nombre}.'})
        # Actualizar detalles y stock
        for idx, detalle in enumerate(detalles):
            nueva_cantidad = int(cantidades[idx])
            producto = detalle.producto
            producto.stock_actual += detalle.cantidad  # devolver stock anterior
            producto.stock_actual -= nueva_cantidad    # restar nuevo
            producto.save()
            detalle.cantidad = nueva_cantidad
            detalle.save()
        venta.observaciones = observaciones
        if fecha:
            venta.fecha = fecha
        venta.save()
        return JsonResponse({'success': True})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})

@require_GET
def autocomplete_productos(request):
    query = request.GET.get('q', '').strip()
    categoria_id = request.GET.get('categoria')
    
    if not query:
        return JsonResponse({'results': []})
    
    # Primero buscar coincidencia exacta por nombre o código
    producto_exacto = Producto.objects.filter(
        Q(nombre__iexact=query) | 
        Q(codigo__codigo__iexact=query)
    ).first()
    
    if producto_exacto:
        # Si hay coincidencia exacta, retornar solo ese producto
        codigo = producto_exacto.codigo_set.first()
        return JsonResponse({
            'results': [{
                'id': producto_exacto.id_producto,
                'nombre': producto_exacto.nombre,
                'codigo': codigo.codigo if codigo else '',
                'precio_venta': float(producto_exacto.precio_unitario),
                'stock': producto_exacto.stock_actual,
                'categoria': producto_exacto.id_categoria.nombre if producto_exacto.id_categoria else None
            }]
        })
    
    # Si no hay coincidencia exacta, buscar coincidencias parciales
    productos = Producto.objects.filter(
        Q(nombre__icontains=query) | 
        Q(codigo__codigo__icontains=query)
    ).distinct()
    
    if categoria_id:
        productos = productos.filter(id_categoria_id=categoria_id)
    
    # Limitar a 10 resultados y ordenar por nombre
    productos = productos.order_by('nombre')[:10]
    
    results = []
    for p in productos:
        codigo = p.codigo_set.first()
        results.append({
            'id': p.id_producto,
            'nombre': p.nombre,
            'codigo': codigo.codigo if codigo else '',
            'precio_venta': float(p.precio_unitario),
            'stock': p.stock_actual,
            'categoria': p.id_categoria.nombre if p.id_categoria else None
        })
    
    return JsonResponse({'results': results})

def listar_reembolsos(request):
    reembolsos = Reembolso.objects.select_related('venta', 'usuario').prefetch_related('detalles__producto').order_by('-fecha_hora')
    # Filtros opcionales
    fecha_inicio = request.GET.get('fecha_inicio')
    fecha_fin = request.GET.get('fecha_fin')
    usuario_id = request.GET.get('usuario')
    producto_id = request.GET.get('producto')
    venta_id = request.GET.get('venta')
    if fecha_inicio:
        reembolsos = reembolsos.filter(fecha_hora__date__gte=fecha_inicio)
    if fecha_fin:
        reembolsos = reembolsos.filter(fecha_hora__date__lte=fecha_fin)
    if usuario_id:
        reembolsos = reembolsos.filter(usuario_id=usuario_id)
    if venta_id and venta_id not in ('', None, 'None'):
        try:
            venta_id_int = int(venta_id)
            reembolsos = reembolsos.filter(venta_id=venta_id_int)
        except ValueError:
            pass
    if producto_id:
        reembolsos = reembolsos.filter(detalles__producto_id=producto_id)
    usuarios = get_user_model().objects.all()
    productos = Producto.objects.all()
    total_reembolsado = reembolsos.aggregate(total=models.Sum('total_devuelto'))['total'] or 0
    resumen_producto = None
    if producto_id:
        # Calcular resumen para el producto filtrado
        detalles = ReembolsoDetalle.objects.filter(producto_id=producto_id, reembolso__in=reembolsos)
        total_unidades = detalles.aggregate(total=models.Sum('cantidad'))['total'] or 0
        total_dinero = detalles.aggregate(total=models.Sum('monto'))['total'] or 0
        usuarios_ids = detalles.values_list('reembolso__usuario__username', flat=True).distinct()
        usuarios_nombres = [u for u in usuarios_ids if u]
        nombre_producto = Producto.objects.filter(id_producto=producto_id).first().nombre if Producto.objects.filter(id_producto=producto_id).exists() else ''
        resumen_producto = {
            'nombre': nombre_producto,
            'total_unidades': total_unidades,
            'total_dinero': total_dinero,
            'usuarios': usuarios_nombres
        }
    return render(request, 'venta/lista_reembolsos.html', {
        'reembolsos': reembolsos,
        'usuarios': usuarios,
        'productos': productos,
        'total_reembolsado': total_reembolsado,
        'filtros': {
            'fecha_inicio': fecha_inicio,
            'fecha_fin': fecha_fin,
            'usuario_id': usuario_id,
            'producto_id': producto_id,
            'venta_id': venta_id,
        },
        'resumen_producto': resumen_producto
    })

def exportar_reembolsos_excel(request):
    # Obtener los mismos filtros que en listar_reembolsos
    reembolsos = Reembolso.objects.select_related('venta', 'usuario').prefetch_related('detalles__producto').order_by('-fecha_hora')
    fecha_inicio = request.GET.get('fecha_inicio')
    fecha_fin = request.GET.get('fecha_fin')
    usuario_id = request.GET.get('usuario')
    producto_id = request.GET.get('producto')
    venta_id = request.GET.get('venta')
    if fecha_inicio:
        reembolsos = reembolsos.filter(fecha_hora__date__gte=fecha_inicio)
    if fecha_fin:
        reembolsos = reembolsos.filter(fecha_hora__date__lte=fecha_fin)
    if usuario_id:
        reembolsos = reembolsos.filter(usuario_id=usuario_id)
    if venta_id and venta_id not in ('', None, 'None'):
        try:
            venta_id_int = int(venta_id)
            reembolsos = reembolsos.filter(venta_id=venta_id_int)
        except ValueError:
            pass
    if producto_id:
        reembolsos = reembolsos.filter(detalles__producto_id=producto_id)

    # Crear el archivo Excel
    output = BytesIO()
    workbook = xlsxwriter.Workbook(output)
    worksheet = workbook.add_worksheet()

    # Formatos
    header_format = workbook.add_format({
        'bold': True,
        'bg_color': '#D9E1F2',
        'border': 1
    })
    money_format = workbook.add_format({
        'num_format': '$#,##0',
        'border': 1
    })
    date_format = workbook.add_format({
        'num_format': 'yyyy-mm-dd hh:mm',
        'border': 1
    })
    border_format = workbook.add_format({'border': 1})

    # Escribir encabezados
    headers = ['Fecha', 'ID Venta', 'Productos', 'Cantidad', 'Total Devuelto', 'Usuario', 'Observaciones']
    for col, header in enumerate(headers):
        worksheet.write(0, col, header, header_format)

    # Escribir datos
    row = 1
    for reembolso in reembolsos:
        for detalle in reembolso.detalles.all():
            worksheet.write(row, 0, reembolso.fecha_hora, date_format)
            worksheet.write(row, 1, reembolso.venta.id_venta, border_format)
            worksheet.write(row, 2, detalle.producto.nombre, border_format)
            worksheet.write(row, 3, detalle.cantidad, border_format)
            worksheet.write(row, 4, float(detalle.monto), money_format)
            worksheet.write(row, 5, reembolso.usuario.username if reembolso.usuario else '', border_format)
            worksheet.write(row, 6, reembolso.observaciones or '', border_format)
            row += 1

    # Ajustar ancho de columnas
    worksheet.set_column('A:A', 20)
    worksheet.set_column('B:B', 10)
    worksheet.set_column('C:C', 30)
    worksheet.set_column('D:D', 10)
    worksheet.set_column('E:E', 15)
    worksheet.set_column('F:F', 15)
    worksheet.set_column('G:G', 40)

    # Escribir total
    total = reembolsos.aggregate(total=models.Sum('total_devuelto'))['total'] or 0
    worksheet.write(row, 3, 'Total:', header_format)
    worksheet.write(row, 4, float(total), money_format)

    workbook.close()
    output.seek(0)

    # Preparar la respuesta
    response = HttpResponse(
        output.read(),
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    response['Content-Disposition'] = f'attachment; filename=reembolsos_{datetime.now().strftime("%Y%m%d_%H%M")}.xlsx'
    return response

def exportar_reembolsos_pdf(request):
    # Obtener los mismos filtros que en listar_reembolsos
    reembolsos = Reembolso.objects.select_related('venta', 'usuario').prefetch_related('detalles__producto').order_by('-fecha_hora')
    fecha_inicio = request.GET.get('fecha_inicio')
    fecha_fin = request.GET.get('fecha_fin')
    usuario_id = request.GET.get('usuario')
    producto_id = request.GET.get('producto')
    venta_id = request.GET.get('venta')
    if fecha_inicio:
        reembolsos = reembolsos.filter(fecha_hora__date__gte=fecha_inicio)
    if fecha_fin:
        reembolsos = reembolsos.filter(fecha_hora__date__lte=fecha_fin)
    if usuario_id:
        reembolsos = reembolsos.filter(usuario_id=usuario_id)
    if venta_id and venta_id not in ('', None, 'None'):
        try:
            venta_id_int = int(venta_id)
            reembolsos = reembolsos.filter(venta_id=venta_id_int)
        except ValueError:
            pass
    if producto_id:
        reembolsos = reembolsos.filter(detalles__producto_id=producto_id)

    # Crear el PDF
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    elements = []
    styles = getSampleStyleSheet()

    # Título
    elements.append(Paragraph("Reporte de Reembolsos", styles['Title']))
    elements.append(Paragraph(f"Generado el {datetime.now().strftime('%Y-%m-%d %H:%M')}", styles['Normal']))
    elements.append(Paragraph("<br/><br/>", styles['Normal']))

    # Datos de la tabla
    data = [['Fecha', 'ID Venta', 'Producto', 'Cantidad', 'Total', 'Usuario', 'Observaciones']]
    for reembolso in reembolsos:
        for detalle in reembolso.detalles.all():
            data.append([
                reembolso.fecha_hora.strftime('%Y-%m-%d %H:%M'),
                str(reembolso.venta.id_venta),
                detalle.producto.nombre,
                str(detalle.cantidad),
                f"${detalle.monto:,.0f}",
                reembolso.usuario.username if reembolso.usuario else '',
                reembolso.observaciones or ''
            ])

    # Crear la tabla
    table = Table(data)
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.white),
        ('TEXTCOLOR', (0, 1), (-1, -1), colors.black),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 1), (-1, -1), 10),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('ALIGN', (3, 1), (4, -1), 'RIGHT'),
    ]))
    elements.append(table)

    # Total
    total = reembolsos.aggregate(total=models.Sum('total_devuelto'))['total'] or 0
    elements.append(Paragraph(f"<br/>Total Reembolsado: ${total:,.0f}", styles['Heading2']))

    # Generar PDF
    doc.build(elements)
    buffer.seek(0)

    # Preparar la respuesta
    response = HttpResponse(buffer.read(), content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename=reembolsos_{datetime.now().strftime("%Y%m%d_%H%M")}.pdf'
    return response

@require_POST
def eliminar_reembolso(request, id_reembolso):
    reembolso = get_object_or_404(Reembolso, id_reembolso=id_reembolso)
    reembolso.delete()
    messages.success(request, f'Reembolso de la venta #{reembolso.venta.id_venta} eliminado correctamente.')
    return redirect('listar_reembolsos')

def boleta_venta(request, id_venta):
    # Leer configuración desde la base de datos
    config = ConfiguracionBoleta.objects.first()
    FERRETERIA_NOMBRE = config.nombre if config else "Ferretería El Ingeniero"
    FERRETERIA_DIRECCION = config.direccion if config else "Av. Principal 123, Ciudad"
    FERRETERIA_FONO = config.fono if config else "Fono: +56 9 1234 5678"
    FERRETERIA_RUT = config.rut if config else "RUT: 12.345.678-9"
    LOGO_PATH = config.logo.path if config and config.logo else None

    venta = get_object_or_404(Venta, id_venta=id_venta)
    detalles = venta.detalles.select_related('producto').all()
    usuario = venta.usuario.username if venta.usuario else '—'
    observaciones = venta.observaciones or '—'
    fecha = venta.fecha.strftime('%d-%m-%Y') if hasattr(venta.fecha, 'strftime') else str(venta.fecha)
    nro_boleta = str(venta.id_venta).zfill(6)

    correo = config.correo if config else ""
    sitio_web = config.sitio_web if config else ""
    mensaje_pie = config.mensaje_pie if config else "¡Gracias por su compra!"

    from io import BytesIO
    buffer = BytesIO()
    p = canvas.Canvas(buffer, pagesize=letter)
    width, height = letter
    y = height - 40

    # Logo (si existe)
    if LOGO_PATH:
        try:
            from reportlab.lib.utils import ImageReader
            logo = ImageReader(LOGO_PATH)
            logo_width, logo_height = logo.getSize()
            max_logo_height = 50
            scale = max_logo_height / logo_height if logo_height > max_logo_height else 1
            display_width = logo_width * scale
            display_height = logo_height * scale
            x = (width - display_width) / 2
            p.drawImage(logo, x, y - display_height, width=display_width, height=display_height, mask='auto')
            y -= display_height + 25  # Más espacio después del logo
        except Exception as e:
            y -= 25

    # Encabezado
    p.setFont("Helvetica-Bold", 16)
    p.drawCentredString(width/2, y, FERRETERIA_NOMBRE)
    y -= 25
    p.setFont("Helvetica", 10)
    p.drawCentredString(width/2, y, FERRETERIA_DIRECCION)
    y -= 15
    p.drawCentredString(width/2, y, FERRETERIA_FONO)
    y -= 15
    p.drawCentredString(width/2, y, FERRETERIA_RUT)
    y -= 13
    if correo:
        p.drawCentredString(width/2, y, correo)
        y -= 13
    if sitio_web:
        p.drawCentredString(width/2, y, sitio_web)
        y -= 13
    y -= 10
    # Fecha y boleta
    p.setFont("Helvetica-Bold", 12)
    p.drawString(40, y, f"Fecha: {fecha}")
    p.drawString(220, y, f"N° Boleta: {nro_boleta}")
    y -= 18
    # Vendedor solo si hay nombre
    if usuario and usuario != '—':
        p.setFont("Helvetica", 10)
        p.drawString(40, y, f"Vendedor: {usuario}")
        y -= 15
    # Tabla de productos
    p.setFont("Helvetica-Bold", 10)
    x_producto = 60
    x_cant = x_producto + 140
    x_unit = x_cant + 50
    x_subt = x_unit + 70
    p.drawString(x_producto, y, "Producto")
    p.drawString(x_cant, y, "Cant.")
    p.drawString(x_unit, y, "P.Unitario")
    p.drawString(x_subt, y, "Subtotal")
    y -= 12
    p.setFont("Helvetica", 10)
    p.line(40, y, 500, y)
    y -= 10
    total = 0
    for det in detalles:
        if det.cantidad == 0:
            continue
        if y < 80:
            p.showPage()
            y = height - 40
        p.drawString(x_producto, y, str(det.producto.nombre))
        p.drawRightString(x_cant + 40, y, str(det.cantidad))
        p.drawRightString(x_unit + 60, y, f"${det.precio_unitario:,.0f}")
        p.drawRightString(x_subt + 60, y, f"${det.subtotal:,.0f}")
        total += det.subtotal
        y -= 15
    y -= 10
    # Totales
    p.setFont("Helvetica-Bold", 14)
    p.drawCentredString(width/2, y, "TOTAL A PAGAR")
    y -= 20
    p.setFont("Helvetica-Bold", 18)
    p.drawCentredString(width/2, y, f"${total:,.0f}")
    y -= 25
    p.setFont("Helvetica-Oblique", 9)
    p.setFillGray(0.4)
    p.drawCentredString(width/2, y, "IVA incluido en el precio")
    y -= 13
    p.drawCentredString(width/2, y, "Documento interno. No válido como boleta electrónica SII.")
    y -= 13
    if mensaje_pie:
        p.setFont("Helvetica", 10)
        p.setFillGray(0)
        p.drawCentredString(width/2, y, mensaje_pie)
    p.setFillGray(0)
    p.showPage()
    p.save()
    buffer.seek(0)
    return FileResponse(buffer, as_attachment=False, filename=f'boleta_venta_{venta.id_venta}.pdf', content_type='application/pdf')

@require_http_methods(["GET", "POST"])
def configurar_boleta(request):
    config = ConfiguracionBoleta.objects.first()
    if request.method == "POST":
        nombre = request.POST.get("nombre", "Ferretería El Ingeniero")
        direccion = request.POST.get("direccion", "Av. Principal 123, Ciudad")
        fono = request.POST.get("fono", "Fono: +56 9 1234 5678")
        rut = request.POST.get("rut", "RUT: 12.345.678-9")
        correo = request.POST.get("correo", "")
        sitio_web = request.POST.get("sitio_web", "")
        mensaje_pie = request.POST.get("mensaje_pie", "¡Gracias por su compra!")
        logo = request.FILES.get("logo")
        if not config:
            config = ConfiguracionBoleta()
        config.nombre = nombre
        config.direccion = direccion
        config.fono = fono
        config.rut = rut
        config.correo = correo
        config.sitio_web = sitio_web
        config.mensaje_pie = mensaje_pie
        if logo:
            config.logo = logo
        config.save()
        return redirect(reverse('ventas'))
    return render(request, 'venta/configurar_boleta.html', {"config": config})


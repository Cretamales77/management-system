from django.shortcuts import render, redirect, get_object_or_404
from home.models import Compra, Producto, Proveedore, DetalleCompra, ReembolsoCompra, ReembolsoCompraDetalle
from django.contrib import messages
from .forms import CompraForm, DetalleCompraFormSet
from django.db import transaction
from django.http import HttpResponse
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
from io import BytesIO
from datetime import datetime

def lista_compras(request):
    try:
        compras = Compra.objects.all().order_by('-fecha')
        return render(request, 'compras/lista_compras.html', {'compras': compras})
    except Exception as e:
        messages.error(request, f"Error al cargar las compras: {str(e)}")
        return render(request, 'compras/lista_compras.html', {'compras': []})

def nueva_compra(request):
    if request.method == 'POST':
        form = CompraForm(request.POST)
        formset = DetalleCompraFormSet(request.POST)
        if form.is_valid() and formset.is_valid():
            try:
                with transaction.atomic():
                    compra = form.save(commit=False)
                    compra.usuario = request.user if request.user.is_authenticated else None
                    compra.save()
                    detalles = formset.save(commit=False)
                    for detalle in detalles:
                        detalle.compra = compra
                        detalle.save()
                        # Actualizar stock del producto
                        detalle.producto.stock_actual += detalle.cantidad
                        detalle.producto.save()
                    formset.save_m2m()
                    compra.actualizar_total()
                    messages.success(request, "Compra registrada exitosamente.")
                    return redirect('lista_compras')
            except Exception as e:
                messages.error(request, f"Error al registrar la compra: {str(e)}")
        else:
            messages.error(request, "Por favor corrige los errores en el formulario.")
    else:
        form = CompraForm()
        formset = DetalleCompraFormSet()
    return render(request, 'compras/nueva_compra.html', {
        'form': form,
        'formset': formset
    })

def detalle_compra(request, id):
    compra = get_object_or_404(Compra, pk=id)
    detalles = compra.detalles.select_related('producto').all()
    return render(request, 'compras/detalle_compra.html', {
        'compra': compra,
        'detalles': detalles
    })

def editar_compra(request, id):
    compra = get_object_or_404(Compra, pk=id)
    if request.method == 'POST':
        try:
            id_producto = request.POST.get('producto')
            id_proveedor = request.POST.get('proveedor')
            cantidad = int(request.POST.get('cantidad'))
            precio_compra = float(request.POST.get('precio_compra'))
            observaciones = request.POST.get('observaciones', '')

            producto = Producto.objects.get(pk=id_producto)
            proveedor = Proveedore.objects.get(pk=id_proveedor)

            # Actualizar stock: restar cantidad anterior y sumar la nueva
            producto_anterior = compra.id_producto
            producto_anterior.stock_actual -= compra.cantidad
            producto_anterior.save()

            producto.stock_actual += cantidad
            producto.save()

            compra.id_producto = producto
            compra.id_proveedor = proveedor
            compra.cantidad = cantidad
            compra.precio_compra = precio_compra
            compra.observaciones = observaciones
            compra.save()

            messages.success(request, "Compra actualizada exitosamente.")
            return redirect('lista_compras')
        except Exception as e:
            messages.error(request, f"Error al actualizar la compra: {str(e)}")

    productos = Producto.objects.all()
    proveedores = Proveedore.objects.all()
    return render(request, 'compras/editar_compra.html', {
        'compra': compra,
        'productos': productos,
        'proveedores': proveedores
    })

def eliminar_compra(request, id):
    compra = get_object_or_404(Compra, pk=id)

    try:
        with transaction.atomic():
            # Actualizar stock de todos los productos de la compra
            for detalle in compra.detalles.all():
                producto = detalle.producto
                producto.stock_actual -= detalle.cantidad
                producto.save()

            # Eliminar la compra (esto también eliminará los detalles por CASCADE)
            compra.delete()
            messages.success(request, "Compra eliminada exitosamente.")
    except Exception as e:
        messages.error(request, f"Error al eliminar la compra: {str(e)}")

    return redirect('lista_compras')

def pdf_compra(request, id):
    compra = get_object_or_404(Compra, pk=id)
    detalles = compra.detalles.select_related('producto').all()
    
    # Crear el PDF
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="compra_{compra.id_compra}.pdf"'
    
    # Crear el documento PDF
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    elements = []
    
    # Estilos
    styles = getSampleStyleSheet()
    title_style = styles['Heading1']
    normal_style = styles['Normal']
    
    # Título
    elements.append(Paragraph(f"COMPROBANTE DE COMPRA #{compra.id_compra}", title_style))
    elements.append(Paragraph("<br/>", normal_style))
    
    # Información de la compra
    compra_info = [
        ['ID de Compra:', str(compra.id_compra)],
        ['Proveedor:', compra.proveedor.nombre if compra.proveedor else 'No especificado'],
        ['Fecha:', compra.fecha.strftime('%d/%m/%Y %H:%M')],
        ['Estado:', compra.estado],
        ['Total:', f"${compra.total_compra:.2f}"],
    ]
    
    if compra.fecha_entrega:
        compra_info.append(['Fecha de Entrega:', compra.fecha_entrega.strftime('%d/%m/%Y %H:%M')])
    
    if compra.observaciones:
        compra_info.append(['Observaciones:', compra.observaciones])
    
    compra_table = Table(compra_info, colWidths=[100, 300])
    compra_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, -1), colors.grey),
        ('TEXTCOLOR', (0, 0), (0, -1), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
        ('BACKGROUND', (1, 0), (1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))
    elements.append(compra_table)
    elements.append(Paragraph("<br/>", normal_style))
    
    # Productos de la compra
    elements.append(Paragraph("Productos de la Compra", styles['Heading2']))
    elements.append(Paragraph("<br/>", normal_style))
    
    # Encabezados de la tabla de productos
    productos_data = [['#', 'Producto', 'Cantidad', 'Precio Compra', 'Subtotal']]
    
    # Datos de productos
    for i, detalle in enumerate(detalles, 1):
        productos_data.append([
            str(i),
            f"{detalle.producto.nombre} ({detalle.producto.marca})",
            str(detalle.cantidad),
            f"${detalle.precio_compra:.2f}",
            f"${detalle.subtotal:.2f}"
        ])
    
    # Fila del total
    productos_data.append(['', '', '', 'TOTAL:', f"${compra.total_compra:.2f}"])
    
    productos_table = Table(productos_data, colWidths=[30, 200, 60, 80, 80])
    productos_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
        ('BACKGROUND', (0, 1), (-1, -2), colors.beige),
        ('ALIGN', (1, 1), (1, -2), 'LEFT'),  # Alinear texto del producto a la izquierda
        ('FONTNAME', (0, 1), (-1, -2), 'Helvetica'),
        ('FONTNAME', (0, -1), (-1, -1), 'Helvetica-Bold'),  # Total en negrita
        ('BACKGROUND', (0, -1), (-1, -1), colors.lightgrey),  # Fondo gris para el total
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))
    elements.append(productos_table)
    
    # Construir el PDF
    doc.build(elements)
    pdf = buffer.getvalue()
    buffer.close()
    response.write(pdf)
    
    return response

def reembolso_compra(request, id):
    compra = get_object_or_404(Compra, pk=id)
    detalles = compra.detalles.select_related('producto').all()
    
    if request.method == 'POST':
        try:
            with transaction.atomic():
                # Crear el reembolso
                reembolso = ReembolsoCompra.objects.create(
                    compra=compra,
                    usuario=request.user if request.user.is_authenticated else None,
                    observaciones=request.POST.get('observaciones', ''),
                    total_devuelto=0
                )
                
                total_devuelto = 0
                
                # Procesar cada producto reembolsado
                for detalle in detalles:
                    cantidad_reembolso = request.POST.get(f'cantidad_reembolso_{detalle.id_detalle}', '0')
                    if cantidad_reembolso and int(cantidad_reembolso) > 0:
                        cantidad_reembolso = int(cantidad_reembolso)
                        if cantidad_reembolso <= detalle.cantidad:
                            # Crear detalle del reembolso
                            monto_reembolso = (detalle.precio_compra * cantidad_reembolso)
                            ReembolsoCompraDetalle.objects.create(
                                reembolso=reembolso,
                                producto=detalle.producto,
                                cantidad=cantidad_reembolso,
                                monto=monto_reembolso
                            )
                            
                            # Actualizar stock del producto
                            detalle.producto.stock_actual -= cantidad_reembolso
                            detalle.producto.save()
                            
                            total_devuelto += monto_reembolso
                
                # Actualizar total del reembolso
                reembolso.total_devuelto = total_devuelto
                reembolso.save()
                
                # Actualizar estados de la compra y detalles
                compra.actualizar_estado()
                for detalle in detalles:
                    detalle.actualizar_estado()
                
                messages.success(request, f"Reembolso registrado exitosamente. Total devuelto: ${total_devuelto:.2f}")
                return redirect('detalle_compra', id=compra.id_compra)
                
        except Exception as e:
            messages.error(request, f"Error al procesar el reembolso: {str(e)}")
    
    return render(request, 'compras/reembolso_compra.html', {
        'compra': compra,
        'detalles': detalles
    })

from django.shortcuts import render, redirect, get_object_or_404
from home.models import Proveedore, Producto, ProductoProveedore
from .forms import ProveedoreForm
from django.contrib import messages

def proveedores(request):
    proveedores = Proveedore.objects.all()
    nombre_usuario = request.session.get('usuario_nombre', 'Invitado')
    return render(request, 'proveedor/proveedores.html', {
        'proveedores': proveedores,
        'nombre_usuario': nombre_usuario,
    })


def agregar_proveedor(request):
    if request.method == 'POST':
        form = ProveedoreForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Proveedor agregado correctamente.")
            return redirect('proveedores')
        else:
            messages.error(request, "Error al agregar el proveedor. Por favor, corrige los errores.")
    else:
        form = ProveedoreForm()
    return render(request, 'proveedor/form_proveedor.html', {'form': form, 'accion': 'Agregar'})


def editar_proveedor(request, id):
    proveedor = get_object_or_404(Proveedore, pk=id)
    if request.method == 'POST':
        form = ProveedoreForm(request.POST, instance=proveedor)
        if form.is_valid():
            form.save()
            messages.success(request, "Proveedor editado correctamente.")
            return redirect('proveedores')
        else:
            messages.error(request, "Error al editar el proveedor.")
    else:
        form = ProveedoreForm(instance=proveedor)
    return render(request, 'proveedor/form_proveedor.html', {'form': form, 'accion': 'Editar'})


def eliminar_proveedor(request, id):
    if request.method == 'POST':
        proveedor = get_object_or_404(Proveedore, id_proveedor=id)
        proveedor.delete()
        messages.success(request, "Proveedor eliminado correctamente.")
    return redirect('proveedores')


def proveedor_producto(request, proveedor_id):
    proveedor = get_object_or_404(Proveedore, pk=proveedor_id)
    producto_proveedores = ProductoProveedore.objects.filter(id_proveedor=proveedor).select_related('id_producto')
    
    # Productos que NO están asociados a este proveedor
    productos_no_en_proveedor = Producto.objects.exclude(
        id_producto__in=producto_proveedores.values_list('id_producto_id', flat=True)
    )
    
    nombre_usuario = request.session.get('usuario_nombre', 'Invitado')

    return render(request, 'proveedor/proveedor_producto.html', {
        'proveedor': proveedor,
        'producto_proveedores': producto_proveedores,
        'productos_no_en_proveedor': productos_no_en_proveedor,
        'nombre_usuario': nombre_usuario,
    })


def agregar_producto_proveedor(request, proveedor_id):
    if request.method == 'POST':
        proveedor = get_object_or_404(Proveedore, pk=proveedor_id)
        producto_id = request.POST.get('producto_id')
        precio_proveedor = request.POST.get('precio_proveedor')
        
        if producto_id and precio_proveedor:
            producto = get_object_or_404(Producto, id_producto=producto_id)
            
            # Crear o actualizar la relación producto-proveedor
            producto_proveedor, created = ProductoProveedore.objects.get_or_create(
                id_proveedor=proveedor,
                id_producto=producto,
                defaults={'precio_proveedor': precio_proveedor}
            )
            
            if not created:
                producto_proveedor.precio_proveedor = precio_proveedor
                producto_proveedor.save()
            
            messages.success(request, f"Producto {producto.nombre} agregado al proveedor {proveedor.nombre} con precio ${precio_proveedor}.")
    return redirect('proveedor_producto', proveedor_id=proveedor_id)


def editar_precio_proveedor(request, proveedor_id, producto_id):
    if request.method == 'POST':
        proveedor = get_object_or_404(Proveedore, pk=proveedor_id)
        producto = get_object_or_404(Producto, id_producto=producto_id)
        nuevo_precio = request.POST.get('precio_proveedor')
        
        if nuevo_precio:
            producto_proveedor = get_object_or_404(ProductoProveedore, 
                                                 id_proveedor=proveedor, 
                                                 id_producto=producto)
            producto_proveedor.precio_proveedor = nuevo_precio
            producto_proveedor.save()
            messages.success(request, f"Precio actualizado para {producto.nombre} a ${nuevo_precio}.")
    
    return redirect('proveedor_producto', proveedor_id=proveedor_id)


def eliminar_producto_proveedor(request, producto_id, proveedor_id):
    if request.method == 'POST':
        try:
            proveedor = get_object_or_404(Proveedore, id_proveedor=proveedor_id)
            producto = get_object_or_404(Producto, id_producto=producto_id)
            
            producto_proveedor = get_object_or_404(ProductoProveedore, 
                                                 id_proveedor=proveedor, 
                                                 id_producto=producto)
            nombre_producto = producto.nombre
            producto_proveedor.delete()
            
            messages.success(request, f"Producto {nombre_producto} eliminado del proveedor {proveedor.nombre}.")
        except Exception as e:
            messages.error(request, f"Error al eliminar el producto: {str(e)}")
    return redirect('proveedor_producto', proveedor_id=proveedor_id)
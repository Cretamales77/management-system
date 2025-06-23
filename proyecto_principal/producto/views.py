from django.shortcuts import render, redirect, get_object_or_404
from home.models import Producto, Codigo
from .forms import ProductoForm
from django.utils import timezone
from django.contrib import messages
from django.http import JsonResponse

def productos(request):
    lista_productos = Producto.objects.all()
    nombre_usuario = request.session.get('usuario_nombre', 'Invitado')
    return render(request, 'producto/productos.html', {
        'productos': lista_productos,
        'nombre_usuario': nombre_usuario,
    })

def agregar_producto(request):
    if request.method == 'POST':
        form = ProductoForm(request.POST)
        if form.is_valid():
            producto = form.save()
            codigo = request.POST.get('codigo')
            if codigo:
                Codigo.objects.create(id_producto=producto, codigo=codigo)
            messages.success(request, "Producto agregado exitosamente.")
        else:
            messages.error(request, "Error al agregar el producto.")
    return redirect('productos')

def editar_producto(request, id):
    producto = get_object_or_404(Producto, id_producto=id)
    if request.method == 'POST':
        form = ProductoForm(request.POST, instance=producto)
        if form.is_valid():
            form.save()
            codigo = request.POST.get('codigo')
            if codigo:
                Codigo.objects.filter(id_producto=producto).delete()
                Codigo.objects.create(id_producto=producto, codigo=codigo)
            messages.success(request, "Producto actualizado exitosamente.")
        else:
            messages.error(request, "Error al actualizar el producto.")
    return redirect('productos')

def eliminar_producto(request, id):
    if request.method == 'POST':
        producto = get_object_or_404(Producto, id_producto=id)
        producto.delete()
        messages.success(request, "Producto eliminado exitosamente.")
    return redirect('productos')

def validar_codigo(request):
    codigo = request.GET.get('codigo', '').strip()
    existe = Codigo.objects.filter(codigo=codigo).exists()
    return JsonResponse({'existe': existe})


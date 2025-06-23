from django.shortcuts import render, redirect, get_object_or_404
from home.models import Categoria, Producto 
from .forms import CategoriaForm
from django.contrib import messages


def categorias(request):
    categorias = Categoria.objects.all()
    nombre_usuario = request.session.get('usuario_nombre', 'Invitado')  # Obtiene el nombre del usuario de la sesión
    return render(request, 'categoria/categorias.html', {
        'categorias': categorias,
        'nombre_usuario': nombre_usuario
    })


def agregar_categoria(request):
    if request.method == 'POST':
        form = CategoriaForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Categoría agregada correctamente.")
            return redirect('categorias')
        else:
            messages.error(request, "Error al agregar la categoría. Por favor, corrige los errores.")
    else:
        form = CategoriaForm()
    return render(request, 'categoria/form_categoria.html', {'form': form, 'accion': 'Agregar'})


def editar_categoria(request, id):
    categoria = get_object_or_404(Categoria, pk=id)
    if request.method == 'POST':
        form = CategoriaForm(request.POST, instance=categoria)
        if form.is_valid():
            form.save()
            messages.success(request, "Categoría editada correctamente.")
            return redirect('categorias')
        else:
            messages.error(request, "Error al editar la categoría. ")
    else:
        form = CategoriaForm(instance=categoria)
    return render(request, 'categoria/form_categoria.html', {'form': form, 'accion': 'Editar'})


def eliminar_categoria(request, id):
    if request.method == 'POST':
        categoria = get_object_or_404(Categoria, id_categoria=id)
        categoria.delete()
        messages.success(request, "Categoría eliminada correctamente.")
    return redirect('categorias')


def categoria_producto(request, categoria_id):
    categoria = get_object_or_404(Categoria, pk=categoria_id)
    productos = Producto.objects.filter(id_categoria=categoria)
    productos_no_en_categoria = Producto.objects.filter(id_categoria__isnull=True)
    nombre_usuario = request.session.get('usuario_nombre', 'Invitado')

    return render(request, 'categoria/categoria_producto.html', {
        'categoria': categoria,
        'productos': productos,
        'productos_no_en_categoria': productos_no_en_categoria,
        'nombre_usuario': nombre_usuario,
    })


def agregar_producto_categoria(request, categoria_id):
    if request.method == 'POST':
        categoria = get_object_or_404(Categoria, pk=categoria_id)
        producto_id = request.POST.get('producto_id')
        if producto_id:
            producto = get_object_or_404(Producto, pk=producto_id)
            producto.id_categoria = categoria
            producto.save()
            messages.success(request, f"Producto {producto.nombre} agregado a la categoría {categoria.nombre}.")
    return redirect('categoria_producto', categoria_id=categoria_id)


def eliminar_producto_categoria(request, producto_id, categoria_id):
    if request.method == 'POST':
        producto = get_object_or_404(Producto, id_producto=producto_id, id_categoria_id=categoria_id)
        producto.id_categoria = None
        producto.save()
        messages.success(request, f"Producto {producto.nombre} eliminado de la categoría.")
        return redirect('categoria_producto', categoria_id=categoria_id)



from django.contrib import admin
from .models import Producto, Categoria, Compra, Venta, ProductoProveedore, Proveedore, Codigo

admin.site.register(Categoria)
admin.site.register(Producto)
admin.site.register(Codigo)
admin.site.register(ProductoProveedore)
admin.site.register(Compra)
admin.site.register(Venta)
admin.site.register(Proveedore)


from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),

    # rutas de la aplicación usuario (en la raíz)
    path('', include('usuario.urls')),

    # rutas de la app home
    path('main/', include('home.urls')),

    # rutas de la app categoria
    path('categoria/', include('categoria.urls')),

    # rutas de la app proveedor
    path('proveedor/', include('proveedor.urls')),

    # rutas de la app producto
    path('producto/', include('producto.urls')),

    # rutas de la app ventas
    path('ventas/', include('venta.urls')),
    path('estadistica/', include('estadistica.urls')),
    
    # rutas de la app compras
    path('compras/', include('compras.urls')),
]

from django.urls import path
from . import views

urlpatterns = [
    path('', views.proveedores, name='proveedores'),  # lista proveedores en /proveedor/
    path('agregar/', views.agregar_proveedor, name='agregar_proveedor'),
    path('editar/<int:id>/', views.editar_proveedor, name='editar_proveedor'),
    path('eliminar/<int:id>/', views.eliminar_proveedor, name='eliminar_proveedor'),
    
    # URLs para gestionar productos de proveedores
    path('<int:proveedor_id>/productos/', views.proveedor_producto, name='proveedor_producto'),
    path('<int:proveedor_id>/productos/agregar/', views.agregar_producto_proveedor, name='agregar_producto_proveedor'),
    path('<int:proveedor_id>/productos/editar-precio/<int:producto_id>/', views.editar_precio_proveedor, name='editar_precio_proveedor'),
    path('<int:proveedor_id>/productos/eliminar/<int:producto_id>/', views.eliminar_producto_proveedor, name='eliminar_producto_proveedor'),
]

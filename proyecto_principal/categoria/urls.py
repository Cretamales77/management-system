from django.urls import path
from . import views

urlpatterns = [
    path('', views.categorias, name='categorias'),  # lista categorías en /categoria/
    
    path('agregar/', views.agregar_categoria, name='agregar_categoria'),
    path('editar/<int:id>/', views.editar_categoria, name='editar_categoria'),
    path('eliminar/<int:id>/', views.eliminar_categoria, name='eliminar_categoria'),

    path('<int:categoria_id>/productos/', views.categoria_producto, name='categoria_producto'),
    path('<int:categoria_id>/productos/agregar/', views.agregar_producto_categoria, name='agregar_producto_categoria'),
    path('<int:categoria_id>/productos/eliminar/<int:producto_id>/', views.eliminar_producto_categoria, name='eliminar_producto_categoria'),
]

from django.urls import path
from . import views


urlpatterns = [
    path('', views.productos, name='productos'),  # lista productos en /producto/
    path('agregar/', views.agregar_producto, name='agregar_producto'),
    path('editar/<int:id>/', views.editar_producto, name='editar_producto'),
    path('eliminar/<int:id>/', views.eliminar_producto, name='eliminar_producto'),
    path('validar/', views.validar_codigo, name='validar_codigo'),
]
from django.urls import path
from . import views

urlpatterns = [
    path('', views.ventas, name='ventas'),
    path('carrito/agregar/', views.agregar_a_carrito, name='agregar_a_carrito'),
    path('carrito/eliminar/<int:producto_id>/', views.eliminar_de_carrito, name='eliminar_de_carrito'),
    path('carrito/editar/<int:producto_id>/', views.editar_carrito, name='editar_carrito'),
    path('carrito/finalizar/', views.finalizar_venta, name='finalizar_venta'),
    path('editar/<int:id>/', views.editar_venta, name='editar_venta'),
    path('eliminar/<int:id>/', views.eliminar_venta, name='eliminar_venta'),
    path('validar_producto/', views.validar_producto, name='validar_producto'),
    path('editar_ajax/<int:id>/', views.editar_venta_ajax, name='editar_venta_ajax'),
    path('autocomplete_productos/', views.autocomplete_productos, name='autocomplete_productos'),
    path('reembolsos/', views.listar_reembolsos, name='listar_reembolsos'),
    path('reembolsos/exportar/excel/', views.exportar_reembolsos_excel, name='exportar_reembolsos_excel'),
    path('reembolsos/exportar/pdf/', views.exportar_reembolsos_pdf, name='exportar_reembolsos_pdf'),
    path('reembolsos/eliminar/<int:id_reembolso>/', views.eliminar_reembolso, name='eliminar_reembolso'),
    path('boleta/<int:id_venta>/', views.boleta_venta, name='boleta_venta'),
    path('configurar-boleta/', views.configurar_boleta, name='configurar_boleta'),
]
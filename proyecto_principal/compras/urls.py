from django.urls import path
from . import views

urlpatterns = [
    path('', views.lista_compras, name='compras'),
    path('compras/', views.lista_compras, name='lista_compras'),
    path('compras/nueva/', views.nueva_compra, name='nueva_compra'),
    path('compras/editar/<int:id>/', views.editar_compra, name='editar_compra'),
    path('compras/eliminar/<int:id>/', views.eliminar_compra, name='eliminar_compra'),
    path('compras/detalle/<int:id>/', views.detalle_compra, name='detalle_compra'),
    path('compras/pdf/<int:id>/', views.pdf_compra, name='pdf_compra'),
    path('compras/reembolso/<int:id>/', views.reembolso_compra, name='reembolso_compra'),
]

from django.urls import path
from . import views

urlpatterns = [
    path('', views.login, name='login'),
    path('logout/', views.logout_view, name='logout'),#logout es para llamar esa view en el html
    path('verificacion/', views.verificacion, name='verificacion'),
    path('verificar/', views.verificar, name='verificar'),
    path('recuperar/', views.recuperar, name='recuperar'),
    
    # Rutas para el módulo de perfiles
    path('perfiles/', views.lista_perfiles, name='lista_perfiles'),
    path('perfiles/nuevo/', views.nuevo_perfil, name='nuevo_perfil'),
    path('perfiles/editar/<int:id_usuario>/', views.editar_perfil, name='editar_perfil'),
    path('perfiles/eliminar/<int:id_usuario>/', views.eliminar_perfil, name='eliminar_perfil'),
]

# urls.py en tu aplicación (por ejemplo, 'inventario/urls.py')
from django.urls import path
from . import views

urlpatterns = [
    path('', views.main, name='main'),
]

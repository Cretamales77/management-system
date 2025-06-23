from django.contrib import admin
from .models import Usuario

class UsuarioAdmin(admin.ModelAdmin):
    list_display = ('id_usuario', 'nombre_usuario', 'correo')
    search_fields = ('nombre_usuario', 'correo')

    # Excluye el campo 'contraseña' del formulario de edición directa
    # para evitar problemas de hash. La contraseña se debe cambiar
    # a través de los mecanismos de Django si fuera el User model.
    # Para este modelo custom, la lógica de cambio de contraseña está en las vistas.
    exclude = ('contraseña',)

admin.site.register(Usuario, UsuarioAdmin)

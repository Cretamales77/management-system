from django.contrib import admin
from django.contrib.auth.hashers import make_password
from .models import Usuario

class UsuarioAdmin(admin.ModelAdmin):
    list_display = ('nombre_usuario', 'correo')

    def save_model(self, request, obj, form, change):
        # Solo en caso de que la contraseña esté en texto plano
        if not obj.contraseña.startswith('pbkdf2_sha256$'):  # verifica si ya está hasheada
            obj.contraseña = make_password(obj.contraseña)
        super().save_model(request, obj, form, change)

admin.site.register(Usuario, UsuarioAdmin)

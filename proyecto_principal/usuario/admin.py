from django.contrib import admin
from .models import Usuario
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

class CustomUserAdmin(UserAdmin):
    add_form = UserCreationForm
    form = UserChangeForm
    model = Usuario
    list_display = ['nombre_usuario', 'correo']
    
    # Define los campos que se mostrarán al añadir un nuevo usuario
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('nombre_usuario', 'correo', 'password', 'password2')}
        ),
    )
    
    # Define los campos que se mostrarán al editar un usuario existente
    fieldsets = (
        (None, {'fields': ('nombre_usuario', 'correo')}),
    )

# Desregistra el modelo de usuario si ya estaba registrado de forma simple
try:
    admin.site.unregister(Usuario)
except admin.sites.NotRegistered:
    pass

# Registra el modelo de usuario con la configuración personalizada
admin.site.register(Usuario, CustomUserAdmin)

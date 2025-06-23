from django.contrib import admin
from .models import Usuario
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .forms import UsuarioCreationForm

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

@admin.register(Usuario)
class UsuarioAdmin(admin.ModelAdmin):
    list_display = ('id_usuario', 'nombre_usuario', 'correo')
    search_fields = ('nombre_usuario', 'correo')

    # Usa nuestro formulario personalizado solo para la página de "añadir"
    add_form = UsuarioCreationForm

    def get_form(self, request, obj=None, **kwargs):
        """
        Usa un formulario diferente para crear que para editar.
        """
        defaults = {}
        if obj is None:
            defaults['form'] = self.add_form
        defaults.update(kwargs)
        return super().get_form(request, obj, **defaults)

    def save_model(self, request, obj, form, change):
        """
        Asegura que la contraseña se guarde correctamente al crear
        un nuevo usuario desde el admin.
        """
        if not change: # Solo al crear un usuario nuevo
            obj.set_password(form.cleaned_data["password"])
        super().save_model(request, obj, form, change)

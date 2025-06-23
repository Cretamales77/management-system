from django.contrib import admin
from django import forms
from .models import Usuario

class UsuarioAdminForm(forms.ModelForm):
    """
    Formulario personalizado para manejar la creación y edición de usuarios
    en el panel de administración.
    """
    # Se define el campo de contraseña para que use el widget de password
    # y no sea obligatorio en la edición (dejar en blanco para no cambiar).
    contraseña = forms.CharField(widget=forms.PasswordInput, required=False, help_text="Dejar en blanco para no cambiar la contraseña. La contraseña se guardará cifrada.")

    class Meta:
        model = Usuario
        fields = ('nombre_usuario', 'correo', 'contraseña')

    def save(self, commit=True):
        # Se sobreescribe el método save para hashear la contraseña
        # solo si se ha introducido una nueva.
        user = super().save(commit=False)
        password = self.cleaned_data.get("contraseña")
        if password:
            user.set_password(password)
        
        if commit:
            user.save()
        return user


class UsuarioAdmin(admin.ModelAdmin):
    # Usa el formulario personalizado
    form = UsuarioAdminForm
    
    list_display = ('nombre_usuario', 'correo', 'is_staff')
    search_fields = ('nombre_usuario', 'correo')

    # Define los campos que se mostrarán en el formulario.
    # Al crear, 'contraseña' será requerido por el form.
    # Al editar, no lo será.
    fields = ('nombre_usuario', 'correo', 'contraseña')


admin.site.register(Usuario, UsuarioAdmin)

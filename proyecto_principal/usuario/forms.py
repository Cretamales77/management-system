from django import forms
from .models import Usuario

class UsuarioCreationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirmar contraseña', widget=forms.PasswordInput)

    class Meta:
        model = Usuario
        fields = ('nombre_usuario', 'correo')

    def clean_nombre_usuario(self):
        nombre_usuario = self.cleaned_data['nombre_usuario']
        if Usuario.objects.filter(nombre_usuario=nombre_usuario).exists():
            raise forms.ValidationError('El nombre de usuario ya está registrado.')
        return nombre_usuario

    def clean_correo(self):
        correo = self.cleaned_data['correo']
        if Usuario.objects.filter(correo=correo).exists():
            raise forms.ValidationError('El correo ya está registrado.')
        return correo

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Las contraseñas no coinciden.')
        return cd['password2']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user 
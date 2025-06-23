from django import forms
from home.models import Proveedore

class ProveedoreForm(forms.ModelForm):
    class Meta:
        model = Proveedore
        fields = [
            'nombre',
            'correo',
            'telefono',
            'direccion',
            'pais',
            'ciudad',
            'comuna'
        ]

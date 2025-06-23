# archivo: forms.py
from django import forms
from home.models import Producto

class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = [
            'id_categoria',
            'nombre',
            'marca',
            'descripcion',
            'stock_actual',
            'stock_minimo',
            'precio_unitario',
        ]
        widgets = {
            'descripcion': forms.Textarea(attrs={'rows': 3}),
        }
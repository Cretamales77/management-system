from django import forms
from home.models import Venta, DetalleVenta, Producto, Codigo

class VentaForm(forms.ModelForm):
    class Meta:
        model = Venta
        fields = ['observaciones']

class DetalleVentaForm(forms.ModelForm):
    class Meta:
        model = DetalleVenta
        fields = ['id_detalle', 'producto', 'cantidad']
        widgets = {
            'id_detalle': forms.HiddenInput(),
            'producto': forms.Select(attrs={'class': 'form-control'}),
            'cantidad': forms.NumberInput(attrs={'class': 'form-control', 'min': '1'})
        }

    def __init__(self, *args, **kwargs):
        self.venta = kwargs.pop('venta', None)
        super().__init__(*args, **kwargs)
        if self.venta:
            # Filtrar productos solo a los que están en la venta original
            self.fields['producto'].queryset = Producto.objects.filter(
                detalleventa__venta=self.venta
            ).distinct()

    def clean_producto(self):
        producto = self.cleaned_data.get('producto')
        if not producto:
            raise forms.ValidationError('Debe seleccionar un producto')
        return producto

    def clean_cantidad(self):
        cantidad = self.cleaned_data.get('cantidad')
        if cantidad is None or cantidad <= 0:
            raise forms.ValidationError('La cantidad debe ser mayor a 0')
        return cantidad



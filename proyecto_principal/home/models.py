from django.db import models
from django.utils import timezone
from django.conf import settings

# ---------------------- MODELOS DE PRODUCTOS Y CATEGORÍAS ----------------------

class Categoria(models.Model):
    id_categoria = models.AutoField(primary_key = True)
    nombre = models.CharField(max_length = 100)
    descripcion = models.TextField(blank = True, null = True)

    def __str__(self):
        return self.nombre


class Producto(models.Model):
    id_producto = models.AutoField(primary_key=True)
    id_categoria = models.ForeignKey(Categoria, on_delete=models.SET_NULL, null=True, blank=True)
    nombre = models.CharField(max_length=100)
    marca = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True)  
    stock_actual = models.IntegerField(default=0)  
    stock_minimo = models.IntegerField(null=True, blank=True)
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2)
    fecha_actualizacion = models.DateTimeField(null=True, blank=True)
    
    def __str__(self):
        return f"{self.nombre} ({self.marca})"

# ---------------------- MODELOS DE VENTAS Y DETALLES ----------------------

class Venta(models.Model):
    id_venta = models.AutoField(primary_key=True)
    fecha = models.DateTimeField(auto_now_add=True)
    fecha_modificacion = models.DateTimeField(null=True, blank=True)
    observaciones = models.TextField(blank=True, null=True)
    total_venta = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    estado = models.CharField(
        max_length=30,
        choices=[
            ('COMPLETADA', 'Completada'),
            ('REEMBOLSADA', 'Reembolsada'),
            ('PARCIALMENTE_REEMBOLSADA', 'Parcialmente Reembolsada'),
            ('ANULADA', 'Anulada')
        ],
        default='COMPLETADA'
    )
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"Venta {self.id_venta} - {self.fecha}"

    def save(self, *args, **kwargs):
        self.fecha_modificacion = timezone.now()
        super().save(*args, **kwargs)

    def actualizar_total(self):
        self.total_venta = sum(detalle.subtotal for detalle in self.detalles.all())
        self.save()

    def actualizar_estado(self):
        reembolsos = self.reembolsos.all()
        if not reembolsos.exists():
            self.estado = 'COMPLETADA'
        else:
            total_reembolsado = sum(reembolso.total_devuelto for reembolso in reembolsos)
            if total_reembolsado >= self.total_venta:
                self.estado = 'REEMBOLSADA'
            elif total_reembolsado > 0:
                self.estado = 'PARCIALMENTE_REEMBOLSADA'
            else:
                self.estado = 'COMPLETADA'
        self.save()


class DetalleVenta(models.Model):
    id_detalle = models.AutoField(primary_key=True)
    venta = models.ForeignKey(Venta, on_delete=models.CASCADE, related_name='detalles')
    producto = models.ForeignKey(Producto, on_delete=models.PROTECT)
    cantidad = models.IntegerField()
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    fecha_creacion = models.DateTimeField(null=True, blank=True)
    fecha_modificacion = models.DateTimeField(null=True, blank=True)
    estado = models.CharField(
        max_length=30,
        choices=[
            ('ACTIVO', 'Activo'),
            ('REEMBOLSADO', 'Reembolsado'),
            ('PARCIALMENTE_REEMBOLSADO', 'Parcialmente Reembolsado')
        ],
        default='ACTIVO'
    )

    def __str__(self):
        return f"Detalle {self.id_detalle} - Venta {self.venta.id_venta} - {self.producto.nombre}"

    def save(self, *args, **kwargs):
        self.subtotal = self.cantidad * self.precio_unitario
        if not self.fecha_creacion:
            self.fecha_creacion = timezone.now()
        self.fecha_modificacion = timezone.now()
        super().save(*args, **kwargs)
        self.venta.actualizar_total()

    def actualizar_estado(self):
        reembolsos = ReembolsoDetalle.objects.filter(
            reembolso__venta=self.venta,
            producto=self.producto
        )
        if not reembolsos.exists():
            self.estado = 'ACTIVO'
        else:
            total_reembolsado = sum(reembolso.cantidad for reembolso in reembolsos)
            if total_reembolsado >= self.cantidad:
                self.estado = 'REEMBOLSADO'
            elif total_reembolsado > 0:
                self.estado = 'PARCIALMENTE_REEMBOLSADO'
            else:
                self.estado = 'ACTIVO'
        self.save()

# ---------------------- MODELOS DE REEMBOLSOS ----------------------

class Reembolso(models.Model):
    id_reembolso = models.AutoField(primary_key=True)
    venta = models.ForeignKey(Venta, on_delete=models.CASCADE, related_name='reembolsos')
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    fecha_hora = models.DateTimeField(auto_now_add=True)
    observaciones = models.TextField(blank=True, null=True)
    total_devuelto = models.DecimalField(max_digits=10, decimal_places=2)

    @property
    def es_reembolso_total(self):
        venta_original = self.venta
        productos_originales = set(venta_original.detalles.values_list('producto_id', flat=True))
        productos_reembolsados = set(self.detalles.values_list('producto_id', flat=True))
        return productos_originales == productos_reembolsados

    def __str__(self):
        return f"Reembolso {self.id_reembolso} de Venta {self.venta.id_venta}"


class ReembolsoDetalle(models.Model):
    reembolso = models.ForeignKey(Reembolso, on_delete=models.CASCADE, related_name='detalles')
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.IntegerField()
    monto = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.cantidad} x {self.producto.nombre} (Reembolso {self.reembolso.id_reembolso})"

# ---------------------- MODELOS DE CONFIGURACIÓN ----------------------

class ConfiguracionBoleta(models.Model):
    nombre = models.CharField(max_length=100, default="Ferretería El Ingeniero")
    direccion = models.CharField(max_length=200, default="Av. Principal 123, Ciudad")
    fono = models.CharField(max_length=50, default="Fono: +56 9 1234 5678")
    rut = models.CharField(max_length=20, default="RUT: 12.345.678-9")
    logo = models.ImageField(upload_to='boleta_logos/', null=True, blank=True)
    fecha_modificacion = models.DateTimeField(auto_now=True)
    correo = models.CharField(max_length=100, blank=True, default="")
    sitio_web = models.CharField(max_length=100, blank=True, default="")
    mensaje_pie = models.CharField(max_length=200, blank=True, default="¡Gracias por su compra!")

    def __str__(self):
        return f"Configuración Boleta ({self.nombre})"

# ---------------------- MODELOS DE CÓDIGOS, PROVEEDORES Y COMPRAS ----------------------

class Codigo(models.Model):
    id_codigo = models.AutoField(primary_key=True)
    id_producto = models.ForeignKey(Producto, on_delete = models.CASCADE)
    codigo = models.CharField(max_length=100)

    def __str__(self):
        return self.codigo


class Proveedore(models.Model):
    id_proveedor = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    correo = models.EmailField()
    telefono = models.CharField(max_length=20)
    direccion = models.CharField(max_length=200)
    pais = models.CharField(max_length=50)
    ciudad = models.CharField(max_length=50)
    comuna = models.CharField(max_length=50)

    def __str__(self):
        return self.nombre


class ProductoProveedore(models.Model):
    id_proveedor = models.ForeignKey(Proveedore, on_delete=models.CASCADE)
    id_producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    precio_proveedor = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, help_text="Precio al que vende este proveedor este producto")

    class Meta:
        unique_together = (('id_proveedor', 'id_producto'),)

    def __str__(self):
        return f"{self.id_producto.nombre} - {self.id_proveedor.nombre}"

# ---------------------- MODELOS DE COMPRAS Y DETALLES ----------------------

class Compra(models.Model):
    id_compra = models.AutoField(primary_key=True)
    proveedor = models.ForeignKey(Proveedore, on_delete=models.SET_NULL, null=True, blank=True)
    fecha = models.DateTimeField(auto_now_add=True)
    fecha_modificacion = models.DateTimeField(null=True, blank=True)
    fecha_entrega = models.DateTimeField(null=True, blank=True)
    observaciones = models.TextField(blank=True, null=True)
    total_compra = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    estado = models.CharField(
        max_length=30,
        choices=[
            ('COMPLETADA', 'Completada'),
            ('REEMBOLSADA', 'Reembolsada'),
            ('PARCIALMENTE_REEMBOLSADA', 'Parcialmente Reembolsada'),
            ('ANULADA', 'Anulada')
        ],
        default='COMPLETADA'
    )
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"Compra {self.id_compra} - {self.fecha}"

    def save(self, *args, **kwargs):
        self.fecha_modificacion = timezone.now()
        super().save(*args, **kwargs)

    def actualizar_total(self):
        self.total_compra = sum(detalle.subtotal for detalle in self.detalles.all())
        self.save()

    def actualizar_estado(self):
        reembolsos = self.reembolsos.all()
        if not reembolsos.exists():
            self.estado = 'COMPLETADA'
        else:
            total_reembolsado = sum(reembolso.total_devuelto for reembolso in reembolsos)
            if total_reembolsado >= self.total_compra:
                self.estado = 'REEMBOLSADA'
            elif total_reembolsado > 0:
                self.estado = 'PARCIALMENTE_REEMBOLSADA'
            else:
                self.estado = 'COMPLETADA'
        self.save()


class DetalleCompra(models.Model):
    id_detalle = models.AutoField(primary_key=True)
    compra = models.ForeignKey(Compra, on_delete=models.CASCADE, related_name='detalles')
    producto = models.ForeignKey(Producto, on_delete=models.PROTECT)
    cantidad = models.IntegerField()
    precio_compra = models.DecimalField(max_digits=10, decimal_places=2)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    fecha_creacion = models.DateTimeField(null=True, blank=True)
    fecha_modificacion = models.DateTimeField(null=True, blank=True)
    estado = models.CharField(
        max_length=30,
        choices=[
            ('ACTIVO', 'Activo'),
            ('REEMBOLSADO', 'Reembolsado'),
            ('PARCIALMENTE_REEMBOLSADO', 'Parcialmente Reembolsado')
        ],
        default='ACTIVO'
    )

    def __str__(self):
        return f"Detalle {self.id_detalle} - Compra {self.compra.id_compra} - {self.producto.nombre}"

    def save(self, *args, **kwargs):
        self.subtotal = self.cantidad * self.precio_compra
        if not self.fecha_creacion:
            self.fecha_creacion = timezone.now()
        self.fecha_modificacion = timezone.now()
        super().save(*args, **kwargs)
        self.compra.actualizar_total()

    def actualizar_estado(self):
        reembolsos = ReembolsoCompraDetalle.objects.filter(
            reembolso__compra=self.compra,
            producto=self.producto
        )
        if not reembolsos.exists():
            self.estado = 'ACTIVO'
        else:
            total_reembolsado = sum(reembolso.cantidad for reembolso in reembolsos)
            if total_reembolsado >= self.cantidad:
                self.estado = 'REEMBOLSADO'
            elif total_reembolsado > 0:
                self.estado = 'PARCIALMENTE_REEMBOLSADO'
            else:
                self.estado = 'ACTIVO'
        self.save()

# ---------------------- MODELOS DE REEMBOLSOS DE COMPRAS ----------------------

class ReembolsoCompra(models.Model):
    id_reembolso = models.AutoField(primary_key=True)
    compra = models.ForeignKey(Compra, on_delete=models.CASCADE, related_name='reembolsos')
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    fecha_hora = models.DateTimeField(auto_now_add=True)
    observaciones = models.TextField(blank=True, null=True)
    total_devuelto = models.DecimalField(max_digits=10, decimal_places=2)

    @property
    def es_reembolso_total(self):
        compra_original = self.compra
        productos_originales = set(compra_original.detalles.values_list('producto_id', flat=True))
        productos_reembolsados = set(self.detalles.values_list('producto_id', flat=True))
        return productos_originales == productos_reembolsados

    def __str__(self):
        return f"Reembolso {self.id_reembolso} de Compra {self.compra.id_compra}"


class ReembolsoCompraDetalle(models.Model):
    reembolso = models.ForeignKey(ReembolsoCompra, on_delete=models.CASCADE, related_name='detalles')
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.IntegerField()
    monto = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.cantidad} x {self.producto.nombre} (Reembolso {self.reembolso.id_reembolso})"

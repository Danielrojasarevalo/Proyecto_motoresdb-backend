from django.db import models
from django.core.validators import MinValueValidator, FileExtensionValidator
from decimal import Decimal


class Proveedor(models.Model):
    """Proveedores de productos agrícolas"""
    ESTADO_CHOICES = [
        ('activo', 'Activo'),
        ('inactivo', 'Inactivo'),
        ('pendiente', 'Pendiente'),
    ]
    
    nombre = models.CharField(max_length=200, unique=True)
    email = models.EmailField(unique=True)
    telefono = models.CharField(max_length=20, blank=True, null=True)
    direccion = models.TextField(blank=True, null=True)
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='activo')
    fecha_registro = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Proveedor'
        verbose_name_plural = 'Proveedores'
        ordering = ['nombre']
    
    def __str__(self):
        return self.nombre


class Categoria(models.Model):
    """Categorías de productos (Orgánico, Mineral, Bioestimulante, etc.)"""
    nombre = models.CharField(max_length=100, unique=True)
    descripcion = models.TextField(blank=True, null=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = 'Categoría'
        verbose_name_plural = 'Categorías'
        ordering = ['nombre']
    
    def __str__(self):
        return self.nombre


class Producto(models.Model):
    """Productos de abonos y fertilizantes"""
    ESTADO_CHOICES = [
        ('disponible', 'Disponible'),
        ('bajo_stock', 'Bajo stock'),
        ('critico', 'Crítico'),
        ('agotado', 'Agotado'),
    ]
    
    nombre = models.CharField(max_length=200)
    categoria = models.ForeignKey(Categoria, on_delete=models.PROTECT, related_name='productos')
    proveedor = models.ForeignKey(Proveedor, on_delete=models.PROTECT, related_name='productos')
    stock_actual = models.IntegerField(default=0, validators=[MinValueValidator(0)])
    stock_minimo = models.IntegerField(default=10, validators=[MinValueValidator(0)])
    stock_maximo = models.IntegerField(default=1000, validators=[MinValueValidator(0)])
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(Decimal('0.01'))], help_text='Precio de compra/costo')
    precio_venta = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(Decimal('0.01'))], default=Decimal('0.01'), help_text='Precio al que se vende al cliente')
    unidad_medida = models.CharField(max_length=50, default='sacos')
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='disponible')
    descripcion = models.TextField(blank=True, null=True)
    codigo_producto = models.CharField(max_length=50, unique=True, blank=True, null=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Producto'
        verbose_name_plural = 'Productos'
        ordering = ['nombre']
    
    def __str__(self):
        return f"{self.nombre} - {self.stock_actual} {self.unidad_medida}"
    
    def actualizar_estado(self):
        """Actualiza el estado del producto según el stock actual"""
        if self.stock_actual == 0:
            self.estado = 'agotado'
        elif self.stock_actual <= self.stock_minimo:
            self.estado = 'critico'
        elif self.stock_actual <= self.stock_minimo * 1.5:
            self.estado = 'bajo_stock'
        else:
            self.estado = 'disponible'
        self.save()


class Cliente(models.Model):
    """Clientes que compran los productos"""
    TIPO_CHOICES = [
        ('cooperativa', 'Cooperativa'),
        ('finca', 'Finca'),
        ('empresa', 'Empresa'),
        ('particular', 'Particular'),
    ]
    
    nombre = models.CharField(max_length=200)
    tipo_cliente = models.CharField(max_length=20, choices=TIPO_CHOICES, default='particular')
    email = models.EmailField(blank=True, null=True)
    telefono = models.CharField(max_length=20, blank=True, null=True)
    direccion = models.TextField(blank=True, null=True)
    nit = models.CharField(max_length=50, unique=True, blank=True, null=True)
    fecha_registro = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Cliente'
        verbose_name_plural = 'Clientes'
        ordering = ['nombre']
    
    def __str__(self):
        return self.nombre


class Movimiento(models.Model):
    """Movimientos de entrada y salida de inventario"""
    TIPO_CHOICES = [
        ('entrada', 'Entrada'),
        ('salida', 'Salida'),
    ]
    
    producto = models.ForeignKey(Producto, on_delete=models.PROTECT, related_name='movimientos')
    tipo_movimiento = models.CharField(max_length=20, choices=TIPO_CHOICES)
    cantidad = models.IntegerField(validators=[MinValueValidator(1)])
    fecha_movimiento = models.DateTimeField()
    proveedor = models.ForeignKey(Proveedor, on_delete=models.SET_NULL, null=True, blank=True, related_name='movimientos')
    referencia = models.CharField(max_length=100, blank=True, null=True, help_text='Ej: Factura, Orden de compra, etc.')
    observaciones = models.TextField(blank=True, null=True)
    usuario_responsable = models.CharField(max_length=100, blank=True, null=True)
    fecha_registro = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = 'Movimiento'
        verbose_name_plural = 'Movimientos'
        ordering = ['-fecha_movimiento']
    
    def __str__(self):
        return f"{self.tipo_movimiento.upper()} - {self.producto.nombre} ({self.cantidad})"
    
    def save(self, *args, **kwargs):
        """Al guardar, actualiza el stock del producto"""
        is_new = self.pk is None
        super().save(*args, **kwargs)
        
        if is_new:
            if self.tipo_movimiento == 'entrada':
                self.producto.stock_actual += self.cantidad
            elif self.tipo_movimiento == 'salida':
                self.producto.stock_actual -= self.cantidad
            
            self.producto.actualizar_estado()


class Factura(models.Model):
    """Facturas de venta"""
    ESTADO_CHOICES = [
        ('pendiente', 'Pendiente'),
        ('pagada', 'Pagada'),
        ('cancelada', 'Cancelada'),
        ('vencida', 'Vencida'),
    ]
    
    numero_factura = models.CharField(max_length=50, unique=True)
    cliente = models.ForeignKey(Cliente, on_delete=models.PROTECT, related_name='facturas')
    fecha_emision = models.DateField()
    fecha_vencimiento = models.DateField(blank=True, null=True)
    subtotal = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    impuestos = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    total = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='pendiente')
    observaciones = models.TextField(blank=True, null=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Factura'
        verbose_name_plural = 'Facturas'
        ordering = ['-fecha_emision']
    
    def __str__(self):
        return f"Factura {self.numero_factura} - {self.cliente.nombre}"
    
    def calcular_total(self):
        """Calcula el total de la factura basado en los detalles"""
        detalles = self.detalles.all()
        self.subtotal = sum(d.subtotal for d in detalles)
        self.total = self.subtotal + self.impuestos
        self.save()


class DetalleFactura(models.Model):
    """Detalles de productos en cada factura"""
    factura = models.ForeignKey(Factura, on_delete=models.CASCADE, related_name='detalles')
    producto = models.ForeignKey(Producto, on_delete=models.PROTECT)
    cantidad = models.IntegerField(validators=[MinValueValidator(1)])
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2)
    subtotal = models.DecimalField(max_digits=12, decimal_places=2)
    descuento = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    
    class Meta:
        verbose_name = 'Detalle de Factura'
        verbose_name_plural = 'Detalles de Factura'
    
    def __str__(self):
        return f"{self.producto.nombre} x {self.cantidad}"
    
    def save(self, *args, **kwargs):
        """Calcula el subtotal antes de guardar"""
        self.subtotal = (self.precio_unitario * self.cantidad) - self.descuento
        super().save(*args, **kwargs)
        # Actualiza el total de la factura
        self.factura.calcular_total()


class ReservaFiesta(models.Model):
    """Citas/reservas de fiestas en el salón de arriba de la tienda"""
    ESTADO_CHOICES = [
        ('pendiente', 'Pendiente'),
        ('confirmada', 'Confirmada'),
        ('realizada', 'Realizada'),
        ('cancelada', 'Cancelada'),
    ]

    nombre_cliente = models.CharField(max_length=200)
    telefono = models.CharField(max_length=20, blank=True, null=True)
    tipo_evento = models.CharField(max_length=100, blank=True, null=True, help_text='Ej: Cumpleaños, Boda, Grado')
    fecha = models.DateField()
    hora_inicio = models.TimeField(blank=True, null=True)
    hora_fin = models.TimeField(blank=True, null=True)
    numero_personas = models.IntegerField(blank=True, null=True, validators=[MinValueValidator(1)])
    precio = models.DecimalField(max_digits=12, decimal_places=2, validators=[MinValueValidator(Decimal('0'))], help_text='Cuánto se cobra por la fiesta')
    abono = models.DecimalField(max_digits=12, decimal_places=2, default=0, validators=[MinValueValidator(Decimal('0'))])
    descripcion = models.TextField(blank=True, null=True)
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='pendiente')
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Reserva de fiesta'
        verbose_name_plural = 'Reservas de fiestas'
        ordering = ['fecha', 'hora_inicio']

    def __str__(self):
        return f"{self.fecha} - {self.nombre_cliente}"

    @property
    def saldo(self):
        return self.precio - self.abono


class Glamping(models.Model):
    """Unidades de glamping que se ofrecen"""
    nombre = models.CharField(max_length=200)
    descripcion = models.TextField(blank=True, null=True)
    capacidad = models.IntegerField(blank=True, null=True, validators=[MinValueValidator(1)], help_text='Número de personas')
    activo = models.BooleanField(default=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Glamping'
        verbose_name_plural = 'Glampings'
        ordering = ['nombre']

    def __str__(self):
        return self.nombre


class GlampingPrecio(models.Model):
    """Diferentes precios de un glamping (entre semana, fin de semana, temporada...)"""
    glamping = models.ForeignKey(Glamping, on_delete=models.CASCADE, related_name='precios')
    concepto = models.CharField(max_length=100, help_text='Ej: Noche entre semana, Fin de semana, Temporada alta')
    precio = models.DecimalField(max_digits=12, decimal_places=2, validators=[MinValueValidator(Decimal('0'))])

    class Meta:
        verbose_name = 'Precio de glamping'
        verbose_name_plural = 'Precios de glamping'
        ordering = ['id']

    def __str__(self):
        return f"{self.glamping.nombre} - {self.concepto}: {self.precio}"


class GlampingImagen(models.Model):
    """Imágenes de un glamping"""
    glamping = models.ForeignKey(Glamping, on_delete=models.CASCADE, related_name='imagenes')
    imagen = models.FileField(
        upload_to='glampings/',
        validators=[FileExtensionValidator(['jpg', 'jpeg', 'png', 'webp', 'gif'])]
    )
    fecha_subida = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Imagen de glamping'
        verbose_name_plural = 'Imágenes de glamping'
        ordering = ['id']

    def __str__(self):
        return f"Imagen de {self.glamping.nombre}"

    def delete(self, *args, **kwargs):
        self.imagen.delete(save=False)
        super().delete(*args, **kwargs)

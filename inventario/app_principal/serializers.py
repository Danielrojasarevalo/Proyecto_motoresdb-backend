from rest_framework import serializers
from django.utils import timezone
from .models import Proveedor, Categoria, Producto, Cliente, Movimiento, Factura, DetalleFactura


class ProveedorSerializer(serializers.ModelSerializer):
    """Serializer para el modelo Proveedor"""
    class Meta:
        model = Proveedor
        fields = '__all__'
        read_only_fields = ['fecha_registro', 'fecha_actualizacion']


class CategoriaSerializer(serializers.ModelSerializer):
    """Serializer para el modelo Categoria"""
    productos_count = serializers.IntegerField(source='productos.count', read_only=True)
    
    class Meta:
        model = Categoria
        fields = ['id', 'nombre', 'descripcion', 'fecha_creacion', 'productos_count']
        read_only_fields = ['fecha_creacion']


class ProductoSerializer(serializers.ModelSerializer):
    """Serializer para el modelo Producto"""
    categoria_nombre = serializers.CharField(source='categoria.nombre', read_only=True)
    proveedor_nombre = serializers.CharField(source='proveedor.nombre', read_only=True)
    estado_display = serializers.CharField(source='get_estado_display', read_only=True)
    
    class Meta:
        model = Producto
        fields = [
            'id', 'nombre', 'categoria', 'categoria_nombre', 'proveedor', 'proveedor_nombre',
            'stock_actual', 'stock_minimo', 'stock_maximo', 'precio_unitario', 'precio_venta', 'unidad_medida',
            'estado', 'estado_display', 'descripcion', 'codigo_producto', 
            'fecha_creacion', 'fecha_actualizacion'
        ]
        read_only_fields = ['fecha_creacion', 'fecha_actualizacion']


class ProductoListSerializer(serializers.ModelSerializer):
    """Serializer simplificado para listados de productos"""
    categoria_nombre = serializers.CharField(source='categoria.nombre', read_only=True)
    proveedor_nombre = serializers.CharField(source='proveedor.nombre', read_only=True)
    
    class Meta:
        model = Producto
        fields = [
            'id', 'nombre', 'categoria_nombre', 'proveedor_nombre',
            'stock_actual', 'stock_minimo', 'stock_maximo', 'precio_unitario', 'precio_venta', 'unidad_medida', 'estado'
        ]


class ClienteSerializer(serializers.ModelSerializer):
    """Serializer para el modelo Cliente"""
    tipo_cliente_display = serializers.CharField(source='get_tipo_cliente_display', read_only=True)
    
    class Meta:
        model = Cliente
        fields = [
            'id', 'nombre', 'tipo_cliente', 'tipo_cliente_display', 'email', 
            'telefono', 'direccion', 'nit', 'fecha_registro', 'fecha_actualizacion'
        ]
        read_only_fields = ['fecha_registro', 'fecha_actualizacion']


class MovimientoSerializer(serializers.ModelSerializer):
    """Serializer para el modelo Movimiento"""
    producto_nombre = serializers.CharField(source='producto.nombre', read_only=True)
    proveedor_nombre = serializers.CharField(source='proveedor.nombre', read_only=True)
    tipo_movimiento_display = serializers.CharField(source='get_tipo_movimiento_display', read_only=True)
    
    class Meta:
        model = Movimiento
        fields = [
            'id', 'producto', 'producto_nombre', 'tipo_movimiento', 'tipo_movimiento_display',
            'cantidad', 'fecha_movimiento', 'proveedor', 'proveedor_nombre', 'referencia',
            'observaciones', 'usuario_responsable', 'fecha_registro'
        ]
        read_only_fields = ['fecha_registro']


class MovimientoCreateSerializer(serializers.ModelSerializer):
    """Serializer para crear movimientos"""
    class Meta:
        model = Movimiento
        fields = [
            'producto', 'tipo_movimiento', 'cantidad', 'fecha_movimiento',
            'proveedor', 'referencia', 'observaciones', 'usuario_responsable'
        ]


class DetalleFacturaSerializer(serializers.ModelSerializer):
    """Serializer para detalles de factura"""
    producto_nombre = serializers.CharField(source='producto.nombre', read_only=True)
    
    class Meta:
        model = DetalleFactura
        fields = [
            'id', 'producto', 'producto_nombre', 'cantidad', 
            'precio_unitario', 'descuento', 'subtotal'
        ]
        read_only_fields = ['subtotal']


class FacturaSerializer(serializers.ModelSerializer):
    """Serializer completo para facturas con detalles"""
    cliente_nombre = serializers.CharField(source='cliente.nombre', read_only=True)
    estado_display = serializers.CharField(source='get_estado_display', read_only=True)
    detalles = DetalleFacturaSerializer(many=True, read_only=True)
    
    class Meta:
        model = Factura
        fields = [
            'id', 'numero_factura', 'cliente', 'cliente_nombre', 'fecha_emision',
            'fecha_vencimiento', 'subtotal', 'impuestos', 'total', 'estado',
            'estado_display', 'observaciones', 'detalles', 'fecha_creacion', 'fecha_actualizacion'
        ]
        read_only_fields = ['subtotal', 'total', 'fecha_creacion', 'fecha_actualizacion']


class FacturaListSerializer(serializers.ModelSerializer):
    """Serializer simplificado para listados de facturas"""
    cliente_nombre = serializers.CharField(source='cliente.nombre', read_only=True)
    
    class Meta:
        model = Factura
        fields = [
            'id', 'numero_factura', 'cliente_nombre', 
            'fecha_emision', 'total', 'estado'
        ]


class FacturaCreateSerializer(serializers.ModelSerializer):
    """Serializer para crear facturas con detalles"""
    detalles = DetalleFacturaSerializer(many=True)
    
    class Meta:
        model = Factura
        fields = [
            'numero_factura', 'cliente', 'fecha_emision', 'fecha_vencimiento',
            'impuestos', 'estado', 'observaciones', 'detalles'
        ]
    
    def create(self, validated_data):
        detalles_data = validated_data.pop('detalles')
        factura = Factura.objects.create(**validated_data)

        for detalle_data in detalles_data:
            DetalleFactura.objects.create(factura=factura, **detalle_data)

        factura.calcular_total()

        # Si la factura se crea directamente como pagada, descontar inventario
        if factura.estado == 'pagada':
            self._generar_salidas(factura)

        return factura

    def _generar_salidas(self, factura):
        """Crea movimientos de salida por cada detalle de la factura"""
        for detalle in factura.detalles.all():
            Movimiento.objects.create(
                producto=detalle.producto,
                tipo_movimiento='salida',
                cantidad=detalle.cantidad,
                fecha_movimiento=timezone.now(),
                referencia=factura.numero_factura,
                observaciones=f'Venta - Factura {factura.numero_factura}',
            )


# Serializers para estadísticas y reportes
class DashboardStatsSerializer(serializers.Serializer):
    """Serializer para estadísticas del dashboard"""
    stock_total = serializers.IntegerField()
    productos_bajo_stock = serializers.IntegerField()
    entradas_recientes = serializers.IntegerField()
    ventas_mes = serializers.DecimalField(max_digits=12, decimal_places=2)
    productos_criticos = serializers.ListField(child=serializers.DictField())


class ReporteInventarioSerializer(serializers.Serializer):
    """Serializer para reportes de inventario"""
    producto = serializers.CharField()
    stock_actual = serializers.IntegerField()
    stock_minimo = serializers.IntegerField()
    estado = serializers.CharField()
    valor_inventario = serializers.DecimalField(max_digits=12, decimal_places=2)

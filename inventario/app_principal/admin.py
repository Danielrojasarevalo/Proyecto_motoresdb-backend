from django.contrib import admin
from .models import Proveedor, Categoria, Producto, Cliente, Movimiento, Factura, DetalleFactura


@admin.register(Proveedor)
class ProveedorAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'email', 'telefono', 'estado', 'fecha_registro']
    list_filter = ['estado', 'fecha_registro']
    search_fields = ['nombre', 'email']
    ordering = ['nombre']


@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'descripcion', 'fecha_creacion']
    search_fields = ['nombre']


@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'categoria', 'proveedor', 'stock_actual', 'precio_unitario', 'estado']
    list_filter = ['categoria', 'proveedor', 'estado']
    search_fields = ['nombre', 'codigo_producto']
    ordering = ['nombre']
    readonly_fields = ['fecha_creacion', 'fecha_actualizacion']


@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'tipo_cliente', 'email', 'telefono', 'nit']
    list_filter = ['tipo_cliente']
    search_fields = ['nombre', 'email', 'nit']
    ordering = ['nombre']


@admin.register(Movimiento)
class MovimientoAdmin(admin.ModelAdmin):
    list_display = ['producto', 'tipo_movimiento', 'cantidad', 'fecha_movimiento', 'proveedor', 'referencia']
    list_filter = ['tipo_movimiento', 'fecha_movimiento']
    search_fields = ['producto__nombre', 'referencia']
    ordering = ['-fecha_movimiento']
    date_hierarchy = 'fecha_movimiento'


class DetalleFacturaInline(admin.TabularInline):
    model = DetalleFactura
    extra = 1
    fields = ['producto', 'cantidad', 'precio_unitario', 'descuento', 'subtotal']
    readonly_fields = ['subtotal']


@admin.register(Factura)
class FacturaAdmin(admin.ModelAdmin):
    list_display = ['numero_factura', 'cliente', 'fecha_emision', 'total', 'estado']
    list_filter = ['estado', 'fecha_emision']
    search_fields = ['numero_factura', 'cliente__nombre']
    ordering = ['-fecha_emision']
    date_hierarchy = 'fecha_emision'
    readonly_fields = ['subtotal', 'total', 'fecha_creacion', 'fecha_actualizacion']
    inlines = [DetalleFacturaInline]


@admin.register(DetalleFactura)
class DetalleFacturaAdmin(admin.ModelAdmin):
    list_display = ['factura', 'producto', 'cantidad', 'precio_unitario', 'subtotal']
    list_filter = ['factura__fecha_emision']
    search_fields = ['factura__numero_factura', 'producto__nombre']
    readonly_fields = ['subtotal']


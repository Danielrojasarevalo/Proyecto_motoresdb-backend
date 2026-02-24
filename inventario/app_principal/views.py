from django.shortcuts import render
from django.db import transaction
from rest_framework import viewsets, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Sum, Count, Q, F
from django.db.models.deletion import ProtectedError
from datetime import datetime, timedelta
from decimal import Decimal

from .models import Proveedor, Categoria, Producto, Cliente, Movimiento, Factura, DetalleFactura
from .serializers import (
    ProveedorSerializer, CategoriaSerializer, ProductoSerializer, ProductoListSerializer,
    ClienteSerializer, MovimientoSerializer, MovimientoCreateSerializer,
    FacturaSerializer, FacturaListSerializer, FacturaCreateSerializer,
    DetalleFacturaSerializer, DashboardStatsSerializer
)


class ProveedorViewSet(viewsets.ModelViewSet):
    """
    ViewSet para gestionar proveedores
    
    list: Obtener todos los proveedores
    create: Crear un nuevo proveedor
    retrieve: Obtener un proveedor específico
    update: Actualizar un proveedor
    destroy: Eliminar un proveedor
    """
    queryset = Proveedor.objects.all()
    serializer_class = ProveedorSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['estado']
    search_fields = ['nombre', 'email']
    ordering_fields = ['nombre', 'fecha_registro']
    ordering = ['nombre']
    
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        try:
            with transaction.atomic():
                productos = instance.productos.all()
                for producto in productos:
                    producto.movimientos.all().delete()
                    DetalleFactura.objects.filter(producto=producto).delete()
                productos.delete()
                instance.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            return Response(
                {"error": f"Error al eliminar el proveedor: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    @action(detail=False, methods=['get'])
    def activos(self, request):
        """Obtener solo proveedores activos"""
        proveedores = self.queryset.filter(estado='activo')
        serializer = self.get_serializer(proveedores, many=True)
        return Response(serializer.data)


class CategoriaViewSet(viewsets.ModelViewSet):
    """
    ViewSet para gestionar categorías de productos
    """
    queryset = Categoria.objects.all()
    serializer_class = CategoriaSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['nombre']
    ordering = ['nombre']

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        try:
            with transaction.atomic():
                productos = instance.productos.all()
                for producto in productos:
                    producto.movimientos.all().delete()
                    DetalleFactura.objects.filter(producto=producto).delete()
                productos.delete()
                instance.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            return Response(
                {"error": f"Error al eliminar la categoría: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class ProductoViewSet(viewsets.ModelViewSet):
    """
    ViewSet para gestionar productos
    """
    queryset = Producto.objects.select_related('categoria', 'proveedor').all()
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['categoria', 'proveedor', 'estado']
    search_fields = ['nombre', 'codigo_producto']
    ordering_fields = ['nombre', 'stock_actual', 'precio_unitario', 'fecha_creacion']
    ordering = ['nombre']
    
    def get_serializer_class(self):
        if self.action == 'list':
            return ProductoListSerializer
        return ProductoSerializer
    
    @action(detail=False, methods=['get'])
    def bajo_stock(self, request):
        """Obtener productos con stock bajo o crítico"""
        productos = self.queryset.filter(
            Q(estado='bajo_stock') | Q(estado='critico') | Q(estado='agotado')
        )
        serializer = self.get_serializer(productos, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def disponibles(self, request):
        """Obtener productos disponibles"""
        productos = self.queryset.filter(estado='disponible')
        serializer = self.get_serializer(productos, many=True)
        return Response(serializer.data)
    
    def _resolver_fks(self, data):
        """Normaliza el payload antes de validar:
        - Resuelve categoria/proveedor si vienen como nombre (string no numérico)
        - Acepta stock_min/stock_max como alias de stock_minimo/stock_maximo
        """
        data = data.copy() if hasattr(data, 'copy') else dict(data)

        # Mapear alias de campos
        for alias, real in [('stock_min', 'stock_minimo'), ('stock_max', 'stock_maximo')]:
            if alias in data and real not in data:
                data[real] = data.pop(alias)

        # Resolver categoria: puede venir como ID numérico, string numérico o nombre
        cat_val = data.get('categoria') or data.get('categoria_nombre')
        if cat_val is not None:
            try:
                int(cat_val)  # Si es numérico, ya es un ID válido
            except (ValueError, TypeError):
                # Es un nombre, buscamos el ID
                try:
                    data['categoria'] = Categoria.objects.get(nombre=cat_val).pk
                except Categoria.DoesNotExist:
                    pass

        # Resolver proveedor: puede venir como ID numérico, string numérico o nombre
        prov_val = data.get('proveedor') or data.get('proveedor_nombre')
        if prov_val is not None:
            try:
                int(prov_val)
            except (ValueError, TypeError):
                try:
                    data['proveedor'] = Proveedor.objects.get(nombre=prov_val).pk
                except Proveedor.DoesNotExist:
                    pass

        return data

    def create(self, request, *args, **kwargs):
        data = self._resolver_fks(request.data)
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        instance = serializer.save()
        instance.actualizar_estado()
        headers = self.get_success_headers(serializer.data)
        return Response(self.get_serializer(instance).data, status=status.HTTP_201_CREATED, headers=headers)

    def update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        instance = self.get_object()
        data = self._resolver_fks(request.data)
        serializer = self.get_serializer(instance, data=data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        # Recalcular estado según stock
        instance.refresh_from_db()
        instance.actualizar_estado()
        return Response(self.get_serializer(instance).data)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        try:
            with transaction.atomic():
                # Eliminar movimientos asociados
                instance.movimientos.all().delete()
                # Eliminar detalles de factura asociados
                DetalleFactura.objects.filter(producto=instance).delete()
                instance.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except ProtectedError as e:
            return Response(
                {"error": f"No se puede eliminar el producto porque tiene registros asociados: {str(e)}"},
                status=status.HTTP_409_CONFLICT
            )
        except Exception as e:
            return Response(
                {"error": f"Error al eliminar el producto: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    @action(detail=True, methods=['post'])
    def actualizar_stock(self, request, pk=None):
        """Actualizar el stock de un producto manualmente"""
        producto = self.get_object()
        nuevo_stock = request.data.get('stock_actual')
        
        if nuevo_stock is None:
            return Response(
                {'error': 'Debe proporcionar el stock_actual'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            producto.stock_actual = int(nuevo_stock)
            producto.actualizar_estado()
            serializer = self.get_serializer(producto)
            return Response(serializer.data)
        except ValueError:
            return Response(
                {'error': 'El stock debe ser un número entero'},
                status=status.HTTP_400_BAD_REQUEST
            )


class ClienteViewSet(viewsets.ModelViewSet):
    """
    ViewSet para gestionar clientes
    """
    queryset = Cliente.objects.all()
    serializer_class = ClienteSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['tipo_cliente']
    search_fields = ['nombre', 'email', 'nit']
    ordering_fields = ['nombre', 'fecha_registro']
    ordering = ['nombre']
    
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        try:
            with transaction.atomic():
                # DetalleFactura tiene on_delete=CASCADE desde Factura, se borran automáticamente
                instance.facturas.all().delete()
                instance.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            return Response(
                {"error": f"Error al eliminar el cliente: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    @action(detail=True, methods=['get'])
    def facturas(self, request, pk=None):
        """Obtener facturas de un cliente"""
        cliente = self.get_object()
        facturas = cliente.facturas.all()
        serializer = FacturaListSerializer(facturas, many=True)
        return Response(serializer.data)


class MovimientoViewSet(viewsets.ModelViewSet):
    """
    ViewSet para gestionar movimientos de inventario
    """
    queryset = Movimiento.objects.select_related('producto', 'proveedor').all()
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['tipo_movimiento', 'producto', 'proveedor']
    search_fields = ['producto__nombre', 'referencia']
    ordering_fields = ['fecha_movimiento', 'fecha_registro']
    ordering = ['-fecha_movimiento']
    
    def get_serializer_class(self):
        if self.action == 'create':
            return MovimientoCreateSerializer
        return MovimientoSerializer
    
    @action(detail=False, methods=['get'])
    def recientes(self, request):
        """Obtener movimientos recientes (últimos 7 días)"""
        fecha_inicio = datetime.now() - timedelta(days=7)
        movimientos = self.queryset.filter(fecha_movimiento__gte=fecha_inicio)
        serializer = self.get_serializer(movimientos, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def entradas(self, request):
        """Obtener solo entradas de inventario"""
        movimientos = self.queryset.filter(tipo_movimiento='entrada')
        serializer = self.get_serializer(movimientos, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def salidas(self, request):
        """Obtener solo salidas de inventario"""
        movimientos = self.queryset.filter(tipo_movimiento='salida')
        serializer = self.get_serializer(movimientos, many=True)
        return Response(serializer.data)


class FacturaViewSet(viewsets.ModelViewSet):
    """
    ViewSet para gestionar facturas
    """
    queryset = Factura.objects.select_related('cliente').prefetch_related('detalles').all()
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['estado', 'cliente']
    search_fields = ['numero_factura', 'cliente__nombre']
    ordering_fields = ['fecha_emision', 'total']
    ordering = ['-fecha_emision']
    
    def get_serializer_class(self):
        if self.action == 'list':
            return FacturaListSerializer
        elif self.action == 'create':
            return FacturaCreateSerializer
        return FacturaSerializer
    
    @action(detail=False, methods=['get'])
    def pendientes(self, request):
        """Obtener facturas pendientes"""
        facturas = self.queryset.filter(estado='pendiente')
        serializer = FacturaListSerializer(facturas, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def pagadas(self, request):
        """Obtener facturas pagadas"""
        facturas = self.queryset.filter(estado='pagada')
        serializer = FacturaListSerializer(facturas, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def cambiar_estado(self, request, pk=None):
        """Cambiar el estado de una factura"""
        factura = self.get_object()
        nuevo_estado = request.data.get('estado')
        
        estados_validos = ['pendiente', 'pagada', 'cancelada', 'vencida']
        if nuevo_estado not in estados_validos:
            return Response(
                {'error': f'Estado inválido. Debe ser uno de: {", ".join(estados_validos)}'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        estado_anterior = factura.estado
        factura.estado = nuevo_estado
        factura.save()

        # Si pasa a pagada y antes NO era pagada, generar salidas de inventario
        if nuevo_estado == 'pagada' and estado_anterior != 'pagada':
            ya_tiene_salidas = Movimiento.objects.filter(
                referencia=factura.numero_factura,
                tipo_movimiento='salida'
            ).exists()
            if not ya_tiene_salidas:
                for detalle in factura.detalles.all():
                    from django.utils import timezone
                    Movimiento.objects.create(
                        producto=detalle.producto,
                        tipo_movimiento='salida',
                        cantidad=detalle.cantidad,
                        fecha_movimiento=timezone.now(),
                        referencia=factura.numero_factura,
                        observaciones=f'Venta - Factura {factura.numero_factura}',
                    )

        serializer = self.get_serializer(factura)
        return Response(serializer.data)


class DashboardViewSet(viewsets.ViewSet):
    """
    ViewSet para obtener estadísticas del dashboard
    """
    
    @action(detail=False, methods=['get'])
    def stats(self, request):
        """Obtener estadísticas generales del dashboard"""
        
        # Stock total
        stock_total = Producto.objects.aggregate(
            total=Sum('stock_actual')
        )['total'] or 0
        
        # Productos bajo stock
        productos_bajo_stock = Producto.objects.filter(
            Q(estado='bajo_stock') | Q(estado='critico') | Q(estado='agotado')
        ).count()
        
        # Entradas recientes (últimos 7 días)
        fecha_inicio = datetime.now() - timedelta(days=7)
        entradas_recientes = Movimiento.objects.filter(
            tipo_movimiento='entrada',
            fecha_movimiento__gte=fecha_inicio
        ).aggregate(total=Sum('cantidad'))['total'] or 0
        
        # Ventas del mes
        primer_dia_mes = datetime.now().replace(day=1)
        ventas_mes = Factura.objects.filter(
            fecha_emision__gte=primer_dia_mes,
            estado='pagada'
        ).aggregate(total=Sum('total'))['total'] or Decimal('0.00')
        
        # Productos críticos
        productos_criticos = Producto.objects.filter(estado='critico').values(
            'id', 'nombre', 'stock_actual', 'stock_minimo'
        )[:5]
        
        data = {
            'stock_total': stock_total,
            'productos_bajo_stock': productos_bajo_stock,
            'entradas_recientes': entradas_recientes,
            'ventas_mes': ventas_mes,
            'productos_criticos': list(productos_criticos)
        }
        
        return Response(data)
    
    @action(detail=False, methods=['get'])
    def resumen_mes(self, request):
        """Obtener resumen financiero del mes"""
        primer_dia_mes = datetime.now().replace(day=1)
        
        facturas_mes = Factura.objects.filter(fecha_emision__gte=primer_dia_mes)
        
        ventas = facturas_mes.filter(estado='pagada').aggregate(
            total=Sum('total')
        )['total'] or Decimal('0.00')
        
        # Costos estimados (suma de precios de entradas del mes)
        entradas_mes = Movimiento.objects.filter(
            tipo_movimiento='entrada',
            fecha_movimiento__gte=primer_dia_mes
        ).select_related('producto')
        
        costos = sum(
            movimiento.cantidad * movimiento.producto.precio_unitario 
            for movimiento in entradas_mes
        )
        
        utilidad = ventas - Decimal(str(costos))
        
        return Response({
            'ventas': ventas,
            'costos': costos,
            'utilidad': utilidad
        })


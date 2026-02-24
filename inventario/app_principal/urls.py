from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    ProveedorViewSet, CategoriaViewSet, ProductoViewSet,
    ClienteViewSet, MovimientoViewSet, FacturaViewSet, DashboardViewSet
)

# Crear el router para las APIs
router = DefaultRouter()
router.register(r'proveedores', ProveedorViewSet, basename='proveedor')
router.register(r'categorias', CategoriaViewSet, basename='categoria')
router.register(r'productos', ProductoViewSet, basename='producto')
router.register(r'clientes', ClienteViewSet, basename='cliente')
router.register(r'movimientos', MovimientoViewSet, basename='movimiento')
router.register(r'facturas', FacturaViewSet, basename='factura')
router.register(r'dashboard', DashboardViewSet, basename='dashboard')

urlpatterns = [
    path('', include(router.urls)),
]

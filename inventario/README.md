# ☕ Sistema de Inventario - Caficultura Verde

Sistema de gestión de inventario de abonos y fertilizantes para cafetales, desarrollado con Django REST Framework.

## 📋 Descripción

Aplicación web para gestionar el inventario completo de productos agrícolas, incluyendo:
- Control de stock de productos
- Gestión de proveedores y clientes
- Registro de movimientos (entradas/salidas)
- Facturación electrónica
- Dashboard con estadísticas en tiempo real
- Reportes y análisis

## 🚀 Tecnologías

- **Backend:** Django 6.0 + Django REST Framework
- **Base de datos:** SQLite (Desarrollo) / PostgreSQL (Producción)
- **Frontend:** Angular (Separado)
- **Autenticación:** Django Authentication

## 📦 Modelos de Base de Datos

### 1. Proveedor
Información de proveedores de productos agrícolas.

**Campos:**
- nombre, email, teléfono, dirección
- estado: activo, inactivo, pendiente

### 2. Categoría
Clasificación de productos (Orgánico, Mineral, Bioestimulante, etc.)

### 3. Producto
Catálogo completo de abonos y fertilizantes.

**Campos:**
- nombre, código, descripción
- categoría, proveedor
- stock_actual, stock_mínimo, stock_máximo
- precio_unitario, unidad_medida
- estado: disponible, bajo_stock, crítico, agotado

### 4. Cliente
Registro de clientes (Cooperativas, Fincas, Empresas, Particulares)

### 5. Movimiento
Registro de entradas y salidas de inventario.

**Tipos:**
- Entrada: Aumenta stock
- Salida: Disminuye stock

### 6. Factura
Documentos de venta con detalles de productos.

**Estados:**
- Pendiente, Pagada, Cancelada, Vencida

### 7. DetalleFactura
Líneas de productos en cada factura.

## 🔧 Instalación

### Requisitos Previos
- Python 3.12+
- pip
- virtualenv (recomendado)

### Paso 1: Clonar o ubicar el proyecto
```bash
cd "/home/daniel/OneDrive/Documentos/semestre5/Motores de base de datos/backend/inventario"
```

### Paso 2: Crear y activar entorno virtual
```bash
# Crear entorno virtual
python -m venv venv

# Activar en Linux/Mac
source venv/bin/activate

# Activar en Windows
venv\Scripts\activate
```

### Paso 3: Instalar dependencias
```bash
pip install django djangorestframework django-cors-headers django-filter
```

O si tienes un archivo `requirements.txt`:
```bash
pip install -r requirements.txt
```

### Paso 4: Configurar base de datos
```bash
# Crear migraciones
python manage.py makemigrations

# Aplicar migraciones
python manage.py migrate
```

### Paso 5: Crear superusuario (Administrador)
```bash
python manage.py createsuperuser
```

Sigue las instrucciones e ingresa:
- Username: admin
- Email: admin@caficultiverde.co
- Password: (tu contraseña segura)

### Paso 6: Cargar datos de prueba (Opcional)
```bash
python manage.py loaddata fixtures/initial_data.json
```

### Paso 7: Iniciar servidor
```bash
python manage.py runserver
```

El servidor estará disponible en: **http://localhost:8000**

## 📚 Documentación de APIs

La documentación completa de las APIs está disponible en:
- **[API_DOCUMENTATION.md](API_DOCUMENTATION.md)** - Documentación detallada de endpoints
- **[POSTMAN_EXAMPLES.md](POSTMAN_EXAMPLES.md)** - Ejemplos con Postman y cURL

### URLs Principales

| Endpoint | Descripción |
|----------|-------------|
| `/api/proveedores/` | CRUD de proveedores |
| `/api/categorias/` | CRUD de categorías |
| `/api/productos/` | CRUD de productos |
| `/api/clientes/` | CRUD de clientes |
| `/api/movimientos/` | Registro de movimientos |
| `/api/facturas/` | Gestión de facturas |
| `/api/dashboard/stats/` | Estadísticas generales |
| `/admin/` | Panel de administración |

## 🎯 Características Principales

### 🔄 Actualización Automática de Stock
- Los movimientos de entrada/salida actualizan automáticamente el stock
- Las facturas generan movimientos de salida automáticos
- Estados de productos actualizados dinámicamente

### 📊 Dashboard Inteligente
- Stock total en tiempo real
- Productos con bajo stock
- Entradas recientes (últimos 7 días)
- Ventas del mes
- Lista de productos críticos

### 🔍 Filtros y Búsqueda
Todos los endpoints principales incluyen:
- Búsqueda por texto
- Filtros por categoría, proveedor, estado
- Ordenamiento personalizado
- Paginación automática

### 💰 Cálculos Automáticos
- Subtotales de facturas
- Totales con impuestos
- Utilidades del mes
- Costos estimados

## 🛠️ Estructura del Proyecto

```
inventario/
├── inventario/              # Configuración del proyecto
│   ├── settings.py         # Configuración principal
│   ├── urls.py             # URLs principales
│   └── wsgi.py             # WSGI config
├── app_principal/          # Aplicación principal
│   ├── models.py           # Modelos de BD
│   ├── serializers.py      # Serializers DRF
│   ├── views.py            # ViewSets y lógica
│   ├── urls.py             # URLs de la app
│   ├── admin.py            # Configuración admin
│   └── migrations/         # Migraciones de BD
├── db.sqlite3              # Base de datos SQLite
├── manage.py               # Script de gestión
├── API_DOCUMENTATION.md    # Documentación APIs
├── POSTMAN_EXAMPLES.md     # Ejemplos Postman
└── README.md               # Este archivo
```

## 🔐 Panel de Administración

Acceder a: **http://localhost:8000/admin**

**Credenciales:** Las que creaste con `createsuperuser`

El panel permite:
- Gestión completa de todos los modelos
- Filtros avanzados
- Búsqueda rápida
- Acciones en lote
- Exportación de datos

## 🌐 Integración con Angular

### Configuración CORS
El backend ya está configurado para aceptar peticiones desde Angular:

```python
# settings.py
CORS_ALLOWED_ORIGINS = [
    "http://localhost:4200",
    "http://127.0.0.1:4200",
]
```

### Ejemplo de Servicio Angular

```typescript
import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';

@Injectable({ providedIn: 'root' })
export class ProductosService {
  private apiUrl = 'http://localhost:8000/api/productos/';

  constructor(private http: HttpClient) {}

  listarProductos() {
    return this.http.get(this.apiUrl);
  }

  crearProducto(producto: any) {
    return this.http.post(this.apiUrl, producto);
  }
}
```

Consulta **API_DOCUMENTATION.md** para más ejemplos completos.

## 📝 Ejemplos de Uso

### Crear un producto
```bash
curl -X POST "http://localhost:8000/api/productos/" \
  -H "Content-Type: application/json" \
  -d '{
    "nombre": "Abono Orgánico Premium",
    "categoria": 1,
    "proveedor": 1,
    "stock_actual": 320,
    "precio_unitario": "45000.00",
    "unidad_medida": "sacos"
  }'
```

### Registrar entrada de inventario
```bash
curl -X POST "http://localhost:8000/api/movimientos/" \
  -H "Content-Type: application/json" \
  -d '{
    "producto": 1,
    "tipo_movimiento": "entrada",
    "cantidad": 100,
    "fecha_movimiento": "2026-02-11T14:00:00Z",
    "proveedor": 1
  }'
```

### Obtener estadísticas del dashboard
```bash
curl -X GET "http://localhost:8000/api/dashboard/stats/"
```

## 🐛 Solución de Problemas

### Error: "No module named 'rest_framework'"
```bash
pip install djangorestframework
```

### Error: "No such table"
```bash
python manage.py migrate
```

### Error de CORS en Angular
Verifica que `django-cors-headers` esté instalado y configurado en `settings.py`

### Puerto 8000 en uso
```bash
# Usar otro puerto
python manage.py runserver 8001
```

## 🧪 Testing

### Ejecutar pruebas
```bash
python manage.py test
```

### Crear datos de prueba
```bash
python manage.py shell
```

```python
from app_principal.models import Proveedor, Categoria, Producto

# Crear proveedor
proveedor = Proveedor.objects.create(
    nombre="BioCafé",
    email="abonos@biocafe.co",
    estado="activo"
)

# Crear categoría
categoria = Categoria.objects.create(
    nombre="Orgánico"
)

# Crear producto
producto = Producto.objects.create(
    nombre="Abono Orgánico Premium",
    categoria=categoria,
    proveedor=proveedor,
    stock_actual=320,
    precio_unitario=45000,
    unidad_medida="sacos"
)
```

## 📈 Próximas Funcionalidades

- [ ] Autenticación JWT
- [ ] Reportes en PDF
- [ ] Gráficos estadísticos
- [ ] Notificaciones por email
- [ ] Exportación a Excel
- [ ] API de WhatsApp para alertas
- [ ] Integración con pasarelas de pago
- [ ] App móvil

## 🤝 Contribuir

1. Fork el proyecto
2. Crea una rama (`git checkout -b feature/nueva-funcionalidad`)
3. Commit tus cambios (`git commit -m 'Agregar nueva funcionalidad'`)
4. Push a la rama (`git push origin feature/nueva-funcionalidad`)
5. Abre un Pull Request

## 📄 Licencia

Este proyecto es de uso educativo y personal.

## 👨‍💻 Autor

**DANIEL ROJAS AREVALO**
- Email: daniel.rojas@example.com
- Proyecto: Caficultura Verde
- Año: 2026

---

## 📞 Soporte

Para reportar bugs o solicitar características:
- Crear un issue en el repositorio
- Contactar al desarrollador

---

**© 2026 DANIEL ROJAS AREVALO - Hecho con 💚 para el campo cafetero** ☕

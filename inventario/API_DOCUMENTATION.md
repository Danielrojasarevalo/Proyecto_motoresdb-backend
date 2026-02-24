# 📚 Documentación de APIs - Sistema de Inventario Caficultura Verde

## 🌐 URL Base
```
http://localhost:8000/api/
```

---

## 📋 Tabla de Contenidos
1. [Proveedores](#-proveedores)
2. [Categorías](#-categorías)
3. [Productos](#-productos)
4. [Clientes](#-clientes)
5. [Movimientos](#-movimientos)
6. [Facturas](#-facturas)
7. [Dashboard](#-dashboard)
8. [Códigos de Estado HTTP](#-códigos-de-estado-http)
9. [Ejemplos de Uso en Angular](#-ejemplos-de-uso-en-angular)

---

## 🏢 Proveedores

### Listar todos los proveedores
```http
GET /api/proveedores/
```

**Parámetros de consulta opcionales:**
- `estado` - Filtrar por estado (activo, inactivo, pendiente)
- `search` - Buscar por nombre o email
- `ordering` - Ordenar por campo (nombre, fecha_registro, -nombre)

**Respuesta exitosa (200 OK):**
```json
[
  {
    "id": 1,
    "nombre": "BioCafé",
    "email": "abonos@biocafe.co",
    "telefono": "3001234567",
    "direccion": "Calle 123 #45-67",
    "estado": "activo",
    "fecha_registro": "2026-01-15T10:30:00Z",
    "fecha_actualizacion": "2026-01-15T10:30:00Z"
  }
]
```

### Obtener un proveedor específico
```http
GET /api/proveedores/{id}/
```

**Respuesta exitosa (200 OK):**
```json
{
  "id": 1,
  "nombre": "BioCafé",
  "email": "abonos@biocafe.co",
  "telefono": "3001234567",
  "direccion": "Calle 123 #45-67",
  "estado": "activo",
  "fecha_registro": "2026-01-15T10:30:00Z",
  "fecha_actualizacion": "2026-01-15T10:30:00Z"
}
```

### Crear un nuevo proveedor
```http
POST /api/proveedores/
```

**Cuerpo de la petición:**
```json
{
  "nombre": "Suelo Verde",
  "email": "soporte@sueloverde.co",
  "telefono": "3009876543",
  "direccion": "Carrera 50 #30-20",
  "estado": "activo"
}
```

**Respuesta exitosa (201 Created):**
```json
{
  "id": 2,
  "nombre": "Suelo Verde",
  "email": "soporte@sueloverde.co",
  "telefono": "3009876543",
  "direccion": "Carrera 50 #30-20",
  "estado": "activo",
  "fecha_registro": "2026-02-11T14:20:00Z",
  "fecha_actualizacion": "2026-02-11T14:20:00Z"
}
```

### Actualizar un proveedor
```http
PUT /api/proveedores/{id}/
PATCH /api/proveedores/{id}/
```

**Cuerpo de la petición (PATCH - actualización parcial):**
```json
{
  "estado": "inactivo"
}
```

### Eliminar un proveedor
```http
DELETE /api/proveedores/{id}/
```

**Respuesta exitosa (204 No Content)**

### Obtener solo proveedores activos
```http
GET /api/proveedores/activos/
```

---

## 🏷️ Categorías

### Listar todas las categorías
```http
GET /api/categorias/
```

**Parámetros de consulta opcionales:**
- `search` - Buscar por nombre
- `ordering` - Ordenar por campo (nombre, -nombre)

**Respuesta exitosa (200 OK):**
```json
[
  {
    "id": 1,
    "nombre": "Orgánico",
    "descripcion": "Abonos orgánicos y naturales",
    "fecha_creacion": "2026-01-10T08:00:00Z",
    "productos_count": 5
  },
  {
    "id": 2,
    "nombre": "Mineral",
    "descripcion": "Fertilizantes minerales",
    "fecha_creacion": "2026-01-10T08:05:00Z",
    "productos_count": 3
  }
]
```

### Crear una categoría
```http
POST /api/categorias/
```

**Cuerpo de la petición:**
```json
{
  "nombre": "Bioestimulante",
  "descripcion": "Productos bioestimulantes para raíces"
}
```

### Actualizar, Eliminar
Mismo patrón que Proveedores con `/api/categorias/{id}/`

---

## 📦 Productos

### Listar todos los productos
```http
GET /api/productos/
```

**Parámetros de consulta opcionales:**
- `categoria` - Filtrar por ID de categoría
- `proveedor` - Filtrar por ID de proveedor
- `estado` - Filtrar por estado (disponible, bajo_stock, critico, agotado)
- `search` - Buscar por nombre o código
- `ordering` - Ordenar por campo (nombre, stock_actual, precio_unitario, -fecha_creacion)

**Respuesta exitosa (200 OK):**
```json
[
  {
    "id": 1,
    "nombre": "Abono Orgánico Premium",
    "categoria_nombre": "Orgánico",
    "proveedor_nombre": "BioCafé",
    "stock_actual": 320,
    "precio_unitario": "45000.00",
    "unidad_medida": "sacos",
    "estado": "disponible"
  }
]
```

### Obtener un producto específico
```http
GET /api/productos/{id}/
```

**Respuesta exitosa (200 OK):**
```json
{
  "id": 1,
  "nombre": "Abono Orgánico Premium",
  "categoria": 1,
  "categoria_nombre": "Orgánico",
  "proveedor": 1,
  "proveedor_nombre": "BioCafé",
  "stock_actual": 320,
  "stock_minimo": 50,
  "stock_maximo": 500,
  "precio_unitario": "45000.00",
  "unidad_medida": "sacos",
  "estado": "disponible",
  "estado_display": "Disponible",
  "descripcion": "Abono orgánico de alta calidad",
  "codigo_producto": "AO-001",
  "fecha_creacion": "2026-01-20T10:00:00Z",
  "fecha_actualizacion": "2026-02-11T12:30:00Z"
}
```

### Crear un producto
```http
POST /api/productos/
```

**Cuerpo de la petición:**
```json
{
  "nombre": "Fertilizante NPK 20-20-20",
  "categoria": 2,
  "proveedor": 3,
  "stock_actual": 45,
  "stock_minimo": 20,
  "stock_maximo": 200,
  "precio_unitario": "62000.00",
  "unidad_medida": "sacos",
  "descripcion": "Fertilizante mineral completo",
  "codigo_producto": "NPK-001"
}
```

### Actualizar un producto
```http
PUT /api/productos/{id}/
PATCH /api/productos/{id}/
```

### Eliminar un producto
```http
DELETE /api/productos/{id}/
```

### Obtener productos con bajo stock
```http
GET /api/productos/bajo_stock/
```

**Respuesta exitosa (200 OK):**
```json
[
  {
    "id": 2,
    "nombre": "Fertilizante NPK 20-20-20",
    "categoria_nombre": "Mineral",
    "proveedor_nombre": "AgroAndes",
    "stock_actual": 12,
    "precio_unitario": "62000.00",
    "unidad_medida": "sacos",
    "estado": "critico"
  }
]
```

### Obtener productos disponibles
```http
GET /api/productos/disponibles/
```

### Actualizar stock manualmente
```http
POST /api/productos/{id}/actualizar_stock/
```

**Cuerpo de la petición:**
```json
{
  "stock_actual": 150
}
```

**Respuesta exitosa (200 OK):**
Retorna el producto con el stock actualizado.

---

## 👥 Clientes

### Listar todos los clientes
```http
GET /api/clientes/
```

**Parámetros de consulta opcionales:**
- `tipo_cliente` - Filtrar por tipo (cooperativa, finca, empresa, particular)
- `search` - Buscar por nombre, email o NIT
- `ordering` - Ordenar por campo (nombre, fecha_registro)

**Respuesta exitosa (200 OK):**
```json
[
  {
    "id": 1,
    "nombre": "Cooperativa La Loma",
    "tipo_cliente": "cooperativa",
    "email": "contacto@laloma.co",
    "telefono": "3101234567",
    "direccion": "Vereda La Loma",
    "nit": "900123456-1",
    "fecha_registro": "2026-01-05T09:00:00Z",
    "fecha_actualizacion": "2026-01-05T09:00:00Z"
  }
]
```

### Crear un cliente
```http
POST /api/clientes/
```

**Cuerpo de la petición:**
```json
{
  "nombre": "Finca El Progreso",
  "tipo_cliente": "finca",
  "email": "elprogreso@gmail.com",
  "telefono": "3159876543",
  "direccion": "Km 15 Vía Chinchiná",
  "nit": "12345678-9"
}
```

### Obtener facturas de un cliente
```http
GET /api/clientes/{id}/facturas/
```

**Respuesta exitosa (200 OK):**
Retorna un array con todas las facturas del cliente.

### Actualizar, Eliminar
Mismo patrón: `PUT/PATCH/DELETE /api/clientes/{id}/`

---

## 📊 Movimientos

### Listar todos los movimientos
```http
GET /api/movimientos/
```

**Parámetros de consulta opcionales:**
- `tipo_movimiento` - Filtrar por tipo (entrada, salida)
- `producto` - Filtrar por ID de producto
- `proveedor` - Filtrar por ID de proveedor
- `search` - Buscar por nombre de producto o referencia
- `ordering` - Ordenar por campo (fecha_movimiento, -fecha_movimiento)

**Respuesta exitosa (200 OK):**
```json
[
  {
    "id": 1,
    "producto": 1,
    "producto_nombre": "Abono Orgánico Premium",
    "tipo_movimiento": "entrada",
    "cantidad": 60,
    "fecha_movimiento": "2026-02-09T10:00:00Z",
    "proveedor": 1,
    "proveedor_nombre": "BioCafé",
    "referencia": "OC-001",
    "observaciones": "Entrada de mercancía semanal",
    "usuario_responsable": "Juan Pérez",
    "fecha_registro": "2026-02-09T10:05:00Z"
  }
]
```

### Crear un movimiento
```http
POST /api/movimientos/
```

**Cuerpo de la petición:**
```json
{
  "producto": 1,
  "tipo_movimiento": "entrada",
  "cantidad": 100,
  "fecha_movimiento": "2026-02-11T14:00:00Z",
  "proveedor": 1,
  "referencia": "OC-002",
  "observaciones": "Nueva compra",
  "usuario_responsable": "María García"
}
```

**IMPORTANTE:** Al crear un movimiento:
- Si es "entrada": aumenta el stock del producto
- Si es "salida": disminuye el stock del producto
- Actualiza automáticamente el estado del producto

**Respuesta exitosa (201 Created):**
Retorna el movimiento creado.

### Obtener movimientos recientes (últimos 7 días)
```http
GET /api/movimientos/recientes/
```

### Obtener solo entradas
```http
GET /api/movimientos/entradas/
```

### Obtener solo salidas
```http
GET /api/movimientos/salidas/
```

### Actualizar, Eliminar
`PUT/PATCH/DELETE /api/movimientos/{id}/`

---

## 🧾 Facturas

### Listar todas las facturas
```http
GET /api/facturas/
```

**Parámetros de consulta opcionales:**
- `estado` - Filtrar por estado (pendiente, pagada, cancelada, vencida)
- `cliente` - Filtrar por ID de cliente
- `search` - Buscar por número de factura o nombre de cliente
- `ordering` - Ordenar por campo (fecha_emision, total, -fecha_emision)

**Respuesta exitosa (200 OK):**
```json
[
  {
    "id": 1,
    "numero_factura": "F-0231",
    "cliente": 1,
    "cliente_nombre": "Cooperativa La Loma",
    "fecha_emision": "2026-02-08",
    "total": "1250000.00",
    "estado": "pagada"
  }
]
```

### Obtener una factura específica
```http
GET /api/facturas/{id}/
```

**Respuesta exitosa (200 OK):**
```json
{
  "id": 1,
  "numero_factura": "F-0231",
  "cliente": 1,
  "cliente_nombre": "Cooperativa La Loma",
  "fecha_emision": "2026-02-08",
  "fecha_vencimiento": "2026-03-08",
  "subtotal": "1150000.00",
  "impuestos": "100000.00",
  "total": "1250000.00",
  "estado": "pagada",
  "observaciones": "",
  "fecha_creacion": "2026-02-08T09:00:00Z",
  "fecha_actualizacion": "2026-02-08T15:30:00Z",
  "detalles": [
    {
      "id": 1,
      "producto": 1,
      "producto_nombre": "Abono Orgánico Premium",
      "cantidad": 20,
      "precio_unitario": "45000.00",
      "subtotal": "900000.00",
      "descuento": "0.00"
    },
    {
      "id": 2,
      "producto": 2,
      "producto_nombre": "Fertilizante NPK 20-20-20",
      "cantidad": 5,
      "precio_unitario": "62000.00",
      "subtotal": "310000.00",
      "descuento": "0.00"
    }
  ]
}
```

### Crear una factura con detalles
```http
POST /api/facturas/
```

**Cuerpo de la petición:**
```json
{
  "numero_factura": "F-0232",
  "cliente": 2,
  "fecha_emision": "2026-02-11",
  "fecha_vencimiento": "2026-03-11",
  "impuestos": "80000.00",
  "estado": "pendiente",
  "observaciones": "Entrega programada para el 15 de febrero",
  "detalles": [
    {
      "producto": 1,
      "cantidad": 15,
      "precio_unitario": "45000.00",
      "descuento": "0.00"
    },
    {
      "producto": 3,
      "cantidad": 10,
      "precio_unitario": "38000.00",
      "descuento": "5000.00"
    }
  ]
}
```

**IMPORTANTE:**
- El campo `subtotal` y `total` se calculan automáticamente
- Los detalles también calculan su `subtotal` automáticamente
- Al crear los detalles, se genera un movimiento de salida para cada producto

**Respuesta exitosa (201 Created):**
Retorna la factura completa con todos sus detalles.

### Actualizar una factura
```http
PUT /api/facturas/{id}/
PATCH /api/facturas/{id}/
```

### Eliminar una factura
```http
DELETE /api/facturas/{id}/
```

### Obtener facturas pendientes
```http
GET /api/facturas/pendientes/
```

### Obtener facturas pagadas
```http
GET /api/facturas/pagadas/
```

### Cambiar estado de una factura
```http
POST /api/facturas/{id}/cambiar_estado/
```

**Cuerpo de la petición:**
```json
{
  "estado": "pagada"
}
```

**Estados válidos:**
- `pendiente`
- `pagada`
- `cancelada`
- `vencida`

**Respuesta exitosa (200 OK):**
Retorna la factura con el nuevo estado.

---

## 📈 Dashboard

### Obtener estadísticas generales
```http
GET /api/dashboard/stats/
```

**Respuesta exitosa (200 OK):**
```json
{
  "stock_total": 1245,
  "productos_bajo_stock": 8,
  "entradas_recientes": 210,
  "ventas_mes": "8400000.00",
  "productos_criticos": [
    {
      "id": 4,
      "nombre": "Bioestimulante Raíz Fuerte",
      "stock_actual": 12,
      "stock_minimo": 20
    }
  ]
}
```

**Descripción de campos:**
- `stock_total`: Total de sacos/unidades en inventario
- `productos_bajo_stock`: Cantidad de productos con bajo stock, crítico o agotado
- `entradas_recientes`: Total de unidades que entraron en los últimos 7 días
- `ventas_mes`: Total de ventas pagadas del mes actual
- `productos_criticos`: Lista de los 5 productos con menor stock

### Obtener resumen financiero del mes
```http
GET /api/dashboard/resumen_mes/
```

**Respuesta exitosa (200 OK):**
```json
{
  "ventas": "8400000.00",
  "costos": "5100000.00",
  "utilidad": "3300000.00"
}
```

**Descripción de campos:**
- `ventas`: Total de facturas pagadas del mes
- `costos`: Estimación de costos basada en entradas del mes
- `utilidad`: Ventas - Costos

---

## 🔢 Códigos de Estado HTTP

| Código | Significado | Descripción |
|--------|-------------|-------------|
| 200 | OK | Petición exitosa |
| 201 | Created | Recurso creado exitosamente |
| 204 | No Content | Recurso eliminado exitosamente |
| 400 | Bad Request | Datos inválidos en la petición |
| 404 | Not Found | Recurso no encontrado |
| 500 | Internal Server Error | Error en el servidor |

---

## 🅰️ Ejemplos de Uso en Angular

### 1. Crear un Servicio Angular

```typescript
// productos.service.ts
import { Injectable } from '@angular/core';
import { HttpClient, HttpParams } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class ProductosService {
  private apiUrl = 'http://localhost:8000/api/productos/';

  constructor(private http: HttpClient) {}

  // Listar todos los productos
  listarProductos(filtros?: any): Observable<any[]> {
    let params = new HttpParams();
    if (filtros) {
      Object.keys(filtros).forEach(key => {
        if (filtros[key]) {
          params = params.set(key, filtros[key]);
        }
      });
    }
    return this.http.get<any[]>(this.apiUrl, { params });
  }

  // Obtener un producto
  obtenerProducto(id: number): Observable<any> {
    return this.http.get<any>(`${this.apiUrl}${id}/`);
  }

  // Crear producto
  crearProducto(producto: any): Observable<any> {
    return this.http.post<any>(this.apiUrl, producto);
  }

  // Actualizar producto
  actualizarProducto(id: number, producto: any): Observable<any> {
    return this.http.put<any>(`${this.apiUrl}${id}/`, producto);
  }

  // Actualizar parcialmente
  actualizarParcial(id: number, datos: any): Observable<any> {
    return this.http.patch<any>(`${this.apiUrl}${id}/`, datos);
  }

  // Eliminar producto
  eliminarProducto(id: number): Observable<any> {
    return this.http.delete(`${this.apiUrl}${id}/`);
  }

  // Productos con bajo stock
  productosBarStock(): Observable<any[]> {
    return this.http.get<any[]>(`${this.apiUrl}bajo_stock/`);
  }

  // Actualizar stock
  actualizarStock(id: number, stock: number): Observable<any> {
    return this.http.post<any>(`${this.apiUrl}${id}/actualizar_stock/`, {
      stock_actual: stock
    });
  }
}
```

### 2. Servicio de Dashboard

```typescript
// dashboard.service.ts
import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class DashboardService {
  private apiUrl = 'http://localhost:8000/api/dashboard/';

  constructor(private http: HttpClient) {}

  obtenerEstadisticas(): Observable<any> {
    return this.http.get<any>(`${this.apiUrl}stats/`);
  }

  obtenerResumenMes(): Observable<any> {
    return this.http.get<any>(`${this.apiUrl}resumen_mes/`);
  }
}
```

### 3. Servicio de Movimientos

```typescript
// movimientos.service.ts
import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class MovimientosService {
  private apiUrl = 'http://localhost:8000/api/movimientos/';

  constructor(private http: HttpClient) {}

  listarMovimientos(): Observable<any[]> {
    return this.http.get<any[]>(this.apiUrl);
  }

  crearMovimiento(movimiento: any): Observable<any> {
    return this.http.post<any>(this.apiUrl, movimiento);
  }

  movimientosRecientes(): Observable<any[]> {
    return this.http.get<any[]>(`${this.apiUrl}recientes/`);
  }

  soloEntradas(): Observable<any[]> {
    return this.http.get<any[]>(`${this.apiUrl}entradas/`);
  }

  soloSalidas(): Observable<any[]> {
    return this.http.get<any[]>(`${this.apiUrl}salidas/`);
  }
}
```

### 4. Servicio de Facturas

```typescript
// facturas.service.ts
import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class FacturasService {
  private apiUrl = 'http://localhost:8000/api/facturas/';

  constructor(private http: HttpClient) {}

  listarFacturas(): Observable<any[]> {
    return this.http.get<any[]>(this.apiUrl);
  }

  obtenerFactura(id: number): Observable<any> {
    return this.http.get<any>(`${this.apiUrl}${id}/`);
  }

  crearFactura(factura: any): Observable<any> {
    return this.http.post<any>(this.apiUrl, factura);
  }

  facturasPendientes(): Observable<any[]> {
    return this.http.get<any[]>(`${this.apiUrl}pendientes/`);
  }

  facturasPagadas(): Observable<any[]> {
    return this.http.get<any[]>(`${this.apiUrl}pagadas/`);
  }

  cambiarEstado(id: number, estado: string): Observable<any> {
    return this.http.post<any>(`${this.apiUrl}${id}/cambiar_estado/`, {
      estado: estado
    });
  }
}
```

### 5. Uso en un Componente

```typescript
// dashboard.component.ts
import { Component, OnInit } from '@angular/core';
import { DashboardService } from './services/dashboard.service';
import { ProductosService } from './services/productos.service';
import { MovimientosService } from './services/movimientos.service';

@Component({
  selector: 'app-dashboard',
  templateUrl: './dashboard.component.html'
})
export class DashboardComponent implements OnInit {
  stats: any = {};
  productos: any[] = [];
  movimientos: any[] = [];
  loading = true;

  constructor(
    private dashboardService: DashboardService,
    private productosService: ProductosService,
    private movimientosService: MovimientosService
  ) {}

  ngOnInit(): void {
    this.cargarDatos();
  }

  cargarDatos(): void {
    // Cargar estadísticas
    this.dashboardService.obtenerEstadisticas().subscribe({
      next: (data) => {
        this.stats = data;
        console.log('Estadísticas:', data);
      },
      error: (error) => {
        console.error('Error al cargar estadísticas:', error);
      }
    });

    // Cargar productos con bajo stock
    this.productosService.productosBarStock().subscribe({
      next: (data) => {
        this.productos = data;
        console.log('Productos bajo stock:', data);
      },
      error: (error) => {
        console.error('Error al cargar productos:', error);
      }
    });

    // Cargar movimientos recientes
    this.movimientosService.movimientosRecientes().subscribe({
      next: (data) => {
        this.movimientos = data;
        this.loading = false;
        console.log('Movimientos recientes:', data);
      },
      error: (error) => {
        console.error('Error al cargar movimientos:', error);
        this.loading = false;
      }
    });
  }
}
```

### 6. Configuración de HttpClient en Angular

```typescript
// app.module.ts
import { NgModule } from '@angular/core';
import { HttpClientModule } from '@angular/common/http';
import { BrowserModule } from '@angular/platform-browser';
import { AppComponent } from './app.component';

@NgModule({
  declarations: [AppComponent],
  imports: [
    BrowserModule,
    HttpClientModule  // ← Importar esto
  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule { }
```

### 7. Ejemplo de Creación de Factura

```typescript
// crear-factura.component.ts
crearNuevaFactura(): void {
  const nuevaFactura = {
    numero_factura: 'F-0233',
    cliente: 1,
    fecha_emision: '2026-02-11',
    fecha_vencimiento: '2026-03-11',
    impuestos: '100000.00',
    estado: 'pendiente',
    detalles: [
      {
        producto: 1,
        cantidad: 20,
        precio_unitario: '45000.00',
        descuento: '0.00'
      },
      {
        producto: 2,
        cantidad: 10,
        precio_unitario: '62000.00',
        descuento: '10000.00'
      }
    ]
  };

  this.facturasService.crearFactura(nuevaFactura).subscribe({
    next: (factura) => {
      console.log('Factura creada:', factura);
      alert(`Factura ${factura.numero_factura} creada exitosamente`);
    },
    error: (error) => {
      console.error('Error al crear factura:', error);
      alert('Error al crear la factura');
    }
  });
}
```

---

## 🔐 Configuración CORS

El backend ya está configurado para aceptar peticiones desde tu frontend Angular. Asegúrate de que en `settings.py` esté configurado:

```python
CORS_ALLOWED_ORIGINS = [
    "http://localhost:4200",  # Angular default port
    "http://127.0.0.1:4200",
]
```

---

## 🚀 Iniciar el Servidor

```bash
cd "/home/daniel/OneDrive/Documentos/semestre5/Motores de base de datos/backend/inventario"

# Activar entorno virtual (si tienes uno)
source ../venv/bin/activate

# Aplicar migraciones
python manage.py makemigrations
python manage.py migrate

# Crear superusuario (opcional)
python manage.py createsuperuser

# Iniciar servidor
python manage.py runserver
```

El servidor estará disponible en: **http://localhost:8000**

El panel de administración en: **http://localhost:8000/admin**

---

## 📝 Notas Importantes

1. **Actualización automática de stock**: Los movimientos actualizan automáticamente el stock de productos.

2. **Cálculos automáticos**: Los totales de facturas y detalles se calculan automáticamente.

3. **Estados de productos**: Se actualizan automáticamente según el stock:
   - `disponible`: stock > stock_minimo * 1.5
   - `bajo_stock`: stock <= stock_minimo * 1.5
   - `critico`: stock <= stock_minimo
   - `agotado`: stock = 0

4. **Validaciones**: Todos los endpoints tienen validaciones de datos.

5. **Filtros y búsqueda**: La mayoría de endpoints soportan filtros y búsqueda.

---

## 📞 Soporte

Para más información o dudas, consulta la documentación de Django REST Framework:
https://www.django-rest-framework.org/

---

**© 2026 DANIEL ROJAS AREVALO - Caficultura Verde** 💚☕

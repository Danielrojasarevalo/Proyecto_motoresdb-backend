# 🚀 Referencia Rápida de APIs

## Base URL
```
http://localhost:8000/api/
```

---

## 📋 Endpoints Resumidos

### Proveedores
| Método | Endpoint | Descripción |
|--------|----------|-------------|
| GET | `/proveedores/` | Listar todos |
| POST | `/proveedores/` | Crear nuevo |
| GET | `/proveedores/{id}/` | Ver detalle |
| PUT/PATCH | `/proveedores/{id}/` | Actualizar |
| DELETE | `/proveedores/{id}/` | Eliminar |
| GET | `/proveedores/activos/` | Solo activos |

**Filtros:** `?estado=activo` `?search=nombre`

---

### Categorías
| Método | Endpoint | Descripción |
|--------|----------|-------------|
| GET | `/categorias/` | Listar todas |
| POST | `/categorias/` | Crear nueva |
| GET | `/categorias/{id}/` | Ver detalle |
| PUT/PATCH | `/categorias/{id}/` | Actualizar |
| DELETE | `/categorias/{id}/` | Eliminar |

**Filtros:** `?search=nombre`

---

### Productos
| Método | Endpoint | Descripción |
|--------|----------|-------------|
| GET | `/productos/` | Listar todos |
| POST | `/productos/` | Crear nuevo |
| GET | `/productos/{id}/` | Ver detalle |
| PUT/PATCH | `/productos/{id}/` | Actualizar |
| DELETE | `/productos/{id}/` | Eliminar |
| GET | `/productos/bajo_stock/` | Con bajo stock |
| GET | `/productos/disponibles/` | Disponibles |
| POST | `/productos/{id}/actualizar_stock/` | Actualizar stock |

**Filtros:** `?categoria=1` `?proveedor=1` `?estado=disponible` `?search=nombre`

---

### Clientes
| Método | Endpoint | Descripción |
|--------|----------|-------------|
| GET | `/clientes/` | Listar todos |
| POST | `/clientes/` | Crear nuevo |
| GET | `/clientes/{id}/` | Ver detalle |
| PUT/PATCH | `/clientes/{id}/` | Actualizar |
| DELETE | `/clientes/{id}/` | Eliminar |
| GET | `/clientes/{id}/facturas/` | Facturas del cliente |

**Filtros:** `?tipo_cliente=cooperativa` `?search=nombre`

---

### Movimientos
| Método | Endpoint | Descripción |
|--------|----------|-------------|
| GET | `/movimientos/` | Listar todos |
| POST | `/movimientos/` | Crear nuevo |
| GET | `/movimientos/{id}/` | Ver detalle |
| PUT/PATCH | `/movimientos/{id}/` | Actualizar |
| DELETE | `/movimientos/{id}/` | Eliminar |
| GET | `/movimientos/recientes/` | Últimos 7 días |
| GET | `/movimientos/entradas/` | Solo entradas |
| GET | `/movimientos/salidas/` | Solo salidas |

**Filtros:** `?tipo_movimiento=entrada` `?producto=1` `?proveedor=1`

---

### Facturas
| Método | Endpoint | Descripción |
|--------|----------|-------------|
| GET | `/facturas/` | Listar todas |
| POST | `/facturas/` | Crear nueva |
| GET | `/facturas/{id}/` | Ver detalle |
| PUT/PATCH | `/facturas/{id}/` | Actualizar |
| DELETE | `/facturas/{id}/` | Eliminar |
| GET | `/facturas/pendientes/` | Solo pendientes |
| GET | `/facturas/pagadas/` | Solo pagadas |
| POST | `/facturas/{id}/cambiar_estado/` | Cambiar estado |

**Filtros:** `?estado=pendiente` `?cliente=1` `?search=F-0001`

---

### Dashboard
| Método | Endpoint | Descripción |
|--------|----------|-------------|
| GET | `/dashboard/stats/` | Estadísticas generales |
| GET | `/dashboard/resumen_mes/` | Resumen financiero |

---

## 🔥 Ejemplos Ultra-Rápidos

### Crear Producto
```json
POST /api/productos/
{
  "nombre": "Abono Orgánico",
  "categoria": 1,
  "proveedor": 1,
  "stock_actual": 100,
  "precio_unitario": "45000.00",
  "unidad_medida": "sacos"
}
```

### Crear Movimiento (Entrada)
```json
POST /api/movimientos/
{
  "producto": 1,
  "tipo_movimiento": "entrada",
  "cantidad": 50,
  "fecha_movimiento": "2026-02-11T10:00:00Z",
  "proveedor": 1
}
```

### Crear Factura
```json
POST /api/facturas/
{
  "numero_factura": "F-0001",
  "cliente": 1,
  "fecha_emision": "2026-02-11",
  "impuestos": "50000.00",
  "estado": "pendiente",
  "detalles": [
    {
      "producto": 1,
      "cantidad": 10,
      "precio_unitario": "45000.00",
      "descuento": "0.00"
    }
  ]
}
```

### Ver Estadísticas
```bash
GET /api/dashboard/stats/
```

**Respuesta:**
```json
{
  "stock_total": 1245,
  "productos_bajo_stock": 8,
  "entradas_recientes": 210,
  "ventas_mes": "8400000.00",
  "productos_criticos": [...]
}
```

---

## 🎯 Estados Comunes

### Producto
- `disponible`
- `bajo_stock`
- `critico`
- `agotado`

### Proveedor
- `activo`
- `inactivo`
- `pendiente`

### Factura
- `pendiente`
- `pagada`
- `cancelada`
- `vencida`

### Movimiento
- `entrada`
- `salida`

### Cliente
- `cooperativa`
- `finca`
- `empresa`
- `particular`

---

## 💡 Tips Importantes

1. **Stock automático**: Los movimientos actualizan el stock automáticamente
2. **Cálculos**: Los totales de facturas se calculan solos
3. **Estado producto**: Se actualiza según el stock
4. **Fechas**: Usar formato ISO 8601: `2026-02-11T10:00:00Z`
5. **Decimales**: Usar strings para precios: `"45000.00"`

---

## 🔍 Búsqueda y Filtros

```bash
# Buscar
?search=orgánico

# Filtrar
?categoria=1&estado=disponible

# Ordenar
?ordering=-fecha_creacion

# Combinar
?search=abono&categoria=1&ordering=precio_unitario
```

---

**© 2026 DANIEL ROJAS AREVALO** 💚☕

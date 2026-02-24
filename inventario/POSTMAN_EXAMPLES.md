# 🧪 Ejemplos de Pruebas - Postman y cURL

## 📋 Índice
1. [Configuración Inicial](#configuración-inicial)
2. [Ejemplos con cURL](#ejemplos-con-curl)
3. [Colección de Postman](#colección-de-postman)
4. [Flujo de Trabajo Completo](#flujo-de-trabajo-completo)

---

## 🔧 Configuración Inicial

### Variables de Entorno
```
BASE_URL = http://localhost:8000/api
```

---

## 💻 Ejemplos con cURL

### 1. PROVEEDORES

#### Listar proveedores
```bash
curl -X GET "http://localhost:8000/api/proveedores/"
```

#### Crear proveedor
```bash
curl -X POST "http://localhost:8000/api/proveedores/" \
  -H "Content-Type: application/json" \
  -d '{
    "nombre": "BioCafé",
    "email": "abonos@biocafe.co",
    "telefono": "3001234567",
    "direccion": "Calle 123 #45-67",
    "estado": "activo"
  }'
```

#### Actualizar proveedor (PATCH)
```bash
curl -X PATCH "http://localhost:8000/api/proveedores/1/" \
  -H "Content-Type: application/json" \
  -d '{
    "estado": "inactivo"
  }'
```

#### Eliminar proveedor
```bash
curl -X DELETE "http://localhost:8000/api/proveedores/1/"
```

#### Filtrar proveedores activos
```bash
curl -X GET "http://localhost:8000/api/proveedores/activos/"
```

#### Buscar proveedor
```bash
curl -X GET "http://localhost:8000/api/proveedores/?search=BioCafé"
```

---

### 2. CATEGORÍAS

#### Listar categorías
```bash
curl -X GET "http://localhost:8000/api/categorias/"
```

#### Crear categoría
```bash
curl -X POST "http://localhost:8000/api/categorias/" \
  -H "Content-Type: application/json" \
  -d '{
    "nombre": "Orgánico",
    "descripcion": "Abonos orgánicos y naturales"
  }'
```

---

### 3. PRODUCTOS

#### Listar productos
```bash
curl -X GET "http://localhost:8000/api/productos/"
```

#### Crear producto
```bash
curl -X POST "http://localhost:8000/api/productos/" \
  -H "Content-Type: application/json" \
  -d '{
    "nombre": "Abono Orgánico Premium",
    "categoria": 1,
    "proveedor": 1,
    "stock_actual": 320,
    "stock_minimo": 50,
    "stock_maximo": 500,
    "precio_unitario": "45000.00",
    "unidad_medida": "sacos",
    "descripcion": "Abono orgánico de alta calidad",
    "codigo_producto": "AO-001"
  }'
```

#### Filtrar por categoría
```bash
curl -X GET "http://localhost:8000/api/productos/?categoria=1"
```

#### Filtrar por estado
```bash
curl -X GET "http://localhost:8000/api/productos/?estado=disponible"
```

#### Productos con bajo stock
```bash
curl -X GET "http://localhost:8000/api/productos/bajo_stock/"
```

#### Actualizar stock manualmente
```bash
curl -X POST "http://localhost:8000/api/productos/1/actualizar_stock/" \
  -H "Content-Type: application/json" \
  -d '{
    "stock_actual": 150
  }'
```

#### Buscar producto
```bash
curl -X GET "http://localhost:8000/api/productos/?search=Orgánico"
```

#### Ordenar por precio
```bash
curl -X GET "http://localhost:8000/api/productos/?ordering=-precio_unitario"
```

---

### 4. CLIENTES

#### Listar clientes
```bash
curl -X GET "http://localhost:8000/api/clientes/"
```

#### Crear cliente
```bash
curl -X POST "http://localhost:8000/api/clientes/" \
  -H "Content-Type: application/json" \
  -d '{
    "nombre": "Cooperativa La Loma",
    "tipo_cliente": "cooperativa",
    "email": "contacto@laloma.co",
    "telefono": "3101234567",
    "direccion": "Vereda La Loma",
    "nit": "900123456-1"
  }'
```

#### Filtrar por tipo
```bash
curl -X GET "http://localhost:8000/api/clientes/?tipo_cliente=cooperativa"
```

#### Ver facturas de un cliente
```bash
curl -X GET "http://localhost:8000/api/clientes/1/facturas/"
```

---

### 5. MOVIMIENTOS

#### Listar movimientos
```bash
curl -X GET "http://localhost:8000/api/movimientos/"
```

#### Crear entrada de inventario
```bash
curl -X POST "http://localhost:8000/api/movimientos/" \
  -H "Content-Type: application/json" \
  -d '{
    "producto": 1,
    "tipo_movimiento": "entrada",
    "cantidad": 100,
    "fecha_movimiento": "2026-02-11T14:00:00Z",
    "proveedor": 1,
    "referencia": "OC-001",
    "observaciones": "Compra semanal de abono orgánico",
    "usuario_responsable": "Juan Pérez"
  }'
```

#### Crear salida de inventario
```bash
curl -X POST "http://localhost:8000/api/movimientos/" \
  -H "Content-Type: application/json" \
  -d '{
    "producto": 1,
    "tipo_movimiento": "salida",
    "cantidad": 20,
    "fecha_movimiento": "2026-02-11T15:00:00Z",
    "referencia": "F-0231",
    "observaciones": "Venta a cliente",
    "usuario_responsable": "María García"
  }'
```

#### Movimientos recientes (últimos 7 días)
```bash
curl -X GET "http://localhost:8000/api/movimientos/recientes/"
```

#### Solo entradas
```bash
curl -X GET "http://localhost:8000/api/movimientos/entradas/"
```

#### Solo salidas
```bash
curl -X GET "http://localhost:8000/api/movimientos/salidas/"
```

#### Filtrar por producto
```bash
curl -X GET "http://localhost:8000/api/movimientos/?producto=1"
```

---

### 6. FACTURAS

#### Listar facturas
```bash
curl -X GET "http://localhost:8000/api/facturas/"
```

#### Crear factura con detalles
```bash
curl -X POST "http://localhost:8000/api/facturas/" \
  -H "Content-Type: application/json" \
  -d '{
    "numero_factura": "F-0231",
    "cliente": 1,
    "fecha_emision": "2026-02-11",
    "fecha_vencimiento": "2026-03-11",
    "impuestos": "100000.00",
    "estado": "pendiente",
    "observaciones": "Entrega programada",
    "detalles": [
      {
        "producto": 1,
        "cantidad": 20,
        "precio_unitario": "45000.00",
        "descuento": "0.00"
      },
      {
        "producto": 2,
        "cantidad": 10,
        "precio_unitario": "62000.00",
        "descuento": "5000.00"
      }
    ]
  }'
```

#### Ver detalle de factura
```bash
curl -X GET "http://localhost:8000/api/facturas/1/"
```

#### Facturas pendientes
```bash
curl -X GET "http://localhost:8000/api/facturas/pendientes/"
```

#### Facturas pagadas
```bash
curl -X GET "http://localhost:8000/api/facturas/pagadas/"
```

#### Cambiar estado de factura
```bash
curl -X POST "http://localhost:8000/api/facturas/1/cambiar_estado/" \
  -H "Content-Type: application/json" \
  -d '{
    "estado": "pagada"
  }'
```

#### Filtrar por cliente
```bash
curl -X GET "http://localhost:8000/api/facturas/?cliente=1"
```

#### Filtrar por estado
```bash
curl -X GET "http://localhost:8000/api/facturas/?estado=pendiente"
```

---

### 7. DASHBOARD

#### Obtener estadísticas
```bash
curl -X GET "http://localhost:8000/api/dashboard/stats/"
```

#### Resumen financiero del mes
```bash
curl -X GET "http://localhost:8000/api/dashboard/resumen_mes/"
```

---

## 📮 Colección de Postman

### Importar esta colección JSON en Postman:

```json
{
  "info": {
    "name": "Caficultura Verde API",
    "description": "API para sistema de inventario de abonos y fertilizantes",
    "schema": "https://schema.getpostman.com/json/collection/v2.1.0/collection.json"
  },
  "variable": [
    {
      "key": "base_url",
      "value": "http://localhost:8000/api",
      "type": "string"
    }
  ],
  "item": [
    {
      "name": "Proveedores",
      "item": [
        {
          "name": "Listar Proveedores",
          "request": {
            "method": "GET",
            "header": [],
            "url": {
              "raw": "{{base_url}}/proveedores/",
              "host": ["{{base_url}}"],
              "path": ["proveedores", ""]
            }
          }
        },
        {
          "name": "Crear Proveedor",
          "request": {
            "method": "POST",
            "header": [
              {
                "key": "Content-Type",
                "value": "application/json"
              }
            ],
            "body": {
              "mode": "raw",
              "raw": "{\n  \"nombre\": \"BioCafé\",\n  \"email\": \"abonos@biocafe.co\",\n  \"telefono\": \"3001234567\",\n  \"direccion\": \"Calle 123 #45-67\",\n  \"estado\": \"activo\"\n}"
            },
            "url": {
              "raw": "{{base_url}}/proveedores/",
              "host": ["{{base_url}}"],
              "path": ["proveedores", ""]
            }
          }
        },
        {
          "name": "Proveedores Activos",
          "request": {
            "method": "GET",
            "header": [],
            "url": {
              "raw": "{{base_url}}/proveedores/activos/",
              "host": ["{{base_url}}"],
              "path": ["proveedores", "activos", ""]
            }
          }
        }
      ]
    },
    {
      "name": "Productos",
      "item": [
        {
          "name": "Listar Productos",
          "request": {
            "method": "GET",
            "header": [],
            "url": {
              "raw": "{{base_url}}/productos/",
              "host": ["{{base_url}}"],
              "path": ["productos", ""]
            }
          }
        },
        {
          "name": "Crear Producto",
          "request": {
            "method": "POST",
            "header": [
              {
                "key": "Content-Type",
                "value": "application/json"
              }
            ],
            "body": {
              "mode": "raw",
              "raw": "{\n  \"nombre\": \"Abono Orgánico Premium\",\n  \"categoria\": 1,\n  \"proveedor\": 1,\n  \"stock_actual\": 320,\n  \"stock_minimo\": 50,\n  \"stock_maximo\": 500,\n  \"precio_unitario\": \"45000.00\",\n  \"unidad_medida\": \"sacos\",\n  \"codigo_producto\": \"AO-001\"\n}"
            },
            "url": {
              "raw": "{{base_url}}/productos/",
              "host": ["{{base_url}}"],
              "path": ["productos", ""]
            }
          }
        },
        {
          "name": "Productos Bajo Stock",
          "request": {
            "method": "GET",
            "header": [],
            "url": {
              "raw": "{{base_url}}/productos/bajo_stock/",
              "host": ["{{base_url}}"],
              "path": ["productos", "bajo_stock", ""]
            }
          }
        }
      ]
    },
    {
      "name": "Movimientos",
      "item": [
        {
          "name": "Crear Entrada",
          "request": {
            "method": "POST",
            "header": [
              {
                "key": "Content-Type",
                "value": "application/json"
              }
            ],
            "body": {
              "mode": "raw",
              "raw": "{\n  \"producto\": 1,\n  \"tipo_movimiento\": \"entrada\",\n  \"cantidad\": 100,\n  \"fecha_movimiento\": \"2026-02-11T14:00:00Z\",\n  \"proveedor\": 1,\n  \"referencia\": \"OC-001\",\n  \"observaciones\": \"Compra semanal\"\n}"
            },
            "url": {
              "raw": "{{base_url}}/movimientos/",
              "host": ["{{base_url}}"],
              "path": ["movimientos", ""]
            }
          }
        },
        {
          "name": "Movimientos Recientes",
          "request": {
            "method": "GET",
            "header": [],
            "url": {
              "raw": "{{base_url}}/movimientos/recientes/",
              "host": ["{{base_url}}"],
              "path": ["movimientos", "recientes", ""]
            }
          }
        }
      ]
    },
    {
      "name": "Facturas",
      "item": [
        {
          "name": "Crear Factura",
          "request": {
            "method": "POST",
            "header": [
              {
                "key": "Content-Type",
                "value": "application/json"
              }
            ],
            "body": {
              "mode": "raw",
              "raw": "{\n  \"numero_factura\": \"F-0231\",\n  \"cliente\": 1,\n  \"fecha_emision\": \"2026-02-11\",\n  \"impuestos\": \"100000.00\",\n  \"estado\": \"pendiente\",\n  \"detalles\": [\n    {\n      \"producto\": 1,\n      \"cantidad\": 20,\n      \"precio_unitario\": \"45000.00\",\n      \"descuento\": \"0.00\"\n    }\n  ]\n}"
            },
            "url": {
              "raw": "{{base_url}}/facturas/",
              "host": ["{{base_url}}"],
              "path": ["facturas", ""]
            }
          }
        },
        {
          "name": "Facturas Pendientes",
          "request": {
            "method": "GET",
            "header": [],
            "url": {
              "raw": "{{base_url}}/facturas/pendientes/",
              "host": ["{{base_url}}"],
              "path": ["facturas", "pendientes", ""]
            }
          }
        }
      ]
    },
    {
      "name": "Dashboard",
      "item": [
        {
          "name": "Estadísticas",
          "request": {
            "method": "GET",
            "header": [],
            "url": {
              "raw": "{{base_url}}/dashboard/stats/",
              "host": ["{{base_url}}"],
              "path": ["dashboard", "stats", ""]
            }
          }
        },
        {
          "name": "Resumen del Mes",
          "request": {
            "method": "GET",
            "header": [],
            "url": {
              "raw": "{{base_url}}/dashboard/resumen_mes/",
              "host": ["{{base_url}}"],
              "path": ["dashboard", "resumen_mes", ""]
            }
          }
        }
      ]
    }
  ]
}
```

---

## 🔄 Flujo de Trabajo Completo

### Escenario: Registrar una venta completa

#### Paso 1: Crear proveedor (si no existe)
```bash
curl -X POST "http://localhost:8000/api/proveedores/" \
  -H "Content-Type: application/json" \
  -d '{"nombre": "BioCafé", "email": "abonos@biocafe.co", "estado": "activo"}'
```

#### Paso 2: Crear categoría (si no existe)
```bash
curl -X POST "http://localhost:8000/api/categorias/" \
  -H "Content-Type: application/json" \
  -d '{"nombre": "Orgánico", "descripcion": "Abonos orgánicos"}'
```

#### Paso 3: Crear producto
```bash
curl -X POST "http://localhost:8000/api/productos/" \
  -H "Content-Type: application/json" \
  -d '{
    "nombre": "Abono Orgánico Premium",
    "categoria": 1,
    "proveedor": 1,
    "stock_actual": 0,
    "stock_minimo": 50,
    "stock_maximo": 500,
    "precio_unitario": "45000.00",
    "unidad_medida": "sacos",
    "codigo_producto": "AO-001"
  }'
```

#### Paso 4: Registrar entrada de inventario
```bash
curl -X POST "http://localhost:8000/api/movimientos/" \
  -H "Content-Type: application/json" \
  -d '{
    "producto": 1,
    "tipo_movimiento": "entrada",
    "cantidad": 320,
    "fecha_movimiento": "2026-02-10T10:00:00Z",
    "proveedor": 1,
    "referencia": "OC-001",
    "observaciones": "Compra inicial"
  }'
```

#### Paso 5: Crear cliente
```bash
curl -X POST "http://localhost:8000/api/clientes/" \
  -H "Content-Type: application/json" \
  -d '{
    "nombre": "Cooperativa La Loma",
    "tipo_cliente": "cooperativa",
    "email": "contacto@laloma.co",
    "nit": "900123456-1"
  }'
```

#### Paso 6: Crear factura de venta
```bash
curl -X POST "http://localhost:8000/api/facturas/" \
  -H "Content-Type: application/json" \
  -d '{
    "numero_factura": "F-0001",
    "cliente": 1,
    "fecha_emision": "2026-02-11",
    "fecha_vencimiento": "2026-03-11",
    "impuestos": "100000.00",
    "estado": "pendiente",
    "detalles": [
      {
        "producto": 1,
        "cantidad": 50,
        "precio_unitario": "45000.00",
        "descuento": "0.00"
      }
    ]
  }'
```

#### Paso 7: Marcar factura como pagada
```bash
curl -X POST "http://localhost:8000/api/facturas/1/cambiar_estado/" \
  -H "Content-Type: application/json" \
  -d '{"estado": "pagada"}'
```

#### Paso 8: Ver estadísticas actualizadas
```bash
curl -X GET "http://localhost:8000/api/dashboard/stats/"
```

---

## 🧪 Pruebas Rápidas

### Script de prueba completo (Bash)
```bash
#!/bin/bash

API_URL="http://localhost:8000/api"

echo "=== Creando Proveedor ==="
curl -X POST "$API_URL/proveedores/" \
  -H "Content-Type: application/json" \
  -d '{"nombre":"BioCafé","email":"abonos@biocafe.co","estado":"activo"}' \
  | jq '.'

echo -e "\n=== Creando Categoría ==="
curl -X POST "$API_URL/categorias/" \
  -H "Content-Type: application/json" \
  -d '{"nombre":"Orgánico"}' \
  | jq '.'

echo -e "\n=== Creando Producto ==="
curl -X POST "$API_URL/productos/" \
  -H "Content-Type: application/json" \
  -d '{
    "nombre":"Abono Orgánico Premium",
    "categoria":1,
    "proveedor":1,
    "stock_actual":100,
    "stock_minimo":20,
    "precio_unitario":"45000.00",
    "unidad_medida":"sacos"
  }' \
  | jq '.'

echo -e "\n=== Ver Estadísticas ==="
curl -X GET "$API_URL/dashboard/stats/" | jq '.'
```

---

## 📊 Respuestas Esperadas

### Respuesta de Error (400 Bad Request)
```json
{
  "nombre": ["Este campo es requerido."],
  "email": ["Introduce una dirección de correo electrónico válida."]
}
```

### Respuesta de Éxito (201 Created)
```json
{
  "id": 1,
  "nombre": "BioCafé",
  "email": "abonos@biocafe.co",
  "estado": "activo",
  "fecha_registro": "2026-02-11T10:30:00Z"
}
```

---

**© 2026 DANIEL ROJAS AREVALO** 💚☕

# AvocadoLegal API

**Nombre Comercial:** JCJ Consultings

API de chat legal embebible para plataformas de gestión de préstamos. Permite a los usuarios consultar con abogados especializados en cobranzas, embargos e intimaciones directamente desde su sistema de gestión.

---

## Tabla de Contenidos

- [Características](#características)
- [Requisitos](#requisitos)
- [Instalación](#instalación)
- [Configuración](#configuración)
- [Ejecución](#ejecución)
- [API REST](#api-rest)
- [Integración del Widget](#integración-del-widget)
- [Panel de Abogados](#panel-de-abogados)
- [Estructura del Proyecto](#estructura-del-proyecto)

---

## Características

- **Chat en tiempo real** entre usuarios y abogados via WebSockets
- **Detección automática** de palabras clave de irregularidad (mora, vencido, cobranza, etc.)
- **Widget JavaScript embebible** con una sola línea de código
- **Scraping automático** de datos del préstamo desde el DOM
- **API REST** para integración programática
- **Panel de abogados** con dashboard, cola de casos y chat
- **Sistema de turnos** y disponibilidad para abogados
- **Autenticación por API Key** para plataformas

---

## Requisitos

- Python 3.11+
- PostgreSQL 16 (producción) / SQLite (desarrollo)
- Redis 7 (producción para WebSockets)

---

## Instalación

```bash
# Clonar el repositorio
cd C:\Users\carlo\AvocadoLegal

# Crear entorno virtual
python -m venv venv

# Activar entorno virtual (Windows)
.\venv\Scripts\activate

# Instalar dependencias
pip install -r requirements/development.txt

# Copiar archivo de entorno
copy .env.example .env

# Ejecutar migraciones
python manage.py migrate

# Crear superusuario
python manage.py createsuperuser

# Recolectar archivos estáticos
python manage.py collectstatic --noinput
```

---

## Configuración

Edita el archivo `.env`:

```env
DEBUG=True
SECRET_KEY=tu-clave-secreta-super-segura
ALLOWED_HOSTS=localhost,127.0.0.1

# Base de datos PostgreSQL (producción)
DB_NAME=avocado_legal
DB_USER=postgres
DB_PASSWORD=tu-password
DB_HOST=localhost
DB_PORT=5432

# Redis (producción)
REDIS_URL=redis://localhost:6379/0

# CORS
CORS_ALLOWED_ORIGINS=http://localhost:3000,https://tu-plataforma.com
```

---

## Ejecución

```bash
# Desarrollo
python manage.py runserver 8080

# Producción (con Daphne)
daphne -b 0.0.0.0 -p 8000 config.asgi:application
```

**URLs disponibles:**
- http://127.0.0.1:8080/ - Redirección al panel
- http://127.0.0.1:8080/admin/ - Admin de Django
- http://127.0.0.1:8080/lawyers/ - Panel de abogados
- http://127.0.0.1:8080/demo/ - Demo del widget

---

## API REST

### Autenticación

Todas las solicitudes a la API requieren un header de autenticación:

```
Authorization: Api-Key avl_xxxxxxxxxxxxxxxxxxxxx
```

### Endpoints

#### Plataformas

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| POST | `/api/v1/platforms/register/` | Registrar plataforma (público) |
| GET | `/api/v1/platforms/clients/` | Listar clientes |
| POST | `/api/v1/platforms/clients/` | Crear cliente |
| GET | `/api/v1/platforms/clients/{id}/` | Detalle de cliente |
| GET | `/api/v1/platforms/clients/{id}/loans/` | Préstamos del cliente |

#### Préstamos

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| GET | `/api/v1/loans/` | Listar préstamos |
| POST | `/api/v1/loans/` | Crear préstamo |
| GET | `/api/v1/loans/{id}/` | Detalle de préstamo |
| GET | `/api/v1/loans/irregular/` | Listar préstamos irregulares |
| POST | `/api/v1/loans/{id}/analyze/` | Analizar préstamo |

#### Conversaciones

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| GET | `/api/v1/conversations/` | Listar conversaciones |
| POST | `/api/v1/conversations/` | Crear conversación |
| GET | `/api/v1/conversations/{id}/` | Detalle con mensajes |
| POST | `/api/v1/conversations/{id}/send_message/` | Enviar mensaje |
| GET | `/api/v1/conversations/{id}/messages/` | Listar mensajes |
| POST | `/api/v1/conversations/{id}/close/` | Cerrar caso |

### Ejemplos

#### Registrar plataforma (obtener API Key)

```bash
curl -X POST http://localhost:8080/api/v1/platforms/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Mi Plataforma de Préstamos",
    "domain": "miplataforma.com",
    "contact_email": "admin@miplataforma.com"
  }'
```

**Respuesta:**
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "name": "Mi Plataforma de Préstamos",
  "api_key": "avl_AbCdEfGhIjKlMnOpQrStUvWxYz123456789",
  "message": "Platform registered successfully. Save your API key securely."
}
```

#### Crear cliente

```bash
curl -X POST http://localhost:8080/api/v1/platforms/clients/ \
  -H "Authorization: Api-Key avl_tu-api-key" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Juan Pérez",
    "cedula": "001-1234567-8",
    "phone": "809-555-1234",
    "email": "juan@email.com"
  }'
```

#### Crear conversación

```bash
curl -X POST http://localhost:8080/api/v1/conversations/ \
  -H "Authorization: Api-Key avl_tu-api-key" \
  -H "Content-Type: application/json" \
  -d '{
    "client": "uuid-del-cliente",
    "loan": "uuid-del-prestamo",
    "subject": "Consulta sobre proceso de cobranza"
  }'
```

---

## Integración del Widget

### Instalación Básica

Agrega este script antes de cerrar el `</body>`:

```html
<script 
  src="https://tu-servidor.com/static/widget/jcj-legal-chat.js" 
  data-api-key="avl_tu-api-key"
  data-api-url="https://tu-servidor.com/api/v1"
  data-position="right">
</script>
```

### Opciones de Configuración

| Atributo | Descripción | Valores |
|----------|-------------|---------|
| `data-api-key` | Tu API Key | String |
| `data-api-url` | URL base de la API | URL |
| `data-position` | Posición del widget | `left` o `right` |

### API JavaScript

El widget expone funciones para control programático:

```javascript
// Abrir el chat
JCJLegal.openChat();

// Cerrar el chat
JCJLegal.closeChat();

// Alternar chat
JCJLegal.toggleChat();

// Mostrar alerta de irregularidad
JCJLegal.showAlert();

// Pre-poblar datos del préstamo (para integraciones avanzadas)
JCJLegal.setLoanData({
  client: {
    name: "Juan Pérez",
    cedula: "001-1234567-8",
    phone: "809-555-1234"
  },
  loan: {
    amount: 50000,
    balance: 35000,
    status: "mora",
    days_overdue: 45
  }
});
```

### Palabras Clave de Detección

El widget detecta automáticamente estas palabras en la página:

- retraso, atraso, mora, vencido, vencida
- cobranza, legal, acuerdo de pago, irregular
- pendiente, incumplimiento, embargo, intimación
- consolidación, reestructuración, refinanciamiento
- demanda, judicial, notificación legal

---

## Panel de Abogados

### Acceso

1. Crear usuario en `/admin/`
2. Crear perfil de Abogado asociado al usuario
3. Acceder a `/lawyers/`

### Funcionalidades

- **Dashboard:** Estadísticas, casos recientes, cola sin asignar
- **Mis Casos:** Lista de conversaciones activas/cerradas
- **Cola:** Casos pendientes de asignación
- **Chat:** Comunicación en tiempo real con clientes
- **Turnos:** Toggle de disponibilidad y turno

---

## Estructura del Proyecto

```
AvocadoLegal/
 apps/
    platforms/      # Plataformas, usuarios, clientes
    loans/          # Préstamos
    conversations/  # Conversaciones y mensajes
    lawyers/        # Abogados y panel
    notifications/  # Notificaciones (futuro)
 config/             # Configuración Django
 static/
    widget/         # Widget JavaScript
 templates/
    lawyers/        # Templates del panel
 requirements/       # Dependencias
 docs/               # Documentación
 manage.py
```

---

## Tecnologías

- **Backend:** Django 5.1, Django REST Framework
- **WebSockets:** Django Channels, Daphne
- **Base de datos:** PostgreSQL / SQLite
- **Cache:** Redis
- **Frontend Widget:** JavaScript vanilla
- **Panel Abogados:** Bootstrap 5.3

---

## Licencia

Proyecto privado de JCJ Consultings.

---

## Soporte

Para soporte técnico, contactar a: soporte@jcjconsultings.com
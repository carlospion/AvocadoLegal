# JCJ Legal Chat Widget

Widget embebible para consultas legales con detección automática de préstamos irregulares.

## 🚀 Instalación

### Opción A: Script Tag via CDN (Recomendado)

```html
<script 
    src="https://cdn.jsdelivr.net/gh/carlospion/AvocadoLegal@v2.1.0/static/widget/jcj-legal-chat.js"
    data-api-key="TU_API_KEY"
    data-api-url="https://tu-servidor.com/api/v1"
    data-position="right"
    data-theme="auto">
</script>
```

### Opción B: Script desde tu servidor

```html
<script 
    src="https://tu-servidor.com/static/widget/jcj-legal-chat.js"
    data-api-key="TU_API_KEY"
    data-api-url="https://tu-servidor.com/api/v1"
    data-position="right">
</script>
```

### Opción C: Solo iframe (Cero configuración de CSP)

```html
<iframe
    src="https://tu-servidor.com/widget/embed/?api_key=TU_API_KEY"
    style="position:fixed; bottom:20px; right:20px; width:400px; height:600px; border:none; z-index:999999;"
    sandbox="allow-scripts allow-same-origin allow-forms">
</iframe>
```

## ⚙️ Configuración

| Atributo | Requerido | Descripción | Default |
|----------|-----------|-------------|---------|
| `data-api-key` | ✅ | API Key de tu plataforma | - |
| `data-api-url` | ⚠️ | URL base de la API | api.avocadolegal.com |
| `data-position` | ❌ | Posición del widget | `right` |
| `data-theme` | ❌ | Tema de colores | `auto` |
| `data-locale` | ❌ | Idioma | `es` |

## 🎮 API Programática

El widget expone una API global para control programático:

```javascript
// Abrir el chat
window.JCJLegal.open();

// Cerrar el chat
window.JCJLegal.close();

// Alternar estado
window.JCJLegal.toggle();

// Obtener configuración actual
window.JCJLegal.getConfig();

// Destruir widget
window.JCJLegal.destroy();
```

## 🔒 Requisitos de CSP

### Si usas CDN (Opción A)
La mayoría de CSPs ya permiten `cdn.jsdelivr.net`. Solo necesitas:

```
frame-src: https://tu-servidor-api.com
```

### Si usas tu servidor (Opción B)
```
script-src: https://tu-servidor-api.com
frame-src: https://tu-servidor-api.com
```

### Si usas solo iframe (Opción C)
```
frame-src: https://tu-servidor-api.com
```

## 🎯 Funcionamiento

### Modo Alert (Detección automática)
Si detecta keywords como "mora", "vencido", "embargo":
- Muestra alert balloon automáticamente
- Ofrece asistencia legal proactiva

### Modo Normal
Sin irregularidades detectadas:
- Muestra botón flotante discreto
- Usuario inicia chat manualmente

## 📋 Keywords Detectados

```
mora, vencido, vencida, atrasado, atrasada, deuda,
cobranza, cobro, penalidad, interés moratorio, embargo,
incumplimiento, impago, default, atraso, irregular
```

## 🔐 Seguridad

- **Sandbox:** El iframe usa `allow-scripts allow-same-origin allow-forms allow-popups`
- **Origin Validation:** Los mensajes postMessage se validan por origen
- **HTTPS:** Toda comunicación es cifrada

## 🔄 Versionado

| Versión | Descripción |
|---------|-------------|
| `@v2.1.0` | API programática, sandbox, validación origin |
| `@v2.0.0` | Dual mode, detección irregularidades |
| `@main` | Desarrollo (no usar en producción) |

## 🛠️ Solución de Problemas

### El widget no aparece
1. Verifica `data-api-key` esté configurado
2. Revisa consola (F12) para errores de CSP
3. Verifica que la API esté accesible

### Error de CSP
```
Refused to frame 'https://...' because it violates CSP
```
**Solución:** Agrega el dominio a `frame-src` en tu CSP

### Cache de jsDelivr
Purga: `https://purge.jsdelivr.net/gh/carlospion/AvocadoLegal@v2.1.0/static/widget/jcj-legal-chat.js`

---

© 2026 JCJ Consultings

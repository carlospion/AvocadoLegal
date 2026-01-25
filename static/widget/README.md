# JCJ Legal Chat Widget

Widget embebible para consultas legales con detección automática de préstamos irregulares.

## 🚀 Instalación Rápida

```html
<script 
    src="https://cdn.jsdelivr.net/gh/carlospion/AvocadoLegal@v2.0.0/static/widget/jcj-legal-chat.js"
    data-api-key="TU_API_KEY"
    data-api-url="https://tu-servidor.com/api/v1"
    data-position="right">
</script>
```

## ⚙️ Configuración

| Atributo | Requerido | Descripción | Valores |
|----------|-----------|-------------|---------|
| `data-api-key` | ✅ | API Key de tu plataforma | String |
| `data-api-url` | ⚠️ | URL base de la API | URL (default: api.avocadolegal.com) |
| `data-position` | ❌ | Posición del widget | `right` (default), `left` |

## 🔒 Requisitos de CSP (Content Security Policy)

Si tu aplicación usa CSP, agrega estos dominios:

```
script-src: https://cdn.jsdelivr.net
frame-src: https://tu-servidor-avocado.com
connect-src: https://tu-servidor-avocado.com
```

### Ejemplo de CSP completo:
```html
<meta http-equiv="Content-Security-Policy" content="
    default-src 'self';
    script-src 'self' 'unsafe-inline' https://cdn.jsdelivr.net;
    frame-src 'self' https://tu-servidor-avocado.com;
    connect-src 'self' https://tu-servidor-avocado.com;
">
```

## 🎯 Funcionamiento

### Modo Alert (Detección de Irregularidades)
Si el widget detecta keywords como "mora", "vencido", "embargo", etc. en la página:
- Muestra un alert balloon automáticamente
- Ofrece asistencia legal proactiva

### Modo Normal
Si no detecta irregularidades:
- Muestra solo el botón flotante
- El usuario puede iniciar chat manualmente

## 📋 Keywords Detectados

```
mora, vencido, vencida, atrasado, atrasada, deuda,
cobranza, cobro, penalidad, interés moratorio, embargo,
incumplimiento, impago, default, atraso, irregular
```

## 🔄 Versionado

Usamos [Semantic Versioning](https://semver.org/):

- **Producción estable:** `@v2.0.0` (recomendado)
- **Última versión:** `@main` (puede tener cambios breaking)

```html
<!-- Versión fija (recomendado para producción) -->
<script src="https://cdn.jsdelivr.net/gh/carlospion/AvocadoLegal@v2.0.0/static/widget/jcj-legal-chat.js"></script>

<!-- Última versión (solo desarrollo) -->
<script src="https://cdn.jsdelivr.net/gh/carlospion/AvocadoLegal@main/static/widget/jcj-legal-chat.js"></script>
```

## 🛠️ Solución de Problemas

### El widget no aparece
1. Verifica que `data-api-key` esté configurado
2. Revisa la consola del navegador (F12) para errores de CSP
3. Asegúrate que la API esté accesible

### Error de CSP
```
Refused to load the script '...' because it violates Content Security Policy
```
**Solución:** Agrega `https://cdn.jsdelivr.net` a tu `script-src`

### Cache de jsDelivr
Si actualizaste el widget y no ves cambios:
1. Purga el cache: `https://purge.jsdelivr.net/gh/carlospion/AvocadoLegal@main/static/widget/jcj-legal-chat.js`
2. Recarga con Ctrl+Shift+R

## 📞 Soporte

- **Documentación API:** [Link a docs]
- **Issues:** [GitHub Issues](https://github.com/carlospion/AvocadoLegal/issues)

---

© 2026 JCJ Consultings. Todos los derechos reservados.

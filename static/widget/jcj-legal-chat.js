/**
 * JCJ Legal Chat Widget Loader v2.1.0
 * 
 * Este script SOLO crea un iframe. Todo el widget vive dentro del iframe.
 * Puede distribuirse via CDN (jsdelivr, unpkg) para máxima compatibilidad.
 * 
 * El iframe tiene su propia CSP, por lo que no afecta la CSP del host.
 * 
 * USO:
 * <script 
 *     src="https://cdn.jsdelivr.net/gh/carlospion/AvocadoLegal@v2.1.0/static/widget/jcj-legal-chat.js"
 *     data-api-key="TU_API_KEY"
 *     data-api-url="https://tu-servidor.com/api/v1"
 *     data-position="right"
 *     data-theme="auto">
 * </script>
 * 
 * API Programática:
 *   window.JCJLegal.open()    - Abre el chat
 *   window.JCJLegal.close()   - Cierra el chat
 *   window.JCJLegal.destroy() - Remueve el widget
 */
(function () {
    'use strict';

    // Obtener configuración del script tag
    const script = document.currentScript;
    if (!script) {
        console.error('[JCJ] No se pudo detectar el script tag');
        return;
    }

    // Keywords que indican préstamos irregulares
    const IRREGULARITY_KEYWORDS = [
        'mora', 'vencido', 'vencida', 'atrasado', 'atrasada', 'deuda',
        'cobranza', 'cobro', 'penalidad', 'interés moratorio', 'embargo',
        'incumplimiento', 'impago', 'default', 'atraso', 'irregular'
    ];

    // Configuración desde atributos del script
    const config = {
        apiKey: script.getAttribute('data-api-key') || '',
        apiUrl: script.getAttribute('data-api-url') ||
            script.getAttribute('data-base-url') ||
            'https://api.avocadolegal.com',
        position: script.getAttribute('data-position') || 'right',
        theme: script.getAttribute('data-theme') || 'auto',
        locale: script.getAttribute('data-locale') || 'es',
    };

    if (!config.apiKey) {
        console.error('[JCJ] Falta data-api-key');
        return;
    }

    // Normalizar apiUrl - remover /api/v1 para construir URL de embed
    const embedBaseUrl = config.apiUrl.replace(/\/api\/v1\/?$/, '');

    // Obtener origin para validación de mensajes
    let widgetOrigin;
    try {
        widgetOrigin = new URL(embedBaseUrl).origin;
    } catch (e) {
        console.error('[JCJ] URL inválida:', embedBaseUrl);
        return;
    }

    // Detectar irregularidades en la página
    function detectIrregularities() {
        const pageText = document.body?.innerText?.toLowerCase() || '';
        for (const keyword of IRREGULARITY_KEYWORDS) {
            if (pageText.includes(keyword.toLowerCase())) {
                return { detected: true, keyword };
            }
        }
        return { detected: false, keyword: '' };
    }

    const detection = detectIrregularities();
    const mode = detection.detected ? 'alert' : 'normal';
    const pageUrl = window.location.href;

    console.log('[JCJ] Mode:', mode, detection.detected ? `(keyword: ${detection.keyword})` : '');

    // Tamaño inicial basado en modo
    const initialWidth = mode === 'alert' ? 340 : 70;
    const initialHeight = mode === 'alert' ? 300 : 70;

    // Construir URL del iframe con parámetros
    const params = new URLSearchParams({
        api_key: config.apiKey,
        api_url: config.apiUrl,
        mode: mode,
        keyword: detection.keyword,
        page_url: pageUrl,
        theme: config.theme,
        locale: config.locale,
    });

    // Crear contenedor - posicionado desde bottom, contenido crece hacia arriba
    const container = document.createElement('div');
    container.id = 'jcj-widget-container';
    container.style.cssText = `
        position: fixed;
        bottom: 20px;
        ${config.position}: 20px;
        width: ${initialWidth}px;
        height: ${initialHeight}px;
        z-index: 2147483647;
        pointer-events: none;
        transition: width 0.3s cubic-bezier(0.4, 0, 0.2, 1), height 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        display: flex;
        flex-direction: column;
        justify-content: flex-end;
    `;

    // Crear iframe - ocupa todo el contenedor, alineado al bottom
    const iframe = document.createElement('iframe');
    iframe.id = 'jcj-widget-iframe';
    iframe.src = `${embedBaseUrl}/widget/embed/?${params.toString()}`;
    iframe.style.cssText = `
        width: 100%;
        height: 100%;
        border: none;
        background: transparent;
        pointer-events: auto;
        border-radius: ${mode === 'alert' ? '16px' : '50%'};
        box-shadow: 0 4px 20px rgba(0,0,0,0.15);
        transition: border-radius 0.3s ease;
    `;

    // Sandbox con permisos mínimos necesarios
    iframe.sandbox = 'allow-scripts allow-same-origin allow-forms allow-popups';
    iframe.allow = 'clipboard-write';
    iframe.setAttribute('allowtransparency', 'true');
    iframe.setAttribute('loading', 'lazy');

    container.appendChild(iframe);
    document.body.appendChild(container);

    // Escuchar mensajes del iframe para resize dinámico
    window.addEventListener('message', function (event) {
        const data = event.data;
        if (!data || typeof data !== 'object') return;

        // Solo procesar mensajes de tipo jcj-*
        if (!data.type || !data.type.startsWith('jcj-')) return;

        console.log('[JCJ] Message received:', data.type, data);

        switch (data.type) {
            case 'jcj-resize':
                // Expandir/contraer widget dinámicamente
                const newWidth = data.width || 60;
                const newHeight = data.height || 60;
                console.log('[JCJ] Resizing to:', newWidth, 'x', newHeight);
                container.style.width = newWidth + 'px';
                container.style.height = newHeight + 'px';
                iframe.style.borderRadius = newWidth > 100 ? '16px' : '50%';
                break;

            case 'jcj-ready':
                console.log('[JCJ] Widget listo v2.1.1');
                break;

            case 'jcj-error':
                console.error('[JCJ]', data.message);
                break;
        }
    });

    // Exponer API global para control programático
    window.JCJLegal = {
        version: '2.1.0',

        open: function () {
            iframe.contentWindow?.postMessage({ type: 'jcj-open' }, widgetOrigin);
        },

        close: function () {
            iframe.contentWindow?.postMessage({ type: 'jcj-close' }, widgetOrigin);
        },

        toggle: function () {
            iframe.contentWindow?.postMessage({ type: 'jcj-toggle' }, widgetOrigin);
        },

        destroy: function () {
            container.remove();
            delete window.JCJLegal;
            console.log('[JCJ] Widget destruido');
        },

        getConfig: function () {
            return { ...config, mode, detection };
        }
    };

    console.log('[JCJ] Widget v2.1.0 loaded');
})();
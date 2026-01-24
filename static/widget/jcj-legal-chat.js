/**
 * JCJ Legal Chat Widget Loader v2.0
 * 
 * Widget siempre visible. Si detecta préstamos irregulares, muestra
 * alert balloon. Si no, muestra solo el botón con placeholder de bienvenida.
 * 
 * USO:
 * <script src="URL/static/widget/jcj-legal-chat.js"
 *         data-api-key="TU_API_KEY"
 *         data-api-url="https://tu-servidor.com/api/v1"
 *         data-position="right">
 * </script>
 */
(function () {
    'use strict';

    // Keywords que indican préstamos irregulares
    const IRREGULARITY_KEYWORDS = [
        'mora', 'vencido', 'vencida', 'atrasado', 'atrasada', 'deuda',
        'cobranza', 'cobro', 'penalidad', 'interés moratorio', 'embargo',
        'incumplimiento', 'impago', 'default', 'atraso', 'irregular'
    ];

    const currentScript = document.currentScript;
    const apiKey = currentScript?.getAttribute('data-api-key') || '';
    const position = currentScript?.getAttribute('data-position') || 'right';

    // Soporte para data-api-url (nuevo) y data-base-url (legacy)
    let baseUrl = currentScript?.getAttribute('data-api-url') ||
        currentScript?.getAttribute('data-base-url') ||
        'https://api.avocadolegal.com';

    // Normalizar baseUrl - remover /api/v1 si está incluido (para construir URL de embed)
    const embedBaseUrl = baseUrl.replace(/\/api\/v1\/?$/, '');

    if (!apiKey) {
        console.error('[JCJ] Missing data-api-key attribute');
        return;
    }

    // Detect irregularities (for alert mode)
    function detectIrregularities() {
        const pageText = document.body?.innerText?.toLowerCase() || '';
        for (const keyword of IRREGULARITY_KEYWORDS) {
            if (pageText.includes(keyword.toLowerCase())) {
                return { detected: true, keyword };
            }
        }
        return { detected: false };
    }

    const detection = detectIrregularities();
    const mode = detection.detected ? 'alert' : 'normal';
    const pageUrl = window.location.href;

    console.log('[JCJ] Mode:', mode, detection.detected ? `(keyword: ${detection.keyword})` : '');

    // Determine initial size based on mode
    const initialWidth = mode === 'alert' ? 340 : 100;
    const initialHeight = mode === 'alert' ? 300 : 100;

    // Create container
    const container = document.createElement('div');
    container.id = 'jcj-widget-container';
    container.style.cssText = `
        position: fixed;
        bottom: 0;
        ${position}: 0;
        width: ${initialWidth}px;
        height: ${initialHeight}px;
        z-index: 2147483647;
        pointer-events: none;
        background: transparent !important;
        border: none !important;
        box-shadow: none !important;
        outline: none !important;
        overflow: visible;
    `;

    // Create iframe - usa embedBaseUrl para la página de embed
    const iframeSrc = `${embedBaseUrl}/widget/embed/?api_key=${encodeURIComponent(apiKey)}&mode=${mode}&keyword=${encodeURIComponent(detection.keyword || '')}&page_url=${encodeURIComponent(pageUrl)}&api_url=${encodeURIComponent(baseUrl)}`;

    const iframe = document.createElement('iframe');
    iframe.id = 'jcj-widget-iframe';
    iframe.src = iframeSrc;
    iframe.style.cssText = `
        width: 100%;
        height: 100%;
        border: none !important;
        background: transparent !important;
        pointer-events: auto;
        box-shadow: none !important;
        outline: none !important;
    `;
    iframe.allow = 'clipboard-write';
    iframe.setAttribute('allowtransparency', 'true');
    iframe.setAttribute('scrolling', 'no');
    iframe.setAttribute('frameborder', '0');
    iframe.setAttribute('loading', 'lazy');

    container.appendChild(iframe);
    document.body.appendChild(container);

    // Listen for resize messages from iframe
    window.addEventListener('message', function (event) {
        if (event.data?.type === 'jcj-resize') {
            const { width, height } = event.data;
            container.style.width = width + 'px';
            container.style.height = height + 'px';
        }
    });

    console.log('[JCJ] Widget v2.0 loaded');
})();
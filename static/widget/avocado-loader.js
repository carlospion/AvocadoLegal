/**
 * JCJ Legal Chat Widget Loader v1.0
 * 
 * Este script solo crea un iframe si detecta irregularidades en préstamos.
 * Toda la lógica del chat se ejecuta dentro del iframe.
 * 
 * Uso:
 * <script src="https://cdn.jsdelivr.net/gh/carlospion/AvocadoLegal@main/static/widget/avocado-loader.js"
 *     data-api-key="TU_API_KEY">
 * </script>
 */
(function () {
    'use strict';

    // Keywords that indicate loan irregularities
    const IRREGULARITY_KEYWORDS = [
        'mora', 'vencido', 'vencida', 'atrasado', 'atrasada', 'deuda',
        'cobranza', 'cobro', 'penalidad', 'interés moratorio', 'embargo',
        'incumplimiento', 'impago', 'default', 'atraso', 'irregular'
    ];

    // Get configuration from script tag
    const currentScript = document.currentScript;
    const apiKey = currentScript?.getAttribute('data-api-key') || '';
    const position = currentScript?.getAttribute('data-position') || 'right';
    const baseUrl = currentScript?.getAttribute('data-base-url') || 'https://api.avocadolegal.com';

    if (!apiKey) {
        console.error('[JCJ] Missing data-api-key attribute');
        return;
    }

    // Detect irregularities in page content
    function detectIrregularities() {
        const pageText = document.body?.innerText?.toLowerCase() || '';
        for (const keyword of IRREGULARITY_KEYWORDS) {
            if (pageText.includes(keyword.toLowerCase())) {
                return { detected: true, keyword };
            }
        }
        return { detected: false };
    }

    // Check for irregularities
    const detection = detectIrregularities();

    if (!detection.detected) {
        console.log('[JCJ] No loan irregularities detected. Widget hidden.');
        return;
    }

    console.log('[JCJ] Irregularity detected:', detection.keyword);

    // Create iframe container - completely transparent, no styling
    const container = document.createElement('div');
    container.id = 'jcj-widget-container';
    container.style.cssText = `
        position: fixed;
        bottom: 0;
        ${position}: 0;
        width: 320px;
        height: 240px;
        z-index: 2147483647;
        pointer-events: none;
        background: transparent !important;
        border: none !important;
        box-shadow: none !important;
        outline: none !important;
        overflow: visible;
    `;

    // Create iframe
    const iframe = document.createElement('iframe');
    const iframeSrc = `${baseUrl}/widget/embed/?api_key=${encodeURIComponent(apiKey)}&position=${position}&keyword=${encodeURIComponent(detection.keyword)}`;

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

    // Listen for messages from iframe to resize container
    window.addEventListener('message', function (event) {
        if (event.data?.type === 'jcj-resize') {
            const { width, height } = event.data;
            container.style.width = width + 'px';
            container.style.height = height + 'px';
        }
    });

    console.log('[JCJ] Widget loader initialized');
})();

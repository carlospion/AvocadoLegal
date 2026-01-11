/**
 * AvocadoLegal Widget Loader v1.0
 * 
 * Este script solo crea un iframe. Toda la lógica del chat
 * se ejecuta dentro del iframe para evitar problemas de CSP.
 * 
 * Uso:
 * <script src="https://cdn.jsdelivr.net/gh/carlospion/AvocadoLegal@main/static/widget/avocado-loader.js"
 *     data-api-key="TU_API_KEY">
 * </script>
 */
(function () {
    'use strict';

    // Get configuration from script tag
    const currentScript = document.currentScript;
    const apiKey = currentScript?.getAttribute('data-api-key') || '';
    const position = currentScript?.getAttribute('data-position') || 'right';
    const baseUrl = currentScript?.getAttribute('data-base-url') || 'https://api.avocadolegal.com';

    if (!apiKey) {
        console.error('[AvocadoLegal] Missing data-api-key attribute');
        return;
    }

    // Create iframe container
    const container = document.createElement('div');
    container.id = 'avocado-widget-container';
    container.style.cssText = `
        position: fixed;
        bottom: 0;
        ${position}: 0;
        width: 80px;
        height: 80px;
        z-index: 2147483647;
        border: none;
        background: transparent;
        pointer-events: none;
    `;

    // Create iframe
    const iframe = document.createElement('iframe');
    const iframeSrc = `${baseUrl}/widget/embed/?api_key=${encodeURIComponent(apiKey)}&position=${position}`;

    iframe.id = 'avocado-widget-iframe';
    iframe.src = iframeSrc;
    iframe.style.cssText = `
        width: 100%;
        height: 100%;
        border: none;
        background: transparent;
        pointer-events: auto;
    `;
    iframe.allow = 'clipboard-write';
    iframe.setAttribute('loading', 'lazy');

    container.appendChild(iframe);
    document.body.appendChild(container);

    // Listen for messages from iframe to resize container
    window.addEventListener('message', function (event) {
        // Verify origin in production
        if (event.data?.type === 'avocado-resize') {
            const { width, height } = event.data;
            container.style.width = width + 'px';
            container.style.height = height + 'px';
        }
    });

    console.log('[AvocadoLegal] Widget loader initialized');
})();

/**
 * JCJ Legal Chat Widget v4
 * Sends scraped client data to API
 */
(function() {
    'use strict';

    const CONFIG = {
        API_BASE_URL: '',
        KEYWORDS: ['mora', 'vencido', 'cobranza', 'legal', 'atraso', 'retraso'],
        POSITION: 'right',
        POLL_INTERVAL: 5000
    };

    let state = {
        isOpen: false,
        showAlert: false,
        conversationId: null,
        clientData: {},
        apiKey: null,
        polling: null
    };

    function init() {
        console.log('[JCJ] Initializing widget v4...');
        const script = document.currentScript || document.querySelector('script[data-api-key]');
        if (script) {
            state.apiKey = script.getAttribute('data-api-key');
            CONFIG.API_BASE_URL = script.getAttribute('data-api-url') || 'http://localhost:8080/api/v1';
            CONFIG.POSITION = script.getAttribute('data-position') || 'right';
        }
        injectStyles();
        createWidget();
        setTimeout(checkKeywords, 2000);
    }

    function injectStyles() {
        const styles = `
            #jcj-widget { position: fixed; bottom: 20px; ${CONFIG.POSITION}: 20px; z-index: 999999; font-family: system-ui, sans-serif; }
            #jcj-btn { width: 60px; height: 60px; border-radius: 50%; background: linear-gradient(135deg, #1a365d, #2b6cb0); border: none; cursor: pointer; box-shadow: 0 4px 15px rgba(0,0,0,0.2); }
            #jcj-btn svg { fill: white; width: 28px; height: 28px; }
            #jcj-alert { position: absolute; bottom: 70px; ${CONFIG.POSITION}: 0; background: white; border-radius: 12px; box-shadow: 0 4px 20px rgba(0,0,0,0.15); padding: 16px; width: 280px; display: none; }
            #jcj-alert.show { display: block; }
            #jcj-alert h4 { margin: 0 0 8px; color: #1a365d; }
            #jcj-alert p { margin: 0 0 12px; color: #555; font-size: 13px; }
            .jcj-btns { display: flex; gap: 8px; }
            .jcj-btns button { flex: 1; padding: 8px; border-radius: 6px; cursor: pointer; }
            .jcj-yes { background: #1a365d; color: white; border: none; }
            .jcj-no { background: white; color: #666; border: 1px solid #ddd; }
            #jcj-chat { position: absolute; bottom: 70px; ${CONFIG.POSITION}: 0; width: 340px; height: 480px; background: white; border-radius: 16px; box-shadow: 0 8px 30px rgba(0,0,0,0.15); display: none; flex-direction: column; }
            #jcj-chat.open { display: flex; }
            .jcj-header { background: linear-gradient(135deg, #1a365d, #2b6cb0); color: white; padding: 14px; display: flex; justify-content: space-between; border-radius: 16px 16px 0 0; }
            .jcj-header h3 { margin: 0; font-size: 15px; }
            .jcj-header button { background: none; border: none; color: white; font-size: 20px; cursor: pointer; }
            #jcj-status { padding: 8px; text-align: center; font-size: 12px; color: #666; background: #f0f0f0; }
            #jcj-messages { flex: 1; overflow-y: auto; padding: 12px; background: #f7fafc; }
            .jcj-msg { margin-bottom: 10px; max-width: 75%; }
            .jcj-msg.system, .jcj-msg.lawyer { margin-right: auto; }
            .jcj-msg.platform_user { margin-left: auto; }
            .jcj-bubble { padding: 10px 12px; border-radius: 12px; font-size: 13px; }
            .jcj-msg.system .jcj-bubble, .jcj-msg.lawyer .jcj-bubble { background: white; }
            .jcj-msg.platform_user .jcj-bubble { background: #1a365d; color: white; }
            .jcj-time { font-size: 10px; color: #999; margin-top: 3px; }
            .jcj-input { padding: 10px; background: white; border-top: 1px solid #eee; display: flex; gap: 8px; border-radius: 0 0 16px 16px; }
            .jcj-input input { flex: 1; padding: 10px; border: 1px solid #ddd; border-radius: 8px; font-size: 13px; }
            .jcj-input button { padding: 10px 14px; background: #1a365d; color: white; border: none; border-radius: 8px; cursor: pointer; }
        `;
        document.head.appendChild(Object.assign(document.createElement('style'), {textContent: styles}));
    }

    function createWidget() {
        const w = document.createElement('div');
        w.id = 'jcj-widget';
        w.innerHTML = `
            <div id="jcj-alert">
                <h4>Irregularidad Detectada</h4>
                <p>Deseas consultar con nuestros Abogados?</p>
                <div class="jcj-btns">
                    <button class="jcj-yes" onclick="JCJLegal.start()">Si, consultar</button>
                    <button class="jcj-no" onclick="JCJLegal.hideAlert()">No</button>
                </div>
            </div>
            <div id="jcj-chat">
                <div class="jcj-header">
                    <h3>JCJ Consultings</h3>
                    <button onclick="JCJLegal.close()">&times;</button>
                </div>
                <div id="jcj-status"></div>
                <div id="jcj-messages"></div>
                <div class="jcj-input">
                    <input type="text" id="jcj-input" placeholder="Escribe tu mensaje..." onkeypress="if(event.key==='Enter')JCJLegal.send()">
                    <button onclick="JCJLegal.send()">Enviar</button>
                </div>
            </div>
            <button id="jcj-btn" onclick="JCJLegal.toggle()">
                <svg viewBox="0 0 24 24"><path d="M12 3c5.5 0 10 3.58 10 8s-4.5 8-10 8c-1.24 0-2.43-.18-3.53-.5C5.55 21 2 21 2 21c2.33-2.33 2.7-3.9 2.75-4.5C3.05 15.07 2 13.13 2 11c0-4.42 4.5-8 10-8z"/></svg>
            </button>`;
        document.body.appendChild(w);
    }

    function checkKeywords() {
        const text = document.body.innerText.toLowerCase();
        if (CONFIG.KEYWORDS.some(k => text.includes(k)) && !state.showAlert && !state.isOpen) {
            scrapeClientData();
            state.showAlert = true;
            document.getElementById('jcj-alert').classList.add('show');
        }
    }

    function scrapeClientData() {
        const text = document.body.innerText;
        state.clientData = {};
        
        // Extract name
        const nameMatch = text.match(/Nombre:\s*([^\n]+)/i);
        if (nameMatch) state.clientData.name = nameMatch[1].trim();
        
        // Extract cedula
        const cedulaMatch = text.match(/Cedula:\s*(\d{3}-\d{7}-\d)/i) || text.match(/(\d{3}-\d{7}-\d)/);
        if (cedulaMatch) state.clientData.cedula = cedulaMatch[1];
        
        // Extract phone
        const phoneMatch = text.match(/Telefono:\s*([\d\-]+)/i);
        if (phoneMatch) state.clientData.phone = phoneMatch[1].trim();
        
        // Extract email
        const emailMatch = text.match(/Email:\s*([^\s\n]+@[^\s\n]+)/i);
        if (emailMatch) state.clientData.email = emailMatch[1].trim();
        
        console.log('[JCJ] Scraped client data:', state.clientData);
    }

    function hideAlert() {
        state.showAlert = false;
        document.getElementById('jcj-alert').classList.remove('show');
    }

    function start() {
        hideAlert();
        open();
        createConversation();
    }

    function open() {
        state.isOpen = true;
        document.getElementById('jcj-chat').classList.add('open');
    }

    function close() {
        state.isOpen = false;
        document.getElementById('jcj-chat').classList.remove('open');
        if (state.polling) { clearInterval(state.polling); state.polling = null; }
    }

    function toggle() {
        state.isOpen ? close() : open();
        if (state.isOpen && !state.conversationId) {
            scrapeClientData();
            createConversation();
        }
    }

    function setStatus(msg) {
        document.getElementById('jcj-status').textContent = msg || '';
    }

    async function api(endpoint, method = 'GET', data = null) {
        const opts = {
            method,
            headers: { 'Content-Type': 'application/json' }
        };
        if (state.apiKey) opts.headers['Authorization'] = 'Api-Key ' + state.apiKey;
        if (data) opts.body = JSON.stringify(data);
        
        const res = await fetch(CONFIG.API_BASE_URL + endpoint, opts);
        const json = await res.json();
        if (!res.ok) throw new Error('Status ' + res.status);
        return json;
    }

    async function createConversation() {
        if (state.conversationId) return;
        setStatus('Conectando...');
        
        try {
            // Send client data along with conversation
            const result = await api('/conversations/', 'POST', {
                subject: 'Consulta web',
                client_data: state.clientData
            });
            
            if (result.id) {
                state.conversationId = result.id;
                console.log('[JCJ] Conversation created:', result.id);
                setStatus('Conectado');
                setTimeout(() => setStatus(''), 2000);
                loadMessages();
                state.polling = setInterval(loadMessages, CONFIG.POLL_INTERVAL);
            }
        } catch (err) {
            console.error('[JCJ] Error:', err);
            setStatus('Error. Reintentando...');
            setTimeout(createConversation, 3000);
        }
    }

    async function loadMessages() {
        if (!state.conversationId) return;
        try {
            const msgs = await api('/conversations/' + state.conversationId + '/messages/');
            render(msgs);
        } catch (err) {
            console.error('[JCJ] Load messages error:', err);
        }
    }

    function render(msgs) {
        const c = document.getElementById('jcj-messages');
        c.innerHTML = msgs.map(m => `
            <div class="jcj-msg ${m.sender_type}">
                <div class="jcj-bubble">${m.content}</div>
                <div class="jcj-time">${m.sender_name} - ${new Date(m.sent_at).toLocaleTimeString()}</div>
            </div>
        `).join('');
        c.scrollTop = c.scrollHeight;
    }

    async function send() {
        const input = document.getElementById('jcj-input');
        const content = input.value.trim();
        if (!content || !state.conversationId) return;
        input.value = '';
        
        try {
            await api('/conversations/' + state.conversationId + '/send_message/', 'POST', {
                content,
                sender_type: 'platform_user',
                sender_name: state.clientData.name || 'Usuario'
            });
            loadMessages();
        } catch (err) {
            setStatus('Error al enviar');
        }
    }

    window.JCJLegal = { start, open, close, toggle, send, hideAlert };

    if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', init);
    else init();
})();
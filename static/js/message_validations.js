
function closeCustomMessage(messageId) {
    const message = document.getElementById(messageId);
    if (!message) return;

    // Aplicar animación de salida
    message.style.animation = 'slideOutUp 0.3s ease-out forwards';
    
    // Esperar a que termine la animación antes de remover
    setTimeout(() => {
        message.remove();
        
        // Verificar si hay más mensajes en el contenedor
        const container = document.getElementById('formErrorsContainer');
        if (container && container.children.length === 0) {
            container.remove(); // Eliminar el contenedor si está vacío
        }
    }, 300); // Este tiempo debe coincidir con la duración de la animación
}

function showCustomMessage(content, type = 'info') {
    console.log('Mostrando mensaje:', content);
    
    // Crear contenedor si no existe
    let container = document.getElementById('formErrorsContainer');
    if (!container) {
        container = document.createElement('div');
        container.id = 'formErrorsContainer';
        container.className = 'messages-container';
        container.style.position = 'fixed';
        container.style.top = '1rem';
        container.style.left = '50%';
        container.style.transform = 'translateX(-50%)';
        container.style.zIndex = '9999';
        container.style.width = '100%';
        container.style.maxWidth = '28rem';
        container.style.padding = '0 1rem';
        document.body.appendChild(container);
    } else {
        container.style.display = 'block';
    }

    const messageId = `msg-${Date.now()}`;
    const icons = {
        'success': 'check',
        'error': 'times-circle', 
        'warning': 'exclamation-triangle',
        'info': 'info-circle'
    };
    
    // Crear elemento de mensaje
    const message = document.createElement('div');
    message.id = messageId;
    message.className = `message-${type}`;
    
    // Aplicar estilos básicos
    Object.assign(message.style, {
        position: 'relative',
        marginBottom: '1rem',
        padding: '1rem',
        borderRadius: '0.75rem',
        boxShadow: '0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06)',
        borderLeft: '4px solid',
        animation: 'slideInDown 0.3s ease-out forwards',
        display: 'flex',
        alignItems: 'flex-start',
        gap: '0.75rem'
    });

    // Estilos según tipo
    const typeStyles = {
        'success': {
            backgroundColor: '#f0fdf4',
            borderColor: '#4ade80',
            color: '#166534'
        },
        'error': {
            backgroundColor: '#fef2f2',
            borderColor: '#f87171',
            color: '#b91c1c'
        },
        'warning': {
            backgroundColor: '#fffbeb',
            borderColor: '#fbbf24',
            color: '#92400e'
        },
        'info': {
            backgroundColor: '#eff6ff',
            borderColor: '#60a5fa',
            color: '#1e40af'
        }
    };
    
    Object.assign(message.style, typeStyles[type] || typeStyles.info);

    // Icono
    const icon = document.createElement('div');
    icon.innerHTML = `<i class="fas fa-${icons[type]}" style="font-size: 1.2rem;"></i>`;
    
    // Contenido
    const contentDiv = document.createElement('div');
    contentDiv.style.flex = '1';
    
    // Si el contenido es string, lo asignamos directamente
    if (typeof content === 'string') {
        contentDiv.innerHTML = content;
    } else if (content instanceof HTMLElement) {
        contentDiv.appendChild(content);
    }
    
    // Botón de cierre
    const closeBtn = document.createElement('button');
    closeBtn.innerHTML = '<i class="fas fa-times"></i>';
    closeBtn.style.background = 'none';
    closeBtn.style.border = 'none';
    closeBtn.style.cursor = 'pointer';
    closeBtn.style.padding = '0.25rem';
    closeBtn.style.marginLeft = '0.5rem';
    closeBtn.onclick = () => closeCustomMessage(messageId);
    
    // Barra de progreso
    const progressBar = document.createElement('div');
    progressBar.style.position = 'absolute';
    progressBar.style.bottom = '0';
    progressBar.style.left = '0';
    progressBar.style.height = '3px';
    progressBar.style.backgroundColor = 'currentColor';
    progressBar.style.opacity = '0.3';
    progressBar.style.width = '100%';
    progressBar.style.animation = 'progressBar 5s linear forwards';
    
    // Ensamblar el mensaje
    message.appendChild(icon);
    message.appendChild(contentDiv);
    message.appendChild(closeBtn);
    message.appendChild(progressBar);
    
    container.appendChild(message);
    aplicarEstilos();
    
    // Auto-ocultar después de 5 segundos
    setTimeout(() => closeCustomMessage(messageId), 5000);
}


function aplicarEstilos() {
    if (!document.getElementById('messagesDynamicStyles')) {
        const style = document.createElement('style');
        style.id = 'messagesDynamicStyles';
        style.textContent = `
            @keyframes slideInDown {
                from { transform: translateY(-20px); opacity: 0; }
                to { transform: translateY(0); opacity: 1; }
            }
            
            @keyframes slideOutUp {
                from { transform: translateY(0); opacity: 1; }
                to { transform: translateY(-20px); opacity: 0; }
            }
            
            @keyframes progressBar {
                from { width: 100%; }
                to { width: 0%; }
            }
            
            .messages-container {
                position: fixed;
                top: 1rem;
                left: 50%;
                transform: translateX(-50%);
                z-index: 9999;
                width: 100%;
                max-width: 28rem;
            }
            
            /* Dark mode styles */
            .dark .message-success {
                background-color: #064e3b !important;
                color: #a7f3d0 !important;
            }
            
            .dark .message-error {
                background-color: #7f1d1d !important;
                color: #fecaca !important;
            }
            
            .dark .message-warning {
                background-color: #78350f !important;
                color: #fde68a !important;
            }
            
            .dark .message-info {
                background-color: #1e3a8a !important;
                color: #bfdbfe !important;
            }
        `;
        document.head.appendChild(style);
    }
}




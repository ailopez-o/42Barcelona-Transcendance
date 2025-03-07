// Se ejecuta cuando hay recarga HTMX
if (document.readyState === "complete") {
    console.log("🚀 [CHAT] El DOM ya está listo HTMX");
    setupChat(); // Si el DOM ya está listo, ejecuta directamente
}

// Se ejecuta cuando hay recarga completa
document.addEventListener("DOMContentLoaded", function () {
    console.log("✅ [CHAT] DOM completamente cargado.");
    setupChat(); // Si el DOM ya está listo, ejecuta directamente
});


function connectWebSocket(currentUsername) {
    // console.log("🚀 Intentando conectar al WebSocket del chat...");

    // Para saber a qué WS hemos de conectarnos. Si estamos en una partida, se añade el ID de la partida
    const gameContainer = document.getElementById("game-container");
    let wsUrl;

    if (gameContainer) {
        const gameId = gameContainer.dataset.gameId;
        wsUrl = `ws://${window.location.host}/ws/chat/${gameId}/`;
    } else {
        wsUrl = `ws://${window.location.host}/ws/chat/`;
    }

    // Si el WebSocket ya está abierto, no lo volvemos a crear
    if (window.chatSocket && window.chatSocket.readyState === WebSocket.OPEN) {
        console.log("🛑 El WebSocket ya está conectado, no se crea otro.");
        return;
    }
    
    window.chatSocket = new WebSocket(wsUrl); // ✅ Se guarda en `window` para que persista

    window.chatSocket.onopen = function () {
        console.log(`✅ Conectado al WebSocket del chat como ${currentUsername}`);
    };

    window.chatSocket.onmessage = function (event) {
        const data = JSON.parse(event.data);
        appendMessage(data.username, data.message);
        console.log("📩 Mensaje recibido:", data);
    };

    window.chatSocket.onclose = function () {
        console.warn("⚠️ Desconectado del WebSocket del chat. Intentando reconectar en 3 segundos...");
        setTimeout(() => connectWebSocket(currentUsername), 3000); // Intentar reconectar automáticamente
    };


    function appendMessage(username, message) {
        const chatContainer = document.getElementById("chat-section");
        if (!chatContainer) return;

        const msgDiv = document.createElement("div");
        msgDiv.classList.add("chat-message", "p-2", "border", "rounded", "mb-1", "bg-light");

        // Crear un span para el nombre de usuario con color dinámico
        const usernameSpan = document.createElement("span");
        usernameSpan.className = "username";
        usernameSpan.textContent = username + ": ";
        usernameSpan.style.color = getColorForUser(username);
        usernameSpan.style.fontWeight = "bold";

        // Crear un nodo de texto para el mensaje
        const messageText = document.createTextNode(message);

        // Ensamblar el mensaje y añadirlo al chat
        msgDiv.appendChild(usernameSpan);
        msgDiv.appendChild(messageText);
        chatContainer.appendChild(msgDiv);
        chatContainer.scrollTop = chatContainer.scrollHeight;
    }
}

function setupChat() {
    console.log("🎮 Configurando el chat...");

    // Elementos del DOM. Comprueba si existen antes de continuar
    const chatContainer = document.getElementById("chat-section");
    const chatForm = document.getElementById("chat-form");
    const chatInput = document.getElementById("chat-input");

    if (!chatContainer || !chatForm || !chatInput) {
        console.error("❌ Error: Elementos del chat no encontrados en el DOM.");
        return;
    }
    
    // Obtener el bloque JSON y parsearlo
    const playerDataElement = document.getElementById("player-data");
    if (!playerDataElement) {
        console.error("❌ Error: No se encontró 'player-data'.");
        return;
    }
    const playerData = JSON.parse(playerDataElement.textContent);
    
    // Verificar si el jugador actual es player1 o player2
    const currentPlayerKey = playerData.current;
    const currentPlayer = playerData[currentPlayerKey] || null;  // Si no es player1 ni player2, será null
    
    // Definir el nombre de usuario solo si el jugador es válido
    const currentUsername = currentPlayer ? currentPlayer.username : "Espectador";
    
    // Opción adicional: Mostrar un mensaje en consola si el usuario es un espectador
    if (!currentPlayer) {
        console.warn("⚠️ Usuario en modo espectador. No tiene permisos para jugar ni chatear.");
    }
    
    console.log("✅ Chat form encontrado en el DOM.");

    // Conexión al WebSocket
    connectWebSocket(currentUsername);

    // Capturar el evento submit para prevenir recarga
    chatForm.addEventListener("submit", function (event) {
        console.log("🚀 Intentando capturar el submit del formulario...");
        event.preventDefault(); // 🚀 Evita que el formulario haga un GET o POST normal

        console.log("📩 Evento submit capturado.");

        const message = chatInput.value.trim();
        if (message !== "") {
            const payload = {
                type: "chat",
                username: currentUsername,
                message: message,
            };

            console.log(`🟢 Intentando enviar mensaje: ${message}`);
            console.log(`📩 Payload enviado:`, payload);

            window.chatSocket.send(JSON.stringify(payload)); // Enviar mensaje al WebSocket
            chatInput.value = "";
        } else {
            console.warn("⚠️ Mensaje vacío. No se envía.");
        }
    });
}

// Función para generar colores dinámicos por usuario
function getColorForUser(username) {
    let hash = 0;
    for (let i = 0; i < username.length; i++) {
        hash = username.charCodeAt(i) + ((hash << 5) - hash);
    }
    const hue = Math.abs(hash) % 360;
    return `hsl(${hue}, 70%, 50%)`;
}
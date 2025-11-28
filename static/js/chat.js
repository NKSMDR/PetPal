// 💬 PetBuddy Chat – AJAX polling skeleton (no backend wired yet)
(function () {
    const chatMessagesEl = document.getElementById('chat-messages');
    const chatForm = document.getElementById('chat-form');
    const messageInput = document.getElementById('chat-message-input');
    const emptyStateEl = document.getElementById('chat-empty-state');
    const bodyEl = document.body;
    const userId = bodyEl ? bodyEl.getAttribute('data-user-id') : null;

    if (!chatMessagesEl || !chatForm || !messageInput) {
        return; // Chat not present on this page
    }

    // Simple helper to append a message bubble to the UI
    function appendMessage({ author, text, isSelf, time }) {
        const row = document.createElement('div');
        row.className = 'chat-message-row' + (isSelf ? ' self' : '');

        if (!isSelf) {
            const avatar = document.createElement('div');
            avatar.className = 'chat-message-avatar';
            avatar.innerHTML = '<i class="fas fa-user-circle"></i>';
            row.appendChild(avatar);
        }

        const bubble = document.createElement('div');
        bubble.className = 'chat-message-bubble';
        bubble.innerHTML = `
            <div class="chat-message-meta">
                <span class="chat-message-author">${author}</span>
                <span class="chat-message-time">${time || 'Just now'}</span>
            </div>
            <div class="chat-message-text">${text}</div>
        `;
        row.appendChild(bubble);

        chatMessagesEl.appendChild(row);
        chatMessagesEl.scrollTop = chatMessagesEl.scrollHeight;

        if (emptyStateEl) {
            emptyStateEl.classList.add('d-none');
        }
    }

    // Handle sending a message (frontend only for now)
    chatForm.addEventListener('submit', function (e) {
        e.preventDefault();
        const rawText = messageInput.value.trim();
        if (!rawText) return;

        appendMessage({
            author: 'You',
            text: rawText,
            isSelf: true,
            time: 'Now'
        });

        messageInput.value = '';

        // 🔧 Placeholder for future AJAX POST:
        // fetch('/chat/send/', {
        //     method: 'POST',
        //     headers: {
        //         'Content-Type': 'application/json',
        //         'X-CSRFToken': getCsrfToken(),
        //     },
        //     body: JSON.stringify({ message: rawText, user_id: userId })
        // });
    });

    // 🔁 Basic polling skeleton (disabled until endpoints exist)
    // function pollMessages() {
    //     fetch('/chat/messages/')
    //         .then(res => res.json())
    //         .then(data => {
    //             // TODO: Render messages from backend
    //         })
    //         .catch(() => { /* ignore for now */ });
    // }
    //
    // setInterval(pollMessages, 4000);

})();



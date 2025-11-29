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

    let lastMessageId = null;
    let pollTimer = null;

    function getContext() {
        return {
            petId: chatForm.dataset.petId || null,
            sellerId: chatForm.dataset.sellerId || null,
            threadId: chatForm.dataset.threadId || null,
            context: chatForm.dataset.context || null,
            role: chatForm.dataset.role || null,
        };
    }

    function getCsrfToken() {
        const name = 'csrftoken';
        const cookies = document.cookie ? document.cookie.split(';') : [];
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.startsWith(name + '=')) {
                return decodeURIComponent(cookie.substring(name.length + 1));
            }
        }
        return null;
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

    function startPollingIfNeeded() {
        const ctx = getContext();
        if (!ctx.petId && !ctx.threadId) {
            return;
        }
        if (pollTimer) {
            clearInterval(pollTimer);
        }
        pollTimer = setInterval(pollMessages, 4000);
        // Initial load
        pollMessages();
    }

    async function pollMessages() {
        const ctx = getContext();
        if (!ctx.petId && !ctx.threadId) return;

        let url;
        const params = new URLSearchParams();

        if (ctx.threadId) {
            url = '/chat/thread/messages/';
            params.append('thread_id', ctx.threadId);
        } else if (ctx.petId) {
            url = '/chat/messages/';
            params.append('pet_id', ctx.petId);
        } else {
            return;
        }

        if (lastMessageId) {
            params.append('since_id', String(lastMessageId));
        }

        try {
            const res = await fetch(`${url}?${params.toString()}`, {
                credentials: 'same-origin',
            });
            if (!res.ok) return;
            const data = await res.json();
            if (data.status !== 'success' || !Array.isArray(data.messages)) {
                return;
            }
            data.messages.forEach((m) => {
                appendMessage({
                    author: m.is_self ? 'You' : m.sender_name,
                    text: m.text,
                    isSelf: !!m.is_self,
                    time: m.created_at,
                });
            });
            if (data.last_id) {
                lastMessageId = data.last_id;
            }
        } catch (e) {
            // Silently ignore for now
        }
    }

    // Handle sending a message
    chatForm.addEventListener('submit', function (e) {
        e.preventDefault();
        const rawText = messageInput.value.trim();
        if (!rawText) return;

        const ctx = getContext();

        // If we don't have any context yet, just keep local echo
        if (!ctx.petId && !ctx.threadId) {
            appendMessage({
                author: 'You',
                text: rawText,
                isSelf: true,
                time: 'Now',
            });
            messageInput.value = '';
            return;
        }

        // Optimistic UI update
        appendMessage({
            author: 'You',
            text: rawText,
            isSelf: true,
            time: 'Now',
        });

        let url;
        const payload = { message: rawText };

        if (ctx.threadId) {
            url = '/chat/thread/send/';
            payload.thread_id = ctx.threadId;
        } else if (ctx.petId) {
            url = '/chat/send/';
            payload.pet_id = ctx.petId;
        } else {
            return;
        }

        messageInput.value = '';

        fetch(url, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCsrfToken() || '',
            },
            credentials: 'same-origin',
            body: JSON.stringify(payload),
        })
            .then((res) => res.json())
            .then((data) => {
                if (data && data.status === 'success' && data.message && data.message.id) {
                    lastMessageId = data.message.id;
                }
            })
            .catch(() => {
                // Ignore for now; message already shown locally
            });
    });

    function clearMessagesUI() {
        chatMessagesEl.innerHTML = '';
        if (emptyStateEl) {
            emptyStateEl.classList.remove('d-none');
        }
        lastMessageId = null;
    }

    async function loadThreads() {
        const listEl = document.getElementById('chat-conversation-list');
        if (!listEl) return;

        listEl.innerHTML = '<div class="text-center py-3 small text-muted">Loading conversations...</div>';

        try {
            const res = await fetch('/chat/threads/', { credentials: 'same-origin' });
            if (!res.ok) {
                listEl.innerHTML = '<div class="text-center py-3 small text-danger">Failed to load chats.</div>';
                return;
            }
            const data = await res.json();
            if (data.status !== 'success' || !Array.isArray(data.threads)) {
                listEl.innerHTML = '<div class="text-center py-3 small text-muted">No conversations yet.</div>';
                return;
            }
            if (!data.threads.length) {
                listEl.innerHTML = '<div class="text-center py-3 small text-muted">No conversations yet.</div>';
                return;
            }

            listEl.innerHTML = '';
            data.threads.forEach((t) => {
                const item = document.createElement('div');
                item.className = 'chat-conversation';
                item.dataset.threadId = t.id;
                item.innerHTML = `
                    <div class="conversation-title">${t.pet_display}</div>
                    <div class="conversation-meta">
                        With ${t.other_user_name}<br/>
                        <span class="text-truncate d-inline-block" style="max-width: 180px;">${t.last_message || ''}</span>
                    </div>
                `;

                item.addEventListener('click', () => {
                    // Highlight active
                    document.querySelectorAll('.chat-conversation').forEach((el) => {
                        el.classList.remove('active');
                    });
                    item.classList.add('active');

                    chatForm.dataset.threadId = String(t.id);
                    chatForm.dataset.context = 'inbox';
                    clearMessagesUI();

                    const convoTitle = document.getElementById('chatConversationTitle');
                    const convoSubtitle = document.getElementById('chatConversationSubtitle');
                    if (convoTitle) {
                        convoTitle.textContent = t.pet_display;
                    }
                    if (convoSubtitle) {
                        convoSubtitle.textContent = `Chat with ${t.other_user_name}`;
                    }

                    startPollingIfNeeded();
                });

                listEl.appendChild(item);
            });
        } catch (e) {
            const listEl2 = document.getElementById('chat-conversation-list');
            if (listEl2) {
                listEl2.innerHTML = '<div class="text-center py-3 small text-danger">Failed to load chats.</div>';
            }
        }
    }

    // Expose a tiny global helper so page-specific code (like Contact Seller
    // or navbar chat) can control the chat modal.
    window.PetBuddyChat = {
        startForCurrentContext: function () {
            lastMessageId = null;
            startPollingIfNeeded();
        },
        openInbox: function () {
            if (!chatForm) return;
            delete chatForm.dataset.petId;
            delete chatForm.dataset.sellerId;
            delete chatForm.dataset.threadId;
            chatForm.dataset.context = 'inbox';

            clearMessagesUI();
            loadThreads();

            const chatModalEl = document.getElementById('chatModal');
            if (chatModalEl && window.bootstrap && window.bootstrap.Modal) {
                const modal = new window.bootstrap.Modal(chatModalEl);
                modal.show();
            }
        }
    };

    // If some page set the context before this script ran, start immediately.
    if (chatForm.dataset.petId) {
        window.PetBuddyChat.startForCurrentContext();
    }
})();



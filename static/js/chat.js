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

            // Check if there are new messages
            const hasNewMessages = data.messages.length > 0;

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
            
            // Update scroll indicators after receiving messages
            setTimeout(() => {
                handleMessageScroll();
            }, 50);

            // Play sound and show notification for new messages from others
            if (hasNewMessages) {
                const hasNewFromOthers = data.messages.some(m => !m.is_self);
                if (hasNewFromOthers) {
                    playNotificationSound();
                    showBrowserNotification(data.messages.find(m => !m.is_self));
                }
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
        
        // Add visual feedback
        const sendBtn = chatForm.querySelector('.chat-send-btn');
        if (sendBtn) {
            sendBtn.disabled = true;
            sendBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i>';
        }

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
            })
            .finally(() => {
                // Reset send button
                const sendBtn = chatForm.querySelector('.chat-send-btn');
                if (sendBtn) {
                    sendBtn.disabled = false;
                    sendBtn.innerHTML = '<i class="fas fa-paper-plane"></i>';
                }
            });
    });

    // Allow Enter key to send message (Shift+Enter for new line)
    if (messageInput) {
        messageInput.addEventListener('keydown', function(e) {
            if (e.key === 'Enter' && !e.shiftKey) {
                e.preventDefault();
                chatForm.dispatchEvent(new Event('submit'));
            }
        });
    }

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
            
            // Update chat count badge
            const chatCountBadge = document.getElementById('chat-count-badge');
            if (chatCountBadge) {
                if (data.threads.length > 0) {
                    chatCountBadge.textContent = data.threads.length;
                    chatCountBadge.style.display = 'inline-block';
                } else {
                    chatCountBadge.style.display = 'none';
                }
            }
            
            data.threads.forEach((t) => {
                const item = document.createElement('div');
                item.className = 'chat-conversation';
                item.dataset.threadId = t.id;

                // Truncate last message
                const lastMsg = t.last_message || 'No messages yet';
                const truncatedMsg = lastMsg.length > 45 ? lastMsg.substring(0, 45) + '...' : lastMsg;

                // Format price
                const priceDisplay = t.pet_price ? `NRS ${t.pet_price.toLocaleString()}` : 'Price N/A';

                // Pet image or placeholder
                const imgHtml = t.pet_image
                    ? `<img src="${t.pet_image}" alt="${t.breed_name}" class="conversation-pet-img">`
                    : `<div class="conversation-pet-placeholder"><i class="fas fa-dog"></i></div>`;

                // Unread badge
                const unreadBadge = t.unread_count > 0
                    ? `<span class="conversation-unread-badge">${t.unread_count}</span>`
                    : '';

                item.innerHTML = `
                    <div class="conversation-layout">
                        <div class="conversation-img-wrapper position-relative">
                            ${imgHtml}
                            ${unreadBadge}
                        </div>
                        <div class="conversation-content">
                            <div class="conversation-title">${t.breed_name}</div>
                            <div class="conversation-price">${priceDisplay}</div>
                            <div class="conversation-meta">
                                <i class="fas fa-user-circle me-1"></i>${t.other_user_name}
                            </div>
                            <div class="conversation-preview">
                                <i class="fas fa-comment-dots me-1"></i>${truncatedMsg}
                            </div>
                        </div>
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
            
            // Check scroll indicators after loading threads
            setTimeout(() => {
                handleSidebarScroll();
            }, 100);
        } catch (e) {
            const listEl2 = document.getElementById('chat-conversation-list');
            if (listEl2) {
                listEl2.innerHTML = '<div class="text-center py-3 small text-danger">Failed to load chats.</div>';
            }
        }
    }

    // Sound notification
    function playNotificationSound() {
        try {
            const audio = new Audio('data:audio/wav;base64,UklGRnoGAABXQVZFZm10IBAAAAABAAEAQB8AAEAfAAABAAgAZGF0YQoGAACBhYqFbF1fdJivrJBhNjVgodDbq2EcBj+a2/LDciUFLIHO8tiJNwgZaLvt559NEAxQp+PwtmMcBjiR1/LMeSwFJHfH8N2QQAoUXrTp66hVFApGn+DyvmwhBDGH0vHZfisFH2W57eSXSwwNT6bh8bljHAU2jdXxz38vBSpTwe/DaiUFJHnJ8N2RQAsTX7Xo7KlWFApGnt/yuWofBDCG0fHZ');
            audio.volume = 0.3;
            audio.play().catch(() => { }); // Silently fail if autoplay blocked
        } catch (e) {
            // Ignore sound errors
        }
    }

    // Browser notification
    function showBrowserNotification(message) {
        // Request permission if not already granted
        if (!('Notification' in window)) {
            return; // Browser doesn't support notifications
        }

        if (Notification.permission === 'granted') {
            createNotification(message);
        } else if (Notification.permission !== 'denied') {
            Notification.requestPermission().then(permission => {
                if (permission === 'granted') {
                    createNotification(message);
                }
            });
        }
    }

    function createNotification(message) {
        if (!message) return;

        const title = '💬 New Message from ' + message.sender_name;
        const options = {
            body: message.text.substring(0, 100) + (message.text.length > 100 ? '...' : ''),
            icon: '/static/img/logo.png', // You can customize this
            badge: '/static/img/logo.png',
            tag: 'chat-message',
            requireInteraction: false,
            silent: false
        };

        try {
            const notification = new Notification(title, options);

            // Close notification after 5 seconds
            setTimeout(() => notification.close(), 5000);

            // Handle notification click
            notification.onclick = function () {
                window.focus();
                notification.close();
            };
        } catch (e) {
            // Ignore notification errors
        }
    }

    // Visual flash notification in title
    let titleFlashInterval = null;
    let originalTitle = document.title;

    function startTitleFlash(message) {
        if (titleFlashInterval) return; // Already flashing

        originalTitle = document.title;
        let isOriginal = true;

        titleFlashInterval = setInterval(() => {
            document.title = isOriginal ? '🔔 New Message!' : originalTitle;
            isOriginal = !isOriginal;
        }, 1000);

        // Stop flashing after 10 seconds
        setTimeout(stopTitleFlash, 10000);
    }

    function stopTitleFlash() {
        if (titleFlashInterval) {
            clearInterval(titleFlashInterval);
            titleFlashInterval = null;
            document.title = originalTitle;
        }
    }

    // Stop title flash when user focuses window
    window.addEventListener('focus', stopTitleFlash);

    // Update unread badge
    function updateUnreadBadge(count) {
        const badge = document.getElementById('chat-unread-badge');
        const notificationDot = document.getElementById('chat-notification-dot');
        
        if (!badge) return;

        if (count > 0) {
            badge.textContent = count > 99 ? '99+' : count;
            badge.classList.remove('d-none');
            if (notificationDot) {
                notificationDot.classList.remove('d-none');
            }
        } else {
            badge.classList.add('d-none');
            if (notificationDot) {
                notificationDot.classList.add('d-none');
            }
        }
    }

    // Check for unread messages periodically (only when not in active chat)
    let unreadCheckTimer = null;
    let lastCheckTime = 0;
    let unreadCount = 0;

    async function checkUnreadMessages() {
        const ctx = getContext();
        // Don't check if user is actively in a chat
        if (ctx.petId || ctx.threadId) {
            return;
        }

        try {
            const res = await fetch('/chat/threads/', {
                credentials: 'same-origin',
            });
            if (!res.ok) return;
            const data = await res.json();
            if (data.status !== 'success') {
                return;
            }

            // Use the total_unread count from backend
            unreadCount = data.total_unread || 0;
            updateUnreadBadge(unreadCount);
        } catch (e) {
            // Silently ignore
        }
    }

    // Start periodic unread check (every 30 seconds)
    function startUnreadCheck() {
        if (unreadCheckTimer) return;
        checkUnreadMessages(); // Check immediately
        unreadCheckTimer = setInterval(checkUnreadMessages, 30000);
    }

    // Stop unread check
    function stopUnreadCheck() {
        if (unreadCheckTimer) {
            clearInterval(unreadCheckTimer);
            unreadCheckTimer = null;
        }
    }

    // Handle scroll indicators for messages
    function handleMessageScroll() {
        if (!chatMessagesEl) return;
        
        const topIndicator = document.getElementById('messages-scroll-top');
        const bottomIndicator = document.getElementById('messages-scroll-bottom');
        
        if (!topIndicator || !bottomIndicator) return;
        
        const scrollTop = chatMessagesEl.scrollTop;
        const scrollHeight = chatMessagesEl.scrollHeight;
        const clientHeight = chatMessagesEl.clientHeight;
        const scrollBottom = scrollHeight - scrollTop - clientHeight;
        
        // Show top indicator if scrolled down more than 50px
        if (scrollTop > 50) {
            topIndicator.classList.add('show');
        } else {
            topIndicator.classList.remove('show');
        }
        
        // Show bottom indicator if not at bottom and has content
        if (scrollBottom > 50 && scrollHeight > clientHeight) {
            bottomIndicator.classList.add('show');
        } else {
            bottomIndicator.classList.remove('show');
        }
    }
    
    // Handle scroll indicators for sidebar
    function handleSidebarScroll() {
        const sidebarBody = document.getElementById('chat-conversation-list');
        const indicator = document.getElementById('sidebar-scroll-indicator');
        
        if (!sidebarBody || !indicator) return;
        
        const scrollTop = sidebarBody.scrollTop;
        const scrollHeight = sidebarBody.scrollHeight;
        const clientHeight = sidebarBody.clientHeight;
        const scrollBottom = scrollHeight - scrollTop - clientHeight;
        
        // Show indicator if there's more content below
        if (scrollBottom > 20 && scrollHeight > clientHeight) {
            indicator.classList.add('show');
        } else {
            indicator.classList.remove('show');
        }
    }
    
    // Add scroll event listeners
    if (chatMessagesEl) {
        chatMessagesEl.addEventListener('scroll', handleMessageScroll);
    }
    
    const sidebarBody = document.getElementById('chat-conversation-list');
    if (sidebarBody) {
        sidebarBody.addEventListener('scroll', handleSidebarScroll);
    }

    // Expose a tiny global helper so page-specific code (like Contact Seller
    // or navbar chat) can control the chat modal.
    window.PetBuddyChat = {
        startForCurrentContext: function () {
            // Don't reset lastMessageId here - it should be set by the initial load
            // lastMessageId = null;
            stopUnreadCheck();
            startPollingIfNeeded();
            
            // Check scroll indicators after context starts
            setTimeout(() => {
                handleMessageScroll();
            }, 100);
        },
        stopPolling: function () {
            if (pollTimer) {
                clearInterval(pollTimer);
                pollTimer = null;
            }
        },
        setLastMessageId: function (id) {
            lastMessageId = id;
        },
        openInbox: function () {
            if (!chatForm) return;
            delete chatForm.dataset.petId;
            delete chatForm.dataset.sellerId;
            delete chatForm.dataset.threadId;
            chatForm.dataset.context = 'inbox';

            clearMessagesUI();
            loadThreads();

            // Clear unread badge when opening inbox
            updateUnreadBadge(0);

            const chatModalEl = document.getElementById('chatModal');
            if (chatModalEl && window.bootstrap && window.bootstrap.Modal) {
                const modal = new window.bootstrap.Modal(chatModalEl);
                modal.show();
            }
        }
    };

    // Start checking for unread messages if user is logged in
    if (userId) {
        startUnreadCheck();
    }

    // If some page set the context before this script ran, start immediately.
    if (chatForm.dataset.petId) {
        window.PetBuddyChat.startForCurrentContext();
    }
})();



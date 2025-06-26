// Chatbot functionality
class ChatbotManager {
    constructor() {
        this.baseURL = 'http://localhost:5000/api';
        this.currentSessionId = this.generateSessionId();
        this.isTyping = false;
        this.messageHistory = [];
        this.currentProducts = [];
        
        this.initializeChatbot();
    }
    
    initializeChatbot() {
        // Set up form event listener
        document.getElementById('chat-form').addEventListener('submit', (e) => {
            e.preventDefault();
            this.sendMessage();
        });
        
        // Set up input handlers
        const chatInput = document.getElementById('chat-input');
        chatInput.addEventListener('input', this.handleInputChange.bind(this));
        chatInput.addEventListener('keydown', this.handleKeyDown.bind(this));
        
        // Load quick actions
        this.loadQuickActions();
        
        // Load recent chat sessions
        this.loadChatSessions();
    }
    
    initialize() {
        // This method is called after authentication
        this.loadQuickActions();
        this.loadChatSessions();
    }
    
    generateSessionId() {
        return 'session_' + Date.now() + '_' + Math.random().toString(36).substr(2, 9);
    }
    
    handleInputChange(e) {
        const input = e.target;
        const charCount = input.value.length;
        const maxLength = 500;
        
        // Update character count
        document.querySelector('.char-count').textContent = `${charCount}/${maxLength}`;
        
        // Enable/disable send button
        const sendBtn = document.querySelector('.send-btn');
        sendBtn.disabled = charCount === 0 || this.isTyping;
    }
    
    handleKeyDown(e) {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            this.sendMessage();
        }
    }
    
    async sendMessage() {
        const input = document.getElementById('chat-input');
        const message = input.value.trim();
        
        if (!message || this.isTyping) return;
        
        // Add user message to chat
        this.addMessageToChat(message, 'user');
        
        // Clear input and disable send button
        input.value = '';
        this.handleInputChange({ target: input });
        
        // Show typing indicator
        this.showTypingIndicator();
        
        try {
            const response = await fetch(`${this.baseURL}/chatbot/message`, {
                method: 'POST',
                headers: window.auth.getAuthHeaders(),
                body: JSON.stringify({
                    message: message,
                    session_id: this.currentSessionId
                })
            });
            
            const data = await response.json();
            
            if (response.ok) {
                // Remove typing indicator
                this.hideTypingIndicator();
                
                // Add bot response to chat
                this.addMessageToChat(data.bot_response, 'bot');
                
                // Store message in history
                this.messageHistory.push({
                    user_message: message,
                    bot_response: data.bot_response,
                    timestamp: new Date().toISOString(),
                    products: data.products || []
                });
                
                // Show products if any
                if (data.products && data.products.length > 0) {
                    this.displayProducts(data.products);
                }
                
                // Update chat sessions
                this.loadChatSessions();
                
            } else {
                this.hideTypingIndicator();
                if (response.status === 401 || response.status === 422) {
                    this.addMessageToChat('Please login first to start chatting. Click the Login button in the top right.', 'bot');
                    window.auth.showToast('Authentication required. Please login.', 'error');
                } else {
                    this.addMessageToChat('Sorry, I encountered an error. Please try again.', 'bot');
                    window.auth.showToast(data.error || 'Failed to send message', 'error');
                }
            }
            
        } catch (error) {
            console.error('Chat error:', error);
            this.hideTypingIndicator();
            this.addMessageToChat('Sorry, I\'m having trouble connecting. Please check your internet connection.', 'bot');
            window.auth.showToast('Network error. Please try again.', 'error');
        }
    }
    
    addMessageToChat(message, sender) {
        const messagesContainer = document.getElementById('chat-messages');
        const messageElement = document.createElement('div');
        messageElement.className = `message-item ${sender}`;
        
        const avatar = document.createElement('div');
        avatar.className = sender === 'user' ? 'user-avatar' : 'bot-avatar';
        avatar.innerHTML = sender === 'user' ? '<i class="fas fa-user"></i>' : '<i class="fas fa-robot"></i>';
        
        const content = document.createElement('div');
        content.className = 'message-content';
        
        // Format message content
        const formattedMessage = this.formatMessage(message);
        content.innerHTML = formattedMessage;
        
        const timestamp = document.createElement('div');
        timestamp.className = 'message-timestamp';
        timestamp.textContent = new Date().toLocaleTimeString();
        content.appendChild(timestamp);
        
        messageElement.appendChild(avatar);
        messageElement.appendChild(content);
        
        messagesContainer.appendChild(messageElement);
        
        // Scroll to bottom
        messagesContainer.scrollTop = messagesContainer.scrollHeight;
    }
    
    formatMessage(message) {
        // Convert markdown-like formatting to HTML
        let formatted = message
            .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')  // Bold
            .replace(/\*(.*?)\*/g, '<em>$1</em>')              // Italic
            .replace(/\n/g, '<br>')                            // Line breaks
            .replace(/^- (.+)$/gm, '<li>$1</li>')              // List items
            .replace(/^(\d+)\. (.+)$/gm, '<li>$1. $2</li>');   // Numbered list items
        
        // Wrap consecutive list items in ul tags
        formatted = formatted.replace(/(<li>.*<\/li>)/s, '<ul>$1</ul>');
        
        return formatted;
    }
    
    showTypingIndicator() {
        this.isTyping = true;
        
        const messagesContainer = document.getElementById('chat-messages');
        const typingElement = document.createElement('div');
        typingElement.className = 'message-item bot typing-indicator';
        typingElement.id = 'typing-indicator';
        
        const avatar = document.createElement('div');
        avatar.className = 'bot-avatar';
        avatar.innerHTML = '<i class="fas fa-robot"></i>';
        
        const content = document.createElement('div');
        content.className = 'message-content';
        content.innerHTML = `
            <div class="typing-dots">
                <div class="typing-dot"></div>
                <div class="typing-dot"></div>
                <div class="typing-dot"></div>
            </div>
            <span>ShopBot is typing...</span>
        `;
        
        typingElement.appendChild(avatar);
        typingElement.appendChild(content);
        
        messagesContainer.appendChild(typingElement);
        messagesContainer.scrollTop = messagesContainer.scrollHeight;
        
        // Disable send button
        document.querySelector('.send-btn').disabled = true;
    }
    
    hideTypingIndicator() {
        this.isTyping = false;
        
        const typingElement = document.getElementById('typing-indicator');
        if (typingElement) {
            typingElement.remove();
        }
        
        // Re-enable send button if input has content
        const input = document.getElementById('chat-input');
        document.querySelector('.send-btn').disabled = input.value.trim().length === 0;
    }
    
    displayProducts(products) {
        this.currentProducts = products;
        const productList = document.getElementById('product-list');
        const productPanel = document.getElementById('product-panel');
        
        // Clear existing products
        productList.innerHTML = '';
        
        // Add products
        products.forEach(product => {
            const productCard = this.createProductCard(product);
            productList.appendChild(productCard);
        });
        
        // Show product panel
        productPanel.classList.remove('hidden');
    }
    
    createProductCard(product) {
        const card = document.createElement('div');
        card.className = 'product-card';
        card.onclick = () => this.showProductDetails(product);
        
        const image = document.createElement('div');
        image.className = 'product-image';
        if (product.image_url && product.image_url !== 'https://via.placeholder.com/300x300?text=' + product.name.replace(' ', '+')) {
            image.innerHTML = `<img src="${product.image_url}" alt="${product.name}" onerror="this.parentNode.innerHTML='<i class=\\"fas fa-image\\"></i>'">`;
        } else {
            image.innerHTML = '<i class="fas fa-image"></i>';
        }
        
        const name = document.createElement('div');
        name.className = 'product-name';
        name.textContent = product.name;
        
        const price = document.createElement('div');
        price.className = 'product-price';
        price.textContent = `$${product.price.toFixed(2)}`;
        
        const rating = document.createElement('div');
        rating.className = 'product-rating';
        const stars = '★'.repeat(Math.floor(product.rating)) + '☆'.repeat(5 - Math.floor(product.rating));
        rating.innerHTML = `<span class="stars">${stars}</span> <span>(${product.rating})</span>`;
        
        const brand = document.createElement('div');
        brand.className = 'product-brand';
        brand.textContent = product.brand || 'Generic';
        
        card.appendChild(image);
        card.appendChild(name);
        card.appendChild(price);
        card.appendChild(rating);
        card.appendChild(brand);
        
        return card;
    }
    
    showProductDetails(product) {
        const modal = document.getElementById('product-modal');
        const title = document.getElementById('product-modal-title');
        const content = document.getElementById('product-detail-content');
        
        title.textContent = product.name;
        
        const detailsHTML = `
            <div class="product-details">
                <div class="product-detail-image">
                    ${product.image_url && product.image_url !== 'https://via.placeholder.com/300x300?text=' + product.name.replace(' ', '+') 
                        ? `<img src="${product.image_url}" alt="${product.name}" onerror="this.style.display='none'; this.nextElementSibling.style.display='flex'">
                           <div class="placeholder-image" style="display:none;"><i class="fas fa-image"></i></div>`
                        : `<div class="placeholder-image"><i class="fas fa-image"></i></div>`
                    }
                </div>
                <div class="product-detail-info">
                    <h3>${product.name}</h3>
                    <p class="product-detail-price">$${product.price.toFixed(2)}</p>
                    <p class="product-detail-brand">Brand: ${product.brand || 'Generic'}</p>
                    <div class="product-detail-rating">
                        <span class="stars">${'★'.repeat(Math.floor(product.rating))}${'☆'.repeat(5 - Math.floor(product.rating))}</span>
                        <span>(${product.rating}/5)</span>
                    </div>
                    <p class="product-detail-stock">Stock: ${product.stock_quantity} available</p>
                    <div class="product-detail-description">
                        <h4>Description</h4>
                        <p>${product.description || 'No description available.'}</p>
                    </div>
                    ${product.attributes && Object.keys(product.attributes).length > 0 
                        ? `<div class="product-detail-attributes">
                             <h4>Specifications</h4>
                             ${Object.entries(product.attributes).map(([key, value]) => 
                                 `<div class="attribute-item">
                                    <span class="attribute-name">${key.replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase())}:</span>
                                    <span class="attribute-value">${value}</span>
                                  </div>`
                             ).join('')}
                           </div>`
                        : ''
                    }
                    <div class="product-actions">
                        <button class="btn btn-primary" onclick="addToWishlist(${product.id})">
                            <i class="fas fa-heart"></i> Add to Wishlist
                        </button>
                        <button class="btn btn-secondary" onclick="shareProduct(${product.id})">
                            <i class="fas fa-share"></i> Share
                        </button>
                    </div>
                </div>
            </div>
        `;
        
        content.innerHTML = detailsHTML;
        modal.classList.remove('hidden');
    }
    
    async loadQuickActions() {
        try {
            const response = await fetch(`${this.baseURL}/chatbot/quick-actions`);
            const data = await response.json();
            
            if (response.ok) {
                const container = document.getElementById('quick-actions-list');
                container.innerHTML = '';
                
                data.quick_actions.forEach(action => {
                    const button = document.createElement('button');
                    button.className = 'quick-action-btn';
                    button.textContent = action.text;
                    button.title = action.description;
                    button.onclick = () => this.useQuickAction(action.text);
                    
                    container.appendChild(button);
                });
            }
        } catch (error) {
            console.error('Failed to load quick actions:', error);
        }
    }
    
    useQuickAction(text) {
        const input = document.getElementById('chat-input');
        input.value = text;
        input.focus();
        this.handleInputChange({ target: input });
    }
    
    async loadChatSessions() {
        if (!window.auth.isAuthenticated()) return;
        
        try {
            const response = await fetch(`${this.baseURL}/chatbot/sessions`, {
                headers: window.auth.getAuthHeaders()
            });
            
            const data = await response.json();
            
            if (response.ok) {
                const container = document.getElementById('chat-sessions-list');
                container.innerHTML = '';
                
                data.sessions.slice(0, 5).forEach(session => {
                    const sessionElement = document.createElement('div');
                    sessionElement.className = 'chat-session-item';
                    sessionElement.onclick = () => this.loadSession(session.session_id);
                    
                    const lastMessage = new Date(session.last_message);
                    const title = session.message_count === 1 ? 'New conversation' : `Conversation (${session.message_count} messages)`;
                    
                    sessionElement.innerHTML = `
                        <div class="chat-session-title">${title}</div>
                        <div class="chat-session-meta">${lastMessage.toLocaleDateString()} • ${lastMessage.toLocaleTimeString()}</div>
                    `;
                    
                    container.appendChild(sessionElement);
                });
            }
        } catch (error) {
            console.error('Failed to load chat sessions:', error);
        }
    }
    
    async loadSession(sessionId) {
        try {
            const response = await fetch(`${this.baseURL}/chatbot/history?session_id=${sessionId}`, {
                headers: window.auth.getAuthHeaders()
            });
            
            const data = await response.json();
            
            if (response.ok) {
                // Clear current chat
                this.clearChat();
                
                // Set current session
                this.currentSessionId = sessionId;
                
                // Load messages in chronological order
                data.chat_history.reverse().forEach(message => {
                    this.addMessageToChat(message.message, 'user');
                    this.addMessageToChat(message.response, 'bot');
                });
                
                window.auth.showToast('Chat session loaded', 'success');
            }
        } catch (error) {
            console.error('Failed to load chat session:', error);
            window.auth.showToast('Failed to load chat session', 'error');
        }
    }
    
    async loadChatHistory() {
        try {
            const response = await fetch(`${this.baseURL}/chatbot/history`, {
                headers: window.auth.getAuthHeaders()
            });
            
            const data = await response.json();
            
            if (response.ok) {
                const historyInfo = `You have ${data.pagination.total} total messages across ${data.chat_history.length} conversations.`;
                window.auth.showToast(historyInfo, 'info');
            }
        } catch (error) {
            console.error('Failed to load chat history:', error);
            window.auth.showToast('Failed to load chat history', 'error');
        }
    }
    
    clearChat() {
        const messagesContainer = document.getElementById('chat-messages');
        const welcomeMessage = messagesContainer.querySelector('.welcome-message');
        
        // Clear all messages except welcome message
        messagesContainer.innerHTML = '';
        if (welcomeMessage) {
            messagesContainer.appendChild(welcomeMessage);
        }
        
        // Clear products
        this.closeProductPanel();
        
        // Reset session
        this.currentSessionId = this.generateSessionId();
        this.messageHistory = [];
        this.currentProducts = [];
    }
    
    closeProductPanel() {
        document.getElementById('product-panel').classList.add('hidden');
    }
    
    exportChat() {
        if (this.messageHistory.length === 0) {
            window.auth.showToast('No messages to export', 'warning');
            return;
        }
        
        const chatData = {
            session_id: this.currentSessionId,
            timestamp: new Date().toISOString(),
            user: window.auth.user.username,
            messages: this.messageHistory
        };
        
        const dataStr = JSON.stringify(chatData, null, 2);
        const dataBlob = new Blob([dataStr], { type: 'application/json' });
        
        const link = document.createElement('a');
        link.href = URL.createObjectURL(dataBlob);
        link.download = `chat-export-${new Date().toISOString().split('T')[0]}.json`;
        link.click();
        
        window.auth.showToast('Chat exported successfully', 'success');
    }
}

// Global chatbot instance
window.chatbot = new ChatbotManager();

// Global functions for HTML onclick handlers
function startNewChat() {
    window.chatbot.clearChat();
    window.auth.showToast('New chat started', 'success');
}

function clearChat() {
    if (confirm('Are you sure you want to clear this chat? This action cannot be undone.')) {
        window.chatbot.clearChat();
        window.auth.showToast('Chat cleared', 'success');
    }
}

function exportChat() {
    window.chatbot.exportChat();
}

function closeProductPanel() {
    window.chatbot.closeProductPanel();
}

function closeProductModal() {
    document.getElementById('product-modal').classList.add('hidden');
}

function showSampleQueries() {
    document.getElementById('sample-queries-modal').classList.remove('hidden');
}

function closeSampleQueriesModal() {
    document.getElementById('sample-queries-modal').classList.add('hidden');
}

function useQuery(query) {
    document.getElementById('chat-input').value = query;
    window.chatbot.handleInputChange({ target: document.getElementById('chat-input') });
    closeSampleQueriesModal();
    document.getElementById('chat-input').focus();
}

function toggleVoiceInput() {
    // Voice input functionality (placeholder)
    window.auth.showToast('Voice input feature coming soon!', 'info');
}

function addToWishlist(productId) {
    // Wishlist functionality (placeholder)
    window.auth.showToast('Added to wishlist! (Feature coming soon)', 'success');
}

function shareProduct(productId) {
    // Share functionality (placeholder)
    if (navigator.share) {
        navigator.share({
            title: 'Check out this product',
            text: 'I found this great product on ShopBot!',
            url: window.location.href
        });
    } else {
        // Fallback to copying URL
        navigator.clipboard.writeText(window.location.href);
        window.auth.showToast('Product link copied to clipboard!', 'success');
    }
}

// Add product detail styles
const productStyles = document.createElement('style');
productStyles.textContent = `
.product-details {
    display: grid;
    grid-template-columns: 1fr 2fr;
    gap: 2rem;
}

.product-detail-image {
    text-align: center;
}

.product-detail-image img {
    width: 100%;
    max-width: 300px;
    height: auto;
    border-radius: var(--radius-lg);
}

.placeholder-image {
    width: 100%;
    max-width: 300px;
    height: 300px;
    background-color: var(--bg-tertiary);
    border-radius: var(--radius-lg);
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 3rem;
    color: var(--text-muted);
    margin: 0 auto;
}

.product-detail-info h3 {
    font-size: 1.5rem;
    font-weight: 600;
    margin-bottom: 1rem;
    color: var(--text-primary);
}

.product-detail-price {
    font-size: 1.75rem;
    font-weight: 700;
    color: var(--primary-color);
    margin-bottom: 1rem;
}

.product-detail-brand {
    font-size: 1rem;
    color: var(--text-secondary);
    margin-bottom: 0.5rem;
}

.product-detail-rating {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    margin-bottom: 1rem;
}

.product-detail-rating .stars {
    color: #fbbf24;
    font-size: 1.125rem;
}

.product-detail-stock {
    font-size: 0.875rem;
    color: var(--text-secondary);
    margin-bottom: 1.5rem;
}

.product-detail-description h4,
.product-detail-attributes h4 {
    font-size: 1rem;
    font-weight: 600;
    margin-bottom: 0.75rem;
    color: var(--text-primary);
}

.product-detail-description p {
    color: var(--text-secondary);
    line-height: 1.6;
    margin-bottom: 1.5rem;
}

.product-detail-attributes {
    margin-bottom: 1.5rem;
}

.attribute-item {
    display: flex;
    justify-content: space-between;
    padding: 0.5rem 0;
    border-bottom: 1px solid var(--border-color);
}

.attribute-item:last-child {
    border-bottom: none;
}

.attribute-name {
    font-weight: 500;
    color: var(--text-primary);
}

.attribute-value {
    color: var(--text-secondary);
}

.product-actions {
    display: flex;
    gap: 1rem;
}

@media (max-width: 768px) {
    .product-details {
        grid-template-columns: 1fr;
        gap: 1.5rem;
    }
    
    .product-actions {
        flex-direction: column;
    }
}
`;
document.head.appendChild(productStyles);

// Main application logic
class AppManager {
    constructor() {
        this.init();
    }
    
    init() {
        // Wait for DOM to be fully loaded
        if (document.readyState === 'loading') {
            document.addEventListener('DOMContentLoaded', () => {
                this.setupApp();
            });
        } else {
            this.setupApp();
        }
    }
    
    setupApp() {
        // Set up event listeners
        this.setupEventListeners();
        
        // Initialize responsive behavior
        this.setupResponsive();
        
        // Set up keyboard shortcuts
        this.setupKeyboardShortcuts();
        
        // Set up error handling
        this.setupErrorHandling();
        
        // Auto-hide loading screen after auth check
        setTimeout(() => {
            if (document.getElementById('loading-screen').classList.contains('hidden')) {
                return; // Already hidden by auth
            }
            document.getElementById('loading-screen').classList.add('hidden');
        }, 2000);
    }
    
    setupEventListeners() {
        // Close modals when clicking outside
        document.addEventListener('click', (e) => {
            if (e.target.classList.contains('modal')) {
                this.closeModal(e.target);
            }
        });
        
        // Escape key to close modals
        document.addEventListener('keydown', (e) => {
            if (e.key === 'Escape') {
                this.closeTopModal();
            }
        });
        
        // Handle window resize for responsive design
        window.addEventListener('resize', this.handleResize.bind(this));
        
        // Handle online/offline status
        window.addEventListener('online', () => {
            window.auth.showToast('Connection restored', 'success');
        });
        
        window.addEventListener('offline', () => {
            window.auth.showToast('Connection lost. Some features may not work.', 'warning');
        });
        
        // Prevent form submission from refreshing page
        document.addEventListener('submit', (e) => {
            e.preventDefault();
        });
        
        // Auto-save draft messages
        const chatInput = document.getElementById('chat-input');
        chatInput.addEventListener('input', this.saveDraftMessage.bind(this));
        
        // Load draft message on page load
        this.loadDraftMessage();
    }
    
    setupResponsive() {
        this.updateResponsiveClasses();
        
        // Add mobile menu toggle if needed
        if (window.innerWidth <= 768) {
            this.setupMobileMenu();
        }
    }
    
    setupMobileMenu() {
        // Add mobile menu toggle button to header if not exists
        const header = document.querySelector('.header-content');
        const existingToggle = header.querySelector('.mobile-menu-toggle');
        
        if (!existingToggle) {
            const toggle = document.createElement('button');
            toggle.className = 'mobile-menu-toggle';
            toggle.innerHTML = '<i class="fas fa-bars"></i>';
            toggle.onclick = this.toggleMobileMenu.bind(this);
            
            // Insert before user info
            const userInfo = header.querySelector('.user-info');
            header.insertBefore(toggle, userInfo);
        }
    }
    
    toggleMobileMenu() {
        const sidebar = document.querySelector('.sidebar');
        sidebar.classList.toggle('mobile-open');
        
        // Add overlay
        if (sidebar.classList.contains('mobile-open')) {
            const overlay = document.createElement('div');
            overlay.className = 'mobile-overlay';
            overlay.onclick = this.toggleMobileMenu.bind(this);
            document.body.appendChild(overlay);
        } else {
            const overlay = document.querySelector('.mobile-overlay');
            if (overlay) overlay.remove();
        }
    }
    
    setupKeyboardShortcuts() {
        document.addEventListener('keydown', (e) => {
            // Ctrl/Cmd + Enter to send message
            if ((e.ctrlKey || e.metaKey) && e.key === 'Enter') {
                if (document.activeElement.id === 'chat-input') {
                    window.chatbot.sendMessage();
                }
            }
            
            // Ctrl/Cmd + N for new chat
            if ((e.ctrlKey || e.metaKey) && e.key === 'n') {
                e.preventDefault();
                startNewChat();
            }
            
            // Ctrl/Cmd + E to export chat
            if ((e.ctrlKey || e.metaKey) && e.key === 'e') {
                e.preventDefault();
                exportChat();
            }
            
            // Ctrl/Cmd + K to focus chat input
            if ((e.ctrlKey || e.metaKey) && e.key === 'k') {
                e.preventDefault();
                document.getElementById('chat-input').focus();
            }
        });
    }
    
    setupErrorHandling() {
        // Global error handler
        window.addEventListener('error', (e) => {
            console.error('Global error:', e.error);
            
            // Show user-friendly error message
            if (window.auth) {
                window.auth.showToast('An unexpected error occurred. Please refresh the page if problems persist.', 'error');
            }
        });
        
        // Unhandled promise rejection handler
        window.addEventListener('unhandledrejection', (e) => {
            console.error('Unhandled promise rejection:', e.reason);
            
            if (window.auth) {
                window.auth.showToast('A network error occurred. Please check your connection.', 'error');
            }
        });
    }
    
    handleResize() {
        this.updateResponsiveClasses();
        
        // Close mobile menus on desktop
        if (window.innerWidth > 768) {
            const sidebar = document.querySelector('.sidebar');
            const productPanel = document.querySelector('.product-panel');
            const overlay = document.querySelector('.mobile-overlay');
            
            sidebar.classList.remove('mobile-open');
            productPanel.classList.remove('mobile-open');
            if (overlay) overlay.remove();
        }
    }
    
    updateResponsiveClasses() {
        const body = document.body;
        
        // Add responsive classes
        if (window.innerWidth <= 480) {
            body.classList.add('mobile-sm');
            body.classList.remove('mobile-lg', 'tablet', 'desktop');
        } else if (window.innerWidth <= 768) {
            body.classList.add('mobile-lg');
            body.classList.remove('mobile-sm', 'tablet', 'desktop');
        } else if (window.innerWidth <= 1024) {
            body.classList.add('tablet');
            body.classList.remove('mobile-sm', 'mobile-lg', 'desktop');
        } else {
            body.classList.add('desktop');
            body.classList.remove('mobile-sm', 'mobile-lg', 'tablet');
        }
    }
    
    closeModal(modal) {
        modal.classList.add('hidden');
    }
    
    closeTopModal() {
        const modals = document.querySelectorAll('.modal:not(.hidden)');
        if (modals.length > 0) {
            const topModal = modals[modals.length - 1];
            this.closeModal(topModal);
        }
    }
    
    saveDraftMessage() {
        const input = document.getElementById('chat-input');
        const message = input.value.trim();
        
        if (message) {
            localStorage.setItem('draft_message', message);
        } else {
            localStorage.removeItem('draft_message');
        }
    }
    
    loadDraftMessage() {
        const draftMessage = localStorage.getItem('draft_message');
        if (draftMessage) {
            const input = document.getElementById('chat-input');
            input.value = draftMessage;
            
            // Trigger input change event
            window.chatbot.handleInputChange({ target: input });
            
            // Show notification
            setTimeout(() => {
                if (window.auth) {
                    window.auth.showToast('Draft message restored', 'info');
                }
            }, 1000);
        }
    }
    
    // Utility methods
    formatCurrency(amount) {
        return new Intl.NumberFormat('en-US', {
            style: 'currency',
            currency: 'USD'
        }).format(amount);
    }
    
    formatDate(dateString) {
        return new Intl.DateTimeFormat('en-US', {
            year: 'numeric',
            month: 'short',
            day: 'numeric',
            hour: '2-digit',
            minute: '2-digit'
        }).format(new Date(dateString));
    }
    
    debounce(func, wait) {
        let timeout;
        return function executedFunction(...args) {
            const later = () => {
                clearTimeout(timeout);
                func(...args);
            };
            clearTimeout(timeout);
            timeout = setTimeout(later, wait);
        };
    }
    
    throttle(func, limit) {
        let inThrottle;
        return function() {
            const args = arguments;
            const context = this;
            if (!inThrottle) {
                func.apply(context, args);
                inThrottle = true;
                setTimeout(() => inThrottle = false, limit);
            }
        };
    }
}

// Initialize app
window.app = new AppManager();

// Performance monitoring
if ('performance' in window) {
    window.addEventListener('load', () => {
        const perfData = performance.getEntriesByType('navigation')[0];
        console.log(`Page load time: ${perfData.loadEventEnd - perfData.fetchStart}ms`);
    });
}

// Service worker registration (for future PWA features)
if ('serviceWorker' in navigator) {
    window.addEventListener('load', () => {
        // navigator.registerServiceWorker('/sw.js') when ready
        console.log('Service worker support detected');
    });
}

// Add mobile-specific styles
const mobileStyles = document.createElement('style');
mobileStyles.textContent = `
.mobile-menu-toggle {
    display: none;
    background: none;
    border: none;
    font-size: 1.25rem;
    color: var(--text-secondary);
    cursor: pointer;
    padding: 0.5rem;
    border-radius: var(--radius-md);
}

.mobile-menu-toggle:hover {
    background-color: var(--bg-tertiary);
    color: var(--text-primary);
}

.mobile-overlay {
    position: fixed;
    top: 0;
    left: 0;
    width: 100vw;
    height: 100vh;
    background-color: rgba(0, 0, 0, 0.5);
    z-index: 150;
}

@media (max-width: 768px) {
    .mobile-menu-toggle {
        display: block;
    }
    
    .sidebar {
        box-shadow: var(--shadow-xl);
    }
    
    .product-panel {
        box-shadow: var(--shadow-xl);
    }
}

/* Loading states */
.btn.loading {
    position: relative;
    color: transparent;
}

.btn.loading::after {
    content: '';
    position: absolute;
    top: 50%;
    left: 50%;
    width: 1rem;
    height: 1rem;
    margin: -0.5rem 0 0 -0.5rem;
    border: 2px solid transparent;
    border-top: 2px solid currentColor;
    border-radius: 50%;
    animation: spin 1s linear infinite;
}

/* Accessibility improvements */
@media (prefers-reduced-motion: reduce) {
    *,
    *::before,
    *::after {
        animation-duration: 0.01ms !important;
        animation-iteration-count: 1 !important;
        transition-duration: 0.01ms !important;
    }
}

/* High contrast mode support */
@media (prefers-contrast: high) {
    :root {
        --border-color: #000000;
        --border-dark: #000000;
        --text-muted: #333333;
    }
}

/* Focus indicators for keyboard navigation */
.btn:focus-visible,
.quick-action-btn:focus-visible,
.chat-session-item:focus-visible,
.product-card:focus-visible {
    outline: 2px solid var(--primary-color);
    outline-offset: 2px;
}

/* Skip to main content link for screen readers */
.skip-link {
    position: absolute;
    top: -40px;
    left: 6px;
    background: var(--primary-color);
    color: white;
    padding: 8px;
    text-decoration: none;
    border-radius: 4px;
    z-index: 9999;
}

.skip-link:focus {
    top: 6px;
}
`;
document.head.appendChild(mobileStyles);

// Add skip link for accessibility
document.addEventListener('DOMContentLoaded', () => {
    const skipLink = document.createElement('a');
    skipLink.href = '#chat-messages';
    skipLink.className = 'skip-link';
    skipLink.textContent = 'Skip to main content';
    document.body.insertBefore(skipLink, document.body.firstChild);
});

// Export for potential module use
if (typeof module !== 'undefined' && module.exports) {
    module.exports = AppManager;
}

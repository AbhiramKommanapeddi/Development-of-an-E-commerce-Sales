// Authentication module
class AuthManager {
    constructor() {
        this.baseURL = 'http://localhost:5000/api';
        this.token = localStorage.getItem('access_token');
        this.user = JSON.parse(localStorage.getItem('user') || 'null');
        this.sessionId = localStorage.getItem('session_id');
        
        this.initializeAuth();
    }
    
    initializeAuth() {
        // Set up form event listeners
        document.getElementById('login-form').addEventListener('submit', (e) => {
            e.preventDefault();
            this.handleLogin();
        });
        
        document.getElementById('register-form').addEventListener('submit', (e) => {
            e.preventDefault();
            this.handleRegister();
        });
        
        // Check if user is already logged in
        if (this.token && this.user) {
            this.showApp();
        } else {
            this.showAuthModal();
        }
    }
    
    async handleLogin() {
        const username = document.getElementById('login-username').value.trim();
        const password = document.getElementById('login-password').value;
        
        if (!username || !password) {
            this.showToast('Please fill in all fields', 'error');
            return;
        }
        
        try {
            const response = await fetch(`${this.baseURL}/auth/login`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ username, password })
            });
            
            const data = await response.json();
            
            if (response.ok) {
                this.handleAuthSuccess(data);
            } else {
                this.showToast(data.error || 'Login failed', 'error');
            }
        } catch (error) {
            console.error('Login error:', error);
            this.showToast('Network error. Please try again.', 'error');
        }
    }
    
    async handleRegister() {
        const username = document.getElementById('register-username').value.trim();
        const email = document.getElementById('register-email').value.trim();
        const password = document.getElementById('register-password').value;
        const confirmPassword = document.getElementById('register-confirm-password').value;
        
        if (!username || !email || !password || !confirmPassword) {
            this.showToast('Please fill in all fields', 'error');
            return;
        }
        
        if (password !== confirmPassword) {
            this.showToast('Passwords do not match', 'error');
            return;
        }
        
        if (password.length < 6) {
            this.showToast('Password must be at least 6 characters long', 'error');
            return;
        }
        
        try {
            const response = await fetch(`${this.baseURL}/auth/register`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ username, email, password })
            });
            
            const data = await response.json();
            
            if (response.ok) {
                this.handleAuthSuccess(data);
            } else {
                this.showToast(data.error || 'Registration failed', 'error');
            }
        } catch (error) {
            console.error('Registration error:', error);
            this.showToast('Network error. Please try again.', 'error');
        }
    }
    
    handleAuthSuccess(data) {
        // Store authentication data
        this.token = data.access_token;
        this.user = data.user;
        this.sessionId = data.session_id;
        
        localStorage.setItem('access_token', this.token);
        localStorage.setItem('user', JSON.stringify(this.user));
        localStorage.setItem('session_id', this.sessionId);
        
        // Show success message
        this.showToast(`Welcome${data.user.username ? ', ' + data.user.username : ''}!`, 'success');
        
        // Hide auth modal and show app
        this.hideAuthModal();
        this.showApp();
    }
    
    async logout() {
        try {
            if (this.token) {
                await fetch(`${this.baseURL}/auth/logout`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'Authorization': `Bearer ${this.token}`
                    },
                    body: JSON.stringify({ session_id: this.sessionId })
                });
            }
        } catch (error) {
            console.error('Logout error:', error);
        } finally {
            // Clear local storage
            localStorage.removeItem('access_token');
            localStorage.removeItem('user');
            localStorage.removeItem('session_id');
            
            // Reset instance variables
            this.token = null;
            this.user = null;
            this.sessionId = null;
            
            // Show auth modal
            this.showAuthModal();
            this.hideApp();
            
            this.showToast('Logged out successfully', 'success');
        }
    }
    
    showAuthModal() {
        document.getElementById('auth-modal').classList.remove('hidden');
        document.getElementById('login-form').classList.remove('hidden');
        document.getElementById('register-form').classList.add('hidden');
        document.getElementById('auth-title').textContent = 'Welcome Back';
        
        // Clear form fields
        this.clearAuthForms();
    }
    
    hideAuthModal() {
        document.getElementById('auth-modal').classList.add('hidden');
    }
    
    showApp() {
        // Hide loading screen
        document.getElementById('loading-screen').classList.add('hidden');
        
        // Show app
        document.getElementById('app').classList.remove('hidden');
        
        // Update user name in header
        if (this.user && this.user.username) {
            document.getElementById('user-name').textContent = this.user.username;
        }
        
        // Initialize other app components
        if (window.chatbot) {
            window.chatbot.initialize();
        }
    }
    
    hideApp() {
        document.getElementById('app').classList.add('hidden');
    }
    
    clearAuthForms() {
        document.getElementById('login-username').value = '';
        document.getElementById('login-password').value = '';
        document.getElementById('register-username').value = '';
        document.getElementById('register-email').value = '';
        document.getElementById('register-password').value = '';
        document.getElementById('register-confirm-password').value = '';
    }
    
    getAuthHeaders() {
        if (!this.token) {
            throw new Error('No authentication token available');
        }
        
        return {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${this.token}`
        };
    }
    
    isAuthenticated() {
        return this.token && this.user;
    }
    
    showToast(message, type = 'info') {
        const container = document.getElementById('toast-container');
        const toast = document.createElement('div');
        toast.className = `toast ${type}`;
        
        const messageElement = document.createElement('div');
        messageElement.className = 'toast-message';
        messageElement.textContent = message;
        
        toast.appendChild(messageElement);
        container.appendChild(toast);
        
        // Auto remove after 5 seconds
        setTimeout(() => {
            if (toast.parentNode) {
                toast.style.animation = 'toastSlideOut 0.3s ease-in forwards';
                setTimeout(() => {
                    if (toast.parentNode) {
                        container.removeChild(toast);
                    }
                }, 300);
            }
        }, 5000);
    }
}

// Global auth instance
window.auth = new AuthManager();

// Global functions for HTML onclick handlers
function closeAuthModal() {
    // Only close if user is authenticated
    if (window.auth.isAuthenticated()) {
        window.auth.hideAuthModal();
    }
}

function switchToRegister() {
    document.getElementById('login-form').classList.add('hidden');
    document.getElementById('register-form').classList.remove('hidden');
    document.getElementById('auth-title').textContent = 'Create Account';
    window.auth.clearAuthForms();
}

function switchToLogin() {
    document.getElementById('register-form').classList.add('hidden');
    document.getElementById('login-form').classList.remove('hidden');
    document.getElementById('auth-title').textContent = 'Welcome Back';
    window.auth.clearAuthForms();
}

function logout() {
    window.auth.logout();
}

function toggleUserMenu() {
    const dropdown = document.getElementById('user-dropdown');
    dropdown.classList.toggle('hidden');
    
    // Close dropdown when clicking outside
    document.addEventListener('click', function closeDropdown(e) {
        if (!e.target.closest('.user-menu')) {
            dropdown.classList.add('hidden');
            document.removeEventListener('click', closeDropdown);
        }
    });
}

function showProfile() {
    // Hide user dropdown
    document.getElementById('user-dropdown').classList.add('hidden');
    
    // Show profile information in a toast for now
    if (window.auth.user) {
        const user = window.auth.user;
        const profileInfo = `Username: ${user.username}\nEmail: ${user.email}\nMember since: ${new Date(user.created_at).toLocaleDateString()}`;
        window.auth.showToast(profileInfo, 'info');
    }
}

function showChatHistory() {
    // Hide user dropdown
    document.getElementById('user-dropdown').classList.add('hidden');
    
    // Load chat history (this will be implemented in the chatbot module)
    if (window.chatbot) {
        window.chatbot.loadChatHistory();
    }
}

// Add CSS for toast slide out animation
const style = document.createElement('style');
style.textContent = `
@keyframes toastSlideOut {
    from {
        transform: translateX(0);
        opacity: 1;
    }
    to {
        transform: translateX(100%);
        opacity: 0;
    }
}
`;
document.head.appendChild(style);

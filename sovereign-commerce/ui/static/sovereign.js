// Sovereign Commerce - Core JavaScript Functions

// Authentication state management
let authToken = localStorage.getItem('sovereign_token');
let currentUser = null;

// Initialize the application
document.addEventListener('DOMContentLoaded', function() {
    initializeApp();
    setupEventListeners();
    checkAuthentication();
});

// Application initialization
function initializeApp() {
    console.log('🏰 Sovereign Commerce Portal Initialized');
    
    // Add sovereign loading indicators
    addLoadingStyles();
    
    // Initialize tooltips and popovers if Bootstrap is available
    if (typeof bootstrap !== 'undefined') {
        const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
        tooltipTriggerList.map(function (tooltipTriggerEl) {
            return new bootstrap.Tooltip(tooltipTriggerEl);
        });
    }
}

// Authentication functions
async function checkAuthentication() {
    if (!authToken) {
        return false;
    }
    
    try {
        const response = await fetch('/api/auth/me', {
            headers: {
                'Authorization': `Bearer ${authToken}`,
                'Content-Type': 'application/json'
            }
        });
        
        if (response.ok) {
            currentUser = await response.json();
            updateUIForAuthenticatedUser();
            return true;
        } else {
            logout();
            return false;
        }
    } catch (error) {
        console.error('🔥 Authentication check failed:', error);
        logout();
        return false;
    }
}

async function login(email, password) {
    try {
        showLoading('Entering the sacred portal...');
        
        const response = await fetch('/api/auth/login', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ email, password })
        });
        
        const data = await response.json();
        
        if (response.ok) {
            authToken = data.access_token;
            localStorage.setItem('sovereign_token', authToken);
            currentUser = data.user;
            
            showSuccess('🏰 Welcome to the Sovereign Portal!');
            updateUIForAuthenticatedUser();
            
            // Redirect based on page context
            if (window.location.pathname === '/') {
                window.location.href = '/dashboard';
            } else {
                window.location.reload();
            }
        } else {
            showError(data.detail || '⚔️ Authentication failed. The portal remains sealed.');
        }
    } catch (error) {
        console.error('🔥 Login error:', error);
        showError('🌩️ Portal connection failed. Please try again.');
    } finally {
        hideLoading();
    }
}

async function register(userData) {
    try {
        showLoading('Forging your sacred sigil...');
        
        const response = await fetch('/api/auth/register', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(userData)
        });
        
        const data = await response.json();
        
        if (response.ok) {
            authToken = data.access_token;
            localStorage.setItem('sovereign_token', authToken);
            currentUser = data.user;
            
            showSuccess(`🌟 Welcome to the diaspora, ${data.user.full_name}! Your sigil: ${data.user.sigil}`);
            updateUIForAuthenticatedUser();
            
            // Redirect to dashboard
            setTimeout(() => {
                window.location.href = '/dashboard';
            }, 2000);
        } else {
            showError(data.detail || '⚔️ Registration failed. The sigil could not be forged.');
        }
    } catch (error) {
        console.error('🔥 Registration error:', error);
        showError('🌩️ Portal connection failed. Please try again.');
    } finally {
        hideLoading();
    }
}

function logout() {
    authToken = null;
    currentUser = null;
    localStorage.removeItem('sovereign_token');
    
    showSuccess('🚪 You have exited the sacred portal.');
    
    // Redirect to home page
    setTimeout(() => {
        window.location.href = '/';
    }, 1500);
}

function updateUIForAuthenticatedUser() {
    if (!currentUser) return;
    
    // Update user-specific elements
    const userNameElements = document.querySelectorAll('#userName');
    const userEmailElements = document.querySelectorAll('#userEmail');
    const userSigilElements = document.querySelectorAll('#userSigil');
    const userRoleElements = document.querySelectorAll('#userRole');
    
    userNameElements.forEach(el => el.textContent = currentUser.full_name);
    userEmailElements.forEach(el => el.textContent = currentUser.email);
    userSigilElements.forEach(el => el.textContent = currentUser.sigil);
    userRoleElements.forEach(el => {
        el.innerHTML = `<i class="fas fa-crown me-1"></i>${currentUser.role.charAt(0).toUpperCase() + currentUser.role.slice(1)}`;
    });
    
    // Update join date if available
    if (currentUser.created_at) {
        const joinDateElements = document.querySelectorAll('#joinDate');
        const joinDate = new Date(currentUser.created_at).toLocaleDateString('en-US', { 
            year: 'numeric', 
            month: 'long' 
        });
        joinDateElements.forEach(el => el.textContent = joinDate);
    }
}

// Event listeners setup
function setupEventListeners() {
    // Login form
    const loginForm = document.getElementById('loginForm');
    if (loginForm) {
        loginForm.addEventListener('submit', async function(e) {
            e.preventDefault();
            const email = document.getElementById('loginEmail').value;
            const password = document.getElementById('loginPassword').value;
            await login(email, password);
        });
    }
    
    // Register form
    const registerForm = document.getElementById('registerForm');
    if (registerForm) {
        registerForm.addEventListener('submit', async function(e) {
            e.preventDefault();
            const userData = {
                full_name: document.getElementById('registerName').value,
                email: document.getElementById('registerEmail').value,
                password: document.getElementById('registerPassword').value,
                role: document.getElementById('registerRole').value
            };
            await register(userData);
        });
    }
}

// API request helper
async function apiRequest(endpoint, options = {}) {
    const defaultOptions = {
        headers: {
            'Content-Type': 'application/json'
        }
    };
    
    if (authToken) {
        defaultOptions.headers['Authorization'] = `Bearer ${authToken}`;
    }
    
    const config = {
        ...defaultOptions,
        ...options,
        headers: {
            ...defaultOptions.headers,
            ...options.headers
        }
    };
    
    try {
        const response = await fetch(endpoint, config);
        
        if (response.status === 401) {
            logout();
            throw new Error('Authentication required');
        }
        
        const data = await response.json();
        
        if (!response.ok) {
            throw new Error(data.detail || 'Request failed');
        }
        
        return data;
    } catch (error) {
        console.error(`🔥 API Request failed: ${endpoint}`, error);
        throw error;
    }
}

// UI Feedback Functions
function showLoading(message = 'Loading...') {
    const existingModal = document.getElementById('loadingModal');
    if (existingModal) {
        existingModal.remove();
    }
    
    const modal = document.createElement('div');
    modal.id = 'loadingModal';
    modal.className = 'modal fade';
    modal.setAttribute('data-bs-backdrop', 'static');
    modal.innerHTML = `
        <div class="modal-dialog modal-sm modal-dialog-centered">
            <div class="modal-content sovereign-modal">
                <div class="modal-body text-center py-4">
                    <div class="spinner-border text-gold mb-3" role="status">
                        <span class="visually-hidden">Loading...</span>
                    </div>
                    <p class="mb-0 text-light">${message}</p>
                </div>
            </div>
        </div>
    `;
    
    document.body.appendChild(modal);
    const bootstrapModal = new bootstrap.Modal(modal);
    bootstrapModal.show();
}

function hideLoading() {
    const loadingModal = document.getElementById('loadingModal');
    if (loadingModal) {
        const bootstrapModal = bootstrap.Modal.getInstance(loadingModal);
        if (bootstrapModal) {
            bootstrapModal.hide();
        }
        setTimeout(() => loadingModal.remove(), 300);
    }
}

function showSuccess(message) {
    showNotification(message, 'success');
}

function showError(message) {
    showNotification(message, 'error');
}

function showInfo(message) {
    showNotification(message, 'info');
}

function showNotification(message, type = 'info') {
    const notification = document.createElement('div');
    notification.className = `notification notification-${type}`;
    notification.innerHTML = `
        <div class="notification-content">
            <div class="notification-icon">
                ${getNotificationIcon(type)}
            </div>
            <div class="notification-message">${message}</div>
            <button class="notification-close" onclick="this.parentElement.parentElement.remove()">
                <i class="fas fa-times"></i>
            </button>
        </div>
    `;
    
    document.body.appendChild(notification);
    
    // Show animation
    setTimeout(() => notification.classList.add('show'), 100);
    
    // Auto-remove after 5 seconds
    setTimeout(() => {
        if (notification.parentElement) {
            notification.classList.remove('show');
            setTimeout(() => notification.remove(), 300);
        }
    }, 5000);
}

function getNotificationIcon(type) {
    switch (type) {
        case 'success':
            return '<i class="fas fa-check-circle"></i>';
        case 'error':
            return '<i class="fas fa-exclamation-triangle"></i>';
        case 'info':
        default:
            return '<i class="fas fa-info-circle"></i>';
    }
}

// Add notification and loading styles
function addLoadingStyles() {
    if (document.getElementById('sovereignStyles')) return;
    
    const styles = document.createElement('style');
    styles.id = 'sovereignStyles';
    styles.textContent = `
        /* Notification Styles */
        .notification {
            position: fixed;
            top: 20px;
            right: 20px;
            min-width: 300px;
            max-width: 500px;
            background: rgba(26, 26, 26, 0.95);
            backdrop-filter: blur(10px);
            border: 1px solid var(--sovereign-gold);
            border-radius: 10px;
            box-shadow: 0 10px 30px rgba(212, 175, 55, 0.3);
            z-index: 9999;
            transform: translateX(100%);
            transition: all 0.3s ease;
        }
        
        .notification.show {
            transform: translateX(0);
        }
        
        .notification-content {
            display: flex;
            align-items: center;
            padding: 1rem;
            color: #fff;
        }
        
        .notification-icon {
            font-size: 1.5rem;
            margin-right: 1rem;
            color: var(--sovereign-gold);
        }
        
        .notification-message {
            flex: 1;
            font-size: 0.95rem;
            line-height: 1.4;
        }
        
        .notification-close {
            background: none;
            border: none;
            color: rgba(255, 255, 255, 0.7);
            font-size: 1rem;
            cursor: pointer;
            margin-left: 1rem;
            transition: color 0.2s ease;
        }
        
        .notification-close:hover {
            color: var(--sovereign-gold);
        }
        
        .notification-success {
            border-color: #10B981;
        }
        
        .notification-success .notification-icon {
            color: #10B981;
        }
        
        .notification-error {
            border-color: #EF4444;
        }
        
        .notification-error .notification-icon {
            color: #EF4444;
        }
        
        /* Loading Spinner Enhancement */
        .spinner-border.text-gold {
            color: var(--sovereign-gold) !important;
            border-color: var(--sovereign-gold);
            border-right-color: transparent;
        }
        
        /* Smooth transitions for all interactive elements */
        .btn, .nav-link, .card, .modal-content {
            transition: all 0.3s ease;
        }
        
        /* Enhanced focus states */
        .form-control:focus, .btn:focus {
            outline: none;
            box-shadow: 0 0 0 0.2rem rgba(212, 175, 55, 0.25);
        }
    `;
    
    document.head.appendChild(styles);
}

// Utility functions
function formatCurrency(amount) {
    return new Intl.NumberFormat('en-US', {
        style: 'currency',
        currency: 'USD'
    }).format(amount);
}

function formatDate(dateString) {
    return new Date(dateString).toLocaleDateString('en-US', {
        year: 'numeric',
        month: 'long',
        day: 'numeric'
    });
}

function formatDateTime(dateString) {
    return new Date(dateString).toLocaleString('en-US', {
        year: 'numeric',
        month: 'short',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
    });
}

function debounce(func, wait) {
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

// Export for use in other scripts
window.SovereignCommerce = {
    apiRequest,
    showLoading,
    hideLoading,
    showSuccess,
    showError,
    showInfo,
    formatCurrency,
    formatDate,
    formatDateTime,
    debounce,
    currentUser: () => currentUser,
    isAuthenticated: () => !!authToken,
    logout
};
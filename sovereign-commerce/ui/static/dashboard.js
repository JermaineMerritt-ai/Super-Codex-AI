// Dashboard Management - Funder Portal

// Dashboard state
let userStats = {
    totalOrders: 0,
    totalSpent: 0,
    ceremonialSeals: 0,
    daysSinceJoined: 0
};
let recentOrders = [];

// Initialize dashboard when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    initializeDashboard();
    loadDashboardData();
    setupDashboardEventListeners();
});

async function initializeDashboard() {
    console.log('📊 Funder Dashboard Portal Initialized');
    
    // Check authentication
    if (!SovereignCommerce.isAuthenticated()) {
        SovereignCommerce.showInfo('🔐 Please authenticate to access your sacred dashboard.');
        setTimeout(() => window.location.href = '/', 2000);
        return;
    }
    
    // Calculate days since joined if user data is available
    const currentUser = SovereignCommerce.currentUser();
    if (currentUser && currentUser.created_at) {
        const joinDate = new Date(currentUser.created_at);
        const today = new Date();
        const diffTime = Math.abs(today - joinDate);
        userStats.daysSinceJoined = Math.ceil(diffTime / (1000 * 60 * 60 * 24));
        updateStatsDisplay();
    }
}

async function loadDashboardData() {
    try {
        SovereignCommerce.showLoading('Loading your sacred portal...');
        
        // Load user statistics
        await Promise.all([
            loadUserStats(),
            loadRecentOrders()
        ]);
        
        SovereignCommerce.showSuccess('🏛️ Sacred portal loaded successfully.');
    } catch (error) {
        console.error('🔥 Failed to load dashboard data:', error);
        SovereignCommerce.showError('⚡ Failed to load your portal. Please refresh.');
    } finally {
        SovereignCommerce.hideLoading();
    }
}

async function loadUserStats() {
    try {
        const data = await SovereignCommerce.apiRequest('/api/users/me/stats');
        
        userStats = {
            ...userStats,
            totalOrders: data.total_orders || 0,
            totalSpent: data.total_spent || 0,
            ceremonialSeals: data.ceremonial_seals || 0
        };
        
        updateStatsDisplay();
    } catch (error) {
        console.error('🔥 Failed to load user stats:', error);
        updateStatsDisplay();
    }
}

async function loadRecentOrders() {
    try {
        const data = await SovereignCommerce.apiRequest('/api/orders?limit=5');
        recentOrders = data;
        renderRecentOrders();
    } catch (error) {
        console.error('🔥 Failed to load recent orders:', error);
        renderRecentOrders([]);
    }
}

function updateStatsDisplay() {
    const totalOrdersEl = document.getElementById('totalOrders');
    const totalSpentEl = document.getElementById('totalSpent');
    const ceremonialSealsEl = document.getElementById('ceremonialSeals');
    const daysSinceEl = document.getElementById('daysSince');
    
    if (totalOrdersEl) {
        animateNumber(totalOrdersEl, userStats.totalOrders);
    }
    
    if (totalSpentEl) {
        totalSpentEl.textContent = SovereignCommerce.formatCurrency(userStats.totalSpent);
    }
    
    if (ceremonialSealsEl) {
        animateNumber(ceremonialSealsEl, userStats.ceremonialSeals);
    }
    
    if (daysSinceEl) {
        animateNumber(daysSinceEl, userStats.daysSinceJoined);
    }
}

function animateNumber(element, targetNumber) {
    const duration = 1000;
    const startNumber = parseInt(element.textContent) || 0;
    const increment = (targetNumber - startNumber) / (duration / 16);
    let currentNumber = startNumber;
    
    const timer = setInterval(() => {
        currentNumber += increment;
        if (increment > 0 && currentNumber >= targetNumber || increment < 0 && currentNumber <= targetNumber) {
            currentNumber = targetNumber;
            clearInterval(timer);
        }
        element.textContent = Math.round(currentNumber);
    }, 16);
}

function renderRecentOrders() {
    const recentOrdersContainer = document.getElementById('recentOrders');
    if (!recentOrdersContainer) return;
    
    if (recentOrders.length === 0) {
        recentOrdersContainer.innerHTML = `
            <div class="text-center py-5">
                <i class="fas fa-scroll fa-3x text-muted mb-3"></i>
                <h5 class="text-light">No Sacred Orders Yet</h5>
                <p class="text-muted mb-4">Begin your journey by exploring the sacred catalog.</p>
                <a href="/catalog" class="btn btn-sovereign">
                    <i class="fas fa-scroll me-2"></i>Browse Sacred Catalog
                </a>
            </div>
        `;
        return;
    }
    
    recentOrdersContainer.innerHTML = createOrdersList();
}

function createOrdersList() {
    return `
        <div class="orders-list">
            ${recentOrders.map(order => createOrderItem(order)).join('')}
        </div>
        ${recentOrders.length >= 5 ? `
            <div class="text-center mt-4">
                <button class="btn btn-outline-sovereign" onclick="viewAllOrders()">
                    <i class="fas fa-list me-2"></i>View All Orders
                </button>
            </div>
        ` : ''}
    `;
}

function createOrderItem(order) {
    return `
        <div class="order-item" onclick="showOrderDetail(${order.id})">
            <div class="d-flex align-items-center justify-content-between">
                <div class="order-info">
                    <div class="order-header d-flex align-items-center mb-2">
                        <h6 class="text-gold mb-0 me-3">Order #${order.id}</h6>
                        <span class="badge ${getStatusBadgeClass(order.status)}">
                            <i class="fas fa-${getStatusIcon(order.status)} me-1"></i>
                            ${order.status.charAt(0).toUpperCase() + order.status.slice(1)}
                        </span>
                    </div>
                    <div class="order-meta">
                        <small class="text-muted">
                            <i class="fas fa-calendar me-1"></i>
                            ${SovereignCommerce.formatDateTime(order.created_at)}
                        </small>
                        <small class="text-muted ms-3">
                            <i class="fas fa-box me-1"></i>
                            ${order.total_items} item${order.total_items !== 1 ? 's' : ''}
                        </small>
                    </div>
                </div>
                <div class="order-total text-end">
                    <div class="total-amount text-gold fw-bold">
                        ${SovereignCommerce.formatCurrency(order.total_amount)}
                    </div>
                    <small class="text-muted">
                        <i class="fas fa-eye me-1"></i>View Details
                    </small>
                </div>
            </div>
        </div>
    `;
}

function getStatusBadgeClass(status) {
    switch (status.toLowerCase()) {
        case 'completed':
            return 'bg-success';
        case 'processing':
            return 'bg-info';
        case 'pending':
            return 'bg-warning text-dark';
        case 'cancelled':
            return 'bg-danger';
        default:
            return 'bg-secondary';
    }
}

function getStatusIcon(status) {
    switch (status.toLowerCase()) {
        case 'completed':
            return 'check-circle';
        case 'processing':
            return 'cog fa-spin';
        case 'pending':
            return 'clock';
        case 'cancelled':
            return 'times-circle';
        default:
            return 'circle';
    }
}

async function showOrderDetail(orderId) {
    try {
        SovereignCommerce.showLoading('Loading sacred order details...');
        
        const order = await SovereignCommerce.apiRequest(`/api/orders/${orderId}`);
        
        const modal = document.getElementById('orderDetailModal');
        const modalBody = document.getElementById('orderDetailBody');
        
        modalBody.innerHTML = createOrderDetailContent(order);
        
        new bootstrap.Modal(modal).show();
        
    } catch (error) {
        console.error('🔥 Failed to load order details:', error);
        SovereignCommerce.showError('⚡ Failed to load order details.');
    } finally {
        SovereignCommerce.hideLoading();
    }
}

function createOrderDetailContent(order) {
    return `
        <div class="order-detail">
            <div class="order-header-detail mb-4">
                <div class="row">
                    <div class="col-md-6">
                        <h5 class="text-gold mb-3">
                            <i class="fas fa-scroll me-2"></i>Order #${order.id}
                        </h5>
                        <div class="order-meta">
                            <p class="mb-2">
                                <strong class="text-gold">Status:</strong>
                                <span class="badge ${getStatusBadgeClass(order.status)} ms-2">
                                    <i class="fas fa-${getStatusIcon(order.status)} me-1"></i>
                                    ${order.status.charAt(0).toUpperCase() + order.status.slice(1)}
                                </span>
                            </p>
                            <p class="mb-2">
                                <strong class="text-gold">Order Date:</strong>
                                <span class="text-light ms-2">${SovereignCommerce.formatDateTime(order.created_at)}</span>
                            </p>
                            ${order.ceremonial_seal ? `
                                <p class="mb-2">
                                    <strong class="text-gold">Ceremonial Seal:</strong>
                                    <span class="text-light ms-2">${order.ceremonial_seal}</span>
                                </p>
                            ` : ''}
                        </div>
                    </div>
                    <div class="col-md-6 text-end">
                        <div class="total-summary">
                            <h4 class="text-gold mb-0">${SovereignCommerce.formatCurrency(order.total_amount)}</h4>
                            <small class="text-muted">Total Sacred Tribute</small>
                        </div>
                    </div>
                </div>
            </div>
            
            <div class="order-items">
                <h6 class="text-gold mb-3">
                    <i class="fas fa-list me-2"></i>Sacred Offerings
                </h6>
                <div class="items-list">
                    ${order.items.map(item => createOrderItemRow(item)).join('')}
                </div>
            </div>
        </div>
    `;
}

function createOrderItemRow(item) {
    return `
        <div class="item-row d-flex align-items-center justify-content-between mb-3 p-3"
             style="background: rgba(255,255,255,0.05); border-radius: 10px;">
            <div class="item-info">
                <h6 class="text-light mb-1">${item.product_name}</h6>
                <small class="text-muted">
                    ${SovereignCommerce.formatCurrency(item.price)} × ${item.quantity}
                </small>
            </div>
            <div class="item-total text-gold fw-bold">
                ${SovereignCommerce.formatCurrency(item.subtotal)}
            </div>
        </div>
    `;
}

async function viewAllOrders() {
    try {
        SovereignCommerce.showLoading('Loading all sacred orders...');
        
        const orders = await SovereignCommerce.apiRequest('/api/orders');
        
        const modal = document.getElementById('allOrdersModal');
        const modalBody = document.getElementById('allOrdersBody');
        
        modalBody.innerHTML = createAllOrdersContent(orders);
        
        new bootstrap.Modal(modal).show();
        
    } catch (error) {
        console.error('🔥 Failed to load all orders:', error);
        SovereignCommerce.showError('⚡ Failed to load order history.');
    } finally {
        SovereignCommerce.hideLoading();
    }
}

function createAllOrdersContent(orders) {
    if (orders.length === 0) {
        return `
            <div class="text-center py-5">
                <i class="fas fa-scroll fa-3x text-muted mb-3"></i>
                <h5 class="text-light">No Sacred Orders Found</h5>
                <p class="text-muted">Your order history will appear here once you make your first purchase.</p>
            </div>
        `;
    }
    
    return `
        <div class="table-responsive">
            <table class="table table-dark table-hover">
                <thead>
                    <tr>
                        <th><i class="fas fa-hashtag me-2"></i>Order</th>
                        <th><i class="fas fa-calendar me-2"></i>Date</th>
                        <th><i class="fas fa-box me-2"></i>Items</th>
                        <th><i class="fas fa-circle me-2"></i>Status</th>
                        <th><i class="fas fa-dollar-sign me-2"></i>Total</th>
                        <th></th>
                    </tr>
                </thead>
                <tbody>
                    ${orders.map(order => createOrderTableRow(order)).join('')}
                </tbody>
            </table>
        </div>
    `;
}

function createOrderTableRow(order) {
    return `
        <tr onclick="showOrderDetail(${order.id})" style="cursor: pointer;">
            <td class="text-gold fw-bold">#${order.id}</td>
            <td>${SovereignCommerce.formatDate(order.created_at)}</td>
            <td>${order.total_items}</td>
            <td>
                <span class="badge ${getStatusBadgeClass(order.status)}">
                    ${order.status.charAt(0).toUpperCase() + order.status.slice(1)}
                </span>
            </td>
            <td class="text-gold">${SovereignCommerce.formatCurrency(order.total_amount)}</td>
            <td>
                <i class="fas fa-eye text-muted"></i>
            </td>
        </tr>
    `;
}

function updateProfile() {
    SovereignCommerce.showInfo('⚒️ Profile update portal coming soon...');
}

function setupDashboardEventListeners() {
    console.log('📡 Dashboard event listeners initialized');
}

// Add dashboard styles
document.addEventListener('DOMContentLoaded', function() {
    addDashboardStyles();
});

function addDashboardStyles() {
    const styles = document.createElement('style');
    styles.textContent = `
        .order-item {
            background: rgba(255, 255, 255, 0.05);
            border: 1px solid rgba(212, 175, 55, 0.2);
            border-radius: 10px;
            padding: 1.25rem;
            margin-bottom: 1rem;
            transition: all 0.3s ease;
            cursor: pointer;
        }
        
        .order-item:hover {
            background: rgba(255, 255, 255, 0.1);
            border-color: var(--sovereign-gold);
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(212, 175, 55, 0.2);
        }
        
        .product-image-large {
            height: 200px;
            background: linear-gradient(45deg, var(--sovereign-gold), var(--sovereign-purple));
            border-radius: 10px;
            display: flex;
            align-items: center;
            justify-content: center;
            color: #000;
        }
        
        .table-dark {
            --bs-table-bg: rgba(255, 255, 255, 0.05);
        }
        
        .table-dark tbody tr:hover {
            background: rgba(212, 175, 55, 0.1) !important;
        }
        
        .empty-state {
            opacity: 0.8;
        }
    `;
    
    document.head.appendChild(styles);
}

// Make functions available globally
window.showOrderDetail = showOrderDetail;
window.viewAllOrders = viewAllOrders;
window.updateProfile = updateProfile;
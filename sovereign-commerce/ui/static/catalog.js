// Catalog Management - Sacred Commerce

// Catalog state management
let products = [];
let filteredProducts = [];
let cart = {
    items: [],
    total: 0
};

// Initialize catalog when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    initializeCatalog();
    loadProducts();
    setupCatalogEventListeners();
    loadCart();
});

async function initializeCatalog() {
    console.log('📜 Sacred Catalog Portal Initialized');
    
    // Check authentication
    if (!SovereignCommerce.isAuthenticated()) {
        showInfo('🔐 Please authenticate to access the sacred catalog.');
        setTimeout(() => window.location.href = '/', 2000);
        return;
    }
    
    updateCartDisplay();
}

async function loadProducts() {
    try {
        SovereignCommerce.showLoading('Unveiling sacred offerings...');
        
        const data = await SovereignCommerce.apiRequest('/api/products');
        products = data;
        filteredProducts = [...products];
        
        renderProducts();
        SovereignCommerce.showSuccess(`🏛️ ${products.length} sacred offerings revealed.`);
    } catch (error) {
        console.error('🔥 Failed to load products:', error);
        SovereignCommerce.showError('⚡ Failed to unveil sacred offerings. Please refresh the portal.');
    } finally {
        SovereignCommerce.hideLoading();
    }
}

function renderProducts() {
    const productGrid = document.getElementById('productGrid');
    if (!productGrid) return;
    
    if (filteredProducts.length === 0) {
        productGrid.innerHTML = `
            <div class="col-12 text-center py-5">
                <div class="empty-state">
                    <i class="fas fa-scroll fa-4x text-gold mb-3 opacity-50"></i>
                    <h4 class="text-light">No Sacred Offerings Found</h4>
                    <p class="text-muted">The cosmic filters have hidden all offerings. Try adjusting your search.</p>
                </div>
            </div>
        `;
        return;
    }
    
    productGrid.innerHTML = filteredProducts.map(product => `
        <div class="col-md-6 col-lg-4 mb-4">
            <div class="product-card" onclick="showProductDetail(${product.id})">
                <div class="product-image">
                    <i class="fas fa-${getProductIcon(product.category)}"></i>
                </div>
                <div class="product-info">
                    <h5 class="product-title">${product.name}</h5>
                    <div class="product-price">${SovereignCommerce.formatCurrency(product.price)}</div>
                    <p class="product-description">${truncateText(product.description, 100)}</p>
                    <div class="product-meta">
                        <small class="text-gold">
                            <i class="fas fa-tag me-1"></i>${product.category || 'Sacred'}
                        </small>
                        ${product.stock > 0 ? 
                            `<small class="text-success ms-3"><i class="fas fa-check-circle me-1"></i>In Stock</small>` :
                            `<small class="text-warning ms-3"><i class="fas fa-exclamation-triangle me-1"></i>Limited</small>`
                        }
                    </div>
                    <div class="mt-3">
                        <button class="btn btn-sovereign btn-sm w-100" onclick="event.stopPropagation(); addToCart(${product.id})">
                            <i class="fas fa-plus-circle me-2"></i>Add to Cart
                        </button>
                    </div>
                </div>
            </div>
        </div>
    `).join('');
}

function getProductIcon(category) {
    const icons = {
        'ceremonial': 'crown',
        'sacred': 'star',
        'knowledge': 'book',
        'regalia': 'gem',
        'artifact': 'scroll',
        'default': 'gift'
    };
    return icons[category?.toLowerCase()] || icons.default;
}

function truncateText(text, maxLength) {
    if (text.length <= maxLength) return text;
    return text.substring(0, maxLength).trim() + '...';
}

async function showProductDetail(productId) {
    const product = products.find(p => p.id === productId);
    if (!product) {
        SovereignCommerce.showError('🔍 Sacred offering not found.');
        return;
    }
    
    const modal = document.getElementById('productModal');
    const modalTitle = document.getElementById('productModalTitle');
    const modalBody = document.getElementById('productModalBody');
    const addToCartBtn = document.getElementById('addToCartBtn');
    
    modalTitle.innerHTML = `<i class="fas fa-${getProductIcon(product.category)} me-2 text-gold"></i>${product.name}`;
    
    modalBody.innerHTML = `
        <div class="row">
            <div class="col-md-4">
                <div class="product-image-large mb-3">
                    <i class="fas fa-${getProductIcon(product.category)} fa-4x text-gold"></i>
                </div>
                <div class="text-center">
                    <div class="product-price h4">${SovereignCommerce.formatCurrency(product.price)}</div>
                    <div class="product-category">
                        <span class="badge bg-gradient-gold">
                            <i class="fas fa-tag me-1"></i>${product.category || 'Sacred'}
                        </span>
                    </div>
                </div>
            </div>
            <div class="col-md-8">
                <div class="product-details">
                    <h6 class="text-gold mb-3">Sacred Description</h6>
                    <p class="text-light mb-4">${product.description}</p>
                    
                    <div class="row mb-3">
                        <div class="col-6">
                            <strong class="text-gold">Stock:</strong><br>
                            <span class="text-light">${product.stock > 0 ? product.stock + ' available' : 'Limited quantity'}</span>
                        </div>
                        <div class="col-6">
                            <strong class="text-gold">Sigil Required:</strong><br>
                            <span class="text-light">Funder or higher</span>
                        </div>
                    </div>
                    
                    ${product.metadata ? `
                        <div class="product-metadata">
                            <h6 class="text-gold mb-2">Sacred Attributes</h6>
                            <div class="metadata-grid">
                                ${Object.entries(product.metadata).map(([key, value]) => `
                                    <div class="metadata-item">
                                        <small class="text-muted">${key}:</small>
                                        <span class="text-light">${value}</span>
                                    </div>
                                `).join('')}
                            </div>
                        </div>
                    ` : ''}
                </div>
            </div>
        </div>
    `;
    
    addToCartBtn.onclick = () => {
        addToCart(productId);
        bootstrap.Modal.getInstance(modal).hide();
    };
    
    new bootstrap.Modal(modal).show();
}

// Cart management
function addToCart(productId) {
    const product = products.find(p => p.id === productId);
    if (!product) {
        SovereignCommerce.showError('🔍 Sacred offering not found.');
        return;
    }
    
    if (product.stock <= 0) {
        SovereignCommerce.showError('⚡ This sacred offering is no longer available.');
        return;
    }
    
    const existingItem = cart.items.find(item => item.product_id === productId);
    
    if (existingItem) {
        existingItem.quantity += 1;
        existingItem.subtotal = existingItem.quantity * existingItem.price;
    } else {
        cart.items.push({
            product_id: productId,
            name: product.name,
            price: product.price,
            quantity: 1,
            subtotal: product.price
        });
    }
    
    updateCartTotal();
    updateCartDisplay();
    saveCart();
    
    SovereignCommerce.showSuccess(`🛒 ${product.name} added to your sacred cart.`);
}

function removeFromCart(productId) {
    const itemIndex = cart.items.findIndex(item => item.product_id === productId);
    if (itemIndex > -1) {
        const item = cart.items[itemIndex];
        cart.items.splice(itemIndex, 1);
        updateCartTotal();
        updateCartDisplay();
        saveCart();
        SovereignCommerce.showSuccess(`🗑️ ${item.name} removed from your cart.`);
        renderCartItems(); // Refresh cart modal if open
    }
}

function updateCartQuantity(productId, newQuantity) {
    const item = cart.items.find(item => item.product_id === productId);
    if (item) {
        if (newQuantity <= 0) {
            removeFromCart(productId);
        } else {
            item.quantity = newQuantity;
            item.subtotal = item.quantity * item.price;
            updateCartTotal();
            updateCartDisplay();
            saveCart();
            renderCartItems(); // Refresh cart modal if open
        }
    }
}

function updateCartTotal() {
    cart.total = cart.items.reduce((total, item) => total + item.subtotal, 0);
}

function updateCartDisplay() {
    const cartCount = document.getElementById('cartCount');
    if (cartCount) {
        cartCount.textContent = cart.items.reduce((total, item) => total + item.quantity, 0);
    }
}

function showCart() {
    renderCartItems();
    new bootstrap.Modal(document.getElementById('cartModal')).show();
}

function renderCartItems() {
    const cartItemsContainer = document.getElementById('cartItems');
    const cartTotal = document.getElementById('cartTotal');
    
    if (!cartItemsContainer) return;
    
    if (cart.items.length === 0) {
        cartItemsContainer.innerHTML = `
            <div class="text-center py-4">
                <i class="fas fa-shopping-cart fa-3x text-muted mb-3"></i>
                <h5 class="text-light">Your Sacred Cart is Empty</h5>
                <p class="text-muted">Add some offerings from the sacred catalog.</p>
            </div>
        `;
        cartTotal.textContent = '0.00';
        return;
    }
    
    cartItemsContainer.innerHTML = cart.items.map(item => `
        <div class="cart-item d-flex align-items-center mb-3 p-3" style="background: rgba(255,255,255,0.05); border-radius: 10px;">
            <div class="item-info flex-grow-1">
                <h6 class="text-gold mb-1">${item.name}</h6>
                <div class="text-muted small">
                    ${SovereignCommerce.formatCurrency(item.price)} each
                </div>
            </div>
            <div class="quantity-controls d-flex align-items-center mx-3">
                <button class="btn btn-sm btn-outline-sovereign" onclick="updateCartQuantity(${item.product_id}, ${item.quantity - 1})">
                    <i class="fas fa-minus"></i>
                </button>
                <span class="mx-3 text-gold fw-bold">${item.quantity}</span>
                <button class="btn btn-sm btn-outline-sovereign" onclick="updateCartQuantity(${item.product_id}, ${item.quantity + 1})">
                    <i class="fas fa-plus"></i>
                </button>
            </div>
            <div class="item-total text-end">
                <div class="text-gold fw-bold">${SovereignCommerce.formatCurrency(item.subtotal)}</div>
                <button class="btn btn-sm text-danger mt-1" onclick="removeFromCart(${item.product_id})" title="Remove item">
                    <i class="fas fa-trash"></i>
                </button>
            </div>
        </div>
    `).join('');
    
    cartTotal.textContent = cart.total.toFixed(2);
}

function saveCart() {
    localStorage.setItem('sovereign_cart', JSON.stringify(cart));
}

function loadCart() {
    const savedCart = localStorage.getItem('sovereign_cart');
    if (savedCart) {
        cart = JSON.parse(savedCart);
        updateCartDisplay();
    }
}

function clearCart() {
    cart = { items: [], total: 0 };
    updateCartDisplay();
    saveCart();
}

async function checkout() {
    if (cart.items.length === 0) {
        SovereignCommerce.showError('🛒 Your sacred cart is empty. Add some offerings first.');
        return;
    }
    
    try {
        SovereignCommerce.showLoading('Preparing ceremonial checkout...');
        
        const orderData = {
            items: cart.items.map(item => ({
                product_id: item.product_id,
                quantity: item.quantity
            }))
        };
        
        const response = await SovereignCommerce.apiRequest('/api/orders', {
            method: 'POST',
            body: JSON.stringify(orderData)
        });
        
        SovereignCommerce.showSuccess(`🏆 Sacred Order ${response.id} completed! Your offerings await.`);
        
        // Clear cart and close modal
        clearCart();
        bootstrap.Modal.getInstance(document.getElementById('cartModal')).hide();
        
        // Redirect to dashboard to view order
        setTimeout(() => {
            window.location.href = '/dashboard';
        }, 2000);
        
    } catch (error) {
        console.error('🔥 Checkout failed:', error);
        SovereignCommerce.showError('⚡ Ceremonial checkout failed: ' + error.message);
    } finally {
        SovereignCommerce.hideLoading();
    }
}

// Search and filtering
function setupCatalogEventListeners() {
    const searchInput = document.getElementById('searchInput');
    const categoryFilter = document.getElementById('categoryFilter');
    const sortBy = document.getElementById('sortBy');
    
    if (searchInput) {
        searchInput.addEventListener('input', SovereignCommerce.debounce(filterProducts, 300));
    }
    
    if (categoryFilter) {
        categoryFilter.addEventListener('change', filterProducts);
    }
    
    if (sortBy) {
        sortBy.addEventListener('change', sortProducts);
    }
}

function filterProducts() {
    const searchTerm = document.getElementById('searchInput')?.value.toLowerCase() || '';
    const selectedCategory = document.getElementById('categoryFilter')?.value || '';
    
    filteredProducts = products.filter(product => {
        const matchesSearch = product.name.toLowerCase().includes(searchTerm) || 
                            product.description.toLowerCase().includes(searchTerm);
        const matchesCategory = !selectedCategory || product.category === selectedCategory;
        
        return matchesSearch && matchesCategory;
    });
    
    sortProducts();
}

function sortProducts() {
    const sortBy = document.getElementById('sortBy')?.value || 'name';
    
    filteredProducts.sort((a, b) => {
        switch (sortBy) {
            case 'price-low':
                return a.price - b.price;
            case 'price-high':
                return b.price - a.price;
            case 'newest':
                return new Date(b.created_at) - new Date(a.created_at);
            case 'name':
            default:
                return a.name.localeCompare(b.name);
        }
    });
    
    renderProducts();
}

// Make functions available globally for onclick handlers
window.showProductDetail = showProductDetail;
window.addToCart = addToCart;
window.removeFromCart = removeFromCart;
window.updateCartQuantity = updateCartQuantity;
window.checkout = checkout;
window.cart = {
    show: showCart,
    clear: clearCart
};
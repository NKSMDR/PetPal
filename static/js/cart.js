// Global Cart Management System
(function() {
    'use strict';
    
    // Cart storage key
    var CART_STORAGE_KEY = 'petstore_cart';
    var MAX_QUANTITY = 99;
    var MIN_QUANTITY = 1;
    
    // Check localStorage availability
    function isLocalStorageAvailable() {
        try {
            var test = '__localStorage_test__';
            localStorage.setItem(test, test);
            localStorage.removeItem(test);
            return true;
        } catch (e) {
            console.error('localStorage is not available:', e);
            return false;
        }
    }
    
    // Validate item object
    function validateItem(item) {
        if (!item || typeof item !== 'object') {
            return { valid: false, error: 'Item must be an object' };
        }
        
        if (!item.id) {
            return { valid: false, error: 'Item must have an id' };
        }
        
        if (!item.type) {
            return { valid: false, error: 'Item must have a type' };
        }
        
        if (!item.name || typeof item.name !== 'string') {
            return { valid: false, error: 'Item must have a valid name' };
        }
        
        if (typeof item.price !== 'number' || item.price < 0) {
            return { valid: false, error: 'Item must have a valid price' };
        }
        
        if (!item.quantity || typeof item.quantity !== 'number' || item.quantity < 1) {
            return { valid: false, error: 'Item must have a valid quantity' };
        }
        
        return { valid: true };
    }
    
    // Normalize item for consistent storage
    function normalizeItem(item) {
        return {
            id: String(item.id),
            type: String(item.type),
            name: String(item.name),
            price: parseFloat(item.price),
            image: item.image || '',
            quantity: parseInt(item.quantity) || 1
        };
    }
    
    // Cart management functions
    window.CartManager = {
        // Get cart from localStorage
        getCart: function() {
            if (!isLocalStorageAvailable()) {
                console.error('localStorage not available');
                return [];
            }
            
            try {
                var cart = localStorage.getItem(CART_STORAGE_KEY);
                var parsedCart = cart ? JSON.parse(cart) : [];
                
                // Validate and normalize cart items
                return parsedCart.map(function(item) {
                    return normalizeItem(item);
                }).filter(function(item) {
                    var validation = validateItem(item);
                    if (!validation.valid) {
                        console.warn('Invalid cart item removed:', validation.error, item);
                        return false;
                    }
                    return true;
                });
            } catch (e) {
                console.error('Error reading cart from localStorage:', e);
                // Clear corrupted cart data
                localStorage.removeItem(CART_STORAGE_KEY);
                return [];
            }
        },
        
        // Save cart to localStorage
        saveCart: function(cart) {
            if (!isLocalStorageAvailable()) {
                console.error('localStorage not available');
                return false;
            }
            
            try {
                // Validate cart is an array
                if (!Array.isArray(cart)) {
                    console.error('Cart must be an array');
                    return false;
                }
                
                // Normalize and validate all items
                var normalizedCart = cart.map(function(item) {
                    return normalizeItem(item);
                }).filter(function(item) {
                    var validation = validateItem(item);
                    if (!validation.valid) {
                        console.warn('Invalid item not saved:', validation.error, item);
                        return false;
                    }
                    return true;
                });
                
                localStorage.setItem(CART_STORAGE_KEY, JSON.stringify(normalizedCart));
                this.updateCartCounter();
                return true;
            } catch (e) {
                console.error('Error saving cart to localStorage:', e);
                
                // Handle quota exceeded error
                if (e.name === 'QuotaExceededError') {
                    alert('Cart storage is full. Please remove some items.');
                }
                return false;
            }
        },
        
        // Add item to cart
        addItem: function(item) {
            // Validate item
            var validation = validateItem(item);
            if (!validation.valid) {
                console.error('Cannot add invalid item:', validation.error);
                return false;
            }
            
            var cart = this.getCart();
            var normalizedItem = normalizeItem(item);
            
            // Check if item already exists
            var existingItemIndex = cart.findIndex(function(cartItem) {
                return String(cartItem.id) === String(normalizedItem.id) && 
                       String(cartItem.type) === String(normalizedItem.type);
            });
            
            if (existingItemIndex > -1) {
                // Update quantity if item exists
                var newQuantity = cart[existingItemIndex].quantity + normalizedItem.quantity;
                
                // Enforce max quantity
                if (newQuantity > MAX_QUANTITY) {
                    console.warn('Maximum quantity reached for item:', normalizedItem.name);
                    cart[existingItemIndex].quantity = MAX_QUANTITY;
                } else {
                    cart[existingItemIndex].quantity = newQuantity;
                }
            } else {
                // Add new item
                cart.push(normalizedItem);
            }
            
            return this.saveCart(cart);
        },
        
        // Remove item from cart
        removeItem: function(itemId, itemType) {
            if (!itemId || !itemType) {
                console.error('itemId and itemType are required');
                return false;
            }
            
            var cart = this.getCart();
            var originalLength = cart.length;
            
            cart = cart.filter(function(item) {
                return !(String(item.id) === String(itemId) && String(item.type) === String(itemType));
            });
            
            if (cart.length === originalLength) {
                console.warn('Item not found in cart:', itemId, itemType);
                return false;
            }
            
            return this.saveCart(cart);
        },
        
        // Update item quantity
        updateQuantity: function(itemId, itemType, newQuantity) {
            if (!itemId || !itemType) {
                console.error('itemId and itemType are required');
                return false;
            }
            
            // Validate and parse quantity
            newQuantity = parseInt(newQuantity);
            if (isNaN(newQuantity)) {
                console.error('Invalid quantity:', newQuantity);
                return false;
            }
            
            var cart = this.getCart();
            
            var itemIndex = cart.findIndex(function(item) {
                return String(item.id) === String(itemId) && String(item.type) === String(itemType);
            });
            
            if (itemIndex === -1) {
                console.warn('Item not found in cart:', itemId, itemType);
                return false;
            }
            
            // Handle quantity changes
            if (newQuantity <= 0) {
                // Remove item if quantity is 0 or less
                cart.splice(itemIndex, 1);
            } else if (newQuantity > MAX_QUANTITY) {
                // Enforce max quantity
                cart[itemIndex].quantity = MAX_QUANTITY;
                console.warn('Quantity capped at maximum:', MAX_QUANTITY);
            } else {
                // Update quantity
                cart[itemIndex].quantity = newQuantity;
            }
            
            return this.saveCart(cart);
        },
        
        // Get total items count
        getTotalItems: function() {
            var cart = this.getCart();
            return cart.reduce(function(sum, item) {
                return sum + (parseInt(item.quantity) || 0);
            }, 0);
        },
        
        // Get total price
        getTotalPrice: function() {
            var cart = this.getCart();
            return cart.reduce(function(sum, item) {
                var price = parseFloat(item.price) || 0;
                var quantity = parseInt(item.quantity) || 0;
                return sum + (price * quantity);
            }, 0);
        },
        
        // Clear cart
        clearCart: function() {
            if (!isLocalStorageAvailable()) {
                console.error('localStorage not available');
                return false;
            }
            
            try {
                localStorage.removeItem(CART_STORAGE_KEY);
                this.updateCartCounter();
                return true;
            } catch (e) {
                console.error('Error clearing cart:', e);
                return false;
            }
        },
        
        // Get item from cart
        getItem: function(itemId, itemType) {
            var cart = this.getCart();
            return cart.find(function(item) {
                return String(item.id) === String(itemId) && String(item.type) === String(itemType);
            });
        },
        
        // Check if item exists in cart
        hasItem: function(itemId, itemType) {
            return this.getItem(itemId, itemType) !== undefined;
        },
        
        // Update cart counter in navbar
        updateCartCounter: function() {
            var totalItems = this.getTotalItems();
            
            // Update various possible cart counter elements
            var selectors = [
                '.cart-counter',
                '.cart-badge', 
                '.badge',
                '#cart-count',
                '[data-cart-count]'
            ];
            
            selectors.forEach(function(selector) {
                var elements = document.querySelectorAll(selector);
                elements.forEach(function(element) {
                    element.textContent = totalItems;
                    if (totalItems > 0) {
                        element.style.display = 'inline';
                        element.setAttribute('aria-label', totalItems + ' items in cart');
                    } else {
                        element.style.display = 'none';
                        element.setAttribute('aria-label', 'Cart is empty');
                    }
                });
            });
            
            // Trigger custom event for cart update
            if (typeof CustomEvent !== 'undefined') {
                try {
                    var event = new CustomEvent('cartUpdated', {
                        detail: {
                            totalItems: totalItems,
                            totalPrice: this.getTotalPrice(),
                            cart: this.getCart()
                        }
                    });
                    document.dispatchEvent(event);
                } catch (e) {
                    console.error('Error dispatching cartUpdated event:', e);
                }
            }
        }
    };
    
    // Initialize cart counter when DOM is loaded
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', function() {
            CartManager.updateCartCounter();
        });
    } else {
        // DOM already loaded
        CartManager.updateCartCounter();
    }
    
    // Update cart counter when page becomes visible (for cross-tab sync)
    document.addEventListener('visibilitychange', function() {
        if (!document.hidden) {
            CartManager.updateCartCounter();
        }
    });
    
    // Listen for storage events (cross-tab sync)
    window.addEventListener('storage', function(e) {
        if (e.key === CART_STORAGE_KEY) {
            CartManager.updateCartCounter();
        }
    });
    
})();

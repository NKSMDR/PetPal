// Image Gallery Functions - Make it global
window.changeMainImage = function(imageUrl, thumbnailElement) {
    console.log('changeMainImage called with:', imageUrl);
    console.log('thumbnailElement:', thumbnailElement);
    
    const mainImage = document.getElementById('mainImage');
    console.log('mainImage element:', mainImage);
    
    if (mainImage && imageUrl) {
        console.log('Starting image change...');
        
        // Add loading effect
        mainImage.style.opacity = '0.5';
        mainImage.style.transition = 'opacity 0.3s ease';
        
        // Change image source
        mainImage.src = imageUrl;
        console.log('Image src set to:', mainImage.src);
        
        // Wait for image to load
        mainImage.onload = function() {
            mainImage.style.opacity = '1';
            console.log('Image loaded successfully');
        };
        
        // Handle load error
        mainImage.onerror = function() {
            console.error('Failed to load image:', imageUrl);
            mainImage.style.opacity = '1';
        };
        
        // Update active thumbnail
        document.querySelectorAll('.thumbnail-item').forEach(item => {
            item.classList.remove('active');
        });
        if (thumbnailElement) {
            thumbnailElement.classList.add('active');
            console.log('Active thumbnail updated');
        }
    } else {
        console.error('Missing mainImage or imageUrl:', {mainImage, imageUrl});
    }
};

// Alternative function for direct event binding
function switchImage(imageUrl, thumbnailElement) {
    return changeMainImage(imageUrl, thumbnailElement);
}

// Initialize thumbnail gallery functionality
function initializeThumbnailGallery() {
    console.log('Initializing thumbnail gallery...');
    
    // Get all thumbnail items
    const thumbnailItems = document.querySelectorAll('.thumbnail-item');
    console.log('Found thumbnail items:', thumbnailItems.length);
    
    // Add click event listeners to each thumbnail
    thumbnailItems.forEach((thumbnail, index) => {
        console.log(`Setting up thumbnail ${index + 1}`);
        
        // Get the image URL from data attribute
        const imageUrl = thumbnail.getAttribute('data-image');
        console.log(`Thumbnail ${index + 1} image URL:`, imageUrl);
        
        // Clear any existing onclick to avoid conflicts
        thumbnail.onclick = null;
        
        // Add new click event listener
        thumbnail.addEventListener('click', function(e) {
            e.preventDefault();
            e.stopPropagation();
            console.log(`Thumbnail ${index + 1} clicked, changing to:`, imageUrl);
            
            if (imageUrl) {
                changeMainImage(imageUrl, thumbnail);
            } else {
                console.error('No image URL found for thumbnail', thumbnail);
            }
        });
        
        // Add visual feedback
        thumbnail.style.cursor = 'pointer';
        thumbnail.title = 'Click to view this image';
        
        // Test if thumbnail is clickable
        thumbnail.addEventListener('mouseenter', function() {
            console.log(`Mouse entered thumbnail ${index + 1}`);
        });
    });
    
    // Also test the main image element and add click handler
    const mainImage = document.getElementById('mainImage');
    if (mainImage) {
        console.log('Main image found:', mainImage.src);
        
        // Add click handler for main image modal
        mainImage.addEventListener('click', function() {
            console.log('Main image clicked, opening modal');
            openImageModal(this.src, this.alt);
        });
    } else {
        console.error('Main image element not found!');
    }
}

// Thumbnail click handler function
function thumbnailClickHandler(e) {
    e.preventDefault();
    const thumbnail = e.currentTarget;
    const imageUrl = thumbnail.getAttribute('data-image');
    changeMainImage(imageUrl, thumbnail);
}

// Open image modal - Clean and simple - Make it global
window.openImageModal = function(imageSrc, imageAlt) {
    console.log('Opening modal with:', imageSrc);
    
    // Remove any existing modals first
    const existingModal = document.querySelector('.image-modal');
    if (existingModal) {
        existingModal.remove();
    }
    
    // Create modal for image zoom
    const modal = document.createElement('div');
    modal.className = 'image-modal';
    modal.innerHTML = `
        <div class="modal-content">
            <img src="${imageSrc}" alt="${imageAlt}">
            <button class="close-modal">&times;</button>
        </div>
    `;

    // Add to document
    document.body.appendChild(modal);

    // Show modal with animation
    setTimeout(() => {
        modal.classList.add('show');
    }, 10);

    // Close modal events
    const closeBtn = modal.querySelector('.close-modal');
    closeBtn.addEventListener('click', closeModal);
    modal.addEventListener('click', function(e) {
        if (e.target === modal) {
            closeModal();
        }
    });
    
    // Close on escape key
    document.addEventListener('keydown', function escapeHandler(e) {
        if (e.key === 'Escape') {
            closeModal();
            document.removeEventListener('keydown', escapeHandler);
        }
    });

    function closeModal() {
        modal.classList.remove('show');
        setTimeout(() => {
            if (modal.parentNode) {
                document.body.removeChild(modal);
            }
        }, 300);
    }
}

// Accessory Detail Page JavaScript
document.addEventListener('DOMContentLoaded', function() {
    console.log('DOM Content Loaded - Initializing accessory detail page...');
    
    // Initialize thumbnail gallery functionality
    initializeThumbnailGallery();
    
    // Add a test function to verify functionality
    window.testThumbnailClick = function() {
        const firstThumbnail = document.querySelector('.thumbnail-item[data-image]');
        if (firstThumbnail) {
            const imageUrl = firstThumbnail.getAttribute('data-image');
            console.log('Testing thumbnail click with URL:', imageUrl);
            changeMainImage(imageUrl, firstThumbnail);
        } else {
            console.error('No thumbnails found for testing');
        }
    };
    
    // Quantity controls
    const quantityInput = document.getElementById('quantity');
    const minusBtn = document.querySelector('.qty-btn.minus');
    const plusBtn = document.querySelector('.qty-btn.plus');

    if (minusBtn && plusBtn && quantityInput) {
        minusBtn.addEventListener('click', function() {
            let currentValue = parseInt(quantityInput.value);
            if (currentValue > 1) {
                quantityInput.value = currentValue - 1;
            }
        });

        plusBtn.addEventListener('click', function() {
            let currentValue = parseInt(quantityInput.value);
            if (currentValue < 10) {
                quantityInput.value = currentValue + 1;
            }
        });

        // Validate quantity input
        quantityInput.addEventListener('input', function() {
            let value = parseInt(this.value);
            if (isNaN(value) || value < 1) {
                this.value = 1;
            } else if (value > 10) {
                this.value = 10;
            }
        });
    }

    // Add smooth scroll animations
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };

    const observer = new IntersectionObserver(function(entries) {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.style.opacity = '1';
                entry.target.style.transform = 'translateY(0)';
            }
        });
    }, observerOptions);

    // Observe cards for animation
    document.querySelectorAll('.details-card, .sidebar-card').forEach(card => {
        card.style.opacity = '0';
        card.style.transform = 'translateY(30px)';
        card.style.transition = 'all 0.6s ease';
        observer.observe(card);
    });

    // Add to cart functionality
    window.addToCart = function(productType, productId) {
        const quantityInputElement = document.getElementById('quantity');
        const quantity = parseInt(quantityInputElement ? quantityInputElement.value : 1) || 1;
        const button = document.querySelector('.add-to-cart-btn');
        
        // Show loading state
        const originalText = button.innerHTML;
        button.innerHTML = '<i class="fas fa-spinner fa-spin me-2"></i>Adding...';
        button.disabled = true;

        // Simulate API call (replace with actual implementation)
        setTimeout(() => {
            // Success feedback
            button.innerHTML = '<i class="fas fa-check me-2"></i>Added to Cart!';
            button.style.background = '#48bb78';
            
            // Reset button after 2 seconds
            setTimeout(() => {
                button.innerHTML = originalText;
                button.style.background = '#ffd700';
                button.disabled = false;
            }, 2000);

            // Show success message
            showNotification('Product added to cart successfully!', 'success');
        }, 1000);
    };

    // Notification system
    function showNotification(message, type = 'info') {
        const notification = document.createElement('div');
        notification.className = `notification notification-${type}`;
        notification.innerHTML = `
            <i class="fas fa-${type === 'success' ? 'check-circle' : 'info-circle'} me-2"></i>
            ${message}
        `;
        
        // Add styles
        notification.style.cssText = `
            position: fixed;
            top: 20px;
            right: 20px;
            background: ${type === 'success' ? '#48bb78' : '#667eea'};
            color: white;
            padding: 15px 20px;
            border-radius: 10px;
            box-shadow: 0 4px 15px rgba(0,0,0,0.2);
            z-index: 9999;
            transform: translateX(100%);
            transition: transform 0.3s ease;
        `;

        document.body.appendChild(notification);

        // Animate in
        setTimeout(() => {
            notification.style.transform = 'translateX(0)';
        }, 100);

        // Remove after 3 seconds
        setTimeout(() => {
            notification.style.transform = 'translateX(100%)';
            setTimeout(() => {
                document.body.removeChild(notification);
            }, 300);
        }, 3000);
    }
});

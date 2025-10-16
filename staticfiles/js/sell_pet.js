// Form submission handling
document.addEventListener('DOMContentLoaded', function() {
    // Handle form submission
    const form = document.getElementById('pet-form');
    const submitBtn = document.getElementById('submit-btn');
    
    if (form && submitBtn) {
        form.addEventListener('submit', function(e) {
            console.log('Form submitted');
            
            // Show loading state
            submitBtn.disabled = true;
            submitBtn.innerHTML = '<i class="fas fa-spinner fa-spin me-2"></i>Submitting...';
            
            // Let the form submit normally - don't prevent default
            // The disabled state and loading text will show until page reloads/redirects
        });
    }
});

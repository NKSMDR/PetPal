// login.js

// Password toggle functionality
function togglePassword() {
    const passwordField = document.getElementById('password');
    const toggleIcon = document.getElementById('toggleIcon');
    
    if (passwordField.type === 'password') {
        passwordField.type = 'text';
        toggleIcon.classList.remove('fa-eye');
        toggleIcon.classList.add('fa-eye-slash');
    } else {
        passwordField.type = 'password';
        toggleIcon.classList.remove('fa-eye-slash');
        toggleIcon.classList.add('fa-eye');
    }
}

// Form validation
document.addEventListener('DOMContentLoaded', function() {
    const loginForm = document.querySelector('.login-form');
    const emailInput = document.getElementById('email');
    const passwordInput = document.getElementById('password');
    
    // Add input event listeners for real-time validation
    emailInput.addEventListener('input', validateEmail);
    passwordInput.addEventListener('input', validatePassword);
    
    // Form submit handler
    loginForm.addEventListener('submit', function(e) {
        if (!validateForm()) {
            e.preventDefault();
        }
    });
});

// Email validation
function validateEmail() {
    const emailInput = document.getElementById('email');
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    
    if (emailInput.value && !emailRegex.test(emailInput.value)) {
        emailInput.classList.add('is-invalid');
        showError(emailInput, 'Please enter a valid email address');
        return false;
    } else {
        emailInput.classList.remove('is-invalid');
        emailInput.classList.add('is-valid');
        hideError(emailInput);
        return true;
    }
}

// Password validation
function validatePassword() {
    const passwordInput = document.getElementById('password');
    
    if (passwordInput.value && passwordInput.value.length < 6) {
        passwordInput.classList.add('is-invalid');
        showError(passwordInput, 'Password must be at least 6 characters');
        return false;
    } else if (passwordInput.value) {
        passwordInput.classList.remove('is-invalid');
        passwordInput.classList.add('is-valid');
        hideError(passwordInput);
        return true;
    }
    return true;
}

// Full form validation
function validateForm() {
    const emailValid = validateEmail();
    const passwordValid = validatePassword();
    const emailInput = document.getElementById('email');
    const passwordInput = document.getElementById('password');
    
    // Check if fields are empty
    if (!emailInput.value) {
        showError(emailInput, 'Email is required');
        return false;
    }
    
    if (!passwordInput.value) {
        showError(passwordInput, 'Password is required');
        return false;
    }
    
    return emailValid && passwordValid;
}

// Show error message
function showError(input, message) {
    hideError(input); // Remove existing error first
    
    const errorDiv = document.createElement('div');
    errorDiv.className = 'invalid-feedback';
    errorDiv.textContent = message;
    
    input.parentNode.appendChild(errorDiv);
}

// Hide error message
function hideError(input) {
    const existingError = input.parentNode.querySelector('.invalid-feedback');
    if (existingError) {
        existingError.remove();
    }
}

// Add loading state to login button
function showLoading() {
    const loginBtn = document.querySelector('.login-btn');
    const originalText = loginBtn.innerHTML;
    
    loginBtn.innerHTML = '<i class="fas fa-spinner fa-spin me-2"></i>Signing In...';
    loginBtn.disabled = true;
    
    // Reset after 3 seconds (remove this in production)
    setTimeout(() => {
        loginBtn.innerHTML = originalText;
        loginBtn.disabled = false;
    }, 3000);
}

// Handle social login buttons
document.addEventListener('DOMContentLoaded', function() {
    const socialBtns = document.querySelectorAll('.social-btn');
    
    socialBtns.forEach(btn => {
        btn.addEventListener('click', function(e) {
            e.preventDefault();
            const provider = this.textContent.includes('Google') ? 'Google' : 'Facebook';
            console.log(`${provider} login clicked`);
            // Add your social login logic here
        });
    });
});

// Add smooth focus effects
document.addEventListener('DOMContentLoaded', function() {
    const inputs = document.querySelectorAll('.form-control');
    
    inputs.forEach(input => {
        input.addEventListener('focus', function() {
            this.parentNode.style.transform = 'scale(1.02)';
        });
        
        input.addEventListener('blur', function() {
            this.parentNode.style.transform = 'scale(1)';
        });
    });
});
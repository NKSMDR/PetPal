// register.js

// Password toggle functionality
function togglePassword(fieldId, iconId) {
    const passwordField = document.getElementById(fieldId);
    const toggleIcon = document.getElementById(iconId);
    
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

// Form validation and initialization
document.addEventListener('DOMContentLoaded', function() {
    const registerForm = document.querySelector('.register-form');
    const inputs = {
        firstName: document.getElementById('firstName'),
        lastName: document.getElementById('lastName'),
        email: document.getElementById('email'),
        phone: document.getElementById('phone'),
        password: document.getElementById('password'),
        confirmPassword: document.getElementById('confirmPassword'),
        userType: document.getElementById('userType'),
        terms: document.getElementById('terms')
    };
    
    // Add password strength indicator
    addPasswordStrengthIndicator();
    
    // Add input event listeners
    inputs.firstName.addEventListener('input', () => validateName(inputs.firstName, 'First name'));
    inputs.lastName.addEventListener('input', () => validateName(inputs.lastName, 'Last name'));
    inputs.email.addEventListener('input', validateEmail);
    inputs.phone.addEventListener('input', validatePhone);
    inputs.password.addEventListener('input', validatePassword);
    inputs.confirmPassword.addEventListener('input', validateConfirmPassword);
    
    // Form submit handler
    registerForm.addEventListener('submit', function(e) {
        if (!validateForm()) {
            e.preventDefault();
        }
    });
    
    // Social register buttons
    const socialBtns = document.querySelectorAll('.social-btn');
    socialBtns.forEach(btn => {
        btn.addEventListener('click', function(e) {
            e.preventDefault();
            const provider = this.textContent.includes('Google') ? 'Google' : 'Facebook';
            console.log(`${provider} register clicked`);
        });
    });
});

// Add password strength indicator
function addPasswordStrengthIndicator() {
    const passwordField = document.getElementById('password');
    const strengthIndicator = document.createElement('div');
    strengthIndicator.className = 'password-strength';
    strengthIndicator.innerHTML = '<div class="password-strength-bar"></div>';
    
    passwordField.parentNode.parentNode.appendChild(strengthIndicator);
}

// Name validation
function validateName(input, fieldName) {
    const value = input.value.trim();
    
    if (value.length < 2) {
        input.classList.add('is-invalid');
        input.classList.remove('is-valid');
        showError(input, `${fieldName} must be at least 2 characters`);
        return false;
    } else if (!/^[a-zA-Z\s]+$/.test(value)) {
        input.classList.add('is-invalid');
        input.classList.remove('is-valid');
        showError(input, `${fieldName} can only contain letters`);
        return false;
    } else {
        input.classList.remove('is-invalid');
        input.classList.add('is-valid');
        hideError(input);
        return true;
    }
}

// Email validation
function validateEmail() {
    const emailInput = document.getElementById('email');
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    const value = emailInput.value.trim();
    
    if (!value) {
        emailInput.classList.remove('is-invalid', 'is-valid');
        hideError(emailInput);
        return false;
    } else if (!emailRegex.test(value)) {
        emailInput.classList.add('is-invalid');
        emailInput.classList.remove('is-valid');
        showError(emailInput, 'Please enter a valid email address');
        return false;
    } else {
        emailInput.classList.remove('is-invalid');
        emailInput.classList.add('is-valid');
        hideError(emailInput);
        return true;
    }
}

// Phone validation
function validatePhone() {
    const phoneInput = document.getElementById('phone');
    const phoneRegex = /^[\+]?[1-9][\d]{0,15}$/;
    const value = phoneInput.value.replace(/\s+/g, '');
    
    if (!value) {
        phoneInput.classList.remove('is-invalid', 'is-valid');
        hideError(phoneInput);
        return false;
    } else if (value.length < 10 || !phoneRegex.test(value)) {
        phoneInput.classList.add('is-invalid');
        phoneInput.classList.remove('is-valid');
        showError(phoneInput, 'Please enter a valid phone number');
        return false;
    } else {
        phoneInput.classList.remove('is-invalid');
        phoneInput.classList.add('is-valid');
        hideError(phoneInput);
        return true;
    }
}

// Password validation with strength indicator
function validatePassword() {
    const passwordInput = document.getElementById('password');
    const value = passwordInput.value;
    const strengthBar = document.querySelector('.password-strength-bar');
    
    if (!value) {
        passwordInput.classList.remove('is-invalid', 'is-valid');
        hideError(passwordInput);
        updatePasswordStrength('', strengthBar);
        return false;
    }
    
    const strength = calculatePasswordStrength(value);
    updatePasswordStrength(strength, strengthBar);
    
    if (value.length < 8) {
        passwordInput.classList.add('is-invalid');
        passwordInput.classList.remove('is-valid');
        showError(passwordInput, 'Password must be at least 8 characters long');
        return false;
    } else if (strength === 'weak') {
        passwordInput.classList.add('is-invalid');
        passwordInput.classList.remove('is-valid');
        showError(passwordInput, 'Password is too weak');
        return false;
    } else {
        passwordInput.classList.remove('is-invalid');
        passwordInput.classList.add('is-valid');
        hideError(passwordInput);
        
        // Revalidate confirm password if it has a value
        const confirmPassword = document.getElementById('confirmPassword');
        if (confirmPassword.value) {
            validateConfirmPassword();
        }
        
        return true;
    }
}

// Calculate password strength
function calculatePasswordStrength(password) {
    let score = 0;
    
    // Length
    if (password.length >= 8) score += 1;
    if (password.length >= 12) score += 1;
    
    // Character types
    if (/[a-z]/.test(password)) score += 1;
    if (/[A-Z]/.test(password)) score += 1;
    if (/[0-9]/.test(password)) score += 1;
    if (/[^A-Za-z0-9]/.test(password)) score += 1;
    
    if (score <= 2) return 'weak';
    if (score <= 3) return 'fair';
    if (score <= 4) return 'good';
    return 'strong';
}

// Update password strength indicator
function updatePasswordStrength(strength, strengthBar) {
    strengthBar.className = 'password-strength-bar';
    
    if (strength) {
        strengthBar.classList.add(`strength-${strength}`);
    }
}

// Confirm password validation
function validateConfirmPassword() {
    const passwordInput = document.getElementById('password');
    const confirmPasswordInput = document.getElementById('confirmPassword');
    const value = confirmPasswordInput.value;
    
    if (!value) {
        confirmPasswordInput.classList.remove('is-invalid', 'is-valid');
        hideError(confirmPasswordInput);
        return false;
    } else if (value !== passwordInput.value) {
        confirmPasswordInput.classList.add('is-invalid');
        confirmPasswordInput.classList.remove('is-valid');
        showError(confirmPasswordInput, 'Passwords do not match');
        return false;
    } else {
        confirmPasswordInput.classList.remove('is-invalid');
        confirmPasswordInput.classList.add('is-valid');
        hideError(confirmPasswordInput);
        return true;
    }
}

// Full form validation
function validateForm() {
    const inputs = {
        firstName: document.getElementById('firstName'),
        lastName: document.getElementById('lastName'),
        email: document.getElementById('email'),
        phone: document.getElementById('phone'),
        password: document.getElementById('password'),
        confirmPassword: document.getElementById('confirmPassword'),
        userType: document.getElementById('userType'),
        terms: document.getElementById('terms')
    };
    
    let isValid = true;
    
    // Validate all fields
    if (!inputs.firstName.value.trim()) {
        showError(inputs.firstName, 'First name is required');
        isValid = false;
    } else {
        isValid = validateName(inputs.firstName, 'First name') && isValid;
    }
    
    if (!inputs.lastName.value.trim()) {
        showError(inputs.lastName, 'Last name is required');
        isValid = false;
    } else {
        isValid = validateName(inputs.lastName, 'Last name') && isValid;
    }
    
    if (!inputs.email.value.trim()) {
        showError(inputs.email, 'Email is required');
        isValid = false;
    } else {
        isValid = validateEmail() && isValid;
    }
    
    if (!inputs.phone.value.trim()) {
        showError(inputs.phone, 'Phone number is required');
        isValid = false;
    } else {
        isValid = validatePhone() && isValid;
    }
    
    if (!inputs.password.value) {
        showError(inputs.password, 'Password is required');
        isValid = false;
    } else {
        isValid = validatePassword() && isValid;
    }
    
    if (!inputs.confirmPassword.value) {
        showError(inputs.confirmPassword, 'Please confirm your password');
        isValid = false;
    } else {
        isValid = validateConfirmPassword() && isValid;
    }
    
    if (!inputs.userType.value) {
        showError(inputs.userType, 'Please select your main interest');
        isValid = false;
    }
    
    if (!inputs.terms.checked) {
        showError(inputs.terms, 'Please agree to the terms and conditions');
        isValid = false;
    }
    
    return isValid;
}

// Show error message
function showError(input, message) {
    hideError(input);
    
    const errorDiv = document.createElement('div');
    errorDiv.className = 'invalid-feedback';
    errorDiv.textContent = message;
    
    if (input.type === 'checkbox') {
        input.parentNode.parentNode.appendChild(errorDiv);
    } else {
        input.parentNode.parentNode.appendChild(errorDiv);
    }
}

// Hide error message
function hideError(input) {
    let container = input.parentNode.parentNode;
    if (input.type === 'checkbox') {
        container = input.parentNode.parentNode;
    }
    
    const existingError = container.querySelector('.invalid-feedback');
    if (existingError) {
        existingError.remove();
    }
}

// Add loading state to register button
function showLoading() {
    const registerBtn = document.querySelector('.register-btn');
    const originalText = registerBtn.innerHTML;
    
    registerBtn.innerHTML = '<i class="fas fa-spinner fa-spin me-2"></i>Creating Account...';
    registerBtn.disabled = true;
    
    // Reset after 3 seconds (remove this in production)
    setTimeout(() => {
        registerBtn.innerHTML = originalText;
        registerBtn.disabled = false;
    }, 3000);
}
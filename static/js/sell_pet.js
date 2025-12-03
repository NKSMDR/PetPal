// Form submission handling
document.addEventListener('DOMContentLoaded', function () {
    // Handle form submission
    const form = document.getElementById('pet-form');
    const submitBtn = document.getElementById('submit-btn');
    const confirmCheckbox = document.getElementById('confirmSubmission');

    if (form && submitBtn && confirmCheckbox) {
        form.addEventListener('submit', function (e) {
            console.log('Form submitted');

            // Check if confirmation checkbox is checked
            if (!confirmCheckbox.checked) {
                e.preventDefault();
                alert('Please check the confirmation checkbox to agree with the terms before submitting.');

                // Scroll to the checkbox
                confirmCheckbox.scrollIntoView({ behavior: 'smooth', block: 'center' });

                // Highlight the checkbox area
                const checkboxCard = confirmCheckbox.closest('.card');
                if (checkboxCard) {
                    checkboxCard.style.border = '2px solid red';
                    setTimeout(function () {
                        checkboxCard.style.border = '';
                    }, 3000);
                }

                return false;
            }

            // Show loading state
            submitBtn.disabled = true;
            submitBtn.innerHTML = '<i class="fas fa-spinner fa-spin me-2"></i>Submitting...';

            // Let the form submit normally
        });
    }
});

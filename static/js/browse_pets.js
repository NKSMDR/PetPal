// Browse Pets Filter Functionality

document.addEventListener('DOMContentLoaded', function () {
    const filterForm = document.getElementById('filterForm');
    const clearBtn = document.getElementById('clearFilters');
    const breedSelect = document.getElementById('breed');
    const ageInput = document.getElementById('age');
    const searchInput = document.getElementById('search');
    const minPriceInput = document.getElementById('min_price');
    const maxPriceInput = document.getElementById('max_price');

    // Auto-submit on dropdown change
    if (breedSelect) {
        breedSelect.addEventListener('change', function () {
            filterForm.submit();
        });
    }

    // Clear filters functionality - redirect to clean URL
    if (clearBtn) {
        clearBtn.addEventListener('click', function (e) {
            e.preventDefault();
            window.location.href = window.location.pathname;
        });
    }

    // Validate price range
    if (filterForm) {
        filterForm.addEventListener('submit', function (e) {
            const minPrice = parseFloat(minPriceInput.value);
            const maxPrice = parseFloat(maxPriceInput.value);

            if (minPrice && maxPrice && minPrice > maxPrice) {
                e.preventDefault();
                alert('Minimum price cannot be greater than maximum price!');
                minPriceInput.focus();
            }
        });
    }

    // Handle Enter key in all inputs
    const inputs = [searchInput, ageInput, minPriceInput, maxPriceInput];
    inputs.forEach(input => {
        if (input) {
            input.addEventListener('keypress', function (e) {
                if (e.key === 'Enter') {
                    e.preventDefault();
                    filterForm.submit();
                }
            });
        }
    });

    // Price validation feedback
    function validatePriceRange() {
        const min = parseFloat(minPriceInput.value) || 0;
        const max = parseFloat(maxPriceInput.value) || Infinity;

        if (min > max && max !== Infinity) {
            maxPriceInput.setCustomValidity('Max price must be greater than min price');
        } else {
            maxPriceInput.setCustomValidity('');
        }
    }

    if (minPriceInput && maxPriceInput) {
        minPriceInput.addEventListener('input', validatePriceRange);
        maxPriceInput.addEventListener('input', validatePriceRange);
    }
});

// Simple map initialization - following your working about page pattern
let map;
let marker = null;

// Form submission handling
document.addEventListener('DOMContentLoaded', function() {
    // Initialize map first
    setTimeout(() => {
        initializeMap();
    }, 500);

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

function initializeMap() {
    console.log('Initializing map...');
    
    // Initialize map - simple and direct like your about page
    map = L.map('location-map').setView([27.7172, 85.3240], 13); // Default to Kathmandu, Nepal
    
    // Add tile layer
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '© OpenStreetMap contributors'
    }).addTo(map);

    console.log('Map initialized');

    // Get form fields using simple selectors
    const latField = document.querySelector('input[name="latitude"]');
    const lngField = document.querySelector('input[name="longitude"]');
    const addressField = document.querySelector('input[name="address"]') || document.querySelector('textarea[name="address"]');
    const cityField = document.querySelector('input[name="city"]');
    const stateField = document.querySelector('input[name="state"]');
    const searchInput = document.getElementById('location-search');
    const searchBtn = document.getElementById('search-btn');
    const currentLocationBtn = document.getElementById('current-location-btn');

    console.log('Form fields found:', {
        latField: !!latField,
        lngField: !!lngField,
        addressField: !!addressField,
        cityField: !!cityField,
        stateField: !!stateField
    });

    // Function to update location
    function updateLocation(lat, lng, address = '') {
        console.log(`Updating location: ${lat}, ${lng}`);
        
        // Update marker
        if (marker) {
            map.removeLayer(marker);
        }
        marker = L.marker([lat, lng]).addTo(map);
        
        // Update form fields
        if (latField) latField.value = lat.toFixed(8);
        if (lngField) lngField.value = lng.toFixed(8);
        
        // Reverse geocode to get address
        if (!address) {
            fetch(`https://nominatim.openstreetmap.org/reverse?format=json&lat=${lat}&lon=${lng}`)
                .then(response => response.json())
                .then(data => {
                    if (data && data.display_name) {
                        if (addressField) addressField.value = data.display_name;
                        
                        // Extract city and state
                        const addressParts = data.address || {};
                        const city = addressParts.city || addressParts.town || addressParts.village || addressParts.suburb || '';
                        const state = addressParts.state || addressParts.region || '';
                        
                        if (city && cityField) cityField.value = city;
                        if (state && stateField) stateField.value = state;
                        
                        console.log('Address updated:', data.display_name);
                    }
                })
                .catch(error => {
                    console.error('Reverse geocoding error:', error);
                    if (addressField) addressField.value = `Location: ${lat.toFixed(6)}, ${lng.toFixed(6)}`;
                });
        } else {
            if (addressField) addressField.value = address;
        }
    }

    // Map click event
    map.on('click', function(e) {
        const lat = e.latlng.lat;
        const lng = e.latlng.lng;
        updateLocation(lat, lng);
    });

    // Search functionality
    function performSearch() {
        const query = searchInput ? searchInput.value.trim() : '';
        if (!query) {
            alert('Please enter a location to search');
            return;
        }

        if (searchBtn) {
            searchBtn.disabled = true;
            searchBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i>';
        }

        fetch(`https://nominatim.openstreetmap.org/search?format=json&q=${encodeURIComponent(query)}&limit=1`)
            .then(response => response.json())
            .then(data => {
                if (data && data.length > 0) {
                    const result = data[0];
                    const lat = parseFloat(result.lat);
                    const lng = parseFloat(result.lon);
                    
                    map.setView([lat, lng], 15);
                    updateLocation(lat, lng, result.display_name);
                } else {
                    alert('Location not found. Please try a different search term.');
                }
            })
            .catch(error => {
                console.error('Search error:', error);
                alert('Search failed. Please try again.');
            })
            .finally(() => {
                if (searchBtn) {
                    searchBtn.disabled = false;
                    searchBtn.innerHTML = '<i class="fas fa-search"></i>';
                }
            });
    }

    // Search button click
    if (searchBtn) {
        searchBtn.addEventListener('click', performSearch);
    }

    // Search on Enter key
    if (searchInput) {
        searchInput.addEventListener('keypress', function(e) {
            if (e.key === 'Enter') {
                e.preventDefault();
                performSearch();
            }
        });
    }

    // Current location button
    if (currentLocationBtn) {
        currentLocationBtn.addEventListener('click', function() {
            if (!navigator.geolocation) {
                alert('Geolocation is not supported by this browser.');
                return;
            }
            
            currentLocationBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Getting Location...';
            currentLocationBtn.disabled = true;
            
            navigator.geolocation.getCurrentPosition(
                function(position) {
                    const lat = position.coords.latitude;
                    const lng = position.coords.longitude;
                    
                    map.setView([lat, lng], 15);
                    updateLocation(lat, lng);
                    
                    currentLocationBtn.innerHTML = '<i class="fas fa-location-arrow"></i> Use Current Location';
                    currentLocationBtn.disabled = false;
                },
                function(error) {
                    console.error('Geolocation error:', error);
                    alert('Unable to get your current location. Please search manually or click on the map.');
                    currentLocationBtn.innerHTML = '<i class="fas fa-location-arrow"></i> Use Current Location';
                    currentLocationBtn.disabled = false;
                }
            );
        });
    }

    // Load existing location if editing
    const existingLat = latField ? latField.value : '';
    const existingLng = lngField ? lngField.value : '';
    if (existingLat && existingLng && !isNaN(existingLat) && !isNaN(existingLng)) {
        const lat = parseFloat(existingLat);
        const lng = parseFloat(existingLng);
        console.log(`Loading existing location: ${lat}, ${lng}`);
        map.setView([lat, lng], 15);
        marker = L.marker([lat, lng]).addTo(map);
    }
}

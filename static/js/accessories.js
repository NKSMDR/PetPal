document.addEventListener("DOMContentLoaded", function() {
  console.log("Price slider script loaded");
  
  // Simple direct approach - no delays
  const minSlider = document.getElementById("min-price-range");
  const maxSlider = document.getElementById("max-price-range");
  const minDisplay = document.getElementById("min-price-display");
  const maxDisplay = document.getElementById("max-price-display");
  const sliderRange = document.getElementById("slider-range");

  console.log("Elements found:", {
    minSlider: !!minSlider,
    maxSlider: !!maxSlider,
    minDisplay: !!minDisplay,
    maxDisplay: !!maxDisplay,
    sliderRange: !!sliderRange
  });

  function updateDisplay() {
    if (!minSlider || !maxSlider) {
      console.log("Sliders not found, cannot update display");
      return;
    }
    
    const minVal = parseInt(minSlider.value);
    const maxVal = parseInt(maxSlider.value);
    
    console.log("Updating display with values:", minVal, maxVal);
    
    // Update price displays immediately
    if (minDisplay) {
      minDisplay.innerHTML = minVal;
      console.log("Updated min display to:", minVal);
    } else {
      console.log("Min display element not found");
    }
    
    if (maxDisplay) {
      maxDisplay.innerHTML = maxVal;
      console.log("Updated max display to:", maxVal);
    } else {
      console.log("Max display element not found");
    }
    
    // Update visual range bar
    updateSliderRange();
  }

  function updateSliderRange() {
    if (!minSlider || !maxSlider || !sliderRange) return;
    
    const minVal = parseInt(minSlider.value);
    const maxVal = parseInt(maxSlider.value);
    const minPrice = parseInt(minSlider.min);
    const maxPrice = parseInt(minSlider.max);
    
    // Calculate percentages for positioning
    const minPercent = ((minVal - minPrice) / (maxPrice - minPrice)) * 100;
    const maxPercent = ((maxVal - minPrice) / (maxPrice - minPrice)) * 100;
    
    // Update the orange range bar
    sliderRange.style.left = minPercent + '%';
    sliderRange.style.width = (maxPercent - minPercent) + '%';
  }

  if (minSlider && maxSlider) {
    console.log("Setting up event listeners");
    
    // Initialize displays
    updateDisplay();
    
    // Real-time updates for min slider
    minSlider.addEventListener('input', function() {
      console.log("Min slider changed to:", this.value);
      updateDisplay();
    });

    // Real-time updates for max slider
    maxSlider.addEventListener('input', function() {
      console.log("Max slider changed to:", this.value);
      updateDisplay();
    });

    // Also listen for 'change' events for better compatibility
    minSlider.addEventListener('change', function() {
      console.log("Min slider change event:", this.value);
      updateDisplay();
    });
    
    maxSlider.addEventListener('change', function() {
      console.log("Max slider change event:", this.value);
      updateDisplay();
    });
    
  } else {
    console.log("Sliders not found, cannot set up event listeners");
  }
});
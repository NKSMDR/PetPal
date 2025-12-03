// Price slider functionality - wrapped in IIFE to avoid conflicts
(function() {
  'use strict';
  
  console.log("🎚️ Price slider script loading...");
  
  function initPriceSlider() {
    const minSlider = document.getElementById("min-price-range");
    const maxSlider = document.getElementById("max-price-range");
    const minDisplay = document.getElementById("min-price-display");
    const maxDisplay = document.getElementById("max-price-display");
    const sliderRange = document.getElementById("slider-range");

    console.log("🔍 Elements found:", {
      minSlider: !!minSlider,
      maxSlider: !!maxSlider,
      minDisplay: !!minDisplay,
      maxDisplay: !!maxDisplay,
      sliderRange: !!sliderRange
    });

    if (!minSlider || !maxSlider || !minDisplay || !maxDisplay) {
      console.error("❌ Required slider elements not found!");
      return;
    }

    // Get min/max values for range calculation
    const minValue = parseInt(minSlider.min);
    const maxValue = parseInt(minSlider.max);
    
    console.log("📊 Price range:", minValue, "to", maxValue);

    function updateDisplay() {
      let minVal = parseInt(minSlider.value);
      let maxVal = parseInt(maxSlider.value);
      
      // Prevent sliders from crossing
      if (minVal >= maxVal) {
        minVal = maxVal - 1;
        if (minVal < minValue) {
          minVal = minValue;
        }
        minSlider.value = minVal;
      }
      
      console.log("🔄 Updating prices: NRS", minVal, "- NRS", maxVal);
      
      // Update the text display
      minDisplay.textContent = minVal;
      maxDisplay.textContent = maxVal;
      
      // Verify the update worked
      console.log("✅ Display now shows:", minDisplay.textContent, "-", maxDisplay.textContent);
      
      // Update visual range bar
      updateSliderRange();
    }

    function updateSliderRange() {
      if (!sliderRange) return;
      
      const minVal = parseInt(minSlider.value);
      const maxVal = parseInt(maxSlider.value);
      
      // Calculate percentages for positioning
      const minPercent = ((minVal - minValue) / (maxValue - minValue)) * 100;
      const maxPercent = ((maxVal - minValue) / (maxValue - minValue)) * 100;
      
      // Update the orange range bar
      sliderRange.style.left = minPercent + '%';
      sliderRange.style.width = (maxPercent - minPercent) + '%';
    }

    // Initialize displays immediately
    updateDisplay();
    
    // Add event listeners for real-time updates
    minSlider.addEventListener('input', function() {
      console.log("🎚️ MIN slider moved to:", this.value);
      updateDisplay();
    });
    
    maxSlider.addEventListener('input', function() {
      console.log("🎚️ MAX slider moved to:", this.value);
      updateDisplay();
    });
    
    // Backup listeners for better compatibility
    minSlider.addEventListener('change', updateDisplay);
    maxSlider.addEventListener('change', updateDisplay);
    
    console.log("✅ Price slider initialized successfully!");
  }

  // Wait for DOM to be ready
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initPriceSlider);
  } else {
    // DOM is already ready
    initPriceSlider();
  }
  
  // Fallback initialization after delay
  setTimeout(function() {
    const minDisplay = document.getElementById("min-price-display");
    if (minDisplay && minDisplay.textContent.includes('price_min')) {
      console.log("⚠️ Retrying initialization...");
      initPriceSlider();
    }
  }, 300);
})();
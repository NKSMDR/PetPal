document.addEventListener("DOMContentLoaded", function () {
  const slider = document.getElementById("custom-slider-range");
  const minInput = document.getElementById("price_min_input");
  const maxInput = document.getElementById("price_max_input");
  const minDisplay = document.getElementById("min-price-slider");
  const maxDisplay = document.getElementById("max-price-slider");

  const minVal = parseInt(minInput.value) || 0;
  const maxVal = parseInt(maxInput.value) || 1000;
  const minPrice = parseInt(slider.getAttribute("data-min")) || 0;
  const maxPrice = parseInt(slider.getAttribute("data-max")) || 1000;

  if (slider && typeof noUiSlider !== "undefined") {
    noUiSlider.create(slider, {
      start: [minVal, maxVal],
      connect: true,
      step: 1,
      range: {
        min: minPrice,
        max: maxPrice
      },
      tooltips: [true, true],
      format: {
        to: function (value) { return Math.round(value); },
        from: function (value) { return Number(value); }
      }
    });

    slider.noUiSlider.on("update", function (values, handle) {
      const val0 = parseInt(values[0]);
      const val1 = parseInt(values[1]);
      minInput.value = val0;
      maxInput.value = val1;
      minDisplay.textContent = val0;
      maxDisplay.textContent = val1;
    });
  }
});
// detail.js
console.log("detail.js loaded ✅");
// Smooth scroll to top when loading the breed detail page
window.addEventListener('load', () => {
  window.scrollTo({ top: 0, behavior: 'smooth' });
});

// Animate trait cards on scroll into view
const cards = document.querySelectorAll('.trait-card');

const observer = new IntersectionObserver((entries) => {
  entries.forEach(entry => {
    if (entry.isIntersecting) {
      entry.target.classList.add('trait-visible');
    }
  });
}, {
  threshold: 0.2
});

cards.forEach(card => observer.observe(card));

// Optional: Highlight active filter fields
document.querySelectorAll('.form-select').forEach(select => {
  select.addEventListener('change', function () {
    if (this.value) {
      this.classList.add('active-filter');
    } else {
      this.classList.remove('active-filter');
    }
  });
});
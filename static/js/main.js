/**
 * AgriSense AI – Main JavaScript
 * Theme toggle, counter animations, status check
 */

'use strict';

// ── Theme Toggle ─────────────────────────────────────────────────
(function initTheme() {
  const saved = localStorage.getItem('agri-theme') || 'dark';
  document.documentElement.setAttribute('data-bs-theme', saved);
  updateThemeIcon(saved);
})();

document.addEventListener('DOMContentLoaded', function () {

  // Theme toggle button
  const toggleBtn = document.getElementById('theme-toggle');
  const themeIcon = document.getElementById('theme-icon');

  if (toggleBtn) {
    toggleBtn.addEventListener('click', function () {
      const current = document.documentElement.getAttribute('data-bs-theme');
      const next = current === 'dark' ? 'light' : 'dark';
      document.documentElement.setAttribute('data-bs-theme', next);
      localStorage.setItem('agri-theme', next);
      updateThemeIcon(next);
    });
  }

  // ── Counter Animations ────────────────────────────────────────
  const counters = document.querySelectorAll('.counter');
  if (counters.length > 0) {
    const observer = new IntersectionObserver((entries) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          animateCounter(entry.target);
          observer.unobserve(entry.target);
        }
      });
    }, { threshold: 0.5 });
    counters.forEach(c => observer.observe(c));
  }

  // ── API Status Check ──────────────────────────────────────────
  checkApiStatus();

  // ── Scroll animations (fade-in on scroll) ─────────────────────
  initScrollAnimations();

});

function updateThemeIcon(theme) {
  const icon = document.getElementById('theme-icon');
  if (icon) {
    icon.className = theme === 'dark' ? 'bi bi-sun-fill' : 'bi bi-moon-fill';
  }
}

function animateCounter(el) {
  const target = parseInt(el.dataset.target, 10);
  const duration = 1500;
  const step = (target / duration) * 16;
  let current = 0;

  function update() {
    current = Math.min(current + step, target);
    el.textContent = Math.floor(current) + (target >= 100 ? '+' : (target > 10 ? '+' : ''));
    if (current < target) requestAnimationFrame(update);
  }
  requestAnimationFrame(update);
}

function checkApiStatus() {
  const badge = document.getElementById('status-badge');
  const statusText = badge ? badge.querySelector('.status-text') : null;
  const modelMode = document.getElementById('model-mode');
  const modelName = document.getElementById('model-name');

  fetch('/api/status')
    .then(res => res.json())
    .then(data => {
      if (badge && statusText) {
        if (data.watsonx_configured) {
          statusText.textContent = 'IBM Granite Live';
          badge.style.background = 'rgba(34, 197, 94, 0.1)';
        } else {
          statusText.textContent = 'Demo Mode';
          badge.style.background = 'rgba(245, 158, 11, 0.1)';
          badge.style.color = '#f59e0b';
          badge.style.borderColor = 'rgba(245, 158, 11, 0.2)';
          const dot = badge.querySelector('.status-dot');
          if (dot) dot.style.background = '#f59e0b';
        }
      }
      if (modelMode) modelMode.textContent = data.mode === 'watsonx' ? 'watsonx.ai Connected' : 'Demo Mode Active';
      if (modelName) modelName.textContent = data.mode === 'watsonx' ? 'IBM Granite' : 'Demo Mode';
    })
    .catch(() => {
      if (statusText) statusText.textContent = 'Offline';
    });
}

function initScrollAnimations() {
  const elements = document.querySelectorAll('[data-aos]');
  if (elements.length === 0) return;

  const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        const el = entry.target;
        const delay = el.dataset.aosDelay || 0;
        setTimeout(() => {
          el.style.opacity = '1';
          el.style.transform = 'translateY(0) translateX(0)';
        }, parseInt(delay));
        observer.unobserve(el);
      }
    });
  }, { threshold: 0.1 });

  elements.forEach(el => {
    el.style.opacity = '0';
    el.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
    if (el.dataset.aos === 'fade-up') el.style.transform = 'translateY(30px)';
    if (el.dataset.aos === 'fade-right') el.style.transform = 'translateX(-30px)';
    if (el.dataset.aos === 'fade-left') el.style.transform = 'translateX(30px)';
    observer.observe(el);
  });
}

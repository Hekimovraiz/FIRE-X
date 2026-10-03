(function() {
  'use strict';
  // Progress bar
  const progressBar = document.getElementById('nav-progress');
  if (progressBar) {
    window.addEventListener('scroll', () => {
      const total = document.body.scrollHeight - window.innerHeight;
      const pct = total > 0 ? (window.scrollY / total) * 100 : 0;
      progressBar.style.width = pct + '%';
    });
  }
  // Navbar scroll shrink
  const navbar = document.getElementById('navbar');
  if (navbar) {
    window.addEventListener('scroll', () => {
      navbar.classList.toggle('scrolled', window.scrollY > 40);
    });
  }
  // Active link
  const path = window.location.pathname.replace(/\/+$/, '') || '/';
  document.querySelectorAll('.nav-link').forEach(link => {
    const href = link.getAttribute('href');
    if (href === path || (path === '/' && href === '/') || (href !== '/' && path.startsWith(href))) {
      link.classList.add('active');
    }
  });
  // Page transitions
  document.querySelectorAll('a[href^="/"]').forEach(link => {
    link.addEventListener('click', e => {
      const href = link.getAttribute('href');
      if (href && !href.startsWith('#') && !link.target) {
        e.preventDefault();
        document.body.style.opacity = '0';
        document.body.style.transition = 'opacity 0.25s ease';
        setTimeout(() => { window.location.href = href; }, 250);
      }
    });
  });
  // Body fade in
  document.addEventListener('DOMContentLoaded', () => {
    document.body.style.opacity = '0';
    requestAnimationFrame(() => {
      document.body.style.transition = 'opacity 0.4s ease';
      document.body.style.opacity = '1';
    });
  });
  // Mobile menu
  const mobileBtn = document.getElementById('mobile-menu-btn');
  const navLinks = document.getElementById('nav-links-list');
  if (mobileBtn && navLinks) {
    mobileBtn.addEventListener('click', () => navLinks.classList.toggle('open'));
  }
  // Intersection observer for .reveal elements
  const observer = new IntersectionObserver((entries) => {
    entries.forEach(e => { if (e.isIntersecting) { e.target.classList.add('visible'); observer.unobserve(e.target); } });
  }, { threshold: 0.1 });
  document.querySelectorAll('.reveal').forEach(el => observer.observe(el));
  // Language toggle
  const langBtn = document.getElementById('nav-lang-btn');
  if (langBtn) {
    const current = localStorage.getItem('firex_lang') || 'en';
    langBtn.textContent = current.toUpperCase();
    langBtn.addEventListener('click', () => {
      const next = localStorage.getItem('firex_lang') === 'az' ? 'en' : 'az';
      localStorage.setItem('firex_lang', next);
      langBtn.textContent = next.toUpperCase();
      window.location.reload();
    });
  }
})();

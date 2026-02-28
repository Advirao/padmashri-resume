/* === main.js — Resume Website Interactivity === */

// ─── Nav scroll effect ───────────────────────────────────────────────────────
const nav = document.getElementById('main-nav');
const onScroll = () => {
  nav.classList.toggle('scrolled', window.scrollY > 10);
};
window.addEventListener('scroll', onScroll, { passive: true });
onScroll();

// ─── Hamburger / mobile menu ─────────────────────────────────────────────────
const hamburger = document.getElementById('hamburger');
const navLinks  = document.getElementById('nav-links');
hamburger.addEventListener('click', () => {
  const open = navLinks.classList.toggle('open');
  hamburger.classList.toggle('active', open);
  hamburger.setAttribute('aria-expanded', String(open));
});
// Close on link click
navLinks.querySelectorAll('.nav-link').forEach(link => {
  link.addEventListener('click', () => {
    navLinks.classList.remove('open');
    hamburger.classList.remove('active');
    hamburger.setAttribute('aria-expanded', 'false');
  });
});

// ─── Scroll Reveal (IntersectionObserver) ────────────────────────────────────
const revealObserver = new IntersectionObserver((entries) => {
  entries.forEach((entry, idx) => {
    if (entry.isIntersecting) {
      // Stagger siblings
      const parent = entry.target.parentElement;
      const siblings = [...parent.querySelectorAll('.reveal')];
      const i = siblings.indexOf(entry.target);
      entry.target.style.transitionDelay = `${i * 80}ms`;
      entry.target.classList.add('visible');
      revealObserver.unobserve(entry.target);
    }
  });
}, { threshold: 0.1, rootMargin: '0px 0px -60px 0px' });

document.querySelectorAll('.reveal').forEach(el => revealObserver.observe(el));

// ─── Active nav link on scroll ────────────────────────────────────────────────
const sections = document.querySelectorAll('section[id], header[id]');
const navItems = document.querySelectorAll('.nav-link');
const sectionObserver = new IntersectionObserver((entries) => {
  entries.forEach(entry => {
    if (entry.isIntersecting) {
      navItems.forEach(n => n.classList.remove('active'));
      const active = document.querySelector(`.nav-link[href="#${entry.target.id}"]`);
      if (active) active.classList.add('active');
    }
  });
}, { threshold: 0.35 });
sections.forEach(s => sectionObserver.observe(s));

// ─── Job accordion toggle ─────────────────────────────────────────────────────
document.querySelectorAll('.job-toggle').forEach(btn => {
  btn.addEventListener('click', () => {
    const targetId = btn.getAttribute('aria-controls');
    const details  = document.getElementById(targetId);
    const expanded = btn.getAttribute('aria-expanded') === 'true';

    if (expanded) {
      details.classList.add('collapsed');
      btn.setAttribute('aria-expanded', 'false');
      btn.textContent = '+';
    } else {
      details.classList.remove('collapsed');
      btn.setAttribute('aria-expanded', 'true');
      btn.textContent = '−';
    }
  });
});

// Allow clicking the job-header (except the button itself) to toggle
document.querySelectorAll('.job-header').forEach(header => {
  header.addEventListener('click', (e) => {
    if (e.target.closest('.job-toggle')) return;
    const btn = header.querySelector('.job-toggle');
    btn.click();
  });
});

// ─── Smooth parallax on hero bg text ─────────────────────────────────────────
const heroBg = document.querySelector('.hero-bg-text');
if (heroBg && window.matchMedia('(prefers-reduced-motion: no-preference)').matches) {
  window.addEventListener('scroll', () => {
    const y = window.scrollY;
    heroBg.style.transform = `translateY(calc(-50% + ${y * 0.15}px))`;
  }, { passive: true });
}

// ─── Hero entrance animation ──────────────────────────────────────────────────
const heroEls = document.querySelectorAll('.hero-label, .hero-title .line, .hero-subtitle, .hero-actions, .hero-stats');
heroEls.forEach((el, i) => {
  el.style.opacity = '0';
  el.style.transform = 'translateY(24px)';
  el.style.transition = 'opacity 0.8s ease, transform 0.8s ease';
  el.style.transitionDelay = `${0.1 + i * 0.1}s`;
  // Trigger after paint
  requestAnimationFrame(() => requestAnimationFrame(() => {
    el.style.opacity = '1';
    el.style.transform = 'translateY(0)';
  }));
});

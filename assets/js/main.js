// ── NAV ACTIVE STATE ──
document.addEventListener('DOMContentLoaded', () => {
  const path = window.location.pathname;
  document.querySelectorAll('.nav-link').forEach(link => {
    const href = link.getAttribute('href');
    if (!href) return;
    if (href === '/fr/' || href === '/en/') {
      if (path === href || path === href.slice(0, -1)) {
        link.classList.add('active');
      }
    } else {
      if (path.includes(href)) {
        link.classList.add('active');
      }
    }
  });
  document.querySelectorAll('.lang-item').forEach(item => {
    const href = item.getAttribute('href') || '';
    if (path.startsWith('/fr') && href.includes('/fr')) {
      item.querySelector('.lang-dot')?.classList.add('active');
      item.querySelector('.lang-btn')?.classList.add('active');
    } else if (path.startsWith('/en') && href.includes('/en')) {
      item.querySelector('.lang-dot')?.classList.add('active');
      item.querySelector('.lang-btn')?.classList.add('active');
    }
  });

  // ── COOKIE CONSENT ──
  const consent = localStorage.getItem('cookie_consent');
  if (consent === 'accepted') {
    loadGA();
  } else if (consent === null) {
    showCookieBanner();
  }
});

function loadGA() {
  if (window.gtagLoaded) return;
  if (document.cookie.split(';').some(c => c.trim().startsWith('ga_exclude=1'))) return;
  window.gtagLoaded = true;
  const s = document.createElement('script');
  s.async = true;
  s.src = 'https://www.googletagmanager.com/gtag/js?id=G-66V1F9V1N2';
  document.head.appendChild(s);
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  window.gtag = gtag;
  gtag('js', new Date());
  gtag('config', 'G-66V1F9V1N2');
}

function showCookieBanner() {
  const banner = document.getElementById('cookie-banner');
  if (banner) banner.style.display = 'flex';
}

function acceptCookies() {
  localStorage.setItem('cookie_consent', 'accepted');
  document.getElementById('cookie-banner').style.display = 'none';
  loadGA();
}

function refuseCookies() {
  localStorage.setItem('cookie_consent', 'refused');
  document.getElementById('cookie-banner').style.display = 'none';
}

// ── LIGHTBOX ──
(function () {
  const ZOOM_IN_SVG  = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><circle cx="11" cy="11" r="7"/><line x1="11" y1="8" x2="11" y2="14"/><line x1="8" y1="11" x2="14" y2="11"/><line x1="16.5" y1="16.5" x2="21" y2="21"/></svg>';
  const ZOOM_OUT_SVG = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><circle cx="11" cy="11" r="7"/><line x1="8" y1="11" x2="14" y2="11"/><line x1="16.5" y1="16.5" x2="21" y2="21"/></svg>';

  const overlay = document.createElement('div');
  overlay.className = 'lightbox-overlay';

  const closeBtn = document.createElement('button');
  closeBtn.className = 'lightbox-close';
  closeBtn.innerHTML = ZOOM_OUT_SVG;
  closeBtn.setAttribute('aria-label', 'Fermer');

  const img = document.createElement('img');
  img.className = 'lightbox-img';

  overlay.appendChild(closeBtn);
  overlay.appendChild(img);

  function open(src, alt) {
    img.src = src; img.alt = alt || '';
    document.body.appendChild(overlay);
    document.body.classList.add('lightbox-open');
    requestAnimationFrame(() => overlay.classList.add('open'));
    document.addEventListener('keydown', onKey);
  }

  function close() {
    overlay.classList.remove('open');
    document.body.classList.remove('lightbox-open');
    document.removeEventListener('keydown', onKey);
    overlay.addEventListener('transitionend', () => overlay.remove(), { once: true });
  }

  function onKey(e) { if (e.key === 'Escape') close(); }

  overlay.addEventListener('click', close);
  closeBtn.addEventListener('click', e => { e.stopPropagation(); close(); });

  function makeZoomBtn() {
    const b = document.createElement('button');
    b.className = 'media-zoom-btn';
    b.innerHTML = ZOOM_IN_SVG;
    b.setAttribute('aria-label', 'Agrandir');
    return b;
  }

  document.addEventListener('DOMContentLoaded', () => {
    // Images d'illustration
    document.querySelectorAll('.article-illus-img').forEach(el => {
      el.addEventListener('click', () => open(el.src, el.alt));
    });

    // Carousel
    document.querySelectorAll('.carousel').forEach(carousel => {
      const zoomBtn = makeZoomBtn();
      carousel.appendChild(zoomBtn);
      zoomBtn.addEventListener('click', e => {
        e.stopPropagation();
        const active = carousel.querySelector('.carousel-slide.active');
        if (active) open(active.src, active.alt);
      });
    });
  });
})();

// ── HAMBURGER MENU ──
document.addEventListener('DOMContentLoaded', () => {
  const hamburger = document.getElementById('hamburger');
  const navLinks = document.getElementById('nav-links');
  if (!hamburger || !navLinks) return;

  hamburger.addEventListener('click', () => {
    const open = navLinks.classList.toggle('open');
    hamburger.classList.toggle('open', open);
    hamburger.setAttribute('aria-expanded', open);
  });

  // Fermer au clic sur un lien
  navLinks.querySelectorAll('.nav-link').forEach(link => {
    link.addEventListener('click', () => {
      navLinks.classList.remove('open');
      hamburger.classList.remove('open');
      hamburger.setAttribute('aria-expanded', 'false');
    });
  });
});

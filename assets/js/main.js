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

  const vid = document.createElement('video');
  vid.className = 'lightbox-video';
  vid.controls = true;

  overlay.appendChild(closeBtn);
  overlay.appendChild(img);
  overlay.appendChild(vid);

  function show() {
    document.body.appendChild(overlay);
    document.body.classList.add('lightbox-open');
    requestAnimationFrame(() => overlay.classList.add('open'));
    document.addEventListener('keydown', onKey);
  }

  function openImg(src, alt) {
    img.src = src; img.alt = alt || '';
    img.style.display = ''; vid.style.display = 'none'; vid.pause(); vid.src = '';
    show();
  }

  function openVid(sources) {
    vid.innerHTML = '';
    sources.forEach(s => { const el = document.createElement('source'); el.src = s.src; el.type = s.type; vid.appendChild(el); });
    vid.load();
    vid.style.display = ''; img.style.display = 'none';
    show();
  }

  function close() {
    overlay.classList.remove('open');
    document.body.classList.remove('lightbox-open');
    vid.pause(); vid.src = '';
    document.removeEventListener('keydown', onKey);
    overlay.addEventListener('transitionend', () => overlay.remove(), { once: true });
  }

  function onKey(e) { if (e.key === 'Escape') close(); }

  overlay.addEventListener('click', close);
  closeBtn.addEventListener('click', e => { e.stopPropagation(); close(); });
  vid.addEventListener('click', e => e.stopPropagation());

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
      el.addEventListener('click', () => openImg(el.src, el.alt));
    });

    // Vidéos
    document.querySelectorAll('.article-video').forEach(container => {
      const video = container.querySelector('video');
      if (!video) return;
      const zoomBtn = makeZoomBtn();
      container.appendChild(zoomBtn);
      zoomBtn.addEventListener('click', e => {
        e.stopPropagation();
        const sources = Array.from(video.querySelectorAll('source')).map(s => ({ src: s.src, type: s.type }));
        if (!sources.length && video.src) sources.push({ src: video.src, type: 'video/mp4' });
        openVid(sources);
      });
    });

    // Carousel
    document.querySelectorAll('.carousel').forEach(carousel => {
      const zoomBtn = makeZoomBtn();
      carousel.appendChild(zoomBtn);
      zoomBtn.addEventListener('click', e => {
        e.stopPropagation();
        const active = carousel.querySelector('.carousel-slide.active');
        if (active) openImg(active.src, active.alt);
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

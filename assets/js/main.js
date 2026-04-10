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
    loadLinkedInBadge();
  } else if (consent === null) {
    showCookieBanner();
  }
});

function loadLinkedInBadge() {
  if (window.linkedInBadgeLoaded) return;
  window.linkedInBadgeLoaded = true;
  const s = document.createElement("script");
  s.src = "https://platform.linkedin.com/badges/js/profile.js";
  s.async = true;
  s.defer = true;
  document.body.appendChild(s);
}

function loadGA() {
  if (window.gtagLoaded) return;
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
  loadLinkedInBadge();
}

function refuseCookies() {
  localStorage.setItem('cookie_consent', 'refused');
  document.getElementById('cookie-banner').style.display = 'none';
}

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

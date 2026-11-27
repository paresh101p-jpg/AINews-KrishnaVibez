// AINews — Core Client-Side Logic (Zero-Hash Architecture)
// Clean URLs, Instant Search, Real Views, Relative Times, Cookie Consent

(function() {
  'use strict';

  // 1. Universal URL Hash Sanitizer: Immediately strip any #hash from address bar
  function cleanUrlHash() {
    if (window.location.hash) {
      try {
        history.replaceState(null, document.title, window.location.pathname + window.location.search);
      } catch (e) {}
    }
  }
  cleanUrlHash();
  window.addEventListener('hashchange', cleanUrlHash);

  // 2. Smooth Scroll for in-page anchors without modifying URL hash
  function initSmoothScrollNoHash() {
    document.querySelectorAll('a[href^="#"]').forEach(a => {
      a.addEventListener('click', (e) => {
        const href = a.getAttribute('href');
        if (!href || href === '#') return;
        const targetId = href.substring(1);
        const targetEl = document.getElementById(targetId);
        if (targetEl) {
          e.preventDefault();
          targetEl.scrollIntoView({ behavior: 'smooth' });
          // Ensure hash is not added to URL
          cleanUrlHash();
        }
      });
    });
  }

  // 3. Instant Search Engine
  function initInstantSearch() {
    const input = document.getElementById('globalSearchInput');
    const dropdown = document.getElementById('searchResultsDropdown');
    if (!input || !dropdown) return;

    let searchIndex = [];
    let isIndexLoaded = false;

    async function loadIndex() {
      if (isIndexLoaded) return;
      try {
        const res = await fetch('/search-index.json');
        if (res.ok) {
          searchIndex = await res.json();
          isIndexLoaded = true;
        }
      } catch (err) {
        console.warn('Search index load error:', err);
      }
    }

    input.addEventListener('focus', () => {
      loadIndex();
    });

    document.addEventListener('keydown', (e) => {
      if (e.key === '/' && document.activeElement !== input) {
        e.preventDefault();
        input.focus();
        loadIndex();
      } else if (e.key === 'Escape') {
        dropdown.style.display = 'none';
        input.blur();
      }
    });

    input.addEventListener('input', () => {
      const q = input.value.trim().toLowerCase();
      if (!q) {
        dropdown.style.display = 'none';
        dropdown.innerHTML = '';
        return;
      }

      if (!isIndexLoaded) {
        loadIndex().then(() => performSearch(q));
      } else {
        performSearch(q);
      }
    });

    function performSearch(query) {
      const results = searchIndex.filter(item => {
        return (
          item.title.toLowerCase().includes(query) ||
          item.snippet.toLowerCase().includes(query) ||
          (item.category && item.category.toLowerCase().includes(query))
        );
      }).slice(0, 7);

      if (results.length === 0) {
        dropdown.innerHTML = `<div class="search-no-results">No technical dispatches matching "<strong>${escapeHtml(query)}</strong>"</div>`;
        dropdown.style.display = 'block';
        return;
      }

      dropdown.innerHTML = results.map(res => `
        <a href="${res.url}" class="search-item">
          <div class="search-item-cat">${escapeHtml(res.category || 'ANALYSIS')}</div>
          <div class="search-item-title">${escapeHtml(res.title)}</div>
          <div class="search-item-snip">${escapeHtml(res.snippet)}</div>
        </a>
      `).join('');
      dropdown.style.display = 'block';
    }

    document.addEventListener('click', (e) => {
      if (!input.contains(e.target) && !dropdown.contains(e.target)) {
        dropdown.style.display = 'none';
      }
    });

    function escapeHtml(str) {
      if (!str) return '';
      return str.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');
    }
  }

  // 4. Relative Time Formatter ("⚡ 2 hours ago")
  function updateRelativeTimes() {
    const timeElements = document.querySelectorAll('[data-pub]');
    const now = new Date();

    timeElements.forEach(el => {
      const pubStr = el.getAttribute('data-pub');
      if (!pubStr) return;
      const pubDate = new Date(pubStr);
      if (isNaN(pubDate.getTime())) return;

      const diffSec = Math.floor((now - pubDate) / 1000);
      let text = '';

      if (diffSec < 60) {
        text = '⚡ Just now';
      } else if (diffSec < 3600) {
        const m = Math.floor(diffSec / 60);
        text = `⚡ ${m} min${m > 1 ? 's' : ''} ago`;
      } else if (diffSec < 86400) {
        const h = Math.floor(diffSec / 3600);
        text = `⚡ ${h} hour${h > 1 ? 's' : ''} ago`;
      } else {
        const d = Math.floor(diffSec / 86400);
        text = `⚡ ${d} day${d > 1 ? 's' : ''} ago`;
      }

      el.textContent = text;
    });
  }

  // 5. Real View Counters
  function initRealViewCounters() {
    const NS = 'ainews-krishnavibez';
    const BASE = 'https://abacus.jasoncameron.dev';
    const cache = new Map();

    function toKey(urlOrSlug) {
      let s = (urlOrSlug || '')
        .replace(/^https?:\/\/[^/]+/, '')
        .replace(/^.*\/articles\//, '')
        .replace(/\.html.*$/, '')
        .replace(/[#?].*$/, '')
        .replace(/[^a-zA-Z0-9_-]/g, '-')
        .replace(/^-+|-+$/g, '');
      if (s.length < 3) s = 'article-' + (s || 'home');
      if (s.length > 64) s = s.slice(0, 48) + '-' + s.slice(-15);
      return s;
    }

    function fmt(n) {
      const num = Number(n) || 0;
      if (num >= 1000000) return (num / 1000000).toFixed(1).replace(/\.0$/, '') + 'M';
      if (num >= 1000) return (num / 1000).toFixed(1).replace(/\.0$/, '') + 'K';
      return num.toLocaleString('en-IN');
    }

    async function fetchViews(key, isHit) {
      const cacheKey = (isHit ? 'hit:' : 'get:') + key;
      if (cache.has(cacheKey)) return cache.get(cacheKey);
      const endpoint = isHit ? `${BASE}/hit/${NS}/${key}` : `${BASE}/get/${NS}/${key}`;
      const p = fetch(endpoint)
        .then(r => (r.ok ? r.json() : { value: 0 }))
        .then(d => {
          const val = Number(d && d.value) || 0;
          return val;
        })
        .catch(() => 0);
      cache.set(cacheKey, p);
      return p;
    }

    // Inside individual article page: increment (+1 real view)
    if (window.location.pathname.indexOf('/articles/') !== -1) {
      const key = toKey(window.location.pathname);
      const metaBar = document.querySelector('.meta-bar');
      if (metaBar) {
        let span = metaBar.querySelector('.article-real-views');
        if (!span) {
          span = document.createElement('span');
          span.className = 'article-real-views';
          span.style.cssText = 'color:#a78bfa; font-weight:700;';
          span.innerHTML = '👁️ <strong class="real-view-count">...</strong> views';
          metaBar.appendChild(span);
        }
        fetchViews(key, true).then(count => {
          const el = span.querySelector('.real-view-count');
          if (el) el.textContent = fmt(count > 0 ? count : 1);
        });
      }
    }

    function refreshHomepageCounts() {
      cache.clear();
      document.querySelectorAll('[data-view-key]').forEach(el => {
        const key = el.getAttribute('data-view-key');
        fetchViews(key, false).then(count => {
          el.textContent = fmt(count > 0 ? count : 1);
        });
      });
    }

    // Homepage Lead Story
    const leadLink = document.querySelector('.lead-story .lead-title a, .lead-story a[href*="/articles/"]');
    const leadByline = document.querySelector('.lead-story .byline-row');
    if (leadLink && leadByline && !leadByline.querySelector('.real-view-count')) {
      const key = toKey(leadLink.getAttribute('href'));
      const dot = document.createElement('span');
      dot.textContent = '•';
      const vSpan = document.createElement('span');
      vSpan.style.cssText = 'color:#a78bfa; font-weight:600;';
      vSpan.innerHTML = `👁️ <span class="real-view-count" data-view-key="${key}">...</span> views`;
      leadByline.appendChild(dot);
      leadByline.appendChild(vSpan);
    }

    // Homepage Wire Dispatches
    document.querySelectorAll('.wire-item').forEach(item => {
      const a = item.querySelector('a[href*="/articles/"]');
      const meta = item.querySelector('.wire-item-meta');
      if (a && meta && !meta.querySelector('.real-view-count')) {
        const key = toKey(a.getAttribute('href'));
        const vSpan = document.createElement('span');
        vSpan.innerHTML = ` • 👁️ <span class="real-view-count" data-view-key="${key}">...</span> views`;
        meta.appendChild(vSpan);
      }
    });

    // Homepage Article Grid Cards
    document.querySelectorAll('.articles-grid .article-card').forEach(card => {
      const a = card.querySelector('.card-title a, a[href*="/articles/"]');
      const meta = card.querySelector('.card-meta');
      if (a && meta && !meta.querySelector('.real-view-count')) {
        const key = toKey(a.getAttribute('href'));
        const dot = document.createElement('span');
        dot.className = 'meta-dot';
        dot.textContent = '•';
        const vSpan = document.createElement('span');
        vSpan.className = 'card-views';
        vSpan.style.cssText = 'color:#a78bfa; font-weight:600;';
        vSpan.innerHTML = `👁️ <span class="real-view-count" data-view-key="${key}">...</span> views`;
        meta.appendChild(dot);
        meta.appendChild(vSpan);
      }
    });

    refreshHomepageCounts();
    window.addEventListener('pageshow', (e) => {
      if (e.persisted) refreshHomepageCounts();
    });
  }

  // 6. Cookie Consent Banner
  function initCookieConsent() {
    if (localStorage.getItem('ainews_cookie_consent')) return;
    
    const banner = document.createElement('div');
    banner.id = 'ainews-cookie-banner';
    banner.style.cssText = `
      position: fixed;
      bottom: 20px;
      left: 50%;
      transform: translateX(-50%);
      width: 90%;
      max-width: 680px;
      background: #0d111a;
      border: 1px solid #1c2433;
      box-shadow: 0 10px 30px rgba(0,0,0,0.85);
      border-radius: 12px;
      padding: 16px 22px;
      z-index: 999999;
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 16px;
      font-size: 0.85rem;
      color: #94a3b8;
      backdrop-filter: blur(10px);
    `;
    banner.innerHTML = `
      <div>
        🍪 <strong>Privacy &amp; Cookie Notice:</strong> We use cookies to ensure site functionality, analyze readership, and support independent tech journalism via Google AdSense. See our <a href="/privacy" style="color:#06b6d4; text-decoration:underline;">Privacy Policy</a>.
      </div>
      <button id="acceptCookiesBtn" style="
        background: #06b6d4;
        color: #030712;
        border: none;
        padding: 8px 16px;
        font-weight: 700;
        border-radius: 6px;
        cursor: pointer;
        white-space: nowrap;
        font-size: 0.82rem;
      ">Accept</button>
    `;
    document.body.appendChild(banner);

    document.getElementById('acceptCookiesBtn').addEventListener('click', () => {
      localStorage.setItem('ainews_cookie_consent', 'true');
      banner.style.opacity = '0';
      banner.style.transition = 'opacity 0.3s ease';
      setTimeout(() => banner.remove(), 300);
    });
  }

  // DOM Content Loaded Initializer
  document.addEventListener('DOMContentLoaded', () => {
    cleanUrlHash();
    initSmoothScrollNoHash();
    initInstantSearch();
    updateRelativeTimes();
    initRealViewCounters();
    initCookieConsent();
    setInterval(updateRelativeTimes, 60000);
  });

})();

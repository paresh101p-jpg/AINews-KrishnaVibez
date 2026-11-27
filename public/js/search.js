/**
 * AINews Live Global Search & Routing Engine
 * High-speed instant search, category filtering & universal hash routing.
 */

(function() {
  const articlesIndex = [
    {
      title: "OpenAI Unveils o3: The First AI Model Capable of Multi-Day Autonomous Reasoning",
      category: "FRONTIER LLMS",
      date: "November 21, 2026",
      url: "/articles/openai-o3-reasoning-breakthrough-system-2-thinking",
      excerpt: "OpenAI officially releases o3, introducing a paradigm shift toward System 2 persistent autonomous reasoning, test-time compute scaling, and iterative self-verification.",
      badge: "BREAKING"
    }
  ];

  fetch('/api/articles.json')
    .then(r => r.ok ? r.json() : [])
    .then(items => {
      if (Array.isArray(items) && items.length > 0) {
        items.forEach(it => {
          if (!articlesIndex.some(a => a.url === it.url)) {
            articlesIndex.push(it);
          }
        });
      }
    })
    .catch(() => {});

  document.addEventListener('DOMContentLoaded', () => {
    initSearch();
    initHashRouter();
    updateRelativeTimes();
    setInterval(updateRelativeTimes, 30000);
    initRealViewCounters();
  });

  function initSearch() {
    const input = document.getElementById('globalSearchInput');
    const dropdown = document.getElementById('searchResultsDropdown');
    if (!input || !dropdown) return;

    document.addEventListener('keydown', (e) => {
      if (e.key === '/' && document.activeElement !== input && !['INPUT', 'TEXTAREA'].includes(document.activeElement.tagName)) {
        e.preventDefault();
        input.focus();
        input.select();
      } else if ((e.ctrlKey || e.metaKey) && e.key.toLowerCase() === 'k') {
        e.preventDefault();
        input.focus();
        input.select();
      } else if (e.key === 'Escape') {
        dropdown.style.display = 'none';
        input.blur();
      }
    });

    input.addEventListener('input', (e) => {
      const q = e.target.value.trim().toLowerCase();
      if (!q) {
        dropdown.style.display = 'none';
        dropdown.innerHTML = '';
        return;
      }

      const results = articlesIndex.filter(a => {
        return a.title.toLowerCase().includes(q) ||
               a.category.toLowerCase().includes(q) ||
               a.excerpt.toLowerCase().includes(q);
      });

      renderResults(results, q, dropdown);
    });

    document.addEventListener('click', (e) => {
      if (!input.contains(e.target) && !dropdown.contains(e.target)) {
        dropdown.style.display = 'none';
      }
    });

    input.addEventListener('focus', () => {
      if (input.value.trim().length > 0) {
        dropdown.style.display = 'block';
      }
    });
  }

  function renderResults(results, query, dropdown) {
    if (results.length === 0) {
      dropdown.innerHTML = `
        <div class="search-empty">
          <span>No articles matching "<strong>${escapeHtml(query)}</strong>"</span>
          <div style="font-size:0.75rem; color:var(--text-muted); margin-top:4px;">Try searching for <em>o3</em>, <em>reasoning</em>, <em>Blackwell</em>, or <em>Agents</em></div>
        </div>
      `;
      dropdown.style.display = 'block';
      return;
    }

    let html = `<div class="search-header">Search Results (${results.length})</div>`;
    results.forEach(res => {
      const highlightedTitle = highlightMatch(res.title, query);
      html += `
        <a href="${res.url}" class="search-item">
          <div class="search-item-meta">
            <span class="search-cat-badge">${res.category}</span>
            <span class="search-date">${res.date}</span>
          </div>
          <div class="search-item-title">${highlightedTitle}</div>
          <div class="search-item-excerpt">${escapeHtml(res.excerpt.slice(0, 110))}...</div>
        </a>
      `;
    });

    dropdown.innerHTML = html;
    dropdown.style.display = 'block';
  }

  function highlightMatch(text, query) {
    const idx = text.toLowerCase().indexOf(query);
    if (idx === -1) return escapeHtml(text);
    const before = escapeHtml(text.slice(0, idx));
    const match = escapeHtml(text.slice(idx, idx + query.length));
    const after = escapeHtml(text.slice(idx + query.length));
    return `${before}<mark class="search-highlight">${match}</mark>${after}`;
  }

  function escapeHtml(str) {
    return str.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');
  }

  /**
   * Universal Hash Router & Dynamic Section / Filter Controller
   * Handles #top-stories, #models, #agents, #silicon, #robotics, #trending, #subscribe,
   * and hashtags like #openai-o3, #gemini-3-0, #claude-3-7-sonnet, etc.
   */
  function initHashRouter() {
    const navLinks = document.querySelectorAll('.main-nav a');
    const trendingPills = document.querySelectorAll('.trending-pill');
    const cards = document.querySelectorAll('.articles-grid .article-card');
    const heading = document.querySelector('.section-heading');
    const headingBar = document.querySelector('.section-heading-bar') || document.getElementById('articles');

    function applyRoute(hashStr, shouldScroll) {
      const rawHash = (hashStr || window.location.hash || '').replace(/^#/, '').trim().toLowerCase();
      
      // Reset active classes
      navLinks.forEach(l => l.classList.remove('active'));
      trendingPills.forEach(p => p.classList.remove('pill-active'));

      let catFilter = null;
      let label = 'Frontier Intelligence & Technical Analysis';
      let activeNav = null;
      let activePill = null;
      let targetScrollEl = headingBar;

      if (!rawHash || rawHash === 'top-stories' || rawHash === '/') {
        catFilter = null;
        label = 'Frontier Intelligence & Technical Analysis';
        activeNav = document.querySelector('.main-nav a[href="#top-stories"], .main-nav a[href="/"]');
        if (rawHash === 'top-stories' && targetScrollEl && shouldScroll) {
          targetScrollEl.scrollIntoView({ behavior: 'smooth' });
        }
      } else if (rawHash === 'models' || rawHash === 'frontier-llms') {
        catFilter = /frontier llms|llm|openai|claude|gemini|o3|reasoning|language model|haiku/i;
        label = 'Category: Frontier LLMs';
        activeNav = document.querySelector('.main-nav a[href="#models"]');
      } else if (rawHash === 'agents' || rawHash === 'agents-coding') {
        catFilter = /agents|coding|software|developer|autonomous|benchmark/i;
        label = 'Category: Agents & Coding';
        activeNav = document.querySelector('.main-nav a[href="#agents"]');
      } else if (rawHash === 'silicon' || rawHash === 'silicon-gpus') {
        catFilter = /silicon|gpu|chip|nvidia|blackwell|neuromorphic|hardware|datacenter/i;
        label = 'Category: Silicon & GPUs';
        activeNav = document.querySelector('.main-nav a[href="#silicon"]');
      } else if (rawHash === 'robotics') {
        catFilter = /robotics|robot|atlas|humanoid|optimus|boston dynamics|figure|embodied/i;
        label = 'Category: Robotics & Embodied AI';
        activeNav = document.querySelector('.main-nav a[href="#robotics"]');
      } else if (rawHash === 'trending') {
        catFilter = /o3|claude|blackwell|deepseek|reasoning|optimus|atlas|figure|gemini|gta/i;
        label = '🔥 Trending Stories & Frontier Breakthroughs';
        activeNav = document.querySelector('.main-nav a[href="#trending"]');
        const trendStrip = document.getElementById('trending');
        if (trendStrip) targetScrollEl = trendStrip;
      } else if (rawHash === 'subscribe' || rawHash === 'dispatch') {
        const subSec = document.getElementById('subscribe') || document.querySelector('.news-wire-panel');
        if (subSec && shouldScroll) {
          subSec.scrollIntoView({ behavior: 'smooth' });
        }
        return;
      } else {
        // Tag / hashtag / keyword filter (e.g. #openai-o3, #gemini-3-0, #claude-3-7-sonnet, etc.)
        const topic = rawHash.replace(/^search-/, '').replace(/-/g, ' ').replace(/\./g, '\\.');
        const cleanDisplay = rawHash.replace(/^search-/, '').toUpperCase();
        catFilter = new RegExp(topic, 'i');
        label = `Trending Topic: #${cleanDisplay}`;
        activePill = document.querySelector(`.trending-pill[href="#${rawHash}"], .trending-pill[data-topic="${rawHash}"]`);
      }

      if (activeNav) activeNav.classList.add('active');
      if (activePill) activePill.classList.add('pill-active');

      if (heading) {
        if (catFilter) {
          heading.innerHTML = `${label} <a href="#top-stories" style="font-size:0.75rem; margin-left:14px; color:var(--accent-cyan); text-decoration:underline; font-weight:600; cursor:pointer;" onclick="location.hash='#top-stories'; return false;">✕ View All Stories</a>`;
        } else {
          heading.textContent = label;
        }
      }

      let matchedCount = 0;
      cards.forEach(card => {
        const cardText = ((card.getAttribute('data-category') || '') + ' ' + card.innerText).toLowerCase();
        if (!catFilter || catFilter.test(cardText)) {
          card.style.display = '';
          matchedCount++;
        } else {
          card.style.display = 'none';
        }
      });

      // Smooth scroll to target section if requested
      if (shouldScroll && targetScrollEl && rawHash && rawHash !== 'top-stories') {
        setTimeout(() => {
          targetScrollEl.scrollIntoView({ behavior: 'smooth' });
        }, 80);
      }
    }

    // Nav click handlers
    navLinks.forEach(link => {
      link.addEventListener('click', (e) => {
        const href = link.getAttribute('href');
        if (!href || href === '/rss.xml') return;
        if (href.startsWith('#')) {
          e.preventDefault();
          window.location.hash = href;
          applyRoute(href, true);
        }
      });
    });

    // Trending pill click handlers
    trendingPills.forEach(pill => {
      pill.addEventListener('click', (e) => {
        const href = pill.getAttribute('href');
        if (href && href.startsWith('#')) {
          e.preventDefault();
          window.location.hash = href;
          applyRoute(href, true);
        }
      });
    });

    // Also support wire category tags (href="#silicon", etc.)
    document.querySelectorAll('.wire-item a[href^="#"]').forEach(a => {
      a.addEventListener('click', (e) => {
        e.preventDefault();
        const href = a.getAttribute('href');
        window.location.hash = href;
        applyRoute(href, true);
      });
    });

    // Hash change event listener (Back / Forward button support)
    window.addEventListener('hashchange', () => {
      applyRoute(window.location.hash, true);
    });

    // Initial load check
    if (window.location.hash) {
      applyRoute(window.location.hash, true);
    }
  }

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

    // 1. Inside individual article page: increment (+1 real view)
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

    // 2. Homepage Lead Story
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

    // 3. Homepage Wire Dispatches
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

    // 4. Homepage Article Grid Cards
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
})();

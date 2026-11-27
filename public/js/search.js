/**
 * AINews Live Global Search Engine
 * High-speed instant search across breaking AI articles, models & silicon analysis.
 */

(function() {
  const articlesIndex = [
    {
      title: "OpenAI Unveils o3: The First AI Model Capable of Multi-Day Autonomous Reasoning",
      category: "FRONTIER LLMS",
      date: "November 21, 2026",
      url: "/articles/openai-o3-reasoning-breakthrough-system-2-thinking.html",
      excerpt: "OpenAI officially releases o3, introducing a paradigm shift toward System 2 persistent autonomous reasoning, test-time compute scaling, and iterative self-verification.",
      badge: "BREAKING"
    }
  ];

  // Also try to load dynamic history if available
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
    initCategoryFilters();
    updateRelativeTimes();
    setInterval(updateRelativeTimes, 30000);
  });

  function initSearch() {
    const input = document.getElementById('globalSearchInput');
    const dropdown = document.getElementById('searchResultsDropdown');
    if (!input || !dropdown) return;

    // Global keyboard shortcut '/' or 'Ctrl+K'
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

    // Input listener
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

    // Close on outside click
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

  function initCategoryFilters() {
    const navLinks = document.querySelectorAll('.main-nav a');
    const cards = document.querySelectorAll('.articles-grid .article-card');
    const heading = document.querySelector('.section-heading');

    navLinks.forEach(link => {
      link.addEventListener('click', (e) => {
        const href = link.getAttribute('href');
        if (href === '/rss.xml') return; // let RSS open

        e.preventDefault();
        navLinks.forEach(l => l.classList.remove('active'));
        link.classList.add('active');

        let catFilter = null;
        let label = 'Frontier Intelligence & Technical Analysis';
        if (href === '#models') {
          catFilter = /frontier llms|llm|openai|claude|gemini|o3|reasoning|language model/i;
          label = 'Category: Frontier LLMs';
        } else if (href === '#agents') {
          catFilter = /agents|coding|software|developer|autonomous/i;
          label = 'Category: Agents & Coding';
        } else if (href === '#silicon') {
          catFilter = /silicon|gpu|chip|nvidia|blackwell|neuromorphic|hardware/i;
          label = 'Category: Silicon & GPUs';
        } else if (href === '#robotics') {
          catFilter = /robotics|robot|atlas|humanoid|optimus|boston dynamics/i;
          label = 'Category: Robotics & Embodied AI';
        }

        if (heading) heading.textContent = label;

        cards.forEach(card => {
          const cardText = ((card.getAttribute('data-category') || '') + ' ' + card.innerText).toLowerCase();
          if (!catFilter || catFilter.test(cardText)) {
            card.style.display = '';
          } else {
            card.style.display = 'none';
          }
        });

        const targetSec = document.querySelector('.section-heading-bar');
        if (targetSec) {
          targetSec.scrollIntoView({ behavior: 'smooth' });
        }
      });
    });

    // Trending pills with data-search
    document.querySelectorAll('.trending-pill').forEach(pill => {
      pill.addEventListener('click', (e) => {
        const searchTerm = pill.getAttribute('data-search');
        if (searchTerm) {
          e.preventDefault();
          const input = document.getElementById('globalSearchInput');
          if (input) {
            input.value = searchTerm;
            input.dispatchEvent(new Event('input'));
            input.focus();
            window.scrollTo({ top: 0, behavior: 'smooth' });
          }
        }
      });
    });
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
      } else if (diffSec < 172800) {
        text = 'Yesterday';
      } else {
        const d = Math.floor(diffSec / 86400);
        text = `${d} days ago`;
      }

      el.textContent = text;
    });
  }
})();

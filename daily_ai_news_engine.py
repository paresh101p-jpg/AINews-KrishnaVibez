# -*- coding: utf-8 -*-
"""
Autonomous Daily Trending AI News Engine for AINews (ainews.krishnavibez.in)
- Discovers today's breaking AI news, frontier model releases, and silicon breakthroughs
- Writes 100% original, in-depth 1500-2000+ words technical journalism article
- Injects NewsArticle, FAQPage, Breadcrumb Schema.org JSON-LD
- Zero Unsplash rule: Uses 100% copyright-free pure AI-generated tech artwork & SVG visuals
- Updates public/articles/{slug}.html, index.html, sitemap.xml, rss.xml
- Deploys automatically to Firebase Hosting (site: ainews-krishnavibez)
"""

import os
import sys
import re
import json
import random
import requests
import subprocess
from datetime import datetime, timezone, timedelta
from google import genai

if sys.stdout and hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
if sys.stderr and hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

_IST = timezone(timedelta(hours=5, minutes=30))

REPO_ROOT = os.path.dirname(os.path.abspath(__file__))
PUBLIC_DIR = os.path.join(REPO_ROOT, "public")
ARTICLES_DIR = os.path.join(PUBLIC_DIR, "articles")
INDEX_FILE = os.path.join(PUBLIC_DIR, "index.html")
SITEMAP_FILE = os.path.join(PUBLIC_DIR, "sitemap.xml")
RSS_FILE = os.path.join(PUBLIC_DIR, "rss.xml")
HISTORY_FILE = os.path.join(REPO_ROOT, "ai_news_history.json")

# Ensure articles directory exists
os.makedirs(ARTICLES_DIR, exist_ok=True)

# Fetch Gemini API Key
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    gk_file = r"E:\Paresh\Auto Post\Auto-Insta-Krishna\gemini_key.txt"
    if os.path.exists(gk_file):
        try:
            with open(gk_file, "r", encoding="utf-8") as f:
                GEMINI_API_KEY = f.read().strip()
        except Exception:
            pass

# 100% Copyright-Free Cloud-Hosted High-Def 1200x675 AI Tech Images (Catbox CDN - Zero Storage Overhead on Firebase)
CATEGORY_IMAGES_MAP = {
    "FRONTIER LLMS": "https://files.catbox.moe/if0d7q.jpg",
    "AGENTS & CODING": "https://files.catbox.moe/q00f8o.jpg",
    "SILICON & GPUS": "https://files.catbox.moe/jej48b.jpg",
    "ROBOTICS": "https://files.catbox.moe/jv0uht.jpg",
    "OPEN SOURCE": "https://files.catbox.moe/y5sgma.jpg"
}
DEFAULT_TECH_HERO_IMAGE = "https://files.catbox.moe/7azw6q.jpg"

def generate_and_upload_catbox_banner(title, category, slug):
    """
    Synthesizes a 100% original 1200x675 HD AI tech banner, uploads to Catbox,
    and returns permanent URL (Zero Firebase storage overhead).
    """
    try:
        from generate_tech_banners import generate_banner
        temp_filename = os.path.join(REPO_ROOT, f"temp_{slug[:25]}.jpg")
        
        # Dynamic color scheme based on category
        color_palette = {
            "FRONTIER LLMS": ("#00f0ff", "#8a2be2"),
            "AGENTS & CODING": ("#10b981", "#3b82f6"),
            "SILICON & GPUS": ("#f59e0b", "#ef4444"),
            "ROBOTICS": ("#a855f7", "#06b6d4"),
            "OPEN SOURCE": ("#22c55e", "#6366f1")
        }
        accent, sec = color_palette.get(category.upper(), ("#00f0ff", "#3b82f6"))
        
        generate_banner(
            temp_filename,
            title[:55],
            f"BREAKING INTELLIGENCE // {category.upper()}",
            accent,
            sec
        )
        
        if os.path.exists(temp_filename):
            url = "https://catbox.moe/user/api.php"
            with open(temp_filename, "rb") as f:
                r = requests.post(url, data={"reqtype": "fileupload"}, files={"fileToUpload": f}, timeout=45)
            try:
                os.remove(temp_filename)
            except Exception:
                pass
            
            if r.status_code == 200 and r.text.strip().startswith("http"):
                catbox_url = r.text.strip()
                print(f"   [Catbox Cloud] Uploaded successfully: {catbox_url}")
                return catbox_url
    except Exception as e:
        print(f"   [Warning] Catbox upload error: {e}. Using verified CDN fallback.")
    
    return CATEGORY_IMAGES_MAP.get(category.upper(), DEFAULT_TECH_HERO_IMAGE)

def call_gemini(prompt):
    client = genai.Client(api_key=GEMINI_API_KEY)
    models = ["gemini-3.1-flash-lite", "gemini-3.7-flash", "gemini-3.8-flash"]
    for m in models:
        try:
            res = client.models.generate_content(model=m, contents=prompt)
            if res and res.text:
                return res.text.strip()
        except Exception as e:
            print(f"   [Notice] {m} failed: {e}. Trying fallback...")
            continue
    raise RuntimeError("All Gemini models failed.")

def get_existing_slugs():
    slugs = []
    if os.path.exists(ARTICLES_DIR):
        for f in os.listdir(ARTICLES_DIR):
            if f.endswith(".html"):
                slugs.append(f[:-5])
    return slugs

def determine_today_ai_news_topic():
    existing = get_existing_slugs()
    now_ist = datetime.now(_IST)
    date_str = now_ist.strftime("%d %B %Y")

    prompt = f"""You are the Editor-in-Chief of AINews (ainews.krishnavibez.in), a leading frontier artificial intelligence publication.
Today's Date: {date_str}.

Identify the SINGLE MOST IMPACTFUL, trending, high-traffic AI breaking news topic right now.
Topics of high interest:
- Frontier LLM releases & architectures (Anthropic Claude 3.7 hybrid reasoning, OpenAI o3 / GPT-5, Google Gemini 2.0 / 3.0 Flash breakthroughs, DeepSeek V3 / R1 reasoning revolution, Meta Llama 4).
- Autonomous AI Agents & Coding Tools (Cursor, Devin, Windsurf, LangGraph, AutoGPT 2.0).
- Silicon & Compute (Nvidia Blackwell B200 / GB200 clusters, AMD MI325X, Cerebras Wafer-Scale Engine, TPU v6).
- Humanoid Robotics & Embodied AI (Tesla Optimus Gen 3, Figure 02, Boston Dynamics Atlas, Unitree G1).

STRICT RULE: Do NOT repeat any of these recently published topics:
{json.dumps(existing[-15:], ensure_ascii=False)}

Output ONLY a valid JSON object with this exact structure:
{{
  "slug": "url-friendly-lowercase-slug-without-html",
  "title": "Compelling, high-CTR news headline between 60 to 90 characters (The Verge / TechCrunch style)",
  "category": "One of: FRONTIER LLMS | AGENTS & CODING | SILICON & GPUS | ROBOTICS | OPEN SOURCE",
  "meta_desc": "Engaging summary between 140 to 160 characters optimized for Google Search and Discover",
  "keywords": "8 to 10 high-volume search keywords separated by commas",
  "read_time": "6 min read",
  "key_stats": "e.g. 94.8% MMLU | 2x Faster Inference | $0.15/1M Tokens",
  "topic_summary": "Short 2-line brief of what makes this announcement revolutionary"
}}
"""
    raw = call_gemini(prompt)
    clean_json = re.sub(r"^```json\s*", "", raw.strip(), flags=re.MULTILINE)
    clean_json = re.sub(r"\s*```$", "", clean_json.strip(), flags=re.MULTILINE)
    data = json.loads(clean_json)
    data["slug"] = re.sub(r"[^a-z0-9\-]", "-", data["slug"].lower()).strip("-")
    return data

def write_ai_news_article_body(topic_meta):
    prompt = f"""You are an elite technical journalist writing for AINews.
Write a comprehensive, highly authoritative, 1500 to 2000+ word technical news breakdown on:
TITLE: {topic_meta['title']}
CATEGORY: {topic_meta['category']}
BRIEF: {topic_meta['topic_summary']}

EDITORIAL GUIDELINES:
1. Tone: Highly articulate, objective, data-driven, and forward-looking (similar to Ars Technica, SemiAnalysis, TechCrunch).
2. Structure:
   - Executive Brief (TL;DR): 3 bullet points highlighting core facts.
   - Section 1: The Breakthrough & Why It Matters (Context, background, market positioning).
   - Section 2: Technical Architecture & Core Innovations (How it works under the hood).
   - Section 3: Benchmark Performance & Real-World Results (Include a formatted HTML <table> with benchmarks vs competitors).
   - Section 4: Enterprise, Developer & Industry Implications (Pricing, API limits, competitive disruption).
   - Section 5: Current Limitations & Safety Considerations.
   - Section 6: Frequently Asked Questions (5 detailed, realistic FAQs with technical answers).
   - Section 7: Final Verdict & Future Outlook.

OUTPUT FORMAT:
Generate ONLY the semantic HTML body content (do NOT include <html> or <body> tags, only the article inner HTML starting with <section class="article-content">).
Use proper HTML tags:
- <h2> for main section headings
- <h3> for sub-headings
- <p> for detailed analytical paragraphs
- <table>, <thead>, <tbody>, <tr>, <th>, <td> with class="tech-table" for benchmark data
- <div class="tech-callout"> for important highlights
- <div class="faq-item"><h3>Q...</h3><p>A...</p></div> for the 5 FAQs
- <div class="tldr-box"> for the executive brief
"""
    body_html = call_gemini(prompt)
    body_html = re.sub(r"^```html\s*", "", body_html.strip(), flags=re.MULTILINE)
    body_html = re.sub(r"\s*```$", "", body_html.strip(), flags=re.MULTILINE)
    return body_html

def assemble_full_article_page(topic_meta, body_html):
    slug = topic_meta["slug"]
    title = topic_meta["title"]
    category = topic_meta["category"]
    meta_desc = topic_meta["meta_desc"]
    keywords = topic_meta["keywords"]
    read_time = topic_meta.get("read_time", "6 min read")
    canonical_url = f"https://ainews.krishnavibez.in/articles/{slug}.html"

    now_ist = datetime.now(_IST)
    date_iso = now_ist.isoformat()
    display_date = now_ist.strftime("%B %d, %Y")

    hero_img = topic_meta.get("hero_image") or CATEGORY_IMAGES_MAP.get(category.upper(), DEFAULT_TECH_HERO_IMAGE)
    if not hero_img.startswith("http"):
        hero_img = f"https://ainews.krishnavibez.in{hero_img}"

    # Extract FAQs for FAQPage Schema
    faq_matches = re.findall(r"<h3>(.*?)</h3>\s*<p>(.*?)</p>", body_html)
    faq_schema_items = []
    for q, a in faq_matches[:5]:
        clean_q = re.sub(r"<[^>]+>", "", q).strip()
        clean_a = re.sub(r"<[^>]+>", "", a).strip()
        if "?" in clean_q or "What" in clean_q or "How" in clean_q or "Why" in clean_q or "Is" in clean_q:
            faq_schema_items.append({
                "@type": "Question",
                "name": clean_q,
                "acceptedAnswer": {
                    "@type": "Answer",
                    "text": clean_a
                }
            })

    schema_graph = [
        {
            "@type": "NewsArticle",
            "@id": f"{canonical_url}#article",
            "isPartOf": {
                "@type": "WebSite",
                "@id": "https://ainews.krishnavibez.in/#website",
                "url": "https://ainews.krishnavibez.in/",
                "name": "AINews",
                "description": "Breaking Artificial Intelligence News & Frontier Tech"
            },
            "headline": title,
            "description": meta_desc,
            "image": hero_img,
            "datePublished": date_iso,
            "dateModified": date_iso,
            "inLanguage": "en-US",
            "mainEntityOfPage": canonical_url,
            "author": {
                "@type": "Person",
                "name": "Paresh Padsala",
                "url": "https://krishnavibez.in/about.html"
            },
            "publisher": {
                "@type": "NewsMediaOrganization",
                "name": "AINews",
                "url": "https://ainews.krishnavibez.in/",
                "logo": {
                    "@type": "ImageObject",
                    "url": "https://files.catbox.moe/r4c345.jpg"
                }
            }
        },
        {
            "@type": "BreadcrumbList",
            "@id": f"{canonical_url}#breadcrumb",
            "itemListElement": [
                {
                    "@type": "ListItem",
                    "position": 1,
                    "name": "Home",
                    "item": "https://ainews.krishnavibez.in/"
                },
                {
                    "@type": "ListItem",
                    "position": 2,
                    "name": "Intelligence",
                    "item": "https://ainews.krishnavibez.in/#news"
                },
                {
                    "@type": "ListItem",
                    "position": 3,
                    "name": title,
                    "item": canonical_url
                }
            ]
        }
    ]

    if faq_schema_items:
        schema_graph.append({
            "@type": "FAQPage",
            "@id": f"{canonical_url}#faq",
            "mainEntity": faq_schema_items
        })

    json_ld_str = json.dumps({"@context": "https://schema.org", "@graph": schema_graph}, ensure_ascii=False, indent=2)

    page_html = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{title} — AINews</title>
  <meta name="description" content="{meta_desc}">
  <meta name="keywords" content="{keywords}">
  <meta name="author" content="Paresh Padsala (AINews)">
  <link rel="canonical" href="{canonical_url}">

  <!-- Open Graph / Social Rich Preview -->
  <meta property="og:site_name" content="AINews">
  <meta property="og:type" content="article">
  <meta property="og:url" content="{canonical_url}">
  <meta property="og:title" content="{title}">
  <meta property="og:description" content="{meta_desc}">
  <meta property="og:image" content="{hero_img}">
  <meta property="og:image:width" content="1200">
  <meta property="og:image:height" content="675">
  <meta property="og:locale" content="en_US">

  <!-- Twitter Cards -->
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="{title}">
  <meta name="twitter:description" content="{meta_desc}">
  <meta name="twitter:image" content="{hero_img}">

  <!-- Google Discover Directives -->
  <meta name="robots" content="index, follow, max-image-preview:large, max-snippet:-1, max-video-preview:-1">
  <meta name="googlebot" content="index, follow, max-image-preview:large">

  <!-- Favicon -->
  <link rel="icon" href="data:image/svg+xml,<svg xmlns=%22http://www.w3.org/2000/svg%22 viewBox=%220 0 100 100%22><text y=%22.9em%22 font-size=%2290%22>⚡</text></svg>">

  <!-- Google AdSense -->
  <meta name="google-adsense-account" content="ca-pub-4064462736581300">
  <script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-4064462736581300" crossorigin="anonymous"></script>

  <!-- Google Analytics -->
  <script async src="https://www.googletagmanager.com/gtag/js?id=G-M7W6128K1Z"></script>
  <script>
    window.dataLayer = window.dataLayer || [];
    function gtag(){{dataLayer.push(arguments);}}
    gtag('js', new Date());
    gtag('config', 'G-M7W6128K1Z');
  </script>

  <!-- Schema.org JSON-LD -->
  <script type="application/ld+json">
{json_ld_str}
  </script>

  <link rel="stylesheet" href="../css/style.css">
  <style>
    .article-wrap {{
      max-width: 860px;
      margin: 0 auto;
      padding: 40px 20px 80px;
    }}
    .article-header {{
      margin-bottom: 28px;
    }}
    .article-badge {{
      display: inline-block;
      background: rgba(6, 182, 212, 0.15);
      color: var(--cyan);
      border: 1px solid rgba(6, 182, 212, 0.35);
      padding: 4px 14px;
      border-radius: 20px;
      font-size: 0.8rem;
      font-weight: 700;
      margin-bottom: 16px;
      text-transform: uppercase;
      letter-spacing: 0.5px;
    }}
    h1.article-title {{
      font-size: clamp(2rem, 3.8vw, 2.9rem);
      line-height: 1.28;
      font-weight: 800;
      color: #fff;
      margin-bottom: 16px;
      letter-spacing: -0.5px;
    }}
    .meta-bar {{
      display: flex;
      align-items: center;
      gap: 16px;
      color: var(--text-muted);
      font-size: 0.9rem;
      padding-bottom: 18px;
      border-bottom: 1px solid var(--border-color);
      flex-wrap: wrap;
    }}
    .hero-img-box {{
      width: 100%;
      border-radius: 16px;
      overflow: hidden;
      margin: 30px 0 36px;
      border: 1px solid var(--border-color);
      box-shadow: 0 16px 36px rgba(0, 0, 0, 0.6);
    }}
    .hero-img-box img {{
      width: 100%;
      height: auto;
      aspect-ratio: 16 / 9;
      object-fit: cover;
      display: block;
    }}
    .article-content h2 {{
      color: #fff;
      font-size: 1.65rem;
      font-weight: 700;
      margin: 44px 0 16px;
      padding-bottom: 10px;
      border-bottom: 1px solid var(--border-color);
    }}
    .article-content h3 {{
      color: var(--cyan);
      font-size: 1.25rem;
      margin: 26px 0 12px;
    }}
    .article-content p {{
      color: #cbd5e1;
      font-size: 1.1rem;
      line-height: 1.85;
      margin-bottom: 22px;
    }}
    .tech-callout, .tldr-box {{
      background: rgba(15, 23, 42, 0.85);
      border-left: 4px solid var(--cyan);
      padding: 20px 24px;
      border-radius: 0 12px 12px 0;
      margin: 30px 0;
      color: #f1f5f9;
    }}
    .tech-callout strong, .tldr-box strong {{
      color: var(--cyan);
    }}
    .tech-table {{
      width: 100%;
      border-collapse: collapse;
      margin: 28px 0;
      font-size: 0.95rem;
      background: var(--bg-card);
      border-radius: 12px;
      overflow: hidden;
      border: 1px solid var(--border-color);
    }}
    .tech-table th, .tech-table td {{
      padding: 12px 18px;
      text-align: left;
      border-bottom: 1px solid var(--border-color);
    }}
    .tech-table th {{
      background: rgba(6, 182, 212, 0.1);
      color: var(--cyan);
      font-weight: 700;
    }}
    .faq-item {{
      background: var(--bg-card);
      border: 1px solid var(--border-color);
      border-radius: 12px;
      padding: 18px 22px;
      margin-bottom: 16px;
    }}
    .faq-item h3 {{
      margin: 0 0 8px;
      color: var(--cyan);
      font-size: 1.1rem;
    }}
    .share-bar {{
      margin: 50px 0 30px;
      padding: 20px;
      background: var(--bg-card);
      border: 1px solid var(--border-color);
      border-radius: 14px;
      display: flex;
      align-items: center;
      gap: 12px;
      flex-wrap: wrap;
    }}
    .share-btn {{
      padding: 8px 16px;
      border-radius: 8px;
      font-size: 0.9rem;
      font-weight: 600;
      color: #fff;
    }}
    .share-tw {{ background: #1da1f2; }}
    .share-li {{ background: #0a66c2; }}
    .share-rd {{ background: #ff4500; }}
  </style>
</head>
<body>

  <!-- 1. Top News Wire Ticker -->
  <div class="top-ticker-bar">
    <div class="container ticker-inner">
      <div class="ticker-live">
        <span class="live-badge"><span class="live-pulse"></span> THE WIRE</span>
        <span class="ticker-text">{title} • Special Frontier Intelligence Report</span>
      </div>
      <div class="ticker-date">{display_date} | Global Tech Edition</div>
    </div>
  </div>

  <!-- 2. Main Editorial Header -->
  <header class="main-header">
    <div class="container header-row">
      <div class="header-brand">
        <a href="/">
          <img src="../assets/logo.png" alt="AINews — Frontier Intelligence" class="header-logo" height="48">
        </a>
      </div>
      <nav class="main-nav">
        <a href="/">Top Stories</a>
        <a href="/#models" class="active">{category}</a>
        <a href="/#agents">Agents &amp; Coding</a>
        <a href="/#silicon">Silicon &amp; GPUs</a>
        <a href="/#robotics">Robotics</a>
        <a href="/rss.xml">RSS Feed</a>
      </nav>
      <div class="header-actions">
        <a href="/#subscribe" class="subscribe-btn">Get Dispatch</a>
      </div>
    </div>
  </header>

  <div class="article-wrap">
    <div class="article-header">
      <div class="article-badge">⚡ {category}</div>
      <h1 class="article-title">{title}</h1>
      <div class="meta-bar">
        <span>✍️ Paresh Padsala (AINews)</span>
        <span>📅 {display_date}</span>
        <span>⏱️ {read_time}</span>
      </div>
    </div>

    <div class="hero-img-box">
      <img src="{hero_img}" alt="{title}" loading="eager" width="1200" height="675">
    </div>

    <article class="article-content">
      {body_html}
    </article>

    <div class="share-bar">
      <span style="font-weight:700; color:#fff;">Share this report:</span>
      <a class="share-btn share-tw" href="https://twitter.com/intent/tweet?text={title}&url={canonical_url}" target="_blank" rel="noopener">Twitter / X</a>
      <a class="share-btn share-li" href="https://www.linkedin.com/sharing/share-offsite/?url={canonical_url}" target="_blank" rel="noopener">LinkedIn</a>
      <a class="share-btn share-rd" href="https://reddit.com/submit?url={canonical_url}&title={title}" target="_blank" rel="noopener">Reddit</a>
    </div>

    <div style="text-align:center; margin-top:40px;">
      <a href="/" style="color:var(--cyan); font-weight:700; text-decoration:none;">← Back to Latest AI News</a>
    </div>
  </div>

  <!-- Editorial Footer -->
  <footer class="site-footer">
    <div class="container">
      <div class="footer-top">
        <div class="footer-brand">
          <img src="../assets/logo.png" alt="AINews" height="42">
          <p>
            AINews is an independent digital news organization delivering uncompromising, data-driven technical journalism on frontier machine intelligence, compute hardware, and autonomous systems.
          </p>
        </div>
        <div class="footer-col">
          <h4>Coverage</h4>
          <ul>
            <li><a href="/#models">Frontier LLMs</a></li>
            <li><a href="/#agents">Autonomous Agents</a></li>
            <li><a href="/#silicon">Silicon &amp; GPUs</a></li>
            <li><a href="/#robotics">Humanoid Robotics</a></li>
          </ul>
        </div>
        <div class="footer-col">
          <h4>Feeds &amp; Index</h4>
          <ul>
            <li><a href="/rss.xml">RSS Feed</a></li>
            <li><a href="/sitemap.xml">XML Sitemap</a></li>
            <li><a href="https://krishnavibez.in" target="_blank">Krishna Vibez Network</a></li>
          </ul>
        </div>
        <div class="footer-col">
          <h4>Editorial</h4>
          <ul>
            <li><a href="/about.html">About the Publication</a></li>
            <li><a href="/ethics.html">Editorial Standards</a></li>
            <li><a href="/contact.html">Press Inquiries</a></li>
          </ul>
        </div>
      </div>
      <div class="footer-bottom">
        <div>© 2026 <strong>AINews</strong>. All rights reserved. Published by Krishna Vibez Network.</div>
        <div>Engineered for Google Discover &amp; Real-Time Frontier Intelligence.</div>
      </div>
    </div>
  </footer>

</body>
</html>"""
    return page_html, hero_img

def update_index_page(topic_meta, hero_img):
    if not os.path.exists(INDEX_FILE):
        return
    slug = topic_meta["slug"]
    title = topic_meta["title"]
    category = topic_meta["category"]
    meta_desc = topic_meta["meta_desc"]
    read_time = topic_meta.get("read_time", "6 min read")
    display_date = datetime.now(_IST).strftime("%B %d, %Y")

    card_html = f"""
    <!-- Article Card: {slug} -->
    <article class="news-card">
      <div class="card-img-wrap">
        <span class="card-badge">{category}</span>
        <img src="{hero_img}" alt="{title}" loading="lazy" width="600" height="338">
      </div>
      <div class="card-body">
        <div class="card-date">{display_date} • {read_time}</div>
        <h2 class="card-title">
          <a href="articles/{slug}.html">{title}</a>
        </h2>
        <p class="card-excerpt">{meta_desc[:145]}...</p>
        <div class="card-footer">
          <span style="color:var(--text-muted); font-size:0.8rem;">By Paresh Padsala</span>
          <a href="articles/{slug}.html" class="read-btn">Read Deep Dive →</a>
        </div>
      </div>
    </article>
"""
    with open(INDEX_FILE, "r", encoding="utf-8") as f:
        html = f.read()

    if '<main class="news-grid">' in html:
        new_html = html.replace('<main class="news-grid">', '<main class="news-grid">\n' + card_html, 1)
        with open(INDEX_FILE, "w", encoding="utf-8") as f:
            f.write(new_html)
        print("✅ Injected article card into index.html.")

def update_sitemap(slug):
    if not os.path.exists(SITEMAP_FILE):
        return
    today_str = datetime.now(_IST).strftime("%Y-%m-%d")
    new_entry = f"""  <url>
    <loc>https://ainews.krishnavibez.in/articles/{slug}.html</loc>
    <lastmod>{today_str}</lastmod>
    <changefreq>daily</changefreq>
    <priority>0.9</priority>
  </url>
"""
    with open(SITEMAP_FILE, "r", encoding="utf-8") as f:
        xml = f.read()
    if f"/articles/{slug}.html" not in xml:
        xml = xml.replace('</urlset>', new_entry + '</urlset>')
        with open(SITEMAP_FILE, "w", encoding="utf-8") as f:
            f.write(xml)
        print("✅ Updated sitemap.xml.")

def update_rss(topic_meta, hero_img):
    if not os.path.exists(RSS_FILE):
        return
    slug = topic_meta["slug"]
    title = topic_meta["title"]
    meta_desc = topic_meta["meta_desc"]
    category = topic_meta["category"]
    now_rfc = datetime.now(_IST).strftime("%a, %d %b %Y %H:%M:%S +0530")
    article_url = f"https://ainews.krishnavibez.in/articles/{slug}.html"

    item_xml = f"""    <item>
      <title>{title}</title>
      <link>{article_url}</link>
      <guid isPermaLink="true">{article_url}</guid>
      <pubDate>{now_rfc}</pubDate>
      <dc:creator>Paresh Padsala (AINews)</dc:creator>
      <category>{category}</category>
      <description><![CDATA[{meta_desc}]]></description>
      <enclosure url="{hero_img}" type="image/jpeg" length="153600" />
      <media:content url="{hero_img}" medium="image" width="1200" height="675" />
    </item>
"""
    with open(RSS_FILE, "r", encoding="utf-8") as f:
        xml = f.read()
    if article_url not in xml:
        match = re.search(r'(<atom:link[^>]+/>)', xml)
        if match:
            xml = xml[:match.end()] + "\n" + item_xml + xml[match.end():]
        else:
            xml = xml.replace('</channel>', item_xml + '</channel>')
        with open(RSS_FILE, "w", encoding="utf-8") as f:
            f.write(xml)
        print("✅ Updated rss.xml.")

def run_pipeline():
    print("=" * 70)
    print("⚡ STARTING AUTONOMOUS AI NEWS PIPELINE (ainews.krishnavibez.in)")
    print("=" * 70)

    print("\n🔍 Step 1: Finding today's top breaking AI news & model breakthroughs...")
    topic_meta = determine_today_ai_news_topic()
    print(f"   Headline: {topic_meta['title']}")
    print(f"   Category: {topic_meta['category']}")
    print(f"   Slug: {topic_meta['slug']}")

    print("\n🖼️ Step 1.5: Synthesizing HD AI Tech Banner & uploading to Catbox (Zero Firebase Overhead)...")
    catbox_img = generate_and_upload_catbox_banner(topic_meta["title"], topic_meta["category"], topic_meta["slug"])
    topic_meta["hero_image"] = catbox_img
    print(f"   Catbox Cloud URL: {catbox_img}")

    print("\n✍️ Step 2: Writing 1500-2000+ words technical journalism report...")
    body_html = write_ai_news_article_body(topic_meta)
    print(f"   Generated {len(body_html)} bytes of structured technical content.")

    print("\n🎨 Step 3: Assembling full HTML with NewsArticle & FAQ Schema (Zero Unsplash)...")
    page_html, hero_img = assemble_full_article_page(topic_meta, body_html)
    article_path = os.path.join(ARTICLES_DIR, f"{topic_meta['slug']}.html")
    with open(article_path, "w", encoding="utf-8") as f:
        f.write(page_html)
    print(f"   Saved article to: {article_path}")

    print("\n📡 Step 4: Updating index.html, sitemap.xml & rss.xml...")
    update_index_page(topic_meta, hero_img)
    update_sitemap(topic_meta["slug"])
    update_rss(topic_meta, hero_img)

    # Save to history
    hist = []
    if os.path.exists(HISTORY_FILE):
        try:
            with open(HISTORY_FILE, "r", encoding="utf-8") as f:
                hist = json.load(f)
        except Exception:
            hist = []
    hist.append({
        "slug": topic_meta["slug"],
        "title": topic_meta["title"],
        "category": topic_meta["category"],
        "created_at": datetime.now(_IST).isoformat()
    })
    with open(HISTORY_FILE, "w", encoding="utf-8") as f:
        json.dump(hist, f, indent=2)

    print("\n" + "=" * 70)
    print("🎉 AI NEWS ARTICLE READY FOR DEPLOYMENT!")
    print(f"   Article: https://ainews.krishnavibez.in/articles/{topic_meta['slug']}.html")
    print("=" * 70)
    return True

if __name__ == "__main__":
    success = run_pipeline()
    sys.exit(0 if success else 1)


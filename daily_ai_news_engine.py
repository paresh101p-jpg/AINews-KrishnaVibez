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
    "FRONTIER LLMS": "https://files.catbox.moe/4v7mse.jpg",
    "AGENTS & CODING": "https://files.catbox.moe/q00f8o.jpg",
    "SILICON & GPUS": "https://files.catbox.moe/zdqjhe.jpg",
    "ROBOTICS": "https://files.catbox.moe/rzevj0.jpg",
    "OPEN SOURCE": "https://files.catbox.moe/y5sgma.jpg"
}
DEFAULT_TECH_HERO_IMAGE = "https://files.catbox.moe/4v7mse.jpg"

def generate_and_upload_catbox_banner(title, category, slug, content=""):
    """
    100% Free Smart-Tagging Editorial Matcher:
    Selects the 100% exact-match photorealistic editorial AI photograph from the
    verified AI Editorial Pool based on semantic topic keywords and LRU rotation.
    Zero generic geometric drawings. Zero repetitions. Zero API costs.
    """
    try:
        from smart_image_matcher import select_best_image_for_article
        chosen_url = select_best_image_for_article(title, category, content=content, slug=slug)
        if chosen_url and chosen_url.startswith("http"):
            print(f"   [Smart Editorial Matcher] Selected 100% Matched Image: {chosen_url}")
            return chosen_url
    except Exception as e:
        print(f"   [Warning] Smart Matcher notice: {e}. Using category verified visual.")
    
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

    prompt = f"""You are the US Bureau Chief & Editor-in-Chief of AINews (ainews.krishnavibez.in) based in Silicon Valley, San Francisco, CA.
Today's Date: {date_str}.

PRIMARY TARGET AUDIENCE: United States Tech Sector, Silicon Valley Engineers, Enterprise AI CTOs, Wall Street Tech Investors, and US AI Developers (High US CPM/CPC).

Identify the SINGLE MOST IMPACTFUL, trending, high-traffic US & Global AI breaking news topic right now.
Topics of primary US interest:
- US Frontier LLM releases (OpenAI o3/GPT-5, Anthropic Claude 3.7 Sonnet, Google Gemini 2.0/3.0, Meta Llama 4).
- US Autonomous AI Agents & Silicon Valley startups (Cursor, Devin, Windsurf, Cognition AI, Perplexity).
- Silicon & US Infrastructure (Nvidia Blackwell B200 / GB200 clusters, AMD, Cerebras, US Datacenter gigawatt buildouts).
- Humanoid Robotics in US industry (Tesla Optimus Gen 3, Figure 02, Boston Dynamics).
- US Regulatory, Copyright & Enterprise ROI impacts (FTC, White House AI safety guidelines, Fortune 500 enterprise adoption).

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
    prompt = f"""You are an elite Silicon Valley technical journalist writing for AINews (US Bureau, San Francisco).
Write a comprehensive, highly authoritative, 1500 to 2000+ word technical news breakdown tailored for the US Tech market on:
TITLE: {topic_meta['title']}
CATEGORY: {topic_meta['category']}
BRIEF: {topic_meta['topic_summary']}

EDITORIAL GUIDELINES (US TARGETED):
1. Tone: Deep, articulate, objective, data-driven, and forward-looking (similar to SemiAnalysis, The Verge, Stratechery, Ars Technica).
2. Economic Framing: Frame all economics in US Dollars ($), US enterprise software ROI, Silicon Valley venture backing, and Big Tech compute cluster CAPEX.
3. Language: Clear, authoritative American English (en-US).
4. Structure:
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
    # Strip any conflicting inline backgrounds (like white/f4f4f4/e7f3fe) so dark theme looks 100% premium
    body_html = re.sub(r'<div class="tldr-box"[^>]*>', '<div class="tldr-box" id="executive-brief">', body_html)
    body_html = re.sub(r'<div class="tech-callout"[^>]*>', '<div class="tech-callout">', body_html)
    body_html = re.sub(r'style="[^"]*(?:background|#f4f4f4|#fff|#e7f3fe|#b3d7ff)[^"]*"', '', body_html)

    # Ensure section IDs exist for Table of Contents & Google Jump-to-Section SEO
    sec_id_map = {
        r"Section 1": "breakthrough",
        r"Section 2": "architecture",
        r"Section 3": "benchmarks",
        r"Section 4": "industry-impact",
        r"Section 5": "limitations",
        r"Section 6": "faq",
        r"Section 7": "outlook"
    }
    for pattern, s_id in sec_id_map.items():
        body_html = re.sub(rf'<h2>({pattern}[^<]*)</h2>', rf'<h2 id="{s_id}">\1</h2>', body_html, flags=re.IGNORECASE)
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
    pub_iso = date_iso
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

    # Build Entity schema for Google Discover Knowledge Graph
    entity_about = [
        {"@type": "Thing", "name": "Artificial Intelligence", "sameAs": "https://en.wikipedia.org/wiki/Artificial_intelligence"}
    ]
    t_lower = (title + " " + keywords + " " + category).lower()
    if "openai" in t_lower:
        entity_about.append({"@type": "Thing", "name": "OpenAI", "sameAs": "https://en.wikipedia.org/wiki/OpenAI"})
    if "nvidia" in t_lower:
        entity_about.append({"@type": "Thing", "name": "Nvidia", "sameAs": "https://en.wikipedia.org/wiki/Nvidia"})
    if "google" in t_lower or "gemini" in t_lower:
        entity_about.append({"@type": "Thing", "name": "Google DeepMind", "sameAs": "https://en.wikipedia.org/wiki/Google_DeepMind"})
    if "anthropic" in t_lower or "claude" in t_lower:
        entity_about.append({"@type": "Thing", "name": "Anthropic", "sameAs": "https://en.wikipedia.org/wiki/Anthropic"})
    if "robot" in t_lower or "humanoid" in t_lower or "figure" in t_lower:
        entity_about.append({"@type": "Thing", "name": "Humanoid Robot", "sameAs": "https://en.wikipedia.org/wiki/Humanoid_robot"})
    if "chip" in t_lower or "semiconductor" in t_lower or "tsmc" in t_lower or "gpu" in t_lower:
        entity_about.append({"@type": "Thing", "name": "Semiconductor", "sameAs": "https://en.wikipedia.org/wiki/Semiconductor"})
    if "quantum" in t_lower:
        entity_about.append({"@type": "Thing", "name": "Quantum Computing", "sameAs": "https://en.wikipedia.org/wiki/Quantum_computing"})

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
                "jobTitle": "Senior Technology Correspondent",
                "url": "https://ainews.krishnavibez.in/authors/paresh-padsala.html"
            },
            "about": entity_about,
            "publisher": {
                "@type": "NewsMediaOrganization",
                "name": "AINews",
                "url": "https://ainews.krishnavibez.in/",
                "logo": {
                    "@type": "ImageObject",
                    "url": "https://ainews.krishnavibez.in/assets/logo.png",
                    "width": 640,
                    "height": 160
                },
                "sameAs": [
                    "https://krishnavibez.in/",
                    "https://twitter.com/ainews_intel"
                ],
                "publishingPrinciples": "https://ainews.krishnavibez.in/ethics.html",
                "correctionsPolicy": "https://ainews.krishnavibez.in/ethics.html"
            },
            "speakable": {
                "@type": "SpeakableSpecification",
                "cssSelector": [".article-headline", ".article-deck", ".lead-paragraph"]
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
  <link rel="alternate" type="application/rss+xml" title="AINews — Frontier AI Intelligence RSS Feed" href="https://ainews.krishnavibez.in/rss.xml">
  <link rel="help" type="text/markdown" title="LLMs Context Manifest" href="https://ainews.krishnavibez.in/llms.txt">

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
  <meta property="article:published_time" content="{pub_iso}">
  <meta property="article:modified_time" content="{pub_iso}">
  <meta property="article:section" content="{category}">
  <meta property="article:author" content="Paresh Padsala">
  <link rel="preconnect" href="https://files.catbox.moe" crossorigin>
  <link rel="dns-prefetch" href="https://files.catbox.moe">

  <!-- Twitter Cards -->
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="{title}">
  <meta name="twitter:description" content="{meta_desc}">
  <meta name="twitter:image" content="{hero_img}">

  <!-- Google Discover Directives -->
  <meta name="robots" content="index, follow, max-image-preview:large, max-snippet:-1, max-video-preview:-1">
  <meta name="googlebot" content="index, follow, max-image-preview:large">

  <!-- USA Market Targeting & Geo Meta Tags -->
  <meta name="geo.region" content="US-CA">
  <meta name="geo.placename" content="San Francisco, California">
  <meta name="geo.position" content="37.7749;-122.4194">
  <meta name="ICBM" content="37.7749, -122.4194">
  <meta property="og:locale" content="en_US">
  <meta name="target" content="all">
  <meta name="coverage" content="Worldwide">
  <meta name="distribution" content="Global">

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
      background: rgba(15, 23, 42, 0.95) !important;
      border: 1px solid rgba(0, 240, 255, 0.25) !important;
      border-left: 4px solid var(--cyan) !important;
      padding: 24px 28px !important;
      border-radius: 0 12px 12px 0 !important;
      margin: 30px 0 !important;
      color: #f1f5f9 !important;
    }}
    .tldr-box h3 {{
      color: var(--cyan) !important;
      margin-bottom: 14px !important;
      font-size: 1.25rem !important;
      letter-spacing: 0.5px !important;
    }}
    .tldr-box ul {{
      margin: 0 !important;
      padding-left: 20px !important;
      color: #cbd5e1 !important;
    }}
    .tldr-box li {{
      margin-bottom: 12px !important;
      line-height: 1.75 !important;
      font-size: 1.02rem !important;
    }}
    .tech-callout strong, .tldr-box strong {{
      color: #38bdf8 !important;
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
  <!-- Google Reader Revenue Manager (Subscribe with Google) -->
  <script async type="application/javascript" src="https://news.google.com/swg/js/v1/swg-basic.js"></script>
  <script>
    (self.SWG_BASIC = self.SWG_BASIC || []).push( basicSubscriptions => {{
      basicSubscriptions.init({{
        type: "NewsArticle",
        isPartOfType: ["Product"],
        isPartOfProductId: "CAow1u2bCw:openaccess",
        clientOptions: {{ theme: "light", lang: "en" }},
      }});
    }});
  </script>
</head>
<body>

  <!-- 1. Top News Wire Ticker -->
  <div class="top-ticker-bar">
    <div class="container ticker-inner">
      <div class="ticker-live">
        <span class="live-badge"><span class="live-pulse"></span> THE WIRE</span>
        <span class="ticker-text">{title} • Special Frontier Intelligence Report</span>
      </div>
      <div class="ticker-date">{display_date} | US &amp; Silicon Valley Edition</div>
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
        <div class="header-search-wrap">
          <div class="search-box">
            <svg class="search-icon" width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="11" cy="11" r="8"></circle><line x1="21" y1="21" x2="16.65" y2="16.65"></line></svg>
            <input type="text" id="globalSearchInput" placeholder="Search AI news, models..." autocomplete="off">
            <span class="search-kbd">/</span>
          </div>
          <div id="searchResultsDropdown" class="search-dropdown"></div>
        </div>
        <a href="/#subscribe" class="subscribe-btn">Get Dispatch</a>
      </div>
    </div>
  </header>
  <div id="readingProgress"></div>

  <div class="article-wrap">
    <div class="article-header">
      <div class="article-badge">⚡ {category}</div>
      <h1 class="article-title">{title}</h1>
      <div class="meta-bar">
        <span>✍️ By <a href="/authors/paresh-padsala.html" style="color:var(--cyan); text-decoration:none; font-weight:600;">Paresh Padsala</a> (US Bureau, San Francisco)</span>
        <span>📅 {display_date}</span>
        <span>⏱️ {read_time}</span>
      </div>
    </div>

    <div class="hero-img-box">
      <img src="{hero_img}" alt="{title}" fetchpriority="high" loading="eager" width="1200" height="675">
    </div>

    <nav class="article-toc" aria-label="Table of Contents">
      <div class="toc-title">📑 In This Investigation (Table of Contents)</div>
      <ul>
        <li><a href="#executive-brief">Executive Brief &amp; Core Takeaways</a></li>
        <li><a href="#breakthrough">Section 1: The Breakthrough &amp; Why It Matters</a></li>
        <li><a href="#architecture">Section 2: Technical Architecture &amp; System 2</a></li>
        <li><a href="#benchmarks">Section 3: Benchmark Performance Matrix</a></li>
        <li><a href="#industry-impact">Section 4: Enterprise &amp; Developer Implications</a></li>
        <li><a href="#limitations">Section 5: Bottlenecks &amp; Safety Safeguards</a></li>
        <li><a href="#faq">Section 6: Technical FAQs</a></li>
        <li><a href="#outlook">Section 7: Final Verdict &amp; Future Outlook</a></li>
      </ul>
    </nav>

    <article class="article-content">
      {body_html}
    </article>

    <!-- Author Bio Card (Google E-E-A-T) -->
    <div class="author-bio-card">
      <div class="author-avatar">PP</div>
      <div class="author-info">
        <div class="author-name"><a href="/authors/paresh-padsala.html">Paresh Padsala</a></div>
        <div class="author-title">Founder &amp; Senior Technology Correspondent · US Bureau (San Francisco)</div>
        <div class="author-bio-text">
          Investigating frontier machine intelligence, reasoning architectures (System-2 deliberation), high-density datacenter silicon, and autonomous humanoid robotics. Verified technical analyst and founder of AINews.
        </div>
        <div class="author-card-links">
          <a href="/authors/paresh-padsala.html">View Full Profile &amp; Dispatches →</a>
          <a href="mailto:editorial@ainews.krishnavibez.in">editorial@ainews.krishnavibez.in</a>
          <a href="https://twitter.com/ainews_intel" target="_blank">@ainews_intel</a>
        </div>
      </div>
    </div>

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

  <script src="/js/search.js"></script>
  <script>
    window.addEventListener('scroll', function() {{
      var h = document.documentElement.scrollHeight - document.documentElement.clientHeight;
      var pct = h > 0 ? (window.scrollY / h) * 100 : 0;
      var bar = document.getElementById('readingProgress');
      if (bar) bar.style.width = pct + '%';
    }});
  </script>
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
          <span style="color:var(--text-muted); font-size:0.8rem;">By <a href="/authors/paresh-padsala.html" style="color:inherit; text-decoration:none;">Paresh Padsala</a></span>
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

def update_sitemap(topic_meta, hero_img=""):
    if not os.path.exists(SITEMAP_FILE):
        return
    slug = topic_meta["slug"]
    title = topic_meta["title"]
    now_ist = datetime.now(_IST)
    iso_date = now_ist.strftime("%Y-%m-%dT%H:%M:%S+05:30")
    new_entry = f"""  <url>
    <loc>https://ainews.krishnavibez.in/articles/{slug}.html</loc>
    <lastmod>{iso_date}</lastmod>
    <changefreq>daily</changefreq>
    <priority>0.9</priority>
    <news:news>
      <news:publication>
        <news:name>AINews</news:name>
        <news:language>en</news:language>
      </news:publication>
      <news:publication_date>{iso_date}</news:publication_date>
      <news:title>{title}</news:title>
    </news:news>
    <image:image>
      <image:loc>{hero_img}</image:loc>
      <image:title>{title}</image:title>
    </image:image>
  </url>
"""
    with open(SITEMAP_FILE, "r", encoding="utf-8") as f:
        xml = f.read()
    if f"/articles/{slug}.html" not in xml:
        xml = xml.replace('</urlset>', new_entry + '</urlset>')
        with open(SITEMAP_FILE, "w", encoding="utf-8") as f:
            f.write(xml)
        print("✅ Updated sitemap.xml with Google News & Discover tags.")

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

def ping_search_engines_and_hubs(article_url):
    """
    Submits new article to IndexNow (Bing, Yandex, Naver) and WebSub (PubSubHubbub)
    for instant global indexing and syndication.
    """
    print("\n🌐 Step 5: Submitting article to IndexNow & WebSub Instant Indexing...")
    # 1. IndexNow Submission
    try:
        indexnow_payload = {
            "host": "ainews.krishnavibez.in",
            "key": "e4c8b21a97d54930ba81f182c6de3421",
            "keyLocation": "https://ainews.krishnavibez.in/e4c8b21a97d54930ba81f182c6de3421.txt",
            "urlList": [
                "https://ainews.krishnavibez.in/",
                article_url
            ]
        }
        req = urllib.request.Request(
            "https://api.indexnow.org/indexnow",
            data=json.dumps(indexnow_payload).encode("utf-8"),
            headers={"Content-Type": "application/json; charset=utf-8", "User-Agent": "AINews-Publisher/1.0"}
        )
        with urllib.request.urlopen(req, timeout=10) as r:
            print(f"   ✅ IndexNow ping successful: HTTP {r.status}")
    except Exception as e:
        print(f"   [Notice] IndexNow ping: {e}")

    # 2. WebSub (PubSubHubbub) Submission
    try:
        websub_data = urllib.parse.urlencode({
            "hub.mode": "publish",
            "hub.url": "https://ainews.krishnavibez.in/rss.xml"
        }).encode("utf-8")
        req = urllib.request.Request(
            "https://pubsubhubbub.appspot.com/publish",
            data=websub_data,
            headers={"Content-Type": "application/x-www-form-urlencoded", "User-Agent": "AINews-Publisher/1.0"}
        )
        with urllib.request.urlopen(req, timeout=10) as r:
            print(f"   ✅ WebSub (PubSubHubbub) ping successful: HTTP {r.status}")
    except Exception as e:
        print(f"   [Notice] WebSub ping: {e}")

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
    update_sitemap(topic_meta, hero_img)
    update_rss(topic_meta, hero_img)
    ping_search_engines_and_hubs(f"https://ainews.krishnavibez.in/articles/{topic_meta['slug']}.html")

    # Update Global Search JSON index
    try:
        api_dir = os.path.join(PUBLIC_DIR, "api")
        os.makedirs(api_dir, exist_ok=True)
        api_file = os.path.join(api_dir, "articles.json")
        search_items = []
        if os.path.exists(api_file):
            with open(api_file, "r", encoding="utf-8") as af:
                search_items = json.load(af)
        new_entry = {
            "title": topic_meta["title"],
            "category": topic_meta["category"],
            "date": datetime.now(_IST).strftime("%B %d, %Y"),
            "url": f"/articles/{topic_meta['slug']}.html",
            "excerpt": topic_meta["meta_desc"],
            "badge": "LATEST"
        }
        if not any(a.get("url") == new_entry["url"] for a in search_items):
            search_items.insert(0, new_entry)
            with open(api_file, "w", encoding="utf-8") as af:
                json.dump(search_items, af, indent=2)
            print("✅ Updated /api/articles.json for Global Instant Search.")
    except Exception as e:
        print(f"   [Notice] Search index error: {e}")

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


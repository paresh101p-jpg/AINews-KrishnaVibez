import os, sys, re, json
from datetime import datetime

REPO_ROOT = r"E:\Paresh\Auto Post\AINews-KrishnaVibez"
sys.path.insert(0, REPO_ROOT)
from daily_ai_news_engine import assemble_full_article_page

orig_file = os.path.join(REPO_ROOT, "original_gta.html")
try:
    with open(orig_file, "r", encoding="utf-8") as f:
        text = f.read()
except Exception:
    with open(orig_file, "r", encoding="utf-16") as f:
        text = f.read()

# Locate article body
b_start = text.find('<div class="article-body">')
b_end = text.find('<!-- Article Footer -->', b_start)
body_html = text[b_start + len('<div class="article-body">'):b_end].strip()
if body_html.endswith("</div>"):
    body_html = body_html[:-6].strip()

print(f"Extracted original body! Word count: {len(body_html.split())}")

# The clean badged GTA 6 image URL (uploaded earlier with zero emoji square boxes and safe margins)
hero_img = "https://files.catbox.moe/8mlkp0.jpg"

topic_meta = {
    "slug": "gta-6-ai-revolution-rockstar-rage-9-neural-patents-npc-simulation",
    "title": "GTA 6 & The AI Revolution: How Rockstar’s RAGE 9 Neural Patents & Machine Learning NPCs Are Reinventing Open Worlds",
    "meta_desc": "An investigative breakdown of Rockstar's RAGE 9 engine, Patent US11684855B2, neural motion matching, and how machine learning simulation powers GTA 6's living world.",
    "category": "NEURAL GRAPHICS & AI",
    "keywords": "GTA 6, Grand Theft Auto VI, Rockstar Games, AI NPCs, RAGE 9, machine learning animation, simulation AI, patent US11684855B2, ray tracing, PS5 Pro PSSR, gaming AI",
    "read_time": "9 min read",
    "key_stats": "Patent US11684855B2 | Hierarchical NPC Graphs | Neural Motion Matching",
    "hero_img": hero_img,
    "pub_time_iso": "2026-11-22T11:39:34+05:30",
    "pub_date_display": "November 22, 2026"
}

# Assemble full standard article
full_page_html, _ = assemble_full_article_page(topic_meta, body_html)

target_file = os.path.join(REPO_ROOT, "public", "articles", "gta-6-ai-revolution-rockstar-rage-9-neural-patents-npc-simulation.html")
with open(target_file, "w", encoding="utf-8") as f:
    f.write(full_page_html)

print(f"Wrote complete article to {target_file}! File size: {os.path.getsize(target_file)} bytes.")

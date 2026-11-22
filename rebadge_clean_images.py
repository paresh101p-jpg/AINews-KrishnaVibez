# -*- coding: utf-8 -*-
import os, sys, json, re, glob

REPO_ROOT = r"E:\Paresh\Auto Post\AINews-KrishnaVibez"
sys.path.insert(0, REPO_ROOT)

from smart_image_matcher import select_best_image_for_article

PUBLIC_DIR = os.path.join(REPO_ROOT, "public")
ARTICLES_DIR = os.path.join(PUBLIC_DIR, "articles")
INDEX_FILE = os.path.join(PUBLIC_DIR, "index.html")
API_FILE = os.path.join(PUBLIC_DIR, "api", "articles.json")

with open(API_FILE, "r", encoding="utf-8") as f:
    articles = json.load(f)

updated_count = 0
for art in articles:
    slug = art["slug"]
    if slug.startswith("gta-6") or slug.startswith("openai-o3"):
        continue
    
    title = art["title"]
    category = art["category"]
    keywords = title + " " + category
    
    print(f"Re-badging {slug} without emoji boxes...")
    try:
        new_banner = select_best_image_for_article(title, category, keywords, slug)
        old_img = art["image"]
        art["image"] = new_banner
        
        # Replace in article HTML file
        art_path = os.path.join(ARTICLES_DIR, f"{slug}.html")
        if os.path.exists(art_path):
            with open(art_path, "r", encoding="utf-8") as f:
                c = f.read()
            c = c.replace(old_img, new_banner)
            with open(art_path, "w", encoding="utf-8") as f:
                f.write(c)
        updated_count += 1
        print(f"  -> New clean banner: {new_banner}")
    except Exception as e:
        print(f"  Error re-badging {slug}: {e}")

# Save updated API file
with open(API_FILE, "w", encoding="utf-8") as f:
    json.dump(articles, f, indent=2)

# Now rebuild index.html cards with the new clean banners!
cards_html = []
for art in articles:
    slug = art["slug"]
    title = art["title"]
    category = art["category"]
    desc = art["description"]
    img_url = art["image"]
    read_time = art.get("read_time", "7 min read")

    card = f"""      <article class="article-card" data-category="{category.lower()}">
        <div class="card-img-holder">
          <span class="category-tag">{category}</span>
          <a href="articles/{slug}.html">
            <img src="{img_url}" alt="{title}" width="600" height="338" loading="lazy">
          </a>
        </div>
        <div class="card-inner">
          <div class="card-meta">
            <span class="article-date">Nov 22, 2026</span>
            <span class="meta-dot">•</span>
            <span class="read-time">{read_time}</span>
          </div>
          <h3 class="card-title">
            <a href="articles/{slug}.html">{title}</a>
          </h3>
          <p class="card-excerpt">{desc}</p>
          <div class="card-footer">
            <span class="author">By Paresh Padsala</span>
            <a href="articles/{slug}.html" class="read-more">Read Full Report →</a>
          </div>
        </div>
      </article>"""
    cards_html.append(card)

with open(INDEX_FILE, "r", encoding="utf-8") as f:
    idx_content = f.read()

marker = '<div class="articles-grid">'
pos = idx_content.find(marker)
if pos != -1:
    depth = 0
    end_pos = -1
    for i in range(pos, len(idx_content)):
        if idx_content[i:i+4] == '<div':
            depth += 1
        elif idx_content[i:i+5] == '</div':
            depth -= 1
            if depth == 0:
                end_pos = i + 6
                break
    if end_pos != -1:
        new_grid = '<div class="articles-grid">\n' + '\n'.join(cards_html) + '\n    </div>'
        new_idx = idx_content[:pos] + new_grid + idx_content[end_pos:]
        with open(INDEX_FILE, "w", encoding="utf-8") as f:
            f.write(new_idx)
        print("Updated index.html with 100% clean, non-tofu cards!")

print(f"\nSUCCESS! Re-badged {updated_count} articles without square emoji boxes.")

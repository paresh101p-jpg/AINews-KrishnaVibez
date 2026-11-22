import glob, os, re, json

articles_dir = r"E:\Paresh\Auto Post\AINews-KrishnaVibez\public\articles"
index_file = r"E:\Paresh\Auto Post\AINews-KrishnaVibez\public\index.html"
api_file = r"E:\Paresh\Auto Post\AINews-KrishnaVibez\public\api\articles.json"

articles_data = []

for fpath in glob.glob(os.path.join(articles_dir, "*.html")):
    slug = os.path.splitext(os.path.basename(fpath))[0]
    with open(fpath, "r", encoding="utf-8", errors="ignore") as f:
        html = f.read()
    
    # Extract metadata
    m_title = re.search(r"<title>(.*?) \| AINews</title>", html)
    title = m_title.group(1).strip() if m_title else slug.replace("-", " ").title()
    
    m_desc = re.search(r'<meta\s+name=["\']description["\']\s+content=["\'](.*?)["\']', html)
    desc = m_desc.group(1).strip() if m_desc else ""
    
    m_cat = re.search(r'<span class=["\']article-kicker["\']>(.*?)</span>', html)
    cat = m_cat.group(1).strip() if m_cat else "ARTIFICIAL INTELLIGENCE"
    
    m_img = re.search(r'<meta\s+property=["\']og:image["\']\s+content=["\'](.*?)["\']', html)
    img = m_img.group(1).strip() if m_img else "https://ainews.krishnavibez.in/assets/logo.png"
    
    m_time = re.search(r'<meta\s+property=["\']article:published_time["\']\s+content=["\'](.*?)["\']', html)
    pub_iso = m_time.group(1).strip() if m_time else "2026-11-22T08:00:00+05:30"
    
    m_read = re.search(r'<span class=["\']article-read-time["\']>(.*?)</span>', html)
    read_time = m_read.group(1).strip() if m_read else "7 min read"
    
    articles_data.append({
        "slug": slug,
        "title": title,
        "description": desc,
        "category": cat,
        "image": img,
        "pub_iso": pub_iso,
        "read_time": read_time,
        "url": f"/articles/{slug}.html"
    })

# Sort newest first
articles_data.sort(key=lambda x: x["pub_iso"], reverse=True)
print(f"Parsed {len(articles_data)} articles.")

# Rebuild article cards for index.html
cards_html = []
for i, art in enumerate(articles_data):
    is_featured = "featured-lead-card" if i == 0 else ""
    card = f"""      <article class="article-card {is_featured}" data-category="{art['category'].lower()}">
        <a href="articles/{art['slug']}.html" class="card-image-link" aria-label="{art['title']}">
          <img src="{art['image']}" alt="{art['title']}" class="card-img" width="1200" height="675" loading="lazy">
        </a>
        <div class="card-content">
          <div class="card-meta">
            <span class="card-tag tag-ai">{art['category']}</span>
            <span class="meta-dot">•</span>
            <time datetime="{art['pub_iso']}">Nov 22, 2026</time>
            <span class="meta-dot">•</span>
            <span class="read-time">{art['read_time']}</span>
          </div>
          <h2 class="card-title">
            <a href="articles/{art['slug']}.html">{art['title']}</a>
          </h2>
          <p class="card-excerpt">{art['description']}</p>
          <div class="card-footer">
            <span class="byline">By <strong>Paresh Padsala</strong></span>
            <a href="articles/{art['slug']}.html" class="read-more-link">Read Full Report →</a>
          </div>
        </div>
      </article>"""
    cards_html.append(card)

# Update index.html
with open(index_file, "r", encoding="utf-8") as f:
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
        with open(index_file, "w", encoding="utf-8") as f:
            f.write(new_idx)
        print(f"Successfully injected all {len(cards_html)} cards into index.html!")

# Update api/articles.json
with open(api_file, "w", encoding="utf-8") as f:
    json.dump(articles_data, f, indent=2)
print(f"Updated api/articles.json with {len(articles_data)} articles.")

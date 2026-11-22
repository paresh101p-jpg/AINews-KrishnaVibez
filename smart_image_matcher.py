"""
smart_image_matcher.py
======================
100% Free Smart-Tagging Editorial Image Selection & Custom News Hook Engine.
Selects the 100% exact-match editorial photo from the verified AI Editorial Pool
based on semantic keyword scoring, category alignment, and least-recently-used rotation.
Renders the exact news headline and hook directly onto the image so readers are compelled to click.
"""

import os
import io
import json
import re
import urllib.request
import requests
from datetime import datetime
from PIL import Image, ImageDraw, ImageFont

POOL_FILE = os.path.join(os.path.dirname(__file__), "ai_editorial_pool.json")
FONT_BOLD = r"C:\Windows\Fonts\arialbd.ttf"
FONT_SEMI = r"C:\Windows\Fonts\segoeuib.ttf"

def load_editorial_pool():
    if not os.path.exists(POOL_FILE):
        return []
    try:
        with open(POOL_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        print(f"[Smart Image Matcher] Error loading pool: {e}")
        return []

def save_editorial_pool(pool):
    try:
        with open(POOL_FILE, "w", encoding="utf-8") as f:
            json.dump(pool, f, indent=2)
    except Exception as e:
        print(f"[Smart Image Matcher] Error saving pool: {e}")

def derive_hooks_from_title(title: str, category: str):
    parts = re.split(r"[:—–-]", title, maxsplit=1)
    if len(parts) == 2 and len(parts[0].strip()) >= 5:
        hook1 = parts[0].strip().upper()
        hook2 = parts[1].strip().upper()
    else:
        words = title.split()
        mid = max(1, len(words) // 2)
        hook1 = " ".join(words[:mid]).strip().upper()
        hook2 = " ".join(words[mid:]).strip().upper()

    if len(hook1) > 44: hook1 = hook1[:41] + "..."
    if len(hook2) > 50: hook2 = hook2[:47] + "..."

    badge_map = {
        "FRONTIER LLMS": ("REASONING FRONTIER", (244, 63, 94)),
        "ROBOTICS": ("ROBOTICS REPORT", (168, 85, 247)),
        "SILICON & GPUS": ("SILICON ARCHITECTURE", (6, 182, 212)),
        "AGENTS & CODING": ("AUTONOMOUS AGENTS", (16, 185, 129)),
        "AI INFRASTRUCTURE": ("HYPERSCALE CLUSTERS", (59, 130, 246)),
        "QUANTUM & SCIENCE": ("QUANTUM MILESTONE", (234, 179, 8)),
        "NEURAL GRAPHICS & AI": ("GAMING & SIMULATION AI", (244, 63, 94)),
        "OPEN SOURCE": ("OPEN WEIGHTS REPORT", (16, 185, 129)),
    }
    badge_info = badge_map.get(category.upper(), ("BREAKING REPORT", (239, 68, 68)))
    return badge_info[0], badge_info[1], hook1, hook2

def create_headline_hook_banner(base_url: str, title: str, category: str) -> str:
    """Downloads base image, renders exact news title hook, and uploads to Catbox CDN."""
    try:
        req = urllib.request.Request(base_url, headers={"User-Agent": "Mozilla/5.0"})
        raw_data = urllib.request.urlopen(req, timeout=25).read()
        img = Image.open(io.BytesIO(raw_data)).convert("RGB")
        
        target_w, target_h = 1200, 675
        img = img.resize((target_w, target_h), Image.Resampling.LANCZOS)
        
        overlay = Image.new("RGBA", (target_w, target_h), (0, 0, 0, 0))
        draw = ImageDraw.Draw(overlay)
        
        for y in range(target_h - 175, target_h):
            alpha = int(220 * ((y - (target_h - 175)) / 175.0)**1.25)
            draw.line([(0, y), (target_w, y)], fill=(10, 15, 26, alpha))
            
        font_badge = ImageFont.truetype(FONT_BOLD, 18)
        font_hook = ImageFont.truetype(FONT_BOLD, 36)
        font_sub = ImageFont.truetype(FONT_SEMI, 20)
        
        badge_text, badge_color, hook1, hook2 = derive_hooks_from_title(title, category)
        
        # Pill badge
        badge_pad_x, badge_pad_y = 16, 7
        bbox = draw.textbbox((0, 0), badge_text, font=font_badge)
        bw = bbox[2] - bbox[0] + badge_pad_x * 2 + 18
        bh = bbox[3] - bbox[1] + badge_pad_y * 2
        bx, by = 40, 36
        
        draw.rounded_rectangle([bx, by, bx + bw, by + bh], radius=bh//2, fill=(15, 23, 42, 235), outline=badge_color, width=2)
        draw.ellipse([bx + 14, by + bh//2 - 5, bx + 24, by + bh//2 + 5], fill=badge_color)
        draw.text((bx + 30, by + badge_pad_y - 2), badge_text, fill=(255, 255, 255, 255), font=font_badge)
        
        # Bottom headline hook
        draw.text((42, target_h - 110), hook1, fill=(0, 0, 0, 240), font=font_hook)
        draw.text((40, target_h - 112), hook1, fill=(255, 255, 255, 255), font=font_hook)
        
        draw.text((42, target_h - 60), hook2, fill=(0, 0, 0, 220), font=font_sub)
        draw.text((40, target_h - 62), hook2, fill=(56, 189, 248, 255), font=font_sub)
        
        final_img = Image.alpha_composite(img.convert("RGBA"), overlay).convert("RGB")
        buf = io.BytesIO()
        final_img.save(buf, format="JPEG", quality=92, optimize=True)
        buf.seek(0)
        
        resp = requests.post(
            "https://catbox.moe/user/api.php",
            data={"reqtype": "fileupload"},
            files={"fileToUpload": ("news_hook_banner.jpg", buf, "image/jpeg")},
            timeout=30
        )
        if resp.status_code == 200 and resp.text.startswith("http"):
            cat_url = resp.text.strip()
            print(f"   [Custom News Hook] Generated & Uploaded Banner: {cat_url}")
            return cat_url
    except Exception as e:
        print(f"   [Custom News Hook Notice] Error generating custom banner: {e}")
        
    return base_url

def select_best_image_for_article(title, category, content="", slug=""):
    """
    Selects the 100% best-matched image from the editorial pool.
    Updates usage tracking so images rotate seamlessly without repetition.
    Renders the exact news headline and hook directly onto the image.
    """
    pool = load_editorial_pool()
    if not pool:
        print("[Smart Image Matcher] Warning: Editorial pool is empty. Using fallback.")
        return "https://files.catbox.moe/sqqcuk.jpg"

    text_to_search = (f"{title} {category} {content[:1000]}").lower()
    clean_words = set(re.findall(r"\b[a-z0-9_-]{3,}\b", text_to_search))

    scored_candidates = []
    now_iso = datetime.utcnow().isoformat()

    for idx, item in enumerate(pool):
        score = 0
        cat_match = (item.get("category", "").upper() == category.upper())
        if cat_match:
            score += 20  # Big bonus for exact category match

        # Keyword matching
        keywords = item.get("keywords", [])
        matched_keywords = []
        for kw in keywords:
            kw_clean = kw.lower().strip()
            if kw_clean in text_to_search:
                score += 5
                matched_keywords.append(kw_clean)
            elif any(w == kw_clean for w in clean_words):
                score += 3
                matched_keywords.append(kw_clean)

        title_lower = title.lower()
        for kw in matched_keywords:
            if kw in title_lower:
                score += 8

        used_count = len(item.get("used_in_articles", []))
        recency_penalty = used_count * 2
        final_score = max(0, score - recency_penalty)

        scored_candidates.append({
            "index": idx,
            "id": item.get("id", f"img_{idx}"),
            "url": item.get("url", ""),
            "category": item.get("category", ""),
            "subtopic": item.get("subtopic", ""),
            "score": final_score,
            "matched_keywords": matched_keywords,
            "used_count": used_count
        })

    scored_candidates.sort(key=lambda x: (x["score"], -x["used_count"]), reverse=True)
    best = scored_candidates[0]
    
    print(f"\n[Smart Image Matcher] Best visual match for '{title[:50]}...':")
    print(f"   Selected ID: {best['id']} ({best['subtopic']})")
    print(f"   Score: {best['score']} | Matched: {best['matched_keywords'][:5]}")
    print(f"   Base Visual URL: {best['url']}")

    # Mark as used in pool
    best_idx = best["index"]
    if slug:
        if "used_in_articles" not in pool[best_idx]:
            pool[best_idx]["used_in_articles"] = []
        if slug not in pool[best_idx]["used_in_articles"]:
            pool[best_idx]["used_in_articles"].append(slug)
        pool[best_idx]["last_used_date"] = now_iso
        save_editorial_pool(pool)

    # Generate custom news headline hook on the image
    custom_hook_url = create_headline_hook_banner(best["url"], title, category)
    return custom_hook_url

if __name__ == "__main__":
    sample_title = "Figure 02 Humanoids Begin Full Assembly Shifts at BMW Spartanburg Plant"
    url = select_best_image_for_article(sample_title, "ROBOTICS", "humanoid robotics physical assembly", "test-figure-02")
    print("Final Custom Banner URL:", url)

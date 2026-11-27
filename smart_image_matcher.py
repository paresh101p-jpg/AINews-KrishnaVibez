"""
smart_image_matcher.py
======================
Next-Generation High-Precision Editorial Image Matcher & Dynamic Headline Hook Engine.
1. Strictly maps articles to true topic-specific editorial visuals (No repetitive blue graphics).
2. Deep entity recognition (Claude vs OpenAI vs Gemini vs DeepSeek vs Optimus vs Blackwell vs Devin).
3. Brand mismatch quarantine & strict recency isolation (Zero consecutive duplicate images).
4. Tier 1 Clean local visual priority with dynamic headline rendering.
"""

import os
import io
import json
import re
import random
import urllib.request
import requests
from datetime import datetime
from PIL import Image, ImageDraw, ImageFont

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
POOL_FILE = os.path.join(BASE_DIR, "ai_editorial_pool.json")
PUBLIC_DIR = os.path.join(BASE_DIR, "public")
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

def detect_article_entity(text: str) -> str:
    """Detects primary tech company, product, or domain entity."""
    t = text.lower()
    if re.search(r"\b(layoff|layoffs|hiring|reskilling|salary|salaries|workforce|recruitment|junior developer|junior engineer|career|careers|job market|employment|jobs)\b", t):
        return "jobs_careers"
    if re.search(r"\b(wall street|valuation|venture capital|capex|revenue|funding round|softbank|nasdaq|stock market|investor|investors|billions|vc funding)\b", t):
        return "finance_vc"
    if re.search(r"\b(us-china|embargo|white house|india|indiaai|eu ai act|sovereignty|export control|middle east|g42|mgx|sovereign ai|regulations)\b", t):
        return "geopolitics"
    if re.search(r"\b(cancer|drug discovery|alphafold|biology|clinical trial|protein|medicine|dna|therapeutics|healthcare|oncology)\b", t):
        return "biomedical"
    if re.search(r"\b(hollywood|cinema|filmmaker|vfx|sora|runway|video generation|virtual production|film studio)\b", t):
        return "entertainment"
    if re.search(r"\b(deepfake|scam|fraud|voice clone|voice cloning|lawsuit|copyright|phishing|malware|heist|court|countermeasures|hackers)\b", t):
        return "cybersecurity"
    if re.search(r"\b(claude|anthropic|sonnet|opus|haiku|dario amodei)\b", t):
        return "anthropic"
    if re.search(r"\b(gemini|deepmind|google|demis hassabis)\b", t):
        return "google"
    if re.search(r"\b(openai|o3|o1|gpt-5|strawberry|sam altman)\b", t):
        return "openai"
    if re.search(r"\b(deepseek|r1|deepseek-r1)\b", t):
        return "deepseek"
    if re.search(r"\b(llama|meta|zuckerberg)\b", t):
        return "meta"
    if re.search(r"\b(tesla|optimus|giga texas)\b", t):
        return "tesla_optimus"
    if re.search(r"\b(figure|figure 02|brett adcock)\b", t):
        return "figure"
    if re.search(r"\b(boston dynamics|atlas|spot)\b", t):
        return "boston_dynamics"
    if re.search(r"\b(blackwell|nvidia|b200|b300|rubin|jensen huang|nvlink)\b", t):
        return "nvidia"
    if re.search(r"\b(cerebras|cs-3|wafer-scale)\b", t):
        return "cerebras"
    if re.search(r"\b(cursor|windsurf|devin|cognition|swe-bench)\b", t):
        return "coding_agent"
    if re.search(r"\b(photonic|optical computing|laser|cpo|co-packaged optics)\b", t):
        return "photonics"
    if re.search(r"\b(power crisis|grid|nuclear|smr|gigawatt|megawatt|energy)\b", t):
        return "energy"
    if re.search(r"\b(gta 6|rockstar|rage 9)\b", t):
        return "gaming"
    if re.search(r"\b(sora|video generation|runway|gen-3|kling)\b", t):
        return "video"
    if re.search(r"\b(neuralink|bci|brain computer|brain chip)\b", t):
        return "bci"
    if re.search(r"\b(quantum|qubit|cryogenic|superconducting|dilution)\b", t):
        return "quantum"
    if re.search(r"\b(tsmc|asml|lithography|cleanroom|foundry|2nm|wafer)\b", t):
        return "foundry"
    return "general"

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

    if len(hook1) > 42: hook1 = hook1[:39] + "..."
    if len(hook2) > 48: hook2 = hook2[:45] + "..."

    badge_map = {
        "JOBS & CAREERS": ("WORKFORCE REPORT", (245, 158, 11)),
        "BUSINESS & FINANCE": ("MARKETS & CAPITAL", (34, 197, 94)),
        "WORLD & GEOPOLITICS": ("GLOBAL AI POLICY", (59, 130, 246)),
        "REAL-WORLD IMPACT": ("HUMAN APPLICATIONS", (20, 184, 166)),
        "ETHICS & SECURITY": ("CYBER DEFENSE & RISKS", (239, 68, 68)),
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

def create_headline_hook_banner(base_visual: str, title: str, category: str) -> str:
    """
    Downloads or opens base visual, draws dynamic headline & badge, uploads to Catbox CDN.
    Supports both remote URLs and local /images/... file paths.
    """
    try:
        if base_visual.startswith("/images/"):
            local_p = os.path.join(PUBLIC_DIR, base_visual.lstrip("/"))
            if os.path.exists(local_p):
                img = Image.open(local_p).convert("RGB")
            else:
                return base_visual
        elif base_visual.startswith("http"):
            req = urllib.request.Request(base_visual, headers={"User-Agent": "Mozilla/5.0"})
            raw_data = urllib.request.urlopen(req, timeout=25).read()
            img = Image.open(io.BytesIO(raw_data)).convert("RGB")
        else:
            return base_visual

        target_w, target_h = 1200, 675
        img = img.resize((target_w, target_h), Image.Resampling.LANCZOS)
        
        overlay = Image.new("RGBA", (target_w, target_h), (0, 0, 0, 0))
        draw = ImageDraw.Draw(overlay)
        
        # Subtle dark gradient at bottom for text contrast
        for y in range(target_h - 175, target_h):
            alpha = int(225 * ((y - (target_h - 175)) / 175.0)**1.25)
            draw.line([(0, y), (target_w, y)], fill=(8, 12, 22, alpha))
            
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
            print(f"   [Dynamic Hook Banner] Generated & Uploaded: {cat_url}")
            return cat_url
    except Exception as e:
        print(f"   [Dynamic Hook Notice] Error generating custom banner: {e}")
        
    return base_visual

def select_best_image_for_article(title: str, category: str, content: str = "", slug: str = "", render_headline: bool = True) -> str:
    """
    High-Precision Topic Matcher:
    1. Extracts target entity (Claude, OpenAI, Gemini, Blackwell, etc.).
    2. Penalizes brand mismatch (-100 pts) and recency reuse (-150 pts).
    3. Rewards exact entity (+70 pts), category match (+25 pts), and Tier 1 visuals.
    4. Renders dynamic headline hook so visual conveys the actual story.
    """
    pool = load_editorial_pool()
    if not pool:
        print("[Smart Image Matcher] Warning: Editorial pool is empty. Using fallback.")
        return "/images/frontier_llm.jpg"

    text_to_search = f"{title} {category} {content[:1200]}".lower()
    clean_words = set(re.findall(r"\b[a-z0-9_-]{3,}\b", text_to_search))
    title_words = set(re.findall(r"\b[a-z0-9_-]{3,}\b", title.lower()))
    
    target_entity = detect_article_entity(text_to_search)

    # Collect recently used images to enforce strict quarantine
    recently_used_ids = []
    for item in pool:
        used_list = item.get("used_in_articles", [])
        if used_list:
            recently_used_ids.append((item.get("id"), item.get("last_used_date", "")))
    recently_used_ids.sort(key=lambda x: x[1], reverse=True)
    recent_id_set_strict = set([x[0] for x in recently_used_ids[:4]])
    recent_id_set_soft = set([x[0] for x in recently_used_ids[4:12]])

    scored_candidates = []
    for idx, item in enumerate(pool):
        item_id = item.get("id", f"img_{idx}")
        score = 0

        # Category match
        if item.get("category", "").upper() == category.upper():
            score += 25

        # Entity matching
        item_entity = item.get("entity", "")
        if target_entity and target_entity != "general":
            if item_entity == target_entity:
                score += 75  # Huge boost for exact brand/product match!
            elif item_entity in ["anthropic", "google", "openai", "deepseek", "meta"] and item_entity != target_entity:
                score -= 120 # Strict penalty: Never mix Claude with OpenAI or Gemini!
            elif item_entity in ["tesla_optimus", "figure", "boston_dynamics"] and item_entity != target_entity:
                score -= 90  # Never mix Tesla Optimus with Boston Dynamics!

        # Keyword matching
        keywords = item.get("keywords", [])
        matched_keywords = []
        for kw in keywords:
            kw_clean = kw.lower().strip()
            if kw_clean in text_to_search:
                score += 8
                matched_keywords.append(kw_clean)
            elif kw_clean in title_words:
                score += 15
                matched_keywords.append(kw_clean)

        # Tier 1 Clean Image bonus
        if item.get("is_clean_tier1"):
            score += 22

        # Recency quarantine
        if item_id in recent_id_set_strict:
            score -= 160 # Banned from consecutive reuse
        elif item_id in recent_id_set_soft:
            score -= 60

        used_count = len(item.get("used_in_articles", []))
        score -= (used_count * 15)

        scored_candidates.append({
            "index": idx,
            "id": item_id,
            "url": item.get("url", ""),
            "category": item.get("category", ""),
            "subtopic": item.get("subtopic", ""),
            "score": score,
            "matched_keywords": matched_keywords,
            "used_count": used_count,
            "entity": item_entity
        })

    scored_candidates.sort(key=lambda x: (x["score"], -x["used_count"]), reverse=True)
    best = scored_candidates[0]

    print(f"\n[Smart Image Matcher] Best visual match for '{title[:50]}...':")
    print(f"   Selected ID: {best['id']} ({best['subtopic']} | {best['entity']})")
    print(f"   Score: {best['score']} | Matched: {best['matched_keywords'][:5]}")
    print(f"   Base Visual: {best['url']}")

    ENTITY_LOCAL_DEFAULTS = {
        "jobs_careers": "/images/autonomous_coding_agents.jpg",
        "finance_vc": "/images/datacenter_liquid_cooling_cluster.jpg",
        "geopolitics": "/images/cybersecurity_neural_shield_defense.jpg",
        "biomedical": "/images/healthcare_robots.jpg",
        "entertainment": "/images/sora_generative_video_holodeck_virtual.jpg",
        "cybersecurity": "/images/cybersecurity_neural_shield_defense.jpg",
        "tesla_optimus": "/images/humanoid_robot_gigafactory_assembly.jpg",
        "figure": "/images/humanoid_semiconductor_cleanroom.jpg",
        "boston_dynamics": "/images/dexterous_bipedal_robot_warehouse_logistics.jpg",
        "nvidia": "/images/blackwell_gpu_interposer_chip_macro.jpg",
        "cerebras": "/images/gpu_silicon_die_architecture.jpg",
        "energy": "/images/gigawatt_ai_datacenter_liquid_cooling.jpg",
        "foundry": "/images/semiconductor_fab_lithography.jpg",
        "quantum": "/images/quantum_cryogenic_chandelier.jpg"
    }

    base_img_url = best["url"]
    if target_entity in ENTITY_LOCAL_DEFAULTS and (best["score"] < 40 or best.get("entity") != target_entity):
        base_img_url = ENTITY_LOCAL_DEFAULTS[target_entity]
        print(f"   [Entity Override] Using dedicated high-res entity visual: {base_img_url}")

    # Mark as used in pool
    best_idx = best["index"]
    now_iso = datetime.utcnow().isoformat()
    if slug:
        if "used_in_articles" not in pool[best_idx]:
            pool[best_idx]["used_in_articles"] = []
        if slug not in pool[best_idx]["used_in_articles"]:
            pool[best_idx]["used_in_articles"].append(slug)
        pool[best_idx]["last_used_date"] = now_iso
        save_editorial_pool(pool)

    # Generate custom news headline hook banner
    if render_headline:
        custom_hook_url = create_headline_hook_banner(base_img_url, title, category)
        return custom_hook_url
    
    return base_img_url

if __name__ == "__main__":
    t = "Figure 02 Humanoids Complete 100,000 Hours of Autonomous Operation at BMW"
    url = select_best_image_for_article(t, "ROBOTICS", "figure 02 bmw humanoid manufacturing", "test-figure-02", render_headline=False)
    print("Selected Visual URL:", url)

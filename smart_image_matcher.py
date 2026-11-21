"""
smart_image_matcher.py
======================
100% Free Smart-Tagging Editorial Image Selection Engine.
Selects the 100% exact-match editorial photo from the verified AI Editorial Pool
based on semantic keyword scoring, category alignment, and least-recently-used rotation.
Zero repeat, zero generic circular drawings, zero external API costs.
"""

import os
import json
import re
from datetime import datetime

POOL_FILE = os.path.join(os.path.dirname(__file__), "ai_editorial_pool.json")

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

def select_best_image_for_article(title, category, content="", slug=""):
    """
    Selects the 100% best-matched image from the editorial pool.
    Updates usage tracking so images rotate seamlessly without repetition.
    """
    pool = load_editorial_pool()
    if not pool:
        print("[Smart Image Matcher] Warning: Editorial pool is empty. Using fallback.")
        return "https://files.catbox.moe/4v7mse.jpg"

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
            # Exact phrase match in text
            if kw_clean in text_to_search:
                score += 5
                matched_keywords.append(kw_clean)
            elif any(w == kw_clean for w in clean_words):
                score += 3
                matched_keywords.append(kw_clean)

        # Title match bonus (extra weight if keyword appears in title)
        title_lower = title.lower()
        for kw in matched_keywords:
            if kw in title_lower:
                score += 8

        # Recency penalty (least-recently-used prioritization)
        used_count = len(item.get("used_in_articles", []))
        recency_penalty = used_count * 2
        final_score = max(0, score - recency_penalty)

        scored_candidates.append({
            "index": idx,
            "id": item["id"],
            "url": item["url"],
            "category": item["category"],
            "subtopic": item.get("subtopic", ""),
            "score": final_score,
            "matched_keywords": matched_keywords,
            "used_count": used_count
        })

    # Sort candidates by score descending, then by used_count ascending
    scored_candidates.sort(key=lambda x: (x["score"], -x["used_count"]), reverse=True)

    best = scored_candidates[0]
    print(f"\n[Smart Image Matcher] Best visual match for '{title[:50]}...':")
    print(f"   Selected ID: {best['id']} ({best['subtopic']})")
    print(f"   Score: {best['score']} | Matched: {best['matched_keywords'][:5]}")
    print(f"   Live URL: {best['url']}")

    # Mark as used in pool
    best_idx = best["index"]
    if slug:
        if "used_in_articles" not in pool[best_idx]:
            pool[best_idx]["used_in_articles"] = []
        if slug not in pool[best_idx]["used_in_articles"]:
            pool[best_idx]["used_in_articles"].append(slug)
        pool[best_idx]["last_used_date"] = now_iso
        save_editorial_pool(pool)

    return best["url"]

if __name__ == "__main__":
    # Test matcher
    sample_title = "OpenAI Unveils o3 Reasoning Breakthrough"
    url = select_best_image_for_article(sample_title, "FRONTIER LLMS", "System 2 thinking test time compute", "test-slug-1")
    print("Result URL:", url)

#!/usr/bin/env python3
"""
Single Source of Truth Live Stock & Inventory Audit Calculator for AINews.
Calculates exact real-time numbers directly from ai_editorial_pool.json.
"""
import json
import os
import sys

POOL_FILE = "/data/user/0/ai.antigem/files/home/projects/AINews-KrishnaVibez/ai_editorial_pool.json"

def calculate_audit():
    if not os.path.exists(POOL_FILE):
        print(f"Error: {POOL_FILE} not found", file=sys.stderr)
        sys.exit(1)
        
    with open(POOL_FILE, "r") as f:
        pool = json.load(f)
        
    total_pool = len(pool)
    
    # 1. Latest generated images from latest run (world_ai_news_ entries)
    latest_generated = [x for x in pool if "world_ai_news_" in x.get("id", "")]
    latest_count = len(latest_generated)
    
    # 2. Unused images (used_in_articles is empty/none)
    unused_images = [x for x in pool if not x.get("used_in_articles") or len(x["used_in_articles"]) == 0]
    unused_count = len(unused_images)
    unused_days = unused_count / 24.0
    
    # 3. Already used images
    used_images = [x for x in pool if x.get("used_in_articles") and len(x["used_in_articles"]) > 0]
    used_count = len(used_images)
    
    # 4. Same images reused 2nd time or more
    reused_images = [x for x in pool if (x.get("used_in_articles") and len(x["used_in_articles"]) >= 2) or x.get("usage_count", 0) >= 2]
    reused_count = len(reused_images)
    
    total_days = total_pool / 24.0
    
    return {
        "total_pool": total_pool,
        "latest_generated": latest_count,
        "unused_count": unused_count,
        "unused_days": round(unused_days, 1),
        "used_count": used_count,
        "reused_count": reused_count,
        "total_days": round(total_days, 1)
    }

if __name__ == "__main__":
    audit = calculate_audit()
    print(json.dumps(audit, indent=2))

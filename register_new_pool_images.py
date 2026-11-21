#!/usr/bin/env python3
import os
import sys
import json
import shutil
import subprocess

REPO_DIR = "/data/user/0/ai.antigem/files/home/projects/AINews-KrishnaVibez"
POOL_FILE = os.path.join(REPO_DIR, "ai_editorial_pool.json")
MAP_FILE = os.path.join(REPO_DIR, "editorial_uploaded_map.json")
URLS_FILE = os.path.join(REPO_DIR, "editorial_catbox_urls.txt")
PUBLIC_IMG_DIR = os.path.join(REPO_DIR, "public", "images")

os.makedirs(PUBLIC_IMG_DIR, exist_ok=True)

def upload_to_catbox(file_path):
    cmd = [
        "curl", "-s",
        "-H", "User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
        "-F", "reqtype=fileupload",
        "-F", f"fileToUpload=@{file_path}",
        "https://catbox.moe/user/api.php"
    ]
    res = subprocess.run(cmd, capture_output=True, text=True)
    out = res.stdout.strip()
    if out.startswith("http"):
        return out
    raise RuntimeError(f"Catbox upload failed: {out} (stderr: {res.stderr})")

def register_image(img_path, img_id, category, badge, hook_title, hook_sub, subtopic, keywords):
    print(f"\n--- Processing: {img_id} ---")
    if not os.path.exists(img_path):
        print(f"Error: {img_path} not found!")
        return False

    # 1. Copy to public/images/
    dest_path = os.path.join(PUBLIC_IMG_DIR, f"{img_id}.jpg")
    shutil.copy2(img_path, dest_path)
    print(f"Copied locally to {dest_path}")

    # 2. Upload to Catbox
    print("Uploading to Catbox...")
    catbox_url = upload_to_catbox(dest_path)
    print(f"Uploaded to Catbox: {catbox_url}")

    # 3. Update editorial_uploaded_map.json
    upload_map = {}
    if os.path.exists(MAP_FILE):
        try:
            with open(MAP_FILE, "r", encoding="utf-8") as f:
                upload_map = json.load(f)
        except Exception:
            upload_map = {}
    upload_map[f"{img_id}.jpg"] = catbox_url
    with open(MAP_FILE, "w", encoding="utf-8") as f:
        json.dump(upload_map, f, indent=2)

    # 4. Append to editorial_catbox_urls.txt
    with open(URLS_FILE, "a", encoding="utf-8") as f:
        f.write(catbox_url + "\n")

    # 5. Update ai_editorial_pool.json
    pool = []
    if os.path.exists(POOL_FILE):
        with open(POOL_FILE, "r", encoding="utf-8") as f:
            pool = json.load(f)

    # Check if id already in pool
    existing = [item for item in pool if item.get("id") == img_id]
    if existing:
        print(f"Updating existing pool entry for {img_id}")
        existing[0]["url"] = catbox_url
        existing[0]["category"] = category
        existing[0]["badge"] = badge
        existing[0]["subtopic"] = subtopic
        existing[0]["hook_title"] = hook_title
        existing[0]["hook_sub"] = hook_sub
        existing[0]["keywords"] = keywords
    else:
        new_entry = {
            "id": img_id,
            "url": catbox_url,
            "category": category,
            "badge": badge,
            "subtopic": subtopic,
            "hook_title": hook_title,
            "hook_sub": hook_sub,
            "keywords": keywords,
            "used_in_articles": [],
            "last_used_date": None
        }
        pool.append(new_entry)

    with open(POOL_FILE, "w", encoding="utf-8") as f:
        json.dump(pool, f, indent=2)

    print(f"Registered {img_id} into pool (Total now: {len(pool)})")
    return True

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python3 register_new_pool_images.py <img_path> <metadata_json>")
        sys.exit(1)
    
    img_path = sys.argv[1]
    meta = json.loads(sys.argv[2])
    register_image(
        img_path=img_path,
        img_id=meta["id"],
        category=meta["category"],
        badge=meta["badge"],
        hook_title=meta["hook_title"],
        hook_sub=meta["hook_sub"],
        subtopic=meta["subtopic"],
        keywords=meta["keywords"]
    )

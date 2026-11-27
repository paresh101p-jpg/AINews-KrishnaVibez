import os
import re
import json
import time
import zipfile
import requests
from concurrent.futures import ThreadPoolExecutor, as_completed
from PIL import Image, ImageDraw, ImageFont

BASE_DIR = r"E:\Paresh\Auto Post\AINews-KrishnaVibez"
ZIP_PATH = r"C:\Users\Admin\OneDrive\Desktop\Nov 21 - 17_14.zip"
RAW_DIR = os.path.join(BASE_DIR, "raw_editorial_images")
PROCESSED_DIR = os.path.join(BASE_DIR, "processed_editorial_images")
MAP_FILE = os.path.join(BASE_DIR, "editorial_uploaded_map.json")
POOL_FILE = os.path.join(BASE_DIR, "ai_editorial_pool.json")
URLS_FILE = os.path.join(BASE_DIR, "editorial_catbox_urls.txt")

os.makedirs(RAW_DIR, exist_ok=True)
os.makedirs(PROCESSED_DIR, exist_ok=True)

FONT_BOLD = r"C:\Windows\Fonts\arialbd.ttf"
FONT_SEMI = r"C:\Windows\Fonts\segoeuib.ttf"

def extract_zip():
    print(f"📦 Extracting zip: {ZIP_PATH} ...")
    extracted = []
    with zipfile.ZipFile(ZIP_PATH, "r") as z:
        for member in z.infolist():
            if member.is_dir():
                continue
            fname = os.path.basename(member.filename)
            if not fname or fname.startswith("."):
                continue
            ext = os.path.splitext(fname)[1].lower()
            if ext in [".jpg", ".jpeg", ".png", ".webp"]:
                target_path = os.path.join(RAW_DIR, fname)
                if not os.path.exists(target_path) or os.path.getsize(target_path) != member.file_size:
                    with z.open(member) as source, open(target_path, "wb") as target:
                        target.write(source.read())
                extracted.append(target_path)
    print(f"✅ Extracted {len(extracted)} editorial images to {RAW_DIR}")
    return extracted

def classify_and_generate_hooks(filename: str):
    name_lower = filename.lower()
    
    # 1. Robotics
    if any(k in name_lower for k in ["robot", "humanoid", "bipedal", "dexterous", "actuator", "quadruped"]):
        category = "ROBOTICS"
        badge = "ROBOTICS REPORT"
        badge_color = (168, 85, 247) # Purple
        hook_title = "HUMANOID FLEET DEPLOYMENT & EMBODIED AI"
        hook_sub = "NEXT-GEN INDUSTRIAL REVOLUTION & PHYSICAL AGILITY"
        keywords = ["robot", "robotics", "humanoid", "figure", "tesla optimus", "boston dynamics", "atlas", "bipedal", "embodied ai", "automation", "factory", "assembly", "manipulation"]
        subtopic = "humanoid_robotics"
        
    # 2. Silicon & Hardware
    elif any(k in name_lower for k in ["silicon", "gpu", "chip", "wafer", "euv", "gaafet", "interposer", "transistor", "semiconductor"]):
        category = "SILICON & GPUS"
        badge = "SILICON ARCHITECTURE"
        badge_color = (6, 182, 212) # Cyan
        hook_title = "NEXT-GEN NEURAL PROCESSING SILICON"
        hook_sub = "2NM EUV LITHO & ULTRA-BANDWIDTH SCALING"
        keywords = ["silicon", "chip", "gpu", "nvidia", "blackwell", "tsmc", "semiconductor", "lithography", "wafer", "interposer", "transistor", "hbm", "hardware", "microchip"]
        subtopic = "semiconductor_silicon"

    # 3. Datacenters & Infrastructure
    elif any(k in name_lower for k in ["server", "datacenter", "rack", "immersion", "cool", "supercomput"]):
        category = "AI INFRASTRUCTURE"
        badge = "AI HYPERSCALE CLUSTERS"
        badge_color = (59, 130, 246) # Blue
        hook_title = "ENTERPRISE AI TRAINING CLUSTERS"
        hook_sub = "TWO-PHASE LIQUID COOLING & GIGA-WATT INFRASTRUCTURE"
        keywords = ["datacenter", "server", "supercomputer", "liquid cooling", "hyperscale", "infrastructure", "power", "cluster", "networking", "cooling"]
        subtopic = "datacenter_infrastructure"

    # 4. Quantum Computing
    elif any(k in name_lower for k in ["quantum", "cryogenic", "chandelier", "dilution", "superconduct"]):
        category = "QUANTUM & SCIENCE"
        badge = "QUANTUM BREAKTHROUGH"
        badge_color = (234, 179, 8) # Gold
        hook_title = "SUPERCONDUCTING QUANTUM MATRIX"
        hook_sub = "DILUTION CRYOGENIC PROCESSORS & COHERENCE"
        keywords = ["quantum", "cryogenic", "superconductor", "qubit", "dilution refrigerator", "quantum computing", "physics", "quantum supremacy"]
        subtopic = "quantum_computing"

    # 5. Coding & Autonomous Agents
    elif any(k in name_lower for k in ["agent", "coding", "devops", "software", "terminal", "engineer"]):
        category = "AGENTS & CODING"
        badge = "AUTONOMOUS AGENTS"
        badge_color = (16, 185, 129) # Emerald Green
        hook_title = "AUTONOMOUS SOFTWARE ENGINEERING SWARMS"
        hook_sub = "MULTI-AGENT ORCHESTRATION & COMPUTER USE"
        keywords = ["coding", "agent", "autonomous agents", "software engineering", "developer", "devops", "terminal", "swarm", "computer use", "ai coding"]
        subtopic = "software_agents"

    # 6. Frontier LLMs & Neural Reasoning
    else:
        category = "FRONTIER LLMS"
        badge = "REASONING FRONTIER"
        badge_color = (244, 63, 94) # Rose Red
        hook_title = "SYSTEM 2 DEEP REASONING MILESTONE"
        hook_sub = "TEST-TIME COMPUTE & AUTONOMOUS PROBLEM SOLVING"
        keywords = ["llm", "reasoning", "system 2", "openai", "gemini", "claude", "deepseek", "frontier model", "transformer", "neural network", "test-time compute", "artificial intelligence", "o3", "cot"]
        subtopic = "frontier_llm_reasoning"
        
    return category, badge, badge_color, hook_title, hook_sub, keywords, subtopic

def apply_editorial_overlay(raw_path: str, output_path: str):
    fname = os.path.basename(raw_path)
    category, badge_text, badge_color, hook_title, hook_sub, _, _ = classify_and_generate_hooks(fname)
    
    img = Image.open(raw_path).convert("RGB")
    target_w, target_h = 1200, 675
    img = img.resize((target_w, target_h), Image.Resampling.LANCZOS)
    
    # Remove Google Flow sparkle watermark from bottom right corner
    try:
        import cv2
        import numpy as np
        arr = np.array(img)
        mask = np.zeros((target_h, target_w), dtype=np.uint8)
        cv2.circle(mask, (target_w - 46, target_h - 46), 28, 255, -1)
        cleaned_arr = cv2.inpaint(arr, mask, 7, cv2.INPAINT_TELEA)
        img = Image.fromarray(cleaned_arr)
    except Exception:
        pass
    
    overlay = Image.new("RGBA", (target_w, target_h), (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)
    
    # Bottom vignette gradient for pristine text readability without obscuring main art
    for y in range(target_h - 170, target_h):
        alpha = int(215 * ((y - (target_h - 170)) / 170.0)**1.25)
        draw.line([(0, y), (target_w, y)], fill=(10, 15, 26, alpha))
        
    font_badge = ImageFont.truetype(FONT_BOLD, 18)
    font_hook = ImageFont.truetype(FONT_BOLD, 36)
    font_sub = ImageFont.truetype(FONT_SEMI, 20)
    
    # 1. Top-Left Pill Badge
    badge_pad_x, badge_pad_y = 16, 7
    bbox = draw.textbbox((0, 0), badge_text, font=font_badge)
    bw = bbox[2] - bbox[0] + badge_pad_x * 2 + 18
    bh = bbox[3] - bbox[1] + badge_pad_y * 2
    bx, by = 40, 36
    
    draw.rounded_rectangle([bx, by, bx + bw, by + bh], radius=bh//2, fill=(15, 23, 42, 235), outline=badge_color, width=2)
    # Status dot
    draw.ellipse([bx + 14, by + bh//2 - 5, bx + 24, by + bh//2 + 5], fill=badge_color)
    draw.text((bx + 30, by + badge_pad_y - 2), badge_text, fill=(255, 255, 255, 255), font=font_badge)
    
    # 2. Bottom Hook Headlines
    # Drop shadow
    draw.text((42, target_h - 110), hook_title, fill=(0, 0, 0, 240), font=font_hook)
    draw.text((40, target_h - 112), hook_title, fill=(255, 255, 255, 255), font=font_hook)
    
    draw.text((42, target_h - 60), hook_sub, fill=(0, 0, 0, 220), font=font_sub)
    draw.text((40, target_h - 62), hook_sub, fill=(56, 189, 248, 255), font=font_sub)
    
    final_img = Image.alpha_composite(img.convert("RGBA"), overlay).convert("RGB")
    final_img.save(output_path, "JPEG", quality=92, optimize=True)

def upload_single_to_catbox(file_path: str, max_retries=4) -> tuple:
    fname = os.path.basename(file_path)
    url = "https://catbox.moe/user/api.php"
    for attempt in range(max_retries):
        try:
            with open(file_path, "rb") as f:
                resp = requests.post(
                    url,
                    data={"reqtype": "fileupload"},
                    files={"fileToUpload": f},
                    timeout=45
                )
            if resp.status_code == 200 and resp.text.startswith("http"):
                cat_url = resp.text.strip()
                return fname, cat_url
            else:
                time.sleep(2)
        except Exception:
            time.sleep(3)
    return fname, ""

def main():
    raw_files = extract_zip()
    
    print("\n🎨 Generating editorial typography & high-CTR hooks for all images...")
    processed_files = []
    for idx, rpath in enumerate(raw_files):
        fname = os.path.basename(rpath)
        out_path = os.path.join(PROCESSED_DIR, fname)
        if not os.path.exists(out_path):
            apply_editorial_overlay(rpath, out_path)
        processed_files.append(out_path)
        if (idx + 1) % 50 == 0 or (idx + 1) == len(raw_files):
            print(f"   [{idx + 1}/{len(raw_files)}] Styled with CTR hook badge: {fname[:35]}...")

    # Load uploaded map
    uploaded_map = {}
    if os.path.exists(MAP_FILE):
        try:
            with open(MAP_FILE, "r", encoding="utf-8") as f:
                uploaded_map = json.load(f)
        except Exception:
            uploaded_map = {}

    pending = [p for p in processed_files if os.path.basename(p) not in uploaded_map]
    print(f"\n🚀 Catbox CDN Upload Phase: Total {len(processed_files)} | Already Uploaded: {len(uploaded_map)} | Pending: {len(pending)}")
    
    if pending:
        start_time = time.time()
        completed = 0
        with ThreadPoolExecutor(max_workers=10) as executor:
            future_to_file = {executor.submit(upload_single_to_catbox, p): p for p in pending}
            for future in as_completed(future_to_file):
                fname, cat_url = future.result()
                completed += 1
                if cat_url:
                    uploaded_map[fname] = cat_url
                    if completed % 25 == 0 or completed == len(pending):
                        print(f"   [{completed}/{len(pending)}] Uploaded: {fname[:35]}... -> {cat_url}")
                        with open(MAP_FILE, "w", encoding="utf-8") as f:
                            json.dump(uploaded_map, f, indent=2)
                else:
                    print(f"   ❌ Failed to upload: {fname}")
        elapsed = time.time() - start_time
        print(f"✅ Upload completed in {elapsed:.1f}s! Total mapped: {len(uploaded_map)}")
        with open(MAP_FILE, "w", encoding="utf-8") as f:
            json.dump(uploaded_map, f, indent=2)

    # Load and enrich ai_editorial_pool.json
    pool = []
    if os.path.exists(POOL_FILE):
        try:
            with open(POOL_FILE, "r", encoding="utf-8") as f:
                pool = json.load(f)
        except Exception:
            pool = []
            
    existing_ids = {item.get("id") for item in pool}
    existing_urls = {item.get("url") for item in pool}
    
    new_pool_items = 0
    all_urls = []
    for ppath in processed_files:
        fname = os.path.basename(ppath)
        cat_url = uploaded_map.get(fname)
        if not cat_url:
            continue
        all_urls.append(cat_url)
        
        item_id = os.path.splitext(fname)[0]
        if item_id in existing_ids or cat_url in existing_urls:
            continue
            
        category, badge_text, _, hook_title, hook_sub, keywords, subtopic = classify_and_generate_hooks(fname)
        
        entry = {
            "id": item_id,
            "url": cat_url,
            "category": category,
            "badge": badge_text,
            "subtopic": subtopic,
            "hook_title": hook_title,
            "hook_sub": hook_sub,
            "keywords": keywords,
            "used_in_articles": [],
            "last_used_date": None
        }
        pool.append(entry)
        existing_ids.add(item_id)
        existing_urls.add(cat_url)
        new_pool_items += 1

    with open(POOL_FILE, "w", encoding="utf-8") as f:
        json.dump(pool, f, indent=2)
        
    with open(URLS_FILE, "w", encoding="utf-8") as f:
        f.write("\n".join(all_urls) + "\n")
        
    print("\n" + "="*60)
    print(f"🎉 SUCCESS: ai_editorial_pool.json now has {len(pool)} total categorized editorial visuals!")
    print(f"🎉 New items added this run: {new_pool_items}")
    print(f"🎉 Catbox URLs written to {URLS_FILE}")
    print("="*60)
    
    # Delete the zip file from Desktop as instructed by user
    if os.path.exists(ZIP_PATH):
        try:
            os.remove(ZIP_PATH)
            print(f"🗑️ Successfully deleted Desktop zip file: {ZIP_PATH}")
        except Exception as e:
            print(f"⚠️ Notice deleting zip file: {e}")

if __name__ == "__main__":
    main()

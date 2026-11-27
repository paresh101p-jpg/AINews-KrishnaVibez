#!/usr/bin/env python3
"""
Upload World AI News images to Catbox CDN
Usage: python3 upload_to_catbox.py
"""

import os
import json
import base64
import time
from datetime import datetime

PROJECT_DIR = "/data/user/0/ai.antigem/files/home/projects/AINews-KrishnaVibez"
IMAGES_DIR = f"{PROJECT_DIR}/public/images/world_ai_news"
UPLOAD_TRACKING = f"{PROJECT_DIR}/world_ai_images_uploaded.json"
POOL_FILE = f"{PROJECT_DIR}/ai_editorial_pool.json"
STATE_FILE = f"{PROJECT_DIR}/.ainews_image_state.json"

def upload_file_to_catbox(file_path):
    """Upload a file to Catbox.moe and return the URL"""
    import requests
    
    url = 'https://catbox.moe/user/api.php'
    
    try:
        with open(file_path, 'rb') as f:
            data = {'reqtype': 'fileupload'}
            files = {'fileToUpload': (os.path.basename(file_path), f, 'image/jpeg')}
            headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36'}
            response = requests.post(url, data=data, files=files, headers=headers, timeout=60)
        
        if response.status_code == 200:
            catbox_url = response.text.strip()
            if catbox_url.startswith('https://files.catbox.moe/'):
                return catbox_url
        print(f"  Unexpected response: {response.status_code} {response.text[:200]}")
        return None
    except Exception as e:
        print(f"Upload error: {e}")
        return None

def main():
    print("=" * 60)
    print("AINews World AI Images - Catbox Upload Script")
    print("=" * 60)
    
    # Check if images directory exists
    if not os.path.exists(IMAGES_DIR):
        print(f"✗ Images directory not found: {IMAGES_DIR}")
        print("  Run image generation first")
        return 1
    
    # List available images
    local_files = sorted([f for f in os.listdir(IMAGES_DIR) if f.endswith('.jpg')])
    
    if not local_files:
        print(f"✗ No images found in {IMAGES_DIR}")
        return 1
    
    print(f"\nFound {len(local_files)} images to upload")
    
    # Load tracking data
    with open(UPLOAD_TRACKING, 'r') as f:
        tracking = json.load(f)
    
    # Load pool
    with open(POOL_FILE, 'r') as f:
        pool = json.load(f)
    
    # Load state
    with open(STATE_FILE, 'r') as f:
        state = json.load(f)
    
    # Create mapping of local files to tracking entries
    file_to_entry = {}
    for entry in tracking.get('entries', []):
        file_to_entry[f"world_ai_news_{entry['news_index']}_img{entry['image_number']}.jpg"] = entry
    
    # Upload process
    uploaded_count = 0
    skipped_count = 0
    
    print(f"\n📤 Starting upload process...")
    
    for local_file in local_files:
        local_path = os.path.join(IMAGES_DIR, local_file)
        
        # Check if already uploaded
        if local_file in file_to_entry:
            entry = file_to_entry[local_file]
            if entry.get('catbox_url'):
                print(f"  ✓ Already uploaded: {local_file}")
                skipped_count += 1
                continue
        
        print(f"\n  Uploading: {local_file}")
        
        # Upload to Catbox
        catbox_url = upload_file_to_catbox(local_path)
        
        if catbox_url:
            print(f"    ✓ Uploaded: {catbox_url}")
            
            # Update tracking
            if local_file in file_to_entry:
                entry = file_to_entry[local_file]
                entry['catbox_url'] = catbox_url
                entry['status'] = 'uploaded'
                entry['uploaded_at'] = datetime.now().isoformat()
            
            # Update pool
            import re
            m = re.search(r'world_ai_news_(\d+)_img(\d+)\.jpg$', local_file)
            if m:
                expected_id = f"world_ai_news_{m.group(1)}_img{m.group(2)}"
                for item in pool:
                    if item.get('id') == expected_id:
                        item['url'] = catbox_url
                        item['status'] = 'active'
                        item['cdn_uploaded'] = True
                        item['uploaded_at'] = datetime.now().isoformat()
                        break
            
            uploaded_count += 1
        else:
            print(f"    ✗ Upload failed: {local_file}")
    
    # Save updates
    with open(UPLOAD_TRACKING, 'w') as f:
        json.dump(tracking, f, indent=2, ensure_ascii=False)
    
    with open(POOL_FILE, 'w') as f:
        json.dump(pool, f, indent=2, ensure_ascii=False)
    
    # Update state
    state['status'] = 'completed'
    state['images_uploaded'] = uploaded_count
    state['last_run_timestamp'] = time.time()
    state['last_run_date'] = datetime.now().isoformat()
    
    with open(STATE_FILE, 'w') as f:
        json.dump(state, f, indent=2)
    
    # Summary
    print(f"\n{'=' * 60}")
    print(f"📈 UPLOAD SUMMARY")
    print(f"{'=' * 60}")
    print(f"   New uploads:     {uploaded_count}")
    print(f"   Skipped (done):  {skipped_count}")
    print(f"   Status:          completed")
    print(f"{'=' * 60}")
    
    return 0

if __name__ == "__main__":
    exit(main())
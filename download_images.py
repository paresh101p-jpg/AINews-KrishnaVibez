#!/usr/bin/env python3
"""
Download and upload generated Google Flow images
Usage: python3 download_images.py
"""

import os
import json
import base64
from datetime import datetime

PROJECT_DIR = "/data/user/0/ai.antigem/files/home/projects/AINews-KrishnaVibez"
IMAGES_DIR = f"{PROJECT_DIR}/public/images/world_ai_news"
UPLOAD_TRACKING = f"{PROJECT_DIR}/world_ai_images_uploaded.json"
POOL_FILE = f"{PROJECT_DIR}/ai_editorial_pool.json"
STATE_FILE = f"{PROJECT_DIR}/.ainews_image_state.json"

def ensure_dir():
    os.makedirs(IMAGES_DIR, exist_ok=True)
    print(f"✓ Ensured directory exists: {IMAGES_DIR}")

def load_tracking():
    with open(UPLOAD_TRACKING, 'r') as f:
        return json.load(f)

def load_pool():
    with open(POOL_FILE, 'r') as f:
        return json.load(f)

def load_state():
    with open(STATE_FILE, 'r') as f:
        return json.load(f)

def save_pool(pool):
    with open(POOL_FILE, 'w') as f:
        json.dump(pool, f, indent=2, ensure_ascii=False)

def save_tracking(tracking):
    with open(UPLOAD_TRACKING, 'w') as f:
        json.dump(tracking, f, indent=2, ensure_ascii=False)

def save_state(state):
    state['last_run_timestamp'] = datetime.now().timestamp()
    state['last_run_date'] = datetime.now().isoformat()
    with open(STATE_FILE, 'w') as f:
        json.dump(state, f, indent=2)

def list_downloaded_images():
    """List locally downloaded images"""
    if os.path.exists(IMAGES_DIR):
        files = [f for f in os.listdir(IMAGES_DIR) if f.endswith('.jpg')]
        print(f"\nFound {len(files)} downloaded images:")
        for f in files[:10]:
            print(f"  {f}")
        if len(files) > 10:
            print(f"  ... and {len(files) - 10} more")
        return files
    return []

def process_downloaded():
    """Process downloaded images and update tracking"""
    tracking = load_tracking()
    pool = load_pool()
    state = load_state()
    
    downloaded = list_downloaded_images()
    
    if not downloaded:
        print("\nNo images found in public/images/world_ai_news/")
        print("Please download images from Google Flow first.")
        return 0
    
    updated_count = 0
    for entry in tracking.get('entries', []):
        # Find matching downloaded file
        entry_id = entry['id']  # e.g., world_ai_news_1_img1
        expected_file = f"{entry_id}.jpg"
        
        if expected_file in downloaded:
            # Update with local file info
            local_path = f"{IMAGES_DIR}/{expected_file}"
            entry['local_path'] = local_path
            entry['status'] = 'downloaded'
            entry['downloaded_at'] = datetime.now().isoformat()
            
            # Update pool
            for pool_item in pool:
                if pool_item.get('id') == entry_id:
                    pool_item['url'] = f'/images/world_ai_news/{expected_file}'
                    pool_item['local_file'] = expected_file
                    pool_item['status'] = 'downloaded'
                    pool_item['downloaded_at'] = datetime.now().isoformat()
                    break
            
            updated_count += 1
    
    # Save updates
    save_pool(pool)
    save_tracking(tracking)
    save_state({**state, 'status': 'images_downloaded', 'images_ready': updated_count})
    
    print(f"\n✓ Processed {updated_count} images")
    print(f"✓ Updated ai_editorial_pool.json")
    print(f"✓ Updated world_ai_images_uploaded.json")
    
    return updated_count

def upload_to_catbox():
    """Upload images to Catbox CDN"""
    import requests
    
    tracking = load_tracking()
    pool = load_pool()
    
    upload_count = 0
    for entry in tracking.get('entries', []):
        if entry.get('status') != 'downloaded':
            continue
        
        expected_file = f"{entry['id']}.jpg"
        local_path = f"{IMAGES_DIR}/{expected_file}"
        
        if not os.path.exists(local_path):
            continue
        
        try:
            with open(local_path, 'rb') as f:
                files = {'file': (expected_file, f, 'image/jpeg')}
                response = requests.post('https://catbox.moe/upload', files=files, timeout=30)
            
            if response.status_code == 200:
                result = response.json()
                if result.get('status') == 'success':
                    catbox_url = result.get('url', '')
                    
                    # Update tracking
                    entry['catbox_url'] = catbox_url
                    entry['upload_status'] = 'uploaded'
                    entry['uploaded_at'] = datetime.now().isoformat()
                    
                    # Update pool
                    for pool_item in pool:
                        if pool_item.get('id') == entry['id']:
                            pool_item['url'] = catbox_url
                            pool_item['status'] = 'active'
                            pool_item['cdn_uploaded'] = True
                            pool_item['uploaded_at'] = datetime.now().isoformat()
                            break
                    
                    upload_count += 1
                    print(f"✓ Uploaded: {expected_file}")
                    
        except Exception as e:
            print(f"✗ Upload failed for {expected_file}: {e}")
    
    save_pool(pool)
    save_tracking(tracking)
    
    print(f"\n✓ Uploaded {upload_count} images to Catbox")
    return upload_count

if __name__ == "__main__":
    import sys
    
    print("=" * 60)
    print("AINews Image Download & Upload Script")
    print("=" * 60)
    
    ensure_dir()
    
    if len(sys.argv) > 1 and sys.argv[1] == 'upload':
        upload_to_catbox()
    else:
        process_downloaded()
    
    print("\nDone!")
import os, sys, json, shutil, requests, time

NEW_IMAGES = [
    {
        'path': r'C:\Users\Admin\.gemini\antigravity\brain\5edf39f6-759b-4d35-b525-27352f306f0f\ai_swarm_intelligence_mesh_1795326212935.jpg',
        'key': 'ai_swarm_intelligence_mesh',
        'category': 'AGENTS & CODING',
        'keywords': ['swarm', 'multi-agent', 'autonomous agents', 'mesh', 'workflow', 'intelligence', 'reasoning', 'orchestration', 'devin', 'claude', 'coding'],
        'description': 'Cybernetic command lab visualizing multi-agent AI swarm topologies and real-time code synthesis workflows.'
    },
    {
        'path': r'C:\Users\Admin\.gemini\antigravity\brain\5edf39f6-759b-4d35-b525-27352f306f0f\humanoid_semiconductor_cleanroom_1795326224637.jpg',
        'key': 'humanoid_semiconductor_cleanroom',
        'category': 'ROBOTICS',
        'keywords': ['humanoid', 'robot', 'robotics', 'cleanroom', 'semiconductor', 'silicon wafer', 'precision', 'bipedal', 'manufacturing', 'tesla optimus', 'figure'],
        'description': 'Advanced bipedal humanoid robot inspecting silicon semiconductor wafer in ISO cleanroom facility.'
    },
    {
        'path': r'C:\Users\Admin\.gemini\antigravity\brain\5edf39f6-759b-4d35-b525-27352f306f0f\cpo_silicon_photonics_chip_v2_1795326281132.jpg',
        'key': 'cpo_silicon_photonics_chip_v2',
        'category': 'SILICON & GPUS',
        'keywords': ['silicon photonics', 'cpo', 'co-packaged optics', 'laser interconnect', 'chip', 'gpu', 'accelerator', 'tsmc', 'nvidia', 'packaging', 'optical computing'],
        'description': 'Co-Packaged Optics AI accelerator chip with cyan and violet silicon photonic waveguides and micro-circuitry.'
    },
    {
        'path': r'C:\Users\Admin\.gemini\antigravity\brain\5edf39f6-759b-4d35-b525-27352f306f0f\cpo_silicon_photonics_chip_1795326256924.jpg',
        'key': 'cpo_silicon_photonics_chip_bench',
        'category': 'SILICON & GPUS',
        'keywords': ['silicon', 'chip', 'photonics', 'packaging', 'hardware', 'semiconductor', 'die', 'microchip', 'optics'],
        'description': 'Silicon photonics multi-die accelerator package with fiber interconnect laser beams on laboratory bench.'
    },
    {
        'path': r'C:\Users\Admin\.gemini\antigravity\brain\5edf39f6-759b-4d35-b525-27352f306f0f\frontier_ai_reasoning_architecture_1795326304616.jpg',
        'key': 'frontier_ai_reasoning_architecture',
        'category': 'FRONTIER LLMS',
        'keywords': ['frontier llms', 'reasoning', 'inference', 'o3', 'o1', 'claude', 'tree of thought', 'deep thinking', 'mathematical logic', 'gpt-5', 'deepseek'],
        'description': 'AI researcher analyzing tree-of-thought branching logic networks and mathematical inference paths on transparent curved glass.'
    },
    {
        'path': r'C:\Users\Admin\.gemini\antigravity\brain\5edf39f6-759b-4d35-b525-27352f306f0f\gigawatt_ai_datacenter_liquid_cooling_1795326324356.jpg',
        'key': 'gigawatt_ai_datacenter_liquid_cooling',
        'category': 'AI INFRASTRUCTURE',
        'keywords': ['datacenter', 'liquid cooling', 'supercomputer', 'gigawatt', 'cluster', 'gpu racks', 'energy', 'power', 'infrastructure', 'hyperscale'],
        'description': 'Enterprise AI supercomputing facility with direct-to-chip liquid cooling manifolds carrying vibrant blue coolant.'
    }
]

dest_dir = r'E:\Paresh\Auto Post\AINews-KrishnaVibez\public\images'
os.makedirs(dest_dir, exist_ok=True)

def upload_to_catbox(file_path):
    url = 'https://catbox.moe/user/api.php'
    with open(file_path, 'rb') as f:
        data = {'reqtype': 'fileupload'}
        files = {'fileToUpload': (os.path.basename(file_path), f, 'image/jpeg')}
        resp = requests.post(url, data=data, files=files, timeout=45)
    if resp.status_code == 200 and resp.text.startswith('http'):
        return resp.text.strip()
    raise RuntimeError(f'Catbox failed: {resp.status_code} {resp.text}')

pool_file = r'E:\Paresh\Auto Post\AINews-KrishnaVibez\ai_editorial_pool.json'
with open(pool_file, 'r', encoding='utf-8') as f:
    pool = json.load(f)

urls_txt_file = r'E:\Paresh\Auto Post\AINews-KrishnaVibez\editorial_catbox_urls.txt'
with open(urls_txt_file, 'r', encoding='utf-8') as f:
    existing_urls = set(f.read().splitlines())

added_count = 0
for item in NEW_IMAGES:
    src = item['path']
    key = item['key']
    if not os.path.exists(src):
        print(f'Skipping missing: {src}')
        continue
    
    local_dest = os.path.join(dest_dir, f"{key}.jpg")
    shutil.copy2(src, local_dest)
    
    # Upload to Catbox
    try:
        catbox_url = upload_to_catbox(local_dest)
        print(f'Uploaded {key}: {catbox_url}')
    except Exception as e:
        print(f'Upload error for {key}: {e}')
        catbox_url = f'https://ainews.krishnavibez.in/images/{key}.jpg'
    
    # Add to pool
    pool_entry = {
        'url': catbox_url,
        'local_file': local_dest,
        'category': item['category'],
        'keywords': item['keywords'],
        'description': item['description'],
        'usage_count': 0,
        'added_at': time.strftime('%Y-%m-%d %H:%M:%S')
    }
    pool.append(pool_entry)
    existing_urls.add(catbox_url)
    added_count += 1

with open(pool_file, 'w', encoding='utf-8') as f:
    json.dump(pool, f, indent=2)

with open(urls_txt_file, 'w', encoding='utf-8') as f:
    f.write('\n'.join(sorted(existing_urls)) + '\n')

print(f'\nSUCCESS! Registered {added_count} new images. Total in pool: {len(pool)}')

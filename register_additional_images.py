import shutil
import os
import requests
import json

dest_dir = r"e:\Paresh\Auto Post\AINews-KrishnaVibez\public\images"
pool_file = r"e:\Paresh\Auto Post\AINews-KrishnaVibez\ai_editorial_pool.json"

with open(pool_file, "r", encoding="utf-8") as f:
    pool = json.load(f)

def upload_to_catbox(file_path):
    url = "https://catbox.moe/user/api.php"
    for attempt in range(4):
        try:
            with open(file_path, "rb") as f:
                data = {"reqtype": "fileupload"}
                files = {"fileToUpload": (os.path.basename(file_path), f, "image/jpeg")}
                resp = requests.post(url, data=data, files=files, timeout=45)
            if resp.status_code == 200 and resp.text.startswith("http"):
                return resp.text.strip()
        except Exception as e:
            print(f"Retry {attempt+1} on {file_path}: {e}")
            import time
            time.sleep(2)
    raise RuntimeError(f"Catbox upload failed after 4 attempts")

ADDITIONAL = [
    {
        "id": "gpu_silicon_die_architecture",
        "src": r"C:\Users\Admin\.gemini\antigravity\brain\5edf39f6-759b-4d35-b525-27352f306f0f\gpu_silicon_die_architecture_1795255134041.jpg",
        "category": "SILICON & GPUS",
        "subtopic": "gpu_microarchitecture_silicon_die",
        "keywords": ["gpu die", "microarchitecture", "blackwell", "hopper", "cuda", "tensor core", "silicon die", "transistor", "semiconductor packaging", "heat spreader", "interconnect", "b200", "h200", "hbm3e", "memory bandwidth"]
    },
    {
        "id": "industrial_quadruped_substation",
        "src": r"C:\Users\Admin\.gemini\antigravity\brain\5edf39f6-759b-4d35-b525-27352f306f0f\industrial_quadruped_substation_1795255131906.jpg",
        "category": "ROBOTICS",
        "subtopic": "industrial_quadruped_patrol",
        "keywords": ["quadruped", "robot dog", "boston dynamics", "spot", "patrol", "substation", "utility", "thermal camera", "inspection robot", "autonomous inspection", "infrastructure", "field robotics"]
    },
    {
        "id": "neuralink_bci_microthread_chip",
        "src": r"C:\Users\Admin\.gemini\antigravity\brain\5edf39f6-759b-4d35-b525-27352f306f0f\bci_neural_implant_editorial_1795255167464.jpg",
        "category": "FRONTIER LLMS",
        "subtopic": "brain_computer_interfaces_neurotech",
        "keywords": ["bci", "neuralink", "brain computer interface", "neural implant", "micro-thread", "neurotechnology", "brain chip", "paralysis", "motor cortex", "biocompatible", "synapse", "neuroscience"]
    }
]

for item in ADDITIONAL:
    dest_path = os.path.join(dest_dir, f"{item['id']}.jpg")
    shutil.copy2(item["src"], dest_path)
    catbox_url = upload_to_catbox(dest_path)
    print(f"Uploaded {item['id']} -> {catbox_url}")
    
    pool.append({
        "id": item["id"],
        "url": catbox_url,
        "category": item["category"],
        "subtopic": item["subtopic"],
        "keywords": item["keywords"],
        "used_in_articles": []
    })

with open(pool_file, "w", encoding="utf-8") as f:
    json.dump(pool, f, indent=2)

print(f"Total entries in ai_editorial_pool.json: {len(pool)}")

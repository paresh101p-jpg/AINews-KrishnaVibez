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

BATCH = [
    {
        "path": "/data/user/0/ai.antigem/files/home/.gemini/antigravity-cli/brain/2d100a0d-ec88-486f-9c47-32ba30a6f4ec/humanoid_robot_gigafactory_1795277790532.jpg",
        "id": "humanoid_robot_gigafactory_assembly",
        "category": "ROBOTICS",
        "badge": "ROBOTICS REPORT",
        "subtopic": "humanoid_robotics",
        "hook_title": "HUMANOID FLEET DEPLOYMENT & EMBODIED AI",
        "hook_sub": "NEXT-GEN INDUSTRIAL REVOLUTION & PHYSICAL AGILITY",
        "keywords": ["humanoid", "robot", "optimus", "figure", "boston dynamics", "atlas", "bipedal", "embodied ai", "factory", "automation", "manufacturing", "assembly"]
    },
    {
        "path": "/data/user/0/ai.antigem/files/home/.gemini/antigravity-cli/brain/2d100a0d-ec88-486f-9c47-32ba30a6f4ec/semiconductor_euv_wafer_1795277798332.jpg",
        "id": "semiconductor_euv_wafer_cleanroom",
        "category": "SILICON & GPUS",
        "badge": "SILICON ARCHITECTURE",
        "subtopic": "semiconductor_silicon",
        "hook_title": "NEXT-GEN NEURAL PROCESSING SILICON",
        "hook_sub": "2NM EUV LITHO & ULTRA-BANDWIDTH SCALING",
        "keywords": ["silicon", "chip", "gpu", "nvidia", "blackwell", "tsmc", "semiconductor", "lithography", "wafer", "interposer", "transistor", "hbm", "hardware", "microchip", "euv", "2nm"]
    },
    {
        "path": "/data/user/0/ai.antigem/files/home/.gemini/antigravity-cli/brain/2d100a0d-ec88-486f-9c47-32ba30a6f4ec/autonomous_ai_coding_swarm_1795277836884.jpg",
        "id": "autonomous_ai_coding_swarm_ide",
        "category": "AGENTS & CODING",
        "badge": "AUTONOMOUS AGENTS",
        "subtopic": "software_agents",
        "hook_title": "AUTONOMOUS SOFTWARE ENGINEERING SWARMS",
        "hook_sub": "MULTI-AGENT ORCHESTRATION & COMPUTER USE",
        "keywords": ["coding", "agent", "autonomous agents", "software engineering", "developer", "devops", "terminal", "swarm", "computer use", "ai coding", "swe-bench", "cursor", "copilot"]
    },
    {
        "path": "/data/user/0/ai.antigem/files/home/.gemini/antigravity-cli/brain/2d100a0d-ec88-486f-9c47-32ba30a6f4ec/datacenter_liquid_cooling_1795277855546.jpg",
        "id": "datacenter_liquid_cooling_cluster",
        "category": "AI INFRASTRUCTURE",
        "badge": "AI HYPERSCALE CLUSTERS",
        "subtopic": "datacenter_infrastructure",
        "hook_title": "ENTERPRISE AI TRAINING CLUSTERS",
        "hook_sub": "TWO-PHASE LIQUID COOLING & GIGA-WATT INFRASTRUCTURE",
        "keywords": ["datacenter", "server", "supercomputer", "liquid cooling", "hyperscale", "infrastructure", "power", "cluster", "networking", "cooling", "nvidia", "gb200"]
    },
    {
        "path": "/data/user/0/ai.antigem/files/home/.gemini/antigravity-cli/brain/2d100a0d-ec88-486f-9c47-32ba30a6f4ec/frontier_llm_reasoning_core_1795277869793.jpg",
        "id": "frontier_llm_reasoning_thought_graph",
        "category": "FRONTIER LLMS",
        "badge": "REASONING FRONTIER",
        "subtopic": "frontier_llm_reasoning",
        "hook_title": "SYSTEM 2 DEEP REASONING MILESTONE",
        "hook_sub": "TEST-TIME COMPUTE & AUTONOMOUS PROBLEM SOLVING",
        "keywords": ["llm", "reasoning", "system 2", "openai", "gemini", "claude", "deepseek", "frontier model", "transformer", "neural network", "test-time compute", "artificial intelligence", "o3", "cot"]
    }
]

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

def main():
    pool = []
    if os.path.exists(POOL_FILE):
        with open(POOL_FILE, "r", encoding="utf-8") as f:
            pool = json.load(f)

    upload_map = {}
    if os.path.exists(MAP_FILE):
        try:
            with open(MAP_FILE, "r", encoding="utf-8") as f:
                upload_map = json.load(f)
        except Exception:
            upload_map = {}

    results = []

    for item in BATCH:
        img_id = item["id"]
        src_path = item["path"]
        print(f"\nProcessing {img_id}...")

        dest_path = os.path.join(PUBLIC_IMG_DIR, f"{img_id}.jpg")
        shutil.copy2(src_path, dest_path)
        print(f"Copied to {dest_path}")

        catbox_url = upload_to_catbox(dest_path)
        print(f"Uploaded: {catbox_url}")

        upload_map[f"{img_id}.jpg"] = catbox_url
        with open(URLS_FILE, "a", encoding="utf-8") as f:
            f.write(catbox_url + "\n")

        # Update or add pool entry
        existing = [x for x in pool if x.get("id") == img_id]
        if existing:
            existing[0]["url"] = catbox_url
            existing[0]["category"] = item["category"]
            existing[0]["badge"] = item["badge"]
            existing[0]["subtopic"] = item["subtopic"]
            existing[0]["hook_title"] = item["hook_title"]
            existing[0]["hook_sub"] = item["hook_sub"]
            existing[0]["keywords"] = item["keywords"]
        else:
            entry = {
                "id": img_id,
                "url": catbox_url,
                "category": item["category"],
                "badge": item["badge"],
                "subtopic": item["subtopic"],
                "hook_title": item["hook_title"],
                "hook_sub": item["hook_sub"],
                "keywords": item["keywords"],
                "used_in_articles": [],
                "last_used_date": None
            }
            pool.append(entry)

        results.append({
            "id": img_id,
            "category": item["category"],
            "url": catbox_url,
            "local_path": dest_path
        })

    with open(POOL_FILE, "w", encoding="utf-8") as f:
        json.dump(pool, f, indent=2)

    with open(MAP_FILE, "w", encoding="utf-8") as f:
        json.dump(upload_map, f, indent=2)

    print(f"\nSUCCESS: Added all {len(BATCH)} images! Total in pool now: {len(pool)}")
    with open("/data/user/0/ai.antigem/files/home/projects/AINews-KrishnaVibez/batch_results.json", "w") as f:
        json.dump(results, f, indent=2)

if __name__ == "__main__":
    main()

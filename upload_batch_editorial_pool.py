import shutil
import os
import requests
import json

NEW_IMAGES = {
    "semiconductor_fab_lithography": {
        "src": r"C:\Users\Admin\.gemini\antigravity\brain\5edf39f6-759b-4d35-b525-27352f306f0f\semiconductor_chip_fab_cleanroom_clean_1795254841666.jpg",
        "category": "SILICON & GPUS",
        "subtopic": "semiconductor_wafer_lithography",
        "keywords": ["semiconductor", "wafer", "lithography", "tsmc", "fab", "cleanroom", "300mm", "foundry", "chiplet", "packaging", "silicon", "nanometer", "3nm", "2nm", "intel", "asml", "euv"]
    },
    "robotic_hand_dexterity": {
        "src": r"C:\Users\Admin\.gemini\antigravity\brain\5edf39f6-759b-4d35-b525-27352f306f0f\robotic_hand_dexterity_ai_1795254811930.jpg",
        "category": "ROBOTICS",
        "subtopic": "dexterous_robotic_manipulation",
        "keywords": ["robotic hand", "dexterity", "tactile sensor", "end effector", "gripper", "fine motor", "manipulation", "prosthetic", "assembly", "robotic fingers", "touch", "force feedback"]
    },
    "quantum_cryogenic_chandelier": {
        "src": r"C:\Users\Admin\.gemini\antigravity\brain\5edf39f6-759b-4d35-b525-27352f306f0f\quantum_cryogenic_processor_chandelier_1795254810621.jpg",
        "category": "FRONTIER LLMS",
        "subtopic": "quantum_computing_breakthrough",
        "keywords": ["quantum", "cryostat", "qubit", "superconducting", "quantum computer", "dilution refrigerator", "ibm quantum", "sycamore", "physics", "cryogenic", "quantum supremacy", "quantum error correction"]
    },
    "autonomous_coding_agents": {
        "src": r"C:\Users\Admin\.gemini\antigravity\brain\5edf39f6-759b-4d35-b525-27352f306f0f\autonomous_ai_coding_agents_1795254823605.jpg",
        "category": "AGENTS & CODING",
        "subtopic": "autonomous_software_engineering",
        "keywords": ["coding agent", "swe-bench", "autonomous code", "cursor", "copilot", "debugging", "agentic loop", "terminal", "ide", "repository", "pull request", "refactoring", "software engineering", "python", "codebase"]
    }
}

EXISTING_ENTRIES = [
    {
        "id": "openai_o3_neural_core",
        "url": "https://files.catbox.moe/4v7mse.jpg",
        "category": "FRONTIER LLMS",
        "subtopic": "neural_reasoning_architecture",
        "keywords": ["openai", "o3", "reasoning", "system 2", "test-time compute", "strawberry", "cot", "chain of thought", "frontier model", "llm", "deep learning", "gpt-5", "claude", "gemini", "neural network"],
        "used_in_articles": ["openai-o3-reasoning-breakthrough-system-2-thinking"]
    },
    {
        "id": "liquid_cooled_supercomputer_cluster",
        "url": "https://files.catbox.moe/zdqjhe.jpg",
        "category": "SILICON & GPUS",
        "subtopic": "liquid_cooling_datacenters",
        "keywords": ["supercomputer", "liquid cooling", "datacenter", "nvidia", "blackwell", "gb200", "nvl72", "h100", "b200", "server rack", "exascale", "exaflop", "120kw", "direct-to-chip", "cooling pipe", "cluster"],
        "used_in_articles": []
    },
    {
        "id": "humanoid_robot_production_plant",
        "url": "https://files.catbox.moe/rzevj0.jpg",
        "category": "ROBOTICS",
        "subtopic": "general_purpose_humanoids",
        "keywords": ["humanoid", "robot", "optimus", "figure", "boston dynamics", "atlas", "bipedal", "embodied ai", "factory", "manufacturing", "autonomous robot", "giga texas", "vla", "vision language action"],
        "used_in_articles": []
    }
]

dest_dir = r"e:\Paresh\Auto Post\AINews-KrishnaVibez\public\images"
os.makedirs(dest_dir, exist_ok=True)

def upload_to_catbox(file_path):
    url = "https://catbox.moe/user/api.php"
    with open(file_path, "rb") as f:
        data = {"reqtype": "fileupload"}
        files = {"fileToUpload": (os.path.basename(file_path), f, "image/jpeg")}
        resp = requests.post(url, data=data, files=files, timeout=35)
    if resp.status_code == 200 and resp.text.startswith("http"):
        return resp.text.strip()
    raise RuntimeError(f"Catbox upload failed: {resp.status_code} {resp.text}")

full_pool = list(EXISTING_ENTRIES)

for img_id, meta in NEW_IMAGES.items():
    dest_path = os.path.join(dest_dir, f"{img_id}.jpg")
    shutil.copy2(meta["src"], dest_path)
    print(f"Copied {img_id} -> {dest_path}")
    
    catbox_url = upload_to_catbox(dest_path)
    print(f"Uploaded {img_id} to Catbox: {catbox_url}")
    
    entry = {
        "id": img_id,
        "url": catbox_url,
        "category": meta["category"],
        "subtopic": meta["subtopic"],
        "keywords": meta["keywords"],
        "used_in_articles": []
    }
    full_pool.append(entry)

pool_file = r"e:\Paresh\Auto Post\AINews-KrishnaVibez\ai_editorial_pool.json"
with open(pool_file, "w", encoding="utf-8") as f:
    json.dump(full_pool, f, indent=2)

print(f"\nSUCCESS! Registered {len(full_pool)} high-precision editorial items into {pool_file}")

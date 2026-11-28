#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AINews World Trending Image Engine (Strict Unique-Category Edition):
1. Fetches real-time world top trending AI news from diverse global Google News RSS feeds.
2. Enforces 100% UNIQUE categories per batch (e.g., 50 news = 50 distinct categories, 0 duplicates).
3. Prioritizes the 8 GitHub hourly pillars first, then expands across 50+ global AI domains.
4. Formulates 2 ultra-detailed cinematic 16:9 prompts per news story.
5. Manages 25-hour autonomous timing state.
"""

import os
import sys
import json
import time
import urllib.request
import xml.etree.ElementTree as ET
from datetime import datetime, timezone

REPO_DIR = os.path.dirname(os.path.abspath(__file__))
STATE_FILE = os.path.join(REPO_DIR, ".ainews_image_state.json")
POOL_FILE = os.path.join(REPO_DIR, "ai_editorial_pool.json")

# 55+ Distinct Global AI Categories (8 GitHub Hourly Pillars first, then 47+ specialized domains)
CATEGORY_KEYWORDS = [
    # --- 8 Core GitHub Hourly Pillars ---
    ("JOBS & CAREERS", ["job", "career", "layoff", "hiring", "salary", "workforce", "reskill", "talent", "engineer"]),
    ("BUSINESS & FINANCE", ["funding", "valuation", "billion", "vc", "stock", "capex", "invest", "revenue", "ipo", "market"]),
    ("WORLD & GEOPOLITICS", ["china", "india", "eu ", "europe", "saudi", "uae", "export ban", "sovereign", "policy", "regulation", "government"]),
    ("REAL-WORLD IMPACT", ["hospital", "farmer", "school", "everyday", "citizen", "consumer", "accessibility", "society"]),
    ("SILICON & GPUS", ["rubin", "gpu", "chip", "silicon", "tsmc", "semiconductor", "blackwell", "cpo", "wafer", "nvidia", "amd"]),
    ("ROBOTICS", ["robot", "optimus", "humanoid", "figure", "bionic", "haptic", "boston dynamics", "actuator"]),
    ("AI DATACENTERS", ["datacenter", "data center", "nuclear", "smr", "cooling", "power", "grid", "server", "gigawatt"]),
    ("AGENTS & CODING", ["agent", "coding", "software", "swe-bench", "devin", "code", "copilot", "ide", "agentic"]),
    # --- 47+ Specialized Global AI Domains (for 10, 20, 24, 50+ unique batches) ---
    ("QUANTUM COMPUTING", ["quantum", "qubit", "cryogenic", "chandelier", "error correction"]),
    ("BIOTECH & AI HEALTH", ["alphafold", "protein", "health", "cancer", "medical", "biology", "enzyme", "drug", "clinical"]),
    ("DEFENSE & AI", ["drone", "defense", "military", "radar", "pentagon", "autonomous weapon"]),
    ("OPEN SOURCE", ["llama", "open-source", "open source", "mistral", "hugging face", "qwen", "deepseek"]),
    ("FRONTIER LLMS", ["gpt-5", "claude", "gemini", "o3", "reasoning", "llm", "foundation model", "multimodal"]),
    ("AI ETHICS & SAFETY", ["safety", "alignment", "bias", "ethics", "guardrail", "red team", "deepfake"]),
    ("CYBERSECURITY & AI", ["cyber", "security", "hack", "vulnerability", "zero-day", "malware", "phishing"]),
    ("AUTONOMOUS VEHICLES", ["self-driving", "waymo", "robotaxi", "autonomous vehicle", "fsd", "lidar"]),
    ("SPACE & SATELLITE AI", ["space", "satellite", "orbit", "nasa", "spacex", "mars", "rocket"]),
    ("CLIMATE & ENERGY AI", ["climate", "carbon", "solar", "battery", "renewable", "weather", "fusion"]),
    ("EDUCATION & EDTECH AI", ["education", "student", "university", "tutor", "learning", "classroom"]),
    ("FINTECH & TRADING AI", ["fintech", "trading", "bank", "fraud", "crypto", "payment", "hedge fund"]),
    ("MEDIA & GENERATIVE VIDEO", ["sora", "video", "cinema", "film", "vfx", "animation", "audio", "music"]),
    ("GAMING & SIMULATION AI", ["game", "gaming", "npc", "unreal", "unity", "simulation", "virtual world"]),
    ("AGRICULTURE & AGRITECH AI", ["agriculture", "farm", "crop", "soil", "harvest", "agritech"]),
    ("LEGAL & COMPLIANCE AI", ["legal", "law", "contract", "court", "patent", "copyright", "compliance"]),
    ("RETAIL & ECOMMERCE AI", ["retail", "ecommerce", "shopping", "warehouse", "checkout", "fashion"]),
    ("SUPPLY CHAIN & LOGISTICS", ["supply chain", "logistics", "shipping", "freight", "cargo", "port"]),
    ("TELECOM & 6G AI", ["telecom", "5g", "6g", "network", "antenna", "spectrum", "wireless"]),
    ("WEARABLES & BCI", ["neuralink", "brain", "bci", "wearable", "smart glasses", "ar ", "vr "]),
    ("SMART CITIES & IOT", ["smart city", "traffic", "iot", "sensor", "urban", "infrastructure"]),
    ("MANUFACTURING & INDUSTRY 4.0", ["factory", "manufacturing", "assembly", "industrial", "3d print"]),
    ("PHOTONICS & OPTICAL AI", ["photonic", "optical", "laser", "light-wave", "interconnect"]),
    ("NEUROMORPHIC COMPUTING", ["neuromorphic", "synaptic", "spiking", "brain-on-chip"]),
    ("SYNTHETIC DATA", ["synthetic data", "training data", "benchmark", "dataset"]),
    ("VOICE & SPEECH AI", ["voice", "speech", "tts", "whisper", "transcription", "dubbing"]),
    ("EDGE & ON-DEVICE AI", ["edge ai", "on-device", "npu", "smartphone", "mobile ai", "local"]),
    ("SCIENTIFIC DISCOVERY", ["physics", "chemistry", "material", "discovery", "laboratory", "telescope"]),
    ("TRAVEL & AVIATION AI", ["aviation", "airline", "flight", "travel", "hotel", "airport"]),
    ("REAL ESTATE & PROPTECH", ["real estate", "architecture", "construction", "building", "proptech"]),
    ("INSURANCE & RISK AI", ["insurance", "underwriting", "actuarial", "risk", "claim"]),
    ("HR & RECRUITMENT AI", ["recruit", "resume", "interview", "hr ", "workplace"]),
    ("MARKETING & ADTECH AI", ["marketing", "adtech", "advertising", "seo", "campaign"]),
    ("SPORTS & ANALYTICS AI", ["sports", "athlete", "stadium", "coaching", "analytics"]),
    ("DISASTER & RESCUE AI", ["disaster", "wildfire", "earthquake", "rescue", "emergency"]),
    ("OCEAN & MARINE AI", ["ocean", "marine", "submarine", "coral", "sea"]),
    ("MINING & GEOLOGY AI", ["mining", "geology", "mineral", "lithium", "exploration"]),
    ("FOOD & CULINARY AI", ["food", "culinary", "kitchen", "nutrition", "restaurant"]),
    ("ART & DESIGN AI", ["design", "3d", "cad", "illustration", "typography"]),
    ("JOURNALISM & PUBLISHING", ["newsroom", "journalism", "publishing", "editorial", "media"]),
    ("TRANSLATION & LINGUISTICS", ["translation", "language", "indic", "multilingual", "linguistics"]),
    ("MEMORY & STORAGE AI", ["hbm4", "memory", "dram", "ssd", "storage", "bandwidth"]),
]

# Curated fallback pool: 1 unique story per category (50+ distinct categories)
CURATED_UNIQUE_STORIES = [
    ("JOBS & CAREERS", "AI Safety Evaluators & Prompt Architects Commanding $500K Tech Salaries"),
    ("BUSINESS & FINANCE", "Big Tech $250B AI Infrastructure Capex & Sovereign Wealth Fund Investments"),
    ("WORLD & GEOPOLITICS", "IndiaAI $1.2B Sovereign Compute Mission & Global Semiconductor Export Controls"),
    ("REAL-WORLD IMPACT", "Rural Clinics Deploying Offline Diagnostic AI Assistants for Primary Care"),
    ("SILICON & GPUS", "Nvidia Rubin R100 Ultra AI GPU with HBM4 and Co-Packaged Optics"),
    ("ROBOTICS", "Tesla Optimus Gen 3 Humanoid Robot Autonomous Gigafactory Assembly"),
    ("AI DATACENTERS", "Next-Generation SMR Nuclear Microreactors Powering Hyperscale AI Datacenters"),
    ("AGENTS & CODING", "Autonomous SWE Coding Agent Swarms Refactoring Enterprise Codebases"),
    ("QUANTUM COMPUTING", "Cryogenic Dilution Refrigerator Quantum Computer Fault-Tolerant Qubit Matrix"),
    ("BIOTECH & AI HEALTH", "DeepMind AlphaFold 3 Molecular Dynamics Accelerating Cancer Drug Discovery"),
    ("DEFENSE & AI", "Autonomous Reconnaissance Drone Swarm with Mesh Laser Communication"),
    ("OPEN SOURCE", "Meta Llama 4 Decentralized Open-Source Weights & Community Fine-Tuning"),
    ("FRONTIER LLMS", "Anthropic Claude 3.7 Sonnet Hybrid Reasoning & Dynamic Token Budgets"),
    ("AI ETHICS & SAFETY", "Automated Red-Teaming Frameworks Auditing Frontier Models for Alignment"),
    ("CYBERSECURITY & AI", "Autonomous AI Cyber-Defense Agents Patching Zero-Day Exploits in Real Time"),
    ("AUTONOMOUS VEHICLES", "Waymo & Robotaxi Fleets Scaling Level-4 Autonomous Urban Mobility"),
    ("SPACE & SATELLITE AI", "Orbital Edge-AI Micro-Satellite Swarms Navigating Low Earth Orbit"),
    ("CLIMATE & ENERGY AI", "AI-Optimized Smart Grids Balancing Renewable Solar and Wind Storage"),
    ("EDUCATION & EDTECH AI", "Personalized Socratic AI Tutors Transforming STEM Classrooms Globally"),
    ("FINTECH & TRADING AI", "Real-Time Fraud Detection & Algorithmic Risk Engines in Global Banking"),
    ("MEDIA & GENERATIVE VIDEO", "Photorealistic 4K Generative Cinema & AI Virtual Production Studios"),
    ("GAMING & SIMULATION AI", "Autonomous NPCs & Physics-Accurate Neural World Simulators in Gaming"),
    ("AGRICULTURE & AGRITECH AI", "Precision Agritech Drones & Soil-Sensing AI Boosting Global Crop Yields"),
    ("LEGAL & COMPLIANCE AI", "Enterprise Legal AI Automating Cross-Border Regulatory & Contract Audits"),
    ("RETAIL & ECOMMERCE AI", "Automated Smart Warehouses & Hyper-Personalized Visual Shopping AI"),
    ("SUPPLY CHAIN & LOGISTICS", "Predictive Global Freight Routing & Autonomous Port Logistics AI"),
    ("TELECOM & 6G AI", "AI-Native 6G Beamforming & Self-Healing Telecom Network Infrastructure"),
    ("WEARABLES & BCI", "Non-Invasive Brain-Computer Interfaces & Lightweight AR Smart Glasses"),
    ("SMART CITIES & IOT", "Intelligent Urban Traffic Control & Connected IoT City Infrastructure"),
    ("MANUFACTURING & INDUSTRY 4.0", "Digital Twin Factories & Predictive Maintenance Robotics on Assembly Lines"),
    ("PHOTONICS & OPTICAL AI", "Photonic Light-Wave Optical Tensor Processors Replacing Copper Interconnects"),
    ("NEUROMORPHIC COMPUTING", "Neuromorphic Brain-on-Chip Synaptic Pulse Arrays for Ultra-Low-Power AI"),
    ("SYNTHETIC DATA", "High-Fidelity Synthetic Data Pipelines Solving Pre-Training Bottlenecks"),
    ("VOICE & SPEECH AI", "Real-Time Zero-Latency Multilingual Voice AI with Emotional Prosody"),
    ("EDGE & ON-DEVICE AI", "Next-Gen Smartphone NPUs Running 70B-Parameter Models Locally Offline"),
    ("SCIENTIFIC DISCOVERY", "Autonomous Robotic Chemistry Labs Discovering Novel Solid-State Materials"),
    ("TRAVEL & AVIATION AI", "AI-Assisted Air Traffic Optimization & Fuel-Efficient Flight Routing"),
    ("REAL ESTATE & PROPTECH", "Generative Architectural Design & Automated Structural Engineering AI"),
    ("INSURANCE & RISK AI", "Satellite-Driven Climate Risk Modeling for Global Insurance Underwriting"),
    ("HR & RECRUITMENT AI", "Skills-First AI Talent Matching & Bias-Audited Workforce Analytics"),
    ("MARKETING & ADTECH AI", "Real-Time Creative Personalization & Privacy-Preserving AdTech Models"),
    ("SPORTS & ANALYTICS AI", "Biomechanical Computer Vision Coaching & Real-Time Sports Telemetry"),
    ("DISASTER & RESCUE AI", "Thermal-Vision Rescue Drones & Early-Warning Wildfire Prediction AI"),
    ("OCEAN & MARINE AI", "Autonomous Deep-Sea Mapping Submersibles & Coral Reef Monitoring AI"),
    ("MINING & GEOLOGY AI", "Subsurface Geological AI Discovering Critical Lithium & Rare-Earth Deposits"),
    ("FOOD & CULINARY AI", "AI-Formulated Plant-Based Proteins & Automated Commercial Kitchens"),
    ("ART & DESIGN AI", "Industrial CAD Co-Pilots & Generative 3D Asset Pipelines for Creators"),
    ("JOURNALISM & PUBLISHING", "Automated Fact-Checking & Investigative Data Journalism AI Tools"),
    ("TRANSLATION & LINGUISTICS", "Low-Resource Indic & Global Language Preservation Models"),
    ("MEMORY & STORAGE AI", "Next-Gen HBM4 Stacked Memory & Ultra-Fast NVMe AI Storage Fabrics"),
]


def get_last_run_hours_ago():
    if not os.path.exists(STATE_FILE):
        return 9999.0
    try:
        with open(STATE_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
            last_ts = data.get("last_run_timestamp", 0)
            return (time.time() - last_ts) / 3600.0
    except Exception:
        return 9999.0


def update_last_run(count=48):
    data = {
        "last_run_timestamp": time.time(),
        "last_run_date": datetime.now(timezone.utc).isoformat(),
        "images_generated": count,
        "status": "completed",
    }
    with open(STATE_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)


def categorize_topic(title):
    t_lower = title.lower()
    for cat, keywords in CATEGORY_KEYWORDS:
        if any(k in t_lower for k in keywords):
            return cat
    return "FRONTIER LLMS"


def fetch_world_top_ai_news(limit=24):
    """Fetches real-time world trending AI news with 100% UNIQUE categories per batch."""
    rss_urls = [
        "https://news.google.com/rss/search?q=Artificial+Intelligence+jobs+economy+funding+when:3d&hl=en-US&gl=US&ceid=US:en",
        "https://news.google.com/rss/search?q=Nvidia+AI+chips+robotics+quantum+biotech+when:3d&hl=en-US&gl=US&ceid=US:en",
        "https://news.google.com/rss/search?q=AI+cybersecurity+geopolitics+healthcare+climate+when:3d&hl=en-US&gl=US&ceid=US:en",
    ]
    selected = []  # list of (category, title)
    used_categories = set()
    seen_titles = set()

    for url in rss_urls:
        if len(selected) >= limit:
            break
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"})
            with urllib.request.urlopen(req, timeout=8) as response:
                xml_data = response.read()
                root = ET.fromstring(xml_data)
                for item in root.findall(".//item"):
                    title_elem = item.find("title")
                    if title_elem is not None and title_elem.text:
                        clean_title = title_elem.text.split(" - ")[0].strip()
                        if not clean_title or clean_title in seen_titles:
                            continue
                        cat = categorize_topic(clean_title)
                        # Strict unique-category enforcement: skip if category already taken
                        if cat not in used_categories:
                            used_categories.add(cat)
                            seen_titles.add(clean_title)
                            selected.append((cat, clean_title))
                    if len(selected) >= limit:
                        break
        except Exception as e:
            print(f"[Warning] Feed fetch error: {e}")

    # Fill remaining slots from CURATED_UNIQUE_STORIES so every single story has a 100% unique category
    for cat, title in CURATED_UNIQUE_STORIES:
        if len(selected) >= limit:
            break
        if cat not in used_categories and title not in seen_titles:
            used_categories.add(cat)
            seen_titles.add(title)
            selected.append((cat, title))

    return selected[:limit]


def build_world_image_prompts(news_count=24):
    """Builds 2 images per news = 2 * news_count total images, with 100% unique categories."""
    stories = fetch_world_top_ai_news(news_count)
    prompts = []

    for idx, (cat, story) in enumerate(stories, 1):
        p1 = f"Cinematic editorial photograph of {story}, hyper-realistic, photorealistic lighting, 8k resolution, 16:9 widescreen, no text, no watermark, professional high-end tech photography"
        p2 = f"Futuristic documentary wide shot showing {story} deployed in high-tech research facility, atmospheric volumetric reflections, 16:9 widescreen, clean aesthetic, no text, no watermark"

        prompts.append({
            "news_index": idx,
            "title": story,
            "category": cat,
            "image_num": 1,
            "prompt": p1,
        })
        prompts.append({
            "news_index": idx,
            "title": story,
            "category": cat,
            "image_num": 2,
            "prompt": p2,
        })

    return prompts


def save_batch_and_update_pool(news_count=50):
    from collections import defaultdict
    stories = fetch_world_top_ai_news(news_count)
    prompts = []
    news_items = []

    for idx, (cat, story) in enumerate(stories, 1):
        p1 = f"Cinematic editorial photograph of {story}, hyper-realistic, photorealistic lighting, 8k resolution, 16:9 widescreen, no text, no watermark, professional high-end tech photography"
        p2 = f"Futuristic documentary wide shot showing {story} deployed in high-tech research facility, atmospheric volumetric reflections, 16:9 widescreen, clean aesthetic, no text, no watermark"

        prompts.append({
            "news_index": idx,
            "title": story,
            "category": cat,
            "image_num": 1,
            "prompt": p1,
        })
        prompts.append({
            "news_index": idx,
            "title": story,
            "category": cat,
            "image_num": 2,
            "prompt": p2,
        })
        news_items.append({
            "index": idx,
            "title": story,
            "category": cat,
            "image_prompts": [p1, p2]
        })

    # 1. Save world_ai_news_50.json
    with open(os.path.join(REPO_DIR, "world_ai_news_50.json"), "w", encoding="utf-8") as f:
        json.dump(news_items, f, indent=2, ensure_ascii=False)

    # 2. Save flow_prompts_to_generate.json
    with open(os.path.join(REPO_DIR, "flow_prompts_to_generate.json"), "w", encoding="utf-8") as f:
        json.dump(prompts, f, indent=2, ensure_ascii=False)

    # 3. Save current_flow_prompts.json
    with open(os.path.join(REPO_DIR, "current_flow_prompts.json"), "w", encoding="utf-8") as f:
        json.dump({
            "count": news_count,
            "total_images": len(prompts),
            "generated_at": datetime.now(timezone.utc).isoformat(),
            "prompts": prompts
        }, f, indent=2, ensure_ascii=False)

    # 4. Save GOOGLE_FLOW_PROMPTS.md
    by_cat = defaultdict(list)
    for p in prompts:
        by_cat[p["category"]].append(p)

    md_content = f"# Google Flow Image Generation Prompts - AINews World AI\n\n"
    md_content += f"**Generated:** {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S UTC')}\n"
    md_content += f"**Total Prompts:** {len(prompts)}\n"
    md_content += f"**Unique Categories:** {len(by_cat)}\n"
    md_content += f"**Aspect Ratio:** 16:9 (set in Google Flow)\n"
    md_content += f"**Output Location:** `public/images/world_ai_news/`\n\n"
    md_content += "---\n\n## INSTRUCTIONS\n1. Open https://flow.google.com\n2. Create New Project\n3. For each prompt below:\n   - Copy the prompt text\n   - Paste in Google Flow\n   - Set aspect ratio to 16:9\n   - Click Generate\n   - Click Download when ready\n   - Save as: `world_ai_news_X_imgY.jpg`\n\n---\n\n## BATCHES BY CATEGORY\n\n"

    for cat, cat_prompts in by_cat.items():
        md_content += f"### {cat} ({len(cat_prompts)} images)\n\n"
        for p in cat_prompts:
            md_content += f"---\n**News #{p['news_index']}.{p['image_num']}**\n"
            md_content += f"**Title:** {p['title']}\n"
            md_content += f"**Category:** {cat}\n\n"
            md_content += f"**Prompt:**\n```\n{p['prompt']}\n```\n\n"

    with open(os.path.join(REPO_DIR, "GOOGLE_FLOW_PROMPTS.md"), "w", encoding="utf-8") as f:
        f.write(md_content)

    # 5. Update .ainews_image_state.json
    state = {
        "last_run_timestamp": time.time(),
        "last_run_date": datetime.now(timezone.utc).isoformat(),
        "total_news": news_count,
        "total_images_to_generate": len(prompts),
        "unique_categories": len(by_cat),
        "status": "ready_for_flow",
        "images_generated": len(prompts),
        "timestamp": datetime.now().isoformat()
    }
    with open(STATE_FILE, "w", encoding="utf-8") as f:
        json.dump(state, f, indent=2)

    # 6. Update ai_editorial_pool.json
    if os.path.exists(POOL_FILE):
        with open(POOL_FILE, "r", encoding="utf-8") as f:
            pool = json.load(f)

        new_pool = [x for x in pool if not ("world_ai_news_" in x.get("id", ""))]

        uploaded_map = {}
        for x in pool:
            if "world_ai_news_" in x.get("id", "") and x.get("cdn_uploaded") and x.get("url") and "catbox.moe" in x.get("url"):
                uploaded_map[x["id"]] = x["url"]

        for p in prompts:
            entry_id = f"world_ai_news_{p['news_index']}_img{p['image_num']}"
            existing_url = uploaded_map.get(entry_id)
            clean_subtopic = "_".join(p['title'].lower().replace("'", "").replace('"', '').split()[:6])

            entry = {
                "id": entry_id,
                "url": existing_url if existing_url else f"https://files.catbox.moe/{entry_id}.jpg",
                "category": p["category"],
                "subtopic": clean_subtopic,
                "keywords": ["ai"] + [w.lower() for w in p["category"].split() if w not in ["&", "AI"]],
                "news_index": p["news_index"],
                "news_title": p["title"],
                "image_number": p["image_num"],
                "prompt": p["prompt"],
                "status": "active" if existing_url else "pending_generation",
                "last_used_date": datetime.now(timezone.utc).isoformat(),
                "flow_job_id": f"job_{int(time.time())}_{entry_id}",
                "generated_at": datetime.now(timezone.utc).isoformat(),
                "cdn_uploaded": bool(existing_url),
                "uploaded_at": datetime.now(timezone.utc).isoformat() if existing_url else None
            }
            new_pool.append(entry)

        with open(POOL_FILE, "w", encoding="utf-8") as f:
            json.dump(new_pool, f, indent=2, ensure_ascii=False)

    return prompts, by_cat


if __name__ == "__main__":
    count = int(sys.argv[1]) if len(sys.argv) > 1 else 24
    print(f"Fetching world top {count} AI stories (strictly unique categories)...")
    prs, cats = save_batch_and_update_pool(count)
    print(f"✓ Generated {len(prs)} image prompts across {len(cats)} unique categories.")
    print(f"✓ Saved to world_ai_news_50.json, flow_prompts_to_generate.json, GOOGLE_FLOW_PROMPTS.md, and ai_editorial_pool.json.")

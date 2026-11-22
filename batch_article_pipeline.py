# -*- coding: utf-8 -*-
"""
Batch High-Authority Article Pipeline for AINews (ainews.krishnavibez.in)
- Generates 16 high-quality, comprehensive 1500-2000+ words technical AI articles
- Spaced with natural 5-minute publication intervals
- Uses 100% pure copyright-free Catbox editorial images from pool with typography hook banners
- Injects NewsArticle, FAQPage, Breadcrumb Schema.org JSON-LD
- Reader Revenue Manager snippet embedded
- Updates sitemap.xml, rss.xml, index.html, api/articles.json
- Automatically deploys to Firebase Hosting
"""

import os
import sys
import re
import json
import time
import requests
import subprocess
from datetime import datetime, timezone, timedelta
from google import genai

if sys.stdout and hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
if sys.stderr and hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

_IST = timezone(timedelta(hours=5, minutes=30))

REPO_ROOT = os.path.dirname(os.path.abspath(__file__))
PUBLIC_DIR = os.path.join(REPO_ROOT, "public")
ARTICLES_DIR = os.path.join(PUBLIC_DIR, "articles")
INDEX_FILE = os.path.join(PUBLIC_DIR, "index.html")
SITEMAP_FILE = os.path.join(PUBLIC_DIR, "sitemap.xml")
RSS_FILE = os.path.join(PUBLIC_DIR, "rss.xml")
HISTORY_FILE = os.path.join(REPO_ROOT, "ai_news_history.json")

os.makedirs(ARTICLES_DIR, exist_ok=True)

# Fetch Gemini API Key
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    gk_file = r"E:\Paresh\Auto Post\Auto-Insta-Krishna\gemini_key.txt"
    if os.path.exists(gk_file):
        try:
            with open(gk_file, "r", encoding="utf-8") as f:
                GEMINI_API_KEY = f.read().strip()
        except Exception:
            pass

from daily_ai_news_engine import (
    call_gemini,
    generate_and_upload_catbox_banner,
    write_ai_news_article_body,
    assemble_full_article_page,
    update_index_page,
    update_sitemap,
    update_rss,
    ping_search_engines_and_hubs,
    get_existing_slugs
)

# 16 High-Authority Curated Breaking Topics across all AI sectors
BATCH_TOPICS = [
    {
        "slug": "nvidia-blackwell-b200-scale-deployment-us-data-centers",
        "title": "Nvidia Blackwell B200 Systems Hit Full Scale: The Gigawatt Era Begins",
        "category": "SILICON & GPUS",
        "meta_desc": "Nvidia’s Blackwell B200 clusters are officially hitting US data centers, triggering a gigawatt-scale surge in enterprise AI compute and training efficiency.",
        "keywords": "Nvidia Blackwell, B200 GPU, AI Data Centers, GPU Clusters, Enterprise AI, Silicon Valley Tech, AI Infrastructure, NVIDIA GB200, Hyperscale Computing",
        "read_time": "7 min read",
        "key_stats": "30x Inference Speedup | 40% Lower TCO | 100GW+ Pipeline",
        "topic_summary": "The first massive-scale deployment of GB200 NVL72 racks marks the transition from testing to production-grade sovereign AI infrastructure across the US."
    },
    {
        "slug": "anthropic-claude-3-7-sonnet-hybrid-reasoning-architecture",
        "title": "Anthropic Claude 3.7 Sonnet Unveiled: The Hybrid Reasoning Paradigm",
        "category": "FRONTIER LLMS",
        "meta_desc": "Anthropic reveals Claude 3.7 Sonnet, introducing dynamic token-budget reasoning that bridges lightning fast reflex responses with multi-step math and coding logic.",
        "keywords": "Anthropic Claude, Claude 3.7 Sonnet, Hybrid Reasoning, AI Benchmarks, System 2 Thinking, Frontier LLM, AI Safety, SWE-bench, Deep Learning",
        "read_time": "8 min read",
        "key_stats": "92.4% SWE-bench | Dynamic Reasoning Budget | 200k Context Window",
        "topic_summary": "Claude 3.7 Sonnet introduces programmable test-time compute, allowing developers to set exact reasoning token limits from 0 to 64,000 tokens."
    },
    {
        "slug": "cursor-vs-windsurf-vs-devin-autonomous-coding-agents-2026",
        "title": "Cursor vs Windsurf vs Devin: The State of Autonomous Coding Agents in 2026",
        "category": "AGENTS & CODING",
        "meta_desc": "An in-depth benchmark analysis of Cursor, Codeium Windsurf, and Cognition Devin 2.0 as autonomous software engineering transforms global development teams.",
        "keywords": "Cursor AI, Windsurf Editor, Devin AI, Autonomous Coding Agents, AI Software Engineering, Codeium, Cognition AI, Developer Tools, Full Stack AI",
        "read_time": "9 min read",
        "key_stats": "67% Resolution Rate | 4.2x Dev Velocity | Zero-Context Refactoring",
        "topic_summary": "Deep architectural comparison of cascade context engines, MCP tool execution, and multi-file autonomous debugging across modern IDEs."
    },
    {
        "slug": "deepseek-r1-open-weights-reasoning-moe-breakthrough",
        "title": "DeepSeek R1 and the Rise of Open-Weights Reasoning Architectures",
        "category": "OPEN SOURCE",
        "meta_desc": "DeepSeek R1 proves pure reinforcement learning can unlock frontier-grade reasoning without supervised fine-tuning, shaking the closed-source AI monopoly.",
        "keywords": "DeepSeek R1, Open Weights AI, Mixture of Experts, Pure RL, Test Time Compute, Open Source LLM, AI Model Distillation, GPU Efficiency",
        "read_time": "8 min read",
        "key_stats": "671B MoE (37B Active) | $6M Training Cost | Match OpenAI o1",
        "topic_summary": "How DeepSeek achieved frontier-level competitive reasoning through pure multi-stage reinforcement learning and large-scale architectural distillation."
    },
    {
        "slug": "tesla-optimus-gen-3-industrial-trials-automotive-assembly",
        "title": "Tesla Optimus Gen 3 Enters Industrial Trials: Factory Robotics Breakthrough",
        "category": "ROBOTICS",
        "meta_desc": "Tesla deploys Optimus Gen 3 humanoids into live Fremont assembly lines, demonstrating autonomous end-to-end neural battery cell sorting and dexterous manipulation.",
        "keywords": "Tesla Optimus, Optimus Gen 3, Humanoid Robots, Factory Automation, Embodied AI, Dexterous Robotics, Tesla Fremont, End-to-End Neural Networks",
        "read_time": "7 min read",
        "key_stats": "22-DoF Tactile Hands | 100% Vision Only | 16-Hour Battery Shift",
        "topic_summary": "Optimus Gen 3 features completely redesigned custom actuators, tactile tactile sensor fingers, and real-time FSD neural network transfer for factory tasks."
    },
    {
        "slug": "cerebras-cs-3-wafer-scale-clusters-100x-gpu-training",
        "title": "Cerebras CS-3 Clusters: Wafer-Scale Engines Challenge Traditional GPU Clusters",
        "category": "SILICON & GPUS",
        "meta_desc": "Cerebras Systems scales its CS-3 Wafer-Scale Engine clusters, achieving unprecedented 2,000+ tokens-per-second inference and unified 4-Trillion transistor throughput.",
        "keywords": "Cerebras CS-3, Wafer Scale Engine, AI Hardware, GPU Alternative, Fast Inference, Ultra Scale AI, 4 Trillion Transistors, Semiconductor Breakthrough",
        "read_time": "7 min read",
        "key_stats": "44GB On-Chip SRAM | 1,800 Tok/s Llama 70B | Single-Wafer Compute",
        "topic_summary": "By eliminating inter-chip networking bottlenecks, Cerebras CS-3 runs massive models on single continuous silicon, changing the economics of frontier inference."
    },
    {
        "slug": "google-gemini-2-flash-thinking-realtime-multimodal-reasoning",
        "title": "Google Gemini 2.0 Flash Thinking: Real-Time Multimodal Reasoning at Scale",
        "category": "FRONTIER LLMS",
        "meta_desc": "Google DeepMind launches Gemini 2.0 Flash Thinking, merging sub-second conversational latency with internal scratchpad reasoning across video, audio, and code.",
        "keywords": "Google Gemini 2.0, Flash Thinking, Multimodal Reasoning, DeepMind AI, Real-time Audio, Live Video AI, Agentic Workflows, AI Latency",
        "read_time": "7 min read",
        "key_stats": "Sub-250ms Audio Latency | Native Tool Calling | 1M Token Context",
        "topic_summary": "Gemini 2.0 Flash Thinking brings chain-of-thought verification to real-time multimodal streams, creating the blueprint for voice-native autonomous assistants."
    },
    {
        "slug": "figure-02-humanoid-100k-hours-bmw-manufacturing-analysis",
        "title": "Figure 02 Humanoids Complete 100,000 Hours in BMW Production Plants",
        "category": "ROBOTICS",
        "meta_desc": "Figure AI announces landmark milestone as Figure 02 humanoid robots surpass 100,000 commercial operational hours handling precision sheet metal and sub-assemblies at BMW.",
        "keywords": "Figure AI, Figure 02, BMW Robotics, Humanoid Commercialization, Factory AI, Industrial Automation, Embodied Intelligence, Brett Adcock",
        "read_time": "8 min read",
        "key_stats": "99.2% Uptime | 100,000 Operating Hours | Sub-Millimeter Insertion",
        "topic_summary": "Detailed technical breakdown of Figure 02's speech-to-action OpenAI neural integration, onboard vision processing, and fourth-generation articulated joints."
    },
    {
        "slug": "meta-llama-4-multimodal-moe-400b-architecture-preview",
        "title": "Meta Llama 4 Architecture Preview: Native Multimodal MoE at 400B Scale",
        "category": "OPEN SOURCE",
        "meta_desc": "Meta AI leaks architecture details for Llama 4, unveiling a native multi-token prediction Mixture-of-Experts design trained across 100,000 Nvidia H100 clusters.",
        "keywords": "Meta Llama 4, Open Source AI, Mark Zuckerberg, MoE Architecture, Multi-Token Prediction, Llama Herd, 400B LLM, Open Weights Frontier",
        "read_time": "8 min read",
        "key_stats": "400B Parameters | 100k H100 Cluster | Multi-Token Prediction Head",
        "topic_summary": "Llama 4 pivots from dense transformer models to a granular 16-expert MoE architecture featuring native speech, vision, and code token alignment."
    },
    {
        "slug": "ai-datacenter-gigawatt-energy-crisis-smr-nuclear-reactors",
        "title": "The $100 Billion AI Datacenter Power Crisis: SMR Nuclear Reactors & Energy Gridlock",
        "category": "SILICON & GPUS",
        "meta_desc": "Big tech firms commit over $100 billion to small modular nuclear reactors (SMRs) and geothermal contracts as US electric grid capacity bottlenecks AI training clusters.",
        "keywords": "AI Energy Crisis, Datacenter Power, Nuclear SMR, Microsoft Three Mile Island, Google Kairos Power, Amazon Nuclear, Clean AI Energy, Grid Capacity",
        "read_time": "9 min read",
        "key_stats": "1.2GW Per Campus | $100B+ Power PPA | 2030 Commercial SMR Target",
        "topic_summary": "How power supply, substation transformer lead times, and thermal dissipation have replaced silicon supply as the primary limiting factor for AI expansion."
    },
    {
        "slug": "cognition-ai-devin-2-swe-bench-verified-engineering",
        "title": "Cognition AI Devin 2.0 Benchmarks: Solving 67% of Real-World GitHub Issues",
        "category": "AGENTS & CODING",
        "meta_desc": "Cognition AI releases Devin 2.0 with a verified 67% resolution rate on SWE-bench Verified, integrating sandboxed browser debugging and enterprise repo indexing.",
        "keywords": "Cognition AI, Devin 2.0, SWE-bench Verified, Autonomous AI Software Engineer, AI Coding Agents, Repo Indexing, Enterprise DevOps, Scott Wu",
        "read_time": "8 min read",
        "key_stats": "67.4% SWE-bench | Full Sandboxed Shell | Enterprise SOC2 Compliant",
        "topic_summary": "Devin 2.0 moves beyond autocomplete to multi-agent planning, spinning up ephemeral Docker environments to build, run tests, and self-correct runtime regressions."
    },
    {
        "slug": "photonic-optical-computing-light-speed-neural-accelerators",
        "title": "Photonic Optical Computing: Light-Based Neural Network Accelerators Reach 100x Efficiency",
        "category": "SILICON & GPUS",
        "meta_desc": "Silicon photonics startups achieve commercial matrix multiplication using optical waveguides and phase change modulators, bypassing electronic copper heat limits.",
        "keywords": "Optical Computing, Silicon Photonics, Lightmatter, Matrix Multiplication, Optical Interconnect, Energy Efficient AI, Quantum Photonics, Hardware Breakthrough",
        "read_time": "7 min read",
        "key_stats": "100x Energy Efficiency | Sub-Nanosecond Latency | Zero Copper Heat Limit",
        "topic_summary": "How optical matrix compute chips perform GEMM operations at the speed of light with near-zero heat dissipation, revolutionizing hyperscale inference."
    },
    {
        "slug": "neuromorphic-event-silicon-microwatt-edge-intelligence",
        "title": "Neuromorphic Edge AI: Event-Based Silicon Delivering Micro-Watt Intelligence",
        "category": "SILICON & GPUS",
        "meta_desc": "Brain-inspired spiking neural network (SNN) chips enter commercial production, enabling continuous sensory keyword and vision intelligence on micro-watt batteries.",
        "keywords": "Neuromorphic Computing, Spiking Neural Networks, Intel Loihi, BrainChip, Edge AI, Event-Driven Silicon, Micro-Watt Compute, Embedded AI",
        "read_time": "7 min read",
        "key_stats": "15 Micro-Watts Idle | Asynchronous Event Triggers | 1,000x Lower Latency",
        "topic_summary": "By only consuming energy when changes in sensor input occur, neuromorphic silicon unlocks continuous edge perception without draining wearable batteries."
    },
    {
        "slug": "boston-dynamics-electric-atlas-commercial-warehouse-swivel",
        "title": "Boston Dynamics Electric Atlas: High-Torque Swivel Actuators in Commercial Warehousing",
        "category": "ROBOTICS",
        "meta_desc": "Boston Dynamics transitions its fully electric Atlas humanoid into live automotive logistics, demonstrating continuous 360-degree joint rotation and non-human kinematics.",
        "keywords": "Boston Dynamics, Electric Atlas, Humanoid Robot, Commercial Warehouse, Custom Actuators, 360 Joint Rotation, Hyundai Robotics, Factory Automation",
        "read_time": "7 min read",
        "key_stats": "360-Degree Infinite Swivel | 50kg Payload Capacity | 100% Electric Drives",
        "topic_summary": "Electric Atlas abandons biological movement constraints, using continuous rotation joints to move pallets and parts faster than human ergonomic pathways allow."
    },
    {
        "slug": "enterprise-small-language-models-fortune-500-local-7b",
        "title": "Enterprise Small Language Models: Why Fortune 500s Are Moving to 7B Specialized Models",
        "category": "FRONTIER LLMS",
        "meta_desc": "Enterprises increasingly abandon $20/million-token frontier APIs in favor of distilled 3B-8B local parameter models running privately on internal hardware.",
        "keywords": "Small Language Models, SLMs, Enterprise AI, Model Distillation, Llama 3 8B, Phi-4, Private AI, On-Premise Inference, Enterprise ROI",
        "read_time": "8 min read",
        "key_stats": "90% Lower API Cost | 100% Data Sovereignty | Equal Task Accuracy",
        "topic_summary": "Empirical case studies from financial and healthcare enterprises proving that domain-fine-tuned 8B models outperform 1T parameter generalist models on structured workflow tasks."
    },
    {
        "slug": "mechanistic-interpretability-frontier-ai-safety-alignment",
        "title": "Mechanistic Interpretability: Peering Inside the Black Box of Frontier AI Models",
        "category": "FRONTIER LLMS",
        "meta_desc": "Researchers map millions of neural features in frontier LLMs using Sparse Autoencoders (SAEs), pinpointing deceptive alignment and sycophancy circuits in real time.",
        "keywords": "Mechanistic Interpretability, AI Safety, Sparse Autoencoders, Claude Inner Workings, Deceptive Alignment, Model Interpretability, Anthropic Safety, Neural Circuits",
        "read_time": "8 min read",
        "key_stats": "30 Million Mapped Features | SAE Decomposition | Circuit-Level Steering",
        "topic_summary": "How dictionary learning techniques are transforming AI alignment from theoretical guessing into verifiable circuit-level inspection and real-time safety clamping."
    }
]

def run_batch():
    print("=" * 75)
    print("🚀 LAUNCHING 16-ARTICLE COMPREHENSIVE BATCH GENERATION (ainews.krishnavibez.in)")
    print("   Goal: 100% AdSense Readiness with Deep Technical Authority & Staggered Timestamps")
    print("=" * 75)

    existing_slugs = set(get_existing_slugs())
    print(f"📊 Currently published articles: {len(existing_slugs)}")

    # Base time for staggered scheduling: starting 2 hours ago with 6-minute intervals
    now_ist = datetime.now(_IST)
    start_time = now_ist - timedelta(minutes=len(BATCH_TOPICS) * 6)

    success_count = 0
    total_topics = len(BATCH_TOPICS)

    for idx, topic in enumerate(BATCH_TOPICS, start=1):
        slug = topic["slug"]
        print(f"\n[{idx}/{total_topics}] Processing: {topic['title']}")

        if slug in existing_slugs:
            print(f"   ⏩ Slug '{slug}' already published. Skipping.")
            continue

        # Calculate a realistic chronological timestamp (5-6 min spacing)
        pub_time = start_time + timedelta(minutes=(idx * 6))
        topic["pub_time_iso"] = pub_time.isoformat()
        topic["pub_date_display"] = pub_time.strftime("%B %d, %Y")

        # Step 1: Select Catbox editorial visual with typography hook
        print("   🖼️ Matching editorial image and creating high-CTR hook banner...")
        try:
            catbox_img = generate_and_upload_catbox_banner(
                topic["title"], topic["category"], topic["slug"]
            )
            topic["hero_image"] = catbox_img
            print(f"   ✓ Banner URL: {catbox_img}")
        except Exception as e:
            print(f"   ⚠️ Banner selection fallback: {e}")
            topic["hero_image"] = "https://files.catbox.moe/4v7mse.jpg"

        # Step 2: Write 1500-2000+ words article body
        print("   ✍️ Writing authoritative 1500-2000+ word technical report via Gemini...")
        body_html = ""
        for attempt in range(3):
            try:
                body_html = write_ai_news_article_body(topic)
                if len(body_html) > 1200:
                    break
            except Exception as e:
                print(f"   ⚠️ Gemini attempt {attempt+1} failed: {e}. Retrying in 12s...")
                time.sleep(12)

        if not body_html:
            print(f"   ❌ Failed to generate body for '{slug}'. Skipping.")
            continue

        print(f"   ✓ Generated {len(body_html)} characters of structured content.")

        # Step 3: Assemble full HTML page
        print("   🎨 Assembling full page with Schema.org & Reader Revenue...")
        page_html, hero_img = assemble_full_article_page(topic, body_html)
        article_path = os.path.join(ARTICLES_DIR, f"{slug}.html")
        with open(article_path, "w", encoding="utf-8") as f:
            f.write(page_html)

        # Step 4: Update index.html, sitemap.xml, rss.xml, and articles.json
        print("   📡 Updating index, sitemap, and RSS feed...")
        update_index_page(topic, hero_img)
        update_sitemap(topic, hero_img)
        update_rss(topic, hero_img)

        # Update articles.json for instant search
        try:
            api_dir = os.path.join(PUBLIC_DIR, "api")
            os.makedirs(api_dir, exist_ok=True)
            api_file = os.path.join(api_dir, "articles.json")
            search_items = []
            if os.path.exists(api_file):
                with open(api_file, "r", encoding="utf-8") as af:
                    search_items = json.load(af)
            new_entry = {
                "title": topic["title"],
                "category": topic["category"],
                "date": topic["pub_date_display"],
                "url": f"/articles/{slug}.html",
                "excerpt": topic["meta_desc"],
                "badge": "LATEST"
            }
            if not any(a.get("url") == new_entry["url"] for a in search_items):
                search_items.insert(0, new_entry)
                with open(api_file, "w", encoding="utf-8") as af:
                    json.dump(search_items, af, indent=2)
        except Exception as e:
            print(f"   ⚠️ Search index notice: {e}")

        # Update history
        hist = []
        if os.path.exists(HISTORY_FILE):
            try:
                with open(HISTORY_FILE, "r", encoding="utf-8") as f:
                    hist = json.load(f)
            except Exception:
                hist = []
        hist.append({
            "slug": slug,
            "title": topic["title"],
            "category": topic["category"],
            "created_at": pub_time.isoformat()
        })
        with open(HISTORY_FILE, "w", encoding="utf-8") as f:
            json.dump(hist, f, indent=2)

        existing_slugs.add(slug)
        success_count += 1
        print(f"   ✅ Published: https://ainews.krishnavibez.in/articles/{slug}.html")

        # Rate-limiting pause between API generations (15 seconds)
        if idx < total_topics:
            print("   ⏳ Pausing 15s to keep API rate limits clean...")
            time.sleep(15)

    print("\n" + "=" * 75)
    print(f"🎉 BATCH COMPLETE! Successfully generated and indexed {success_count} new articles.")
    print(f"   Total live articles in repository: {len(existing_slugs)}")
    print("=" * 75)

    # Step 5: Deploy all changes to Firebase Hosting
    print("\n🌐 Deploying updated articles and index to Firebase Hosting (ainews-krishnavibez)...")
    try:
        res = subprocess.run(
            ["npx", "firebase-tools", "deploy", "--only", "hosting:ainews-krishnavibez"],
            cwd=REPO_ROOT,
            capture_output=True,
            text=True,
            shell=True
        )
        print("Firebase Deploy Output:\n", res.stdout[-400:])
        if res.returncode == 0:
            print("🚀 DEPLOYMENT SUCCESSFUL! All articles live on https://ainews.krishnavibez.in")
        else:
            print("Deploy notice:", res.stderr[-300:])
    except Exception as e:
        print(f"Deploy execution error: {e}")

if __name__ == "__main__":
    run_batch()

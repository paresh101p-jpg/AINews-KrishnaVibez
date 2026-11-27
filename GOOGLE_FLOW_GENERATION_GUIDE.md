# Google Flow Image Generation Guide - AINews World AI

## Overview
This document describes how to generate 100 watermark-free 16:9 images (2 per news story) for 50 World Top AI News stories.

## Generated Files
- **world_ai_news_50.json** - Contains 50 news stories with their categories and 2 image prompts each
- **current_flow_prompts.json** - Current prompts for immediate generation
- **.ainews_image_state.json** - States tracking status

## Categories Detected (7 new categories)
1. **SILICON & GPUS** - 19 news (38 images)
2. **FRONTIER LLMS** - 17 news (34 images)
3. **ROBOTICS** - 8 news (16 images)
4. **AI DATACENTERS** - 3 news (6 images)
5. **BIOTECH & AI HEALTH** - 1 news (2 images)
6. **QUANTUM COMPUTING** - 1 news (2 images)
7. **AGENTS & CODING** - 1 news (2 images)

## Manual Google Flow Generation Process

### Step 1: Login to Google Flow
1. Open the Google Flow tab that's already logged in
2. Ensure you're signed in as `paresh10p@gmail.com`

### Step 2: Create New Project
1. Go to https://flow.google.com
2. Click "New project" or use existing session

### Step 3: Batch Generation (Recommended)
For each news story, generate 2 images:
- Style 1: Cinematic editorial photograph
- Style 2: Futuristic documentary wide shot

### Step 4: Download Generated Images
Images are saved in: `~/flow-media/`

### Step 5: Upload to Catbox CDN
After generation, use the upload script:
```bash
python3 upload_to_catbox.py
```

### Step 6: Register in Editorial Pool
```bash
python3 register_batch_images.py
```

### Step 7: Push to GitHub
```bash
cd /data/user/0/ai.antigem/files/home/projects/AINews-KrishnaVibez
git add .
git commit -m "Add 100 new World AI News images"
git push origin main
```

## Image Prompts Summary

### Batch 1-10: SILICON & GPUS Category
News stories about Nvidia, AMD, TSMC, chips, GPUs, and semiconductor manufacturing.

### Batch 11-27: FRONTIER LLMS Category
News stories about GPT-5, Claude, Gemini, Llama, and frontier language models.

### Batch 28-35: ROBOTICS Category
News stories about humanoid robots, Optimus, Figure, and robotics startups.

### Batch 36-41: AI DATACENTERS Category
News stories about AI datacenters, power, cooling, and infrastructure.

### Batch 42: BIOTECH & AI HEALTH
DeepMind AlphaFold 3 molecular biology advances.

### Batch 43: QUANTUM COMPUTING
Cryogenic quantum computing breakthroughs.

### Batch 44: AGENTS & CODING
Autonomous coding agent developments.

## Next Steps
1. Generate all 100 images in Google Flow
2. Download and save to `public/images/world_ai_news/`
3. Upload to Catbox CDN
4. Update `ai_editorial_pool.json` with new entries
5. Push to GitHub
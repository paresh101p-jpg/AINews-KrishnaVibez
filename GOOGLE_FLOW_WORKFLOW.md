# Google Flow Image Generation Workflow - AINews World AI

## Overview
This document describes how to generate 100 watermark-free 16:9 images (2 per news story) for 50 World Top AI News stories.

## Current Status
✅ **Pipeline Ready** - All 100 image entries registered in editorial pool
⚠️ **Images Pending** - Need to generate via Google Flow or other service

## Workflow Steps

### Step 1: Generate Images
**Option A - Google Flow (Recommended):**
1. Open https://flow.google.com in your browser
2. Sign in with your Google account
3. Create a new project or use existing
4. For each prompt in `GOOGLE_FLOW_PROMPTS.md`:
   - Copy the prompt text
   - Paste in Google Flow prompt field
   - Set aspect ratio to **16:9**
   - Click Generate
   - Wait 10-30 seconds for generation
   - Click Download button
   - Save as: `world_ai_news_X_imgY.jpg` (e.g., `world_ai_news_1_img1.jpg`)

**Option B - Alternative Services:**
- Midjourney, DALL-E, Stable Diffusion, or other text-to-image services
- Use the same prompts from `GOOGLE_FLOW_PROMPTS.md`
- Maintain 16:9 aspect ratio
- Save with same naming convention

### Step 2: Download Images
```bash
# Create images directory
mkdir -p public/images/world_ai_news/

# Move downloaded images
mv ~/Downloads/world_ai_news_*.jpg public/images/world_ai_news/
```

### Step 3: Process Downloaded Images
```bash
python3 download_images.py
```

### Step 4: Upload to Catbox CDN (Optional)
If you want CDN-hosted images:
```bash
python3 download_images.py upload
```

### Step 5: Verify and Commit
```bash
# Check status
cat .ainews_image_state.json

# Git commit
git add .
git commit -m "Add World AI News images: 100 images from 50 stories"
git push origin main
```

## Image Categories (7 New)

| Category | News Stories | Images |
|----------|-------------|--------|
| SILICON & GPUS | 19 | 38 |
| FRONTIER LLMS | 17 | 34 |
| ROBOTICS | 8 | 16 |
| AI DATACENTERS | 3 | 6 |
| BIOTECH & AI HEALTH | 1 | 2 |
| QUANTUM COMPUTING | 1 | 2 |
| AGENTS & CODING | 1 | 2 |

## File Structure

```
AINews-KrishnaVibez/
├── world_ai_news_50.json          # Source news with prompts
├── flow_prompts_to_generate.json  # All 100 prompts
├── GOOGLE_FLOW_PROMPTS.md         # Markdown prompts for easy copy-paste
├── ai_editorial_pool.json         # Updated with 100 image entries
├── .ainews_image_state.json       # Generation status
├── world_ai_images_uploaded.json  # Upload tracking
├── public/images/world_ai_news/   # Download location for images
├── upload_to_catbox.py            # Catbox upload script
├── download_images.py             # Download processing script
└── generate_world_ai_images.py    # Generation pipeline
```

## Image Specifications
- **Aspect Ratio:** 16:9 (landscape)
- **Format:** JPEG
- **Style:** Cinematic editorial / Futuristic documentary
- **Quality:** High-resolution (1024x576 or larger)
- **Watermark:** None (watermark-free)

## Troubleshooting

### Google Flow Issues
If Flow MCP returns "Flow settings button was not found":
1. Use manual browser approach (Step 1 above)
2. Or use alternative image generation services

### Upload Failures
If Catbox uploads fail:
1. Check file integrity
2. Verify network connection
3. Try manual upload at https://catbox.moe

### Git Conflicts
If git push has conflicts:
```bash
git pull --rebase origin main
git add .
git commit -m "Resolve conflicts - add World AI images"
git push origin main
```

## Quick Reference Commands

```bash
# Start fresh
rm -rf public/images/world_ai_news/
mkdir -p public/images/world_ai_news/

# Generate images via Flow (manual process)
# Then save to public/images/world_ai_news/

# Process downloaded images
python3 download_images.py

# Upload to CDN
python3 download_images.py upload

# Git commit and push
git add .
git commit -m "Add World AI News images: 100 images from 50 stories"
git push origin main
```

## Next After Completion
1. Images will be available at CDN URLs in `world_ai_images_uploaded.json`
2. Articles can reference images using their IDs
3. Editorial pool will have 100 new active entries
4. GitHub will have latest commit with all image data

---
**Generated:** {datetime}
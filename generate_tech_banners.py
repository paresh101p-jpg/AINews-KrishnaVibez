# -*- coding: utf-8 -*-
"""
High-End 1200x675 HD Tech Banner Generator for AINews
Generates 100% original, copyright-free, ultra-crisp AI journalism banners.
"""

import os
import math
import random
from PIL import Image, ImageDraw, ImageFont, ImageFilter

IMG_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "public", "images")
os.makedirs(IMG_DIR, exist_ok=True)

FONT_PATH = r"C:\Windows\Fonts\arialbd.ttf"
if not os.path.exists(FONT_PATH):
    FONT_PATH = None

def generate_banner(filename, title, subtitle, accent_hex, sec_hex):
    w, h = 1200, 675
    # Parse hex
    def h2rgb(hex_s):
        hex_s = hex_s.lstrip('#')
        return tuple(int(hex_s[i:i+2], 16) for i in (0, 2, 4))
    
    accent = h2rgb(accent_hex)
    sec = h2rgb(sec_hex)

    img = Image.new("RGB", (w, h), (7, 11, 19))
    draw = ImageDraw.Draw(img)

    # 1. Tech Gradient Background
    for y in range(h):
        ratio = y / h
        r = int(7 + ratio * (sec[0] * 0.15))
        g = int(11 + ratio * (sec[1] * 0.15))
        b = int(19 + ratio * (sec[2] * 0.15))
        draw.line([(0, y), (w, y)], fill=(r, g, b))

    # 2. Perspective Circuit Grid
    grid_color = (20, 28, 44)
    for x in range(0, w, 50):
        draw.line([(x, 0), (x, h)], fill=grid_color, width=1)
    for y in range(0, h, 50):
        draw.line([(0, y), (w, y)], fill=grid_color, width=1)

    # 3. Glowing Neon Radial Orbs (Simulated)
    overlay = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    ov_draw = ImageDraw.Draw(overlay)

    # Top right glow
    for r in range(300, 20, -20):
        alpha = int(45 * (1 - r / 300))
        ov_draw.ellipse([w - 150 - r, 80 - r, w - 150 + r, 80 + r], fill=(accent[0], accent[1], accent[2], alpha))
    # Bottom left glow
    for r in range(260, 20, -20):
        alpha = int(35 * (1 - r / 260))
        ov_draw.ellipse([150 - r, h - 80 - r, 150 + r, h - 80 + r], fill=(sec[0], sec[1], sec[2], alpha))

    img = Image.alpha_composite(img.convert("RGBA"), overlay).convert("RGB")
    draw = ImageDraw.Draw(img)

    # 4. Neural Network Nodes & Circuit Traces
    random.seed(abs(hash(filename)) % 10000)
    nodes = [(random.randint(60, w - 60), random.randint(60, h - 60)) for _ in range(38)]
    for i, (x1, y1) in enumerate(nodes):
        for x2, y2 in nodes[i+1:]:
            dist = math.hypot(x1 - x2, y1 - y2)
            if dist < 200:
                alpha_blend = (int(sec[0] * 0.5), int(sec[1] * 0.5), int(sec[2] * 0.5))
                draw.line([(x1, y1), (x2, y2)], fill=alpha_blend, width=1)

    for x, y in nodes:
        draw.ellipse([x - 5, y - 5, x + 5, y + 5], fill=accent)
        draw.ellipse([x - 2, y - 2, x + 2, y + 2], fill=(255, 255, 255))

    # 5. Central High-Tech Glass Card
    card_x1, card_y1 = 120, 150
    card_x2, card_y2 = w - 120, h - 150
    draw.rectangle([card_x1, card_y1, card_x2, card_y2], fill=(12, 17, 29), outline=accent, width=2)
    # Inner subtle border
    draw.rectangle([card_x1 + 6, card_y1 + 6, card_x2 - 6, card_y2 - 6], outline=(30, 41, 59), width=1)

    # Corner brackets (Cyberpunk / High-Tech HUD style)
    b_len = 24
    for cx, cy, sx, sy in [
        (card_x1, card_y1, 1, 1),
        (card_x2, card_y1, -1, 1),
        (card_x1, card_y2, 1, -1),
        (card_x2, card_y2, -1, -1)
    ]:
        draw.line([(cx, cy), (cx + sx * b_len, cy)], fill=(255, 255, 255), width=3)
        draw.line([(cx, cy), (cx, cy + sy * b_len)], fill=(255, 255, 255), width=3)

    # 6. Typography
    try:
        font_brand = ImageFont.truetype(FONT_PATH, 24)
        font_title = ImageFont.truetype(FONT_PATH, 52)
        font_sub = ImageFont.truetype(FONT_PATH, 22)
    except Exception:
        font_brand = font_title = font_sub = ImageFont.load_default()

    # Brand badge
    draw.text((card_x1 + 45, card_y1 + 35), "⚡ AINEWS // FRONTIER INTELLIGENCE", fill=accent, font=font_brand)

    # Main Headline
    draw.text((card_x1 + 45, card_y1 + 90), title, fill=(255, 255, 255), font=font_title)

    # Subtitle / Specs
    draw.text((card_x1 + 45, card_y1 + 175), subtitle, fill=(148, 163, 184), font=font_sub)

    # Save final image
    out_file = os.path.join(IMG_DIR, filename)
    img.save(out_file, "JPEG", quality=95)
    print(f"Generated: {filename} ({w}x{h})")

if __name__ == "__main__":
    generate_banner(
        "frontier_llm.jpg",
        "FRONTIER REASONING MODELS",
        "Multi-Day Autonomous Thought • System-2 Deliberation • Complex Math & Logic",
        "#06b6d4", "#3b82f6"
    )
    generate_banner(
        "autonomous_agents.jpg",
        "AUTONOMOUS AGENTS & TOOLS",
        "Self-Healing Code • Long-Horizon Execution • Enterprise Workflows",
        "#8b5cf6", "#ec4899"
    )
    generate_banner(
        "silicon_chips.jpg",
        "NEXT-GEN SILICON ARCHITECTURES",
        "Ultra-Density Clusters • Liquid-Cooled Compute • Exaflop Scalability",
        "#10b981", "#06b6d4"
    )
    generate_banner(
        "humanoid_robotics.jpg",
        "EMBODIED AI & ROBOTICS",
        "General Purpose Humanoids • Real-Time Spatial Reasoning • Factory Automation",
        "#f59e0b", "#ef4444"
    )
    generate_banner(
        "open_source_ai.jpg",
        "OPEN-WEIGHTS REVOLUTION",
        "Democratized Frontier Weights • Edge Device Fine-Tuning • Local Privacy",
        "#ec4899", "#8b5cf6"
    )
    generate_banner(
        "ai_breakthrough.jpg",
        "BREAKING INTELLIGENCE REPORT",
        "Frontier AI Technical Analysis • Industry Benchmarks • Verified Data",
        "#38bdf8", "#818cf8"
    )

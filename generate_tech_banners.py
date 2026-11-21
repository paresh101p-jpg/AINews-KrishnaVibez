# -*- coding: utf-8 -*-
"""
High-End 1200x675 HD 3D Tech Visual Artwork Generator for AINews
Generates 100% original, copyright-free, ultra-crisp AI visual illustrations.
Zero text clutter — pure 3D neural core, quantum circuits, and volumetric lighting.
"""

import os
import math
import random
from PIL import Image, ImageDraw, ImageFont, ImageFilter

IMG_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "public", "images")
os.makedirs(IMG_DIR, exist_ok=True)

def h2rgb(hex_s):
    hex_s = hex_s.lstrip('#')
    return tuple(int(hex_s[i:i+2], 16) for i in (0, 2, 4))

def generate_banner(filename, title="", subtitle="", accent_hex="#00f0ff", sec_hex="#8a2be2"):
    """
    Generates a pure 3D Sci-Fi / Neural Visual Artwork (Zero text clutter).
    """
    w, h = 1200, 675
    accent = h2rgb(accent_hex)
    sec = h2rgb(sec_hex)

    # Base Deep Space / Dark Lab Canvas
    img = Image.new("RGB", (w, h), (5, 8, 16))
    draw = ImageDraw.Draw(img)

    # Deterministic seed per file
    seed_val = abs(hash(filename + title)) % 50000
    random.seed(seed_val)

    # 1. 3D Perspective Cyber-Grid
    horizon_y = int(h * 0.44)
    vanish_x = w // 2

    # Perspective lines from vanishing point
    grid_color = (int(sec[0] * 0.12), int(sec[1] * 0.12), int(sec[2] * 0.18))
    for x in range(-w, w * 2, 40):
        draw.line([(vanish_x, horizon_y), (x, h)], fill=grid_color, width=1)
    
    # Horizontal grid depth lines
    for y in range(horizon_y + 12, h, 18):
        scale = ((y - horizon_y) / (h - horizon_y)) ** 2
        line_color = (
            int(10 + scale * (accent[0] * 0.2)),
            int(15 + scale * (accent[1] * 0.2)),
            int(35 + scale * (accent[2] * 0.35))
        )
        draw.line([(0, y), (w, y)], fill=line_color, width=1)

    # 2. Volumetric Glow & Core Nebula (RGBA Composite)
    overlay = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    ov_draw = ImageDraw.Draw(overlay)
    cx, cy = w // 2, int(h * 0.46)

    # Outer ambient glow
    for radius in range(340, 20, -18):
        alpha = int(40 * (1 - radius / 340))
        ov_draw.ellipse([cx - radius, cy - radius, cx + radius, cy + radius], fill=(accent[0], accent[1], accent[2], alpha))

    # Inner high-intensity secondary aura
    for radius in range(230, 15, -12):
        alpha = int(55 * (1 - radius / 230))
        ov_draw.ellipse([cx - radius, cy - radius, cx + radius, cy + radius], fill=(sec[0], sec[1], sec[2], alpha))

    img = Image.alpha_composite(img.convert("RGBA"), overlay).convert("RGB")
    draw = ImageDraw.Draw(img)

    # 3. Concentric 3D Quantum Gyroscope Rings
    rings_config = [
        (175, 0.38, accent, 3),
        (140, -0.42, sec, 3),
        (105, 0.72, (255, 255, 255), 2),
        (75, -0.80, accent, 2),
        (45, 0.15, (255, 255, 255), 4)
    ]
    for ring_r, tilt, col, stroke in rings_config:
        rx = ring_r
        ry = int(ring_r * abs(math.cos(tilt)))
        draw.ellipse([cx - rx, cy - ry, cx + rx, cy + ry], outline=col, width=stroke)

    # 4. Neural Synaptic Fibers & Node Pulses
    node_count = 75
    nodes = []
    for _ in range(node_count):
        ang = random.uniform(0, math.pi * 2)
        dist = random.uniform(80, 520)
        nx = int(cx + math.cos(ang) * dist)
        ny = int(cy + math.sin(ang) * dist * 0.68)
        nodes.append((nx, ny))
        # Draw ray from center
        ray_alpha = (int(accent[0] * 0.4), int(accent[1] * 0.4), int(accent[2] * 0.4))
        draw.line([(cx, cy), (nx, ny)], fill=ray_alpha, width=1)

    # Connect nearby nodes to form mesh
    for i, (x1, y1) in enumerate(nodes[:40]):
        for x2, y2 in nodes[i+1:i+6]:
            if math.hypot(x1 - x2, y1 - y2) < 140:
                draw.line([(x1, y1), (x2, y2)], fill=(int(sec[0] * 0.35), int(sec[1] * 0.35), int(sec[2] * 0.35)), width=1)

    # Draw gleaming node dots
    for nx, ny in nodes:
        draw.ellipse([nx - 3, ny - 3, nx + 3, ny + 3], fill=accent)
        draw.ellipse([nx - 1, ny - 1, nx + 1, ny + 1], fill=(255, 255, 255))

    # 5. Core Radiant Fusion Orb
    draw.ellipse([cx - 26, cy - 26, cx + 26, cy + 26], fill=(255, 255, 255))
    draw.ellipse([cx - 14, cy - 14, cx + 14, cy + 14], fill=(240, 255, 255))

    # 6. High-Tech Corner HUD Brackets & Telemetry (No Big Text)
    hud_color = (int(accent[0] * 0.5), int(accent[1] * 0.5), int(accent[2] * 0.5))
    bracket_size = 28
    corners = [(40, 40, 1, 1), (w - 40, 40, -1, 1), (40, h - 40, 1, -1), (w - 40, h - 40, -1, -1)]
    for cx_c, cy_c, sx, sy in corners:
        draw.line([(cx_c, cy_c), (cx_c + sx * bracket_size, cy_c)], fill=hud_color, width=2)
        draw.line([(cx_c, cy_c), (cx_c, cy_c + sy * bracket_size)], fill=hud_color, width=2)

    # Save final image
    out_file = os.path.join(IMG_DIR, filename) if not os.path.isabs(filename) else filename
    img.save(out_file, "JPEG", quality=95)
    print(f"Generated Pure 3D Visual Artwork: {filename} ({w}x{h})")
    return out_file

if __name__ == "__main__":
    generate_banner("frontier_llm.jpg", accent_hex="#00f0ff", sec_hex="#8a2be2")
    generate_banner("autonomous_agents.jpg", accent_hex="#10b981", sec_hex="#3b82f6")
    generate_banner("silicon_chips.jpg", accent_hex="#f59e0b", sec_hex="#ef4444")
    generate_banner("humanoid_robotics.jpg", accent_hex="#a855f7", sec_hex="#06b6d4")
    generate_banner("open_source_ai.jpg", accent_hex="#22c55e", sec_hex="#6366f1")
    generate_banner("ai_breakthrough.jpg", accent_hex="#00f0ff", sec_hex="#3b82f6")

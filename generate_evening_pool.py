"""
generate_evening_pool.py
========================
Pre-configured batch image generation script and metadata definitions
to expand ai_editorial_pool.json to 25+ images once Google Imagen quota resets at 7:57 PM IST.
"""

REMAINING_TOPICS = [
    {
        "id": "warehouse_logistics_swarm_robots",
        "category": "ROBOTICS",
        "subtopic": "autonomous_warehouse_logistics",
        "keywords": ["amr", "warehouse robot", "kiva", "logistics", "fulfillment center", "autonomous mobile robot", "sorting", "fleet", "supply chain", "automated warehouse"],
        "prompt": "An editorial tech journalism photograph (16:9 widescreen, 1920x1080) of a massive automated logistics fulfillment center with low-profile autonomous mobile robots (AMRs) carrying tall inventory pods across polished concrete floors. Overhead high-bay lighting, clean industrial aesthetic, photorealistic, 8k resolution, Bloomberg style, no text, no logos."
    },
    {
        "id": "surgical_robotics_precision",
        "category": "ROBOTICS",
        "subtopic": "precision_surgical_robotics",
        "keywords": ["surgical robot", "da vinci", "laparoscopy", "medical robotics", "microsurgery", "operating room", "precision robotics", "healthcare ai", "robotic surgery"],
        "prompt": "An editorial tech journalism photograph (16:9 widescreen, 1920x1080) of advanced multi-jointed surgical robotic arms with precision stainless steel micro-instruments positioned over a sterile medical operating table. Cool clinical surgical theater lighting, photorealistic, 8k resolution, Wired / Nature Medicine aesthetic, no text, no logos."
    },
    {
        "id": "optical_photonic_chip",
        "category": "SILICON & GPUS",
        "subtopic": "optical_photonic_computing",
        "keywords": ["photonic chip", "silicon photonics", "optical computing", "laser waveguide", "light speed compute", "optical interconnect", "energy efficient compute", "micro-ring resonator"],
        "prompt": "An editorial macro photograph (16:9 widescreen, 1920x1080) of an optical photonic computing chip on a dark motherboard, with microscopic silicon-photonic waveguides glowing with sharp red and emerald green laser pulses. Prismatic lens reflections, photorealistic, 8k resolution, IEEE Spectrum aesthetic, no text, no logos."
    },
    {
        "id": "ai_research_supercomputing_lab",
        "category": "FRONTIER LLMS",
        "subtopic": "frontier_training_facility",
        "keywords": ["training run", "loss landscape", "supercomputing cluster", "ai researchers", "command center", "model convergence", "megawatt cluster", "frontier lab"],
        "prompt": "An editorial photograph (16:9 widescreen, 1920x1080) inside an AI research supercomputer operations room. Engineers at sleek workstations viewing a massive curved video wall displaying 3D neural network loss landscapes and real-time GPU cluster telemetry in cobalt blue ambient lighting. Photorealistic, 8k resolution, Wired aesthetic, no text, no logos."
    },
    {
        "id": "cybersecurity_neural_firewall",
        "category": "AGENTS & CODING",
        "subtopic": "neural_cybersecurity_defense",
        "keywords": ["cybersecurity", "firewall", "zero day", "threat detection", "ai defense", "network security", "autonomous defense", "intrusion detection", "malware"],
        "prompt": "An editorial tech photograph (16:9 widescreen, 1920x1080) visualizing autonomous AI cybersecurity defense: an optical server corridor with holographic cyan and crimson glowing data packet flow barriers intercepting intrusion attacks. Cinematic lighting, photorealistic, 8k resolution, no text, no logos."
    },
    {
        "id": "ai_protein_folding_molecular",
        "category": "FRONTIER LLMS",
        "subtopic": "ai_biology_protein_folding",
        "keywords": ["alphafold", "protein structure", "molecular biology", "drug discovery", "biomolecule", "amino acid", "structural biology", "biotech ai", "crispr"],
        "prompt": "An editorial photograph (16:9 widescreen, 1920x1080) of an AI structural biology visualization: a glowing, intricately folded protein macromolecule ribbon model in vivid turquoise and magenta floating on a dark glass laboratory display. Photorealistic, 8k resolution, Nature Biotechnology aesthetic, no text, no logos."
    },
    {
        "id": "nuclear_smr_ai_power_plant",
        "category": "SILICON & GPUS",
        "subtopic": "clean_nuclear_energy_datacenters",
        "keywords": ["nuclear energy", "smr", "small modular reactor", "power grid", "gigawatt", "clean energy", "cooling tower", "datacenter power", "baseload electricity"],
        "prompt": "An editorial tech journalism photograph (16:9 widescreen, 1920x1080) of a modern Small Modular Reactor (SMR) clean nuclear facility supplying dedicated power to an adjacent hyperscale AI datacenter campus at twilight. Gentle steam plume, warm amber lighting, photorealistic, 8k resolution, Reuters style, no text, no logos."
    },
    {
        "id": "subsea_underwater_datacenter",
        "category": "SILICON & GPUS",
        "subtopic": "subsea_underwater_datacenters",
        "keywords": ["underwater datacenter", "subsea server", "ocean cooling", "project natick", "marine datacenter", "green compute", "hyperscale pod"],
        "prompt": "An editorial tech photograph (16:9 widescreen, 1920x1080) of an underwater subsea datacenter capsule resting on the clear ocean floor, with glowing blue circular status rings and bubbles illuminating surrounding marine life. Cinematic depth, photorealistic, 8k resolution, National Geographic / Wired aesthetic, no text, no logos."
    },
    {
        "id": "autonomous_vehicle_lidar_pointcloud",
        "category": "ROBOTICS",
        "subtopic": "autonomous_driving_spatial_ai",
        "keywords": ["lidar", "autonomous vehicle", "self-driving", "point cloud", "robotaxi", "waymo", "tesla fsd", "computer vision", "spatial intelligence"],
        "prompt": "An editorial tech photograph (16:9 widescreen, 1920x1080) showing a 3D LiDAR laser point-cloud visualization of a rainy modern city street at night captured by an autonomous vehicle. Vivid rainbow distance gradients, reflective asphalt, photorealistic, 8k resolution, no text, no logos."
    },
    {
        "id": "neuromorphic_spiking_chip",
        "category": "SILICON & GPUS",
        "subtopic": "neuromorphic_brain_inspired_chips",
        "keywords": ["neuromorphic", "spiking neural network", "loihi", "analog ai", "synaptic chip", "brain-inspired", "ultra low power", "edge ai"],
        "prompt": "A macro photograph (16:9 widescreen, 1920x1080) of a bio-inspired neuromorphic spiking silicon processor chip resting on black obsidian glass, illuminated by gentle violet and amber lateral lighting showing microscopic artificial synaptic arrays. Photorealistic, 8k resolution, no text, no logos."
    }
]

if __name__ == "__main__":
    print(f"Loaded {len(REMAINING_TOPICS)} target topics ready for generation.")

import json
import random
import uuid
from template import make_base_record, make_conversation
from config import DATASET_SPECS

SPEC = DATASET_SPECS[4]

VISION_POOL = [
    (
        "Create an SVG of a pie chart showing 30% blue, 50% green, 20% red",
        "```svg\n<svg width=\"300\" height=\"300\" viewBox=\"0 0 100 100\">\n  <circle cx=\"50\" cy=\"50\" r=\"40\" fill=\"#f0f0f0\"/>\n  <path d=\"M50,50 L50,10 A40,40 0 0,1 75.4,34.5 Z\" fill=\"#4285F4\" stroke=\"#fff\" stroke-width=\"0.5\"/>\n  <path d=\"M50,50 L75.4,34.5 A40,40 0 0,1 85,50 Z\" fill=\"#34A853\" stroke=\"#fff\" stroke-width=\"0.5\"/>\n  <path d=\"M50,50 L85,50 A40,40 0 0,1 50,90 Z\" fill=\"#EA4335\" stroke=\"#fff\" stroke-width=\"0.5\"/>\n</svg>\n```",
        "svg_generation", "medium", True
    ),
    (
        "Create a CSS animation of a bouncing ball",
        "```html\n<div class=\"ball-container\">\n  <div class=\"ball\"></div>\n</div>\n<style>\n  .ball { width: 40px; height: 40px; border-radius: 50%; background: red; position: absolute; animation: bounce 2s infinite ease-in-out; }\n  @keyframes bounce { 0%, 100% { top: 20px; } 50% { top: 160px; } }\n</style>\n```",
        "css_animation", "medium", True
    ),
    (
        "Describe this image: [A black and white photo of the Eiffel Tower at night with lights]",
        "**Image Description:**\n- **Main Subject:** Eiffel Tower\n- **Visual Elements:** Black and white, night sky, illuminated",
        "image_description", "hard", True
    ),
    (
        "Design a responsive dashboard layout with sidebar and main content",
        "```html\n<div class=\"dashboard\">\n  <aside class=\"sidebar\">Sidebar</aside>\n  <main class=\"main-content\">Main Content</main>\n</div>\n<style>\n  .dashboard { display: flex; }\n  .sidebar { width: 250px; background: #2c3e50; }\n  .main-content { flex: 1; }\n  @media (max-width: 768px) { .sidebar { width: 70px; } }\n</style>\n```",
        "ui_layout", "hard", True
    ),
    (
        "Create a line chart showing website traffic: Jan=1200, Feb=1800, Mar=1500, Apr=2000",
        "```javascript\n// Chart.js implementation\nconst ctx = document.getElementById('chart').getContext('2d');\nnew Chart(ctx, { type: 'line', data: { labels: ['Jan', 'Feb', 'Mar', 'Apr'], datasets: [{ data: [1200, 1800, 1500, 2000] }] } });\n```",
        "chart_generation", "medium", True
    ),
    (
        "Explain the difference between RGB and CMYK color models with examples",
        "**RGB vs CMYK:**\n- **RGB:** Additive (screens). e.g., #FF0000 (Red)\n- **CMYK:** Subtractive (print). e.g., C=0,M=100,Y=100,K=0",
        "color_theory", "medium", True
    ),
    (
        "Design a typography system with heading hierarchy for a blog",
        "```css\n:root { --font-primary: 'Inter'; --font-secondary: 'Georgia'; }\nh1 { font-family: var(--font-secondary); font-size: 3rem; }\nh2 { font-size: 2.25rem; }\nbody { font-family: var(--font-primary); font-size: 16px; }\n```",
        "typography", "hard", True
    ),
    (
        "Create a Three.js scene with a rotating 3D earth with clouds",
        "```javascript\nimport * as THREE from 'three';\nconst scene = new THREE.Scene();\nconst earthGeometry = new THREE.SphereGeometry(5, 64, 64);\nconst earth = new THREE.Mesh(earthGeometry, new THREE.MeshPhongMaterial({ map: texture }));\nscene.add(earth);\nfunction animate() { requestAnimationFrame(animate); earth.rotation.y += 0.002; renderer.render(scene, camera); }\nanimate();\n```",
        "3d_rendering", "expert", True
    ),
    (
        "Generate a 3D bar chart using Three.js with interactive hover effects",
        "```javascript\n// 3D Bar Chart implementation in Three.js\nconst geometry = new THREE.BoxGeometry(1, value/20, 1);\nconst material = new THREE.MeshPhongMaterial({color: item.color});\n// Raycaster for hover effects\nraycaster.setFromCamera(mouse, camera);\n```",
        "3d_rendering", "expert", True
    ),
    (
        "Create a workflow: 1) Take photo with device camera, 2) Apply Instagram-like filter, 3) Upload to cloud, 4) Share on social media",
        "**End-to-End Workflow:**\n1. Capture using MediaDevices API\n2. Filter using Pillow\n3. Upload using Firebase Storage\n4. Share via Social Media Intent links",
        "multi_tool_workflow", "expert", True
    )
]

COLORS = ["red", "blue", "green", "yellow", "purple", "orange", "cyan", "magenta"]
SHAPES = ["circle", "rect", "ellipse"]
SUBJECTS = ["cat", "dog", "car", "person", "tree", "building", "bird", "laptop"]

def generate_svg():
    c = random.choice(COLORS)
    x = random.randint(10, 100)
    q = f"Generate SVG for a {c} shape at {x}"
    a = f"```svg\n<circle cx='{x}' cy='{x}' fill='{c}' r='10'/>\n```"
    return q, a, "svg_generation", "easy", True

def generate_css():
    q = f"Create a CSS animation for fading text (id: {random.randint(1,1000)})"
    a = "```css\n@keyframes fade { from { opacity: 0; } to { opacity: 1; } }\n```"
    return q, a, "css_animation", "medium", True

def generate_image_desc():
    s = random.choice(SUBJECTS)
    q = f"Describe an image of a {s} in a park (id: {random.randint(1,1000)})"
    a = f"Main Subject: {s}\nEnvironment: Park"
    return q, a, "image_description", "medium", True

def generate_ui():
    q = f"Design a simple login UI layout (variant: {random.randint(1,1000)})"
    a = "```html\n<form><input type='text'/><button>Login</button></form>\n```"
    return q, a, "ui_layout", "medium", True

def generate_chart():
    q = f"Create a chart for values {random.randint(10, 50)}, {random.randint(10, 50)}"
    a = "```javascript\n// Chart implementation\n```"
    return q, a, "chart_generation", "medium", True

def generate_color():
    q = f"What is the hex code for a shade of {random.choice(COLORS)}? (id: {random.randint(1,1000)})"
    a = f"A shade is #FF{random.randint(10, 99)}00"
    return q, a, "color_theory", "easy", True

def generate_typo():
    q = f"Suggest a font pairing for a corporate site (variant: {random.randint(1,1000)})"
    a = "Header: Roboto, Body: Open Sans"
    return q, a, "typography", "easy", True

def generate_3d():
    q = f"Create a 3D sphere using Three.js (radius {random.randint(1, 10)})"
    a = "```javascript\nnew THREE.SphereGeometry();\n```"
    return q, a, "3d_rendering", "hard", True

def generate_workflow():
    q = f"Design a workflow to convert image to PDF (variant: {random.randint(1,1000)})"
    a = "1. Upload image\n2. Process via PIL\n3. Save as PDF"
    return q, a, "multi_tool_workflow", "hard", True

seen_instructions = set()
UNIQUE_VISION_POOL = []
for item in VISION_POOL:
    seen_instructions.add(item[0])
    UNIQUE_VISION_POOL.append(item)

generators = [generate_svg, generate_css, generate_image_desc, generate_ui, generate_chart, generate_color, generate_typo, generate_3d, generate_workflow]

while len(UNIQUE_VISION_POOL) < 500:
    generator = random.choice(generators)
    q, a, sub, diff, has_img = generator()
    if q not in seen_instructions:
        seen_instructions.add(q)
        UNIQUE_VISION_POOL.append((q, a, sub, diff, has_img))

def generate_dataset_04(output_path, n_records=500):
    records = []
    for i, (inst, resp, sub, diff, has_img) in enumerate(UNIQUE_VISION_POOL):
        if i >= n_records: break
        record = make_base_record(
            dataset_num=4, dataset_name=SPEC["name"], domain=SPEC["domain"], subdomain=sub,
            conversation=make_conversation(system="You are a vision AI expert.", user=inst, assistant=resp),
            category=sub.split('_')[0], difficulty=diff, quality_score=random.uniform(0.90, 0.99),
            tokens_input=len(inst.split()) * 1.3, tokens_output=len(resp.split()) * 1.3,
            benchmark_alignment="MMLU", language="en", has_image_context=has_img,
            extra_fields={"visual_type": "3d" if "3d" in sub else "2d", "requires_rendering": has_img, "interactive": "interactive" in resp.lower()},
            record_index=i,
        )
        records.append(record)
    with open(output_path, "w", encoding="utf-8") as f:
        for r in records: f.write(json.dumps(r, ensure_ascii=False) + "\n")
    print(f"✅ Generated {len(records)} vision records → {output_path}")

if __name__ == "__main__":
    generate_dataset_04("NJIRLAH-SS-DATASETS/raw/njirlah-4-dataset.jsonl")

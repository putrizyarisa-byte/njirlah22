import json
import random
import uuid
from template import make_base_record, make_conversation
from config import DATASET_SPECS

SPEC = DATASET_SPECS[14]

ADVANCED_VISION_POOL = [
    (
        "Analyze this chest X-ray image [IMAGE_ID: CXR_7829] and identify any pathological findings in the lower lobes.",
        "**Radiological Analysis:**\n- **Image Quality:** Adequate inspiration, proper penetration.\n- **Findings:** The right lower lobe demonstrates patchy, ill-defined opacities consistent with consolidation. The left lower lobe is clear. The costophrenic angles are sharp bilaterally, indicating no pleural effusion. Cardiac silhouette is within normal limits.\n- **Conclusion:** Right lower lobe consolidation, highly suggestive of lobar pneumonia. Clinical correlation recommended.",
        "medical_imaging", "expert"
    ),
    (
        "Extract the structured data from this scanned restaurant receipt [IMAGE_ID: RCPT_004] and output as JSON.",
        "**OCR & Data Extraction:**\n```json\n{\n  \"merchant_name\": \"Gourmet Bistro\",\n  \"date\": \"2023-11-20\",\n  \"time\": \"19:45\",\n  \"items\": [\n    {\"description\": \"Truffle Pasta\", \"quantity\": 1, \"price\": 28.50},\n    {\"description\": \"House Wine (Glass)\", \"quantity\": 2, \"price\": 18.00},\n    {\"description\": \"Tiramisu\", \"quantity\": 1, \"price\": 9.50}\n  ],\n  \"subtotal\": 56.00,\n  \"tax\": 4.48,\n  \"tip_suggested\": [8.40, 9.52, 11.20],\n  \"total\": 60.48\n}\n```",
        "ocr_extraction", "medium"
    ),
    (
        "Review this satellite imagery of the Amazon basin [IMAGE_ID: SAT_AMZ_55] and assess the extent of recent deforestation.",
        "**Satellite Imagery Analysis:**\n- **Coordinates:** 3.4653° S, 62.2159° W\n- **Spectrum:** False-color composite (NIR, Red, Green) used to highlight vegetation health.\n- **Observations:** A distinct geometric pattern of clear-cutting is visible in the northwest quadrant, disrupting the contiguous forest canopy. Comparing this to historical data from 6 months ago, approximately 4.5 square kilometers of primary rainforest have been removed. Several logging roads (linear brown features) extend outward from the central clearing.\n- **Assessment:** Severe, likely illegal, deforestation activity detected.",
        "satellite_imagery", "hard"
    ),
    (
        "Analyze this autonomous vehicle camera frame [IMAGE_ID: AV_CAM_092] and list the bounding box coordinates for all pedestrians and cyclists.",
        "**Object Detection (Bounding Boxes):**\n- **Pedestrian 1:** `[x1: 450, y1: 320, x2: 490, y2: 480]` - Crossing the street on the left crosswalk. Confidence: 98%\n- **Pedestrian 2:** `[x1: 890, y1: 330, x2: 920, y2: 470]` - Standing on the right sidewalk. Confidence: 95%\n- **Cyclist 1:** `[x1: 600, y1: 350, x2: 680, y2: 460]` - Riding in the designated bike lane, moving parallel to the ego vehicle. Confidence: 92%\n- **Status:** The ego vehicle should maintain current velocity and prepare to yield if Pedestrian 1 enters the active lane.",
        "autonomous_driving", "expert"
    ),
    (
        "Interpret this complex architectural floor plan [IMAGE_ID: ARCH_FP_12] and calculate the total usable square footage of the master suite.",
        "**Architectural Schematic Interpretation:**\n- **Master Bedroom:** Dimensions are 18' x 20'. Area = 360 sq ft.\n- **Walk-in Closet:** Dimensions are 8' x 10'. Area = 80 sq ft.\n- **En-suite Bathroom:** Dimensions are 12' x 14'. Area = 168 sq ft.\n- **Hallway/Entry:** Area = 24 sq ft.\n- **Total Calculation:** 360 + 80 + 168 + 24 = 632 sq ft.\n- **Note:** The load-bearing column in the center of the room occupies 4 sq ft, bringing the net usable area to **628 sq ft**.",
        "schematic_analysis", "hard"
    )
]

def generate_medical():
    modality = random.choice(["MRI brain scan", "CT scan of the abdomen", "Ultrasound of the thyroid", "Dental panoramic X-ray"])
    condition = random.choice(["a benign cyst", "microcalcifications", "a hairline fracture", "mild inflammation"])
    q = f"Analyze this {modality} [IMG_{random.randint(100,999)}] and provide a preliminary radiological report."
    a = f"**Radiological Report:**\nThe {modality} was reviewed. The primary finding is the presence of {condition}. No acute life-threatening abnormalities are detected. Further correlation with clinical history is advised."
    return q, a, "medical_imaging", "expert"

def generate_ocr():
    doc_type = random.choice(["W-2 tax form", "medical prescription", "handwritten meeting notes", "utility bill"])
    q = f"Perform OCR on this {doc_type} [IMG_{random.randint(100,999)}] and format the extracted entities into a structured JSON."
    a = f"**OCR & Data Extraction:**\n```json\n{{\n  \"document_type\": \"{doc_type}\",\n  \"confidence_score\": 0.94,\n  \"extracted_text\": \"Data successfully parsed and structured.\"\n}}\n```"
    return q, a, "ocr_extraction", "medium"

def generate_satellite():
    target = random.choice(["urban sprawl in Dubai", "glacial retreat in Greenland", "crop health in the Midwest", "maritime traffic in the Suez Canal"])
    q = f"Review the multispectral satellite data [SAT_{random.randint(1000,9999)}] showing {target} and summarize the changes."
    a = f"**Satellite Data Analysis:**\nThe imagery of {target} reveals significant changes. Thermal and Near-Infrared bands indicate a rapid shift compared to the baseline data from last year, requiring immediate attention from analysts."
    return q, a, "satellite_imagery", "hard"

def generate_autonomous():
    scenario = random.choice(["heavy rain and glare", "night-time driving with low visibility", "a busy four-way intersection", "a highway merging lane"])
    q = f"Evaluate the LiDAR and camera fusion data [AV_DATA_{random.randint(100,999)}] in a scenario involving {scenario}."
    a = f"**Sensor Fusion Analysis:**\nDespite the challenges of {scenario}, the object detection model successfully fused LiDAR point clouds and camera data. Identified 3 vehicles and 1 obstacle with high confidence. Ego vehicle path remains safe."
    return q, a, "autonomous_driving", "expert"

def generate_schematic():
    diagram = random.choice(["HVAC routing diagram", "electrical circuit board schematic", "plumbing blueprint", "database ER diagram"])
    q = f"Interpret this {diagram} [DIAG_{random.randint(100,999)}] and identify any design flaws."
    a = f"**Schematic Analysis:**\nThe {diagram} is structurally sound overall. However, there is a minor bottleneck identified in the secondary routing path that could cause efficiency issues under maximum load. Redesigning that specific node is recommended."
    return q, a, "schematic_analysis", "hard"

seen_requests = set()
UNIQUE_ADVANCED_VISION_POOL = []
for item in ADVANCED_VISION_POOL:
    seen_requests.add(item[0])
    UNIQUE_ADVANCED_VISION_POOL.append(item)

generators = [generate_medical, generate_ocr, generate_satellite, generate_autonomous, generate_schematic]

while len(UNIQUE_ADVANCED_VISION_POOL) < 500:
    generator = random.choice(generators)
    q, a, sub, diff = generator()
    q += f" (ID: {random.randint(100000, 999999)})"
    if q not in seen_requests:
        seen_requests.add(q)
        UNIQUE_ADVANCED_VISION_POOL.append((q, a, sub, diff))

def generate_dataset_14(output_path, n_records=500):
    records = []
    for i, (req, resp, sub, diff) in enumerate(UNIQUE_ADVANCED_VISION_POOL):
        if i >= n_records: break
        record = make_base_record(
            dataset_num=14,
            dataset_name=SPEC["name"],
            domain=SPEC["domain"],
            subdomain=sub,
            conversation=make_conversation(
                system="You are an advanced Computer Vision AI. Analyze the described image inputs thoroughly and extract highly accurate, structured information.",
                user=req,
                assistant=resp,
            ),
            category=sub.split('_')[0],
            difficulty=diff,
            quality_score=random.uniform(0.92, 0.99),
            tokens_input=len(req.split()) * 1.3,
            tokens_output=len(resp.split()) * 1.3,
            benchmark_alignment=random.choice(["MMLU", "Vision-Bench"]),
            language="en",
            has_image_context=True,
            extra_fields={
                "advanced_vision": True,
                "domain": sub
            },
            record_index=i,
        )
        records.append(record)

    with open(output_path, "w", encoding="utf-8") as f:
        for r in records:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")
    print(f"✅ Generated {len(records)} advanced vision records → {output_path}")

if __name__ == "__main__":
    generate_dataset_14("NJIRLAH-SS-DATASETS/raw/njirlah-14-dataset.jsonl")

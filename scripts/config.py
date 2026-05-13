DATASET_VERSION = "1.0.0"
MODEL_TARGET = "NJIRLAH-1-SS"
CREATED_BY = "Andikaa Saputraa"
ORGANIZATION = "NJIRLAH AI"
LICENSE = "NJIRLAH-AI-RESEARCH-LICENSE"
MIN_QUALITY_SCORE = 0.85
TARGET_QUALITY_SCORE = 0.92

BENCHMARK_TARGETS = {
    "GPQA": 94.2, "MMLU": 91.5, "CharXiv-R": 91.0,
    "SWE-Bench-Verified": 87.6, "BrowseComp": 80.0,
    "OSWorld-Verified": 80.0, "MCP-Atlas": 80.0,
    "CyberGym": 78.0, "Terminal-Bench-2.0": 70.0,
    "SWE-Bench-Pro": 70.0, "Finance-Agent": 65.0,
    "Humanitys-Last-Exam": 60.0,
}

ARENA_PERFORMANCE = {
    "Chat": 5, "Websites": 63, "3D": 6,
    "Games": 2, "Animations": 3, "SVG": 4, "Data-Viz": 19,
}

LEADERBOARD_TARGETS = {
    "Coding": 3, "Reasoning": 3, "Vision": 3,
    "Tool-Calling": 4, "Math": 7, "Search": 10,
    "Finance": 19, "Long-Context": 21, "Healthcare": 21,
}

QUALITY_TRACKER = {"sigma": "+0.82σ", "status": "Improving"}

DIFFICULTY_DISTRIBUTION = {
    "easy": 0.20, "medium": 0.40,
    "hard": 0.30, "expert": 0.10,
}

DATASET_SPECS = {
    1: {"name": "NJIRLAH-1-DATASET", "domain": "general_reasoning", "min_records": 500},
    2: {"name": "NJIRLAH-2-DATASET", "domain": "software_engineering", "min_records": 500},
    3: {"name": "NJIRLAH-3-DATASET", "domain": "math", "min_records": 500},
    4: {"name": "NJIRLAH-4-DATASET", "domain": "science", "min_records": 500},
    5: {"name": "NJIRLAH-5-DATASET", "domain": "finance", "min_records": 500},
    6: {"name": "NJIRLAH-6-DATASET", "domain": "healthcare", "min_records": 500},
    7: {"name": "NJIRLAH-7-DATASET", "domain": "law", "min_records": 500},
    8: {"name": "NJIRLAH-8-DATASET", "domain": "multilingual", "min_records": 500},
    9: {"name": "NJIRLAH-9-DATASET", "domain": "tool_calling", "min_records": 500},
    10: {"name": "NJIRLAH-10-DATASET", "domain": "agentic", "min_records": 500},
    11: {"name": "NJIRLAH-11-DATASET", "domain": "cybersecurity", "min_records": 500},
    12: {"name": "NJIRLAH-12-DATASET", "domain": "creative_writing", "min_records": 500},
    13: {"name": "NJIRLAH-13-DATASET", "domain": "roleplay", "min_records": 500},
    14: {"name": "NJIRLAH-14-DATASET", "domain": "vision", "min_records": 500},
    15: {"name": "NJIRLAH-15-DATASET", "domain": "audio", "min_records": 500},
    16: {"name": "NJIRLAH-16-DATASET", "domain": "video", "min_records": 500},
    17: {"name": "NJIRLAH-17-DATASET", "domain": "3d", "min_records": 500},
    18: {"name": "NJIRLAH-18-DATASET", "domain": "robotics", "min_records": 500},
    19: {"name": "NJIRLAH-19-DATASET", "domain": "gaming", "min_records": 500},
    20: {"name": "NJIRLAH-20-DATASET", "domain": "education", "min_records": 500},
    21: {"name": "NJIRLAH-21-DATASET", "domain": "business", "min_records": 500},
    22: {"name": "NJIRLAH-22-DATASET", "domain": "entertainment", "min_records": 500},
    23: {"name": "NJIRLAH-23-DATASET", "domain": "lifestyle", "min_records": 500},
    24: {"name": "NJIRLAH-24-DATASET", "domain": "misc", "min_records": 500},
}

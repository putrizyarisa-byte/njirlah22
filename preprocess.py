"""
NJIRLAH-1-SS — Dataset Preprocessor v2.0
========================================
Standalone utility untuk memvalidasi dan meng-inspect
dataset sebelum di-upload ke Modal training pipeline.
Updated: 2026-05-11
"""

import json
import glob
import os


def format_conversation(conv: list[dict]) -> str:
    """Format percakapan dari JSONL ke ChatML-style text."""
    parts = []
    for turn in conv:
        role = turn.get("role", "user")
        content = turn.get("content", "")
        if role == "system":
            parts.append(f"<|system|>\n{content}</s>")
        elif role == "user":
            parts.append(f"<|user|>\n{content}</s>")
        elif role == "assistant":
            parts.append(f"<|assistant|>\n{content}</s>")
    return "\n".join(parts)


def preprocess_datasets(data_dir: str = "NJIRLAH-SS-DATASETS/final", min_quality: float = 0.85):
    """Load, filter, dan preprocess seluruh dataset JSONL."""
    file_paths = sorted(glob.glob(os.path.join(data_dir, "*.jsonl")))
    print(f"📂 Found {len(file_paths)} dataset files in '{data_dir}'")

    all_records = []
    stats = {"total_lines": 0, "loaded": 0, "skipped_no_conv": 0,
             "skipped_low_quality": 0, "skipped_short": 0, "errors": 0}

    for fp in file_paths:
        fname = os.path.basename(fp)
        file_loaded = 0
        with open(fp, "r", encoding="utf-8") as f:
            for line in f:
                stats["total_lines"] += 1
                try:
                    record = json.loads(line.strip())

                    # Filter: must have conversation
                    if "conversation" not in record:
                        stats["skipped_no_conv"] += 1
                        continue

                    # Filter: quality score
                    quality = record.get("quality_score", 0)
                    if quality < min_quality:
                        stats["skipped_low_quality"] += 1
                        continue

                    # Format text
                    text = format_conversation(record["conversation"])
                    if len(text.strip()) < 50:
                        stats["skipped_short"] += 1
                        continue

                    all_records.append({
                        "text": text,
                        "id": record.get("id", ""),
                        "domain": record.get("domain", "unknown"),
                        "quality_score": quality,
                    })
                    file_loaded += 1
                    stats["loaded"] += 1
                except (json.JSONDecodeError, KeyError):
                    stats["errors"] += 1

        print(f"  ✅ {fname}: {file_loaded} records loaded")

    # Print summary
    print(f"\n{'='*50}")
    print(f"📊 Preprocessing Summary")
    print(f"{'='*50}")
    print(f"  Total lines scanned : {stats['total_lines']}")
    print(f"  Records loaded      : {stats['loaded']}")
    print(f"  Skipped (no conv)   : {stats['skipped_no_conv']}")
    print(f"  Skipped (low quality): {stats['skipped_low_quality']}")
    print(f"  Skipped (too short) : {stats['skipped_short']}")
    print(f"  Parse errors        : {stats['errors']}")
    print(f"{'='*50}")

    return all_records


if __name__ == "__main__":
    records = preprocess_datasets()
    if records:
        print(f"\n🎉 Dataset ready — {len(records)} records preprocessed successfully!")
        print(f"   Preview first record text (100 chars):")
        print(f"   {records[0]['text'][:100]}...")
    else:
        print("\n❌ No records found. Check your dataset files.")

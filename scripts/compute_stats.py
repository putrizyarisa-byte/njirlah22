import json
from pathlib import Path

def compute_stats(folder="NJIRLAH-SS-DATASETS/final"):
    total = 0
    for i in range(1, 25):
        path = Path(folder)/f"njirlah-{i}-dataset.jsonl"
        if not path.exists(): continue
        with open(path, encoding="utf-8") as f:
            records = [json.loads(line) for line in f]
            total += len(records)
            print(f"Dataset {i}: {len(records)} records")
    print(f"\n📊 Total: {total} records")

if __name__ == "__main__":
    compute_stats()

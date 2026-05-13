import json
from pathlib import Path
from collections import defaultdict

def check_duplicates(folder="NJIRLAH-SS-DATASETS/raw"):
    all_convs = defaultdict(list)
    for i in range(1, 25):
        path = Path(folder)/f"njirlah-{i}-dataset.jsonl"
        if not path.exists(): continue
        with open(path, encoding="utf-8") as f:
            for line_num, line in enumerate(f, 1):
                try:
                    conv = json.dumps(json.loads(line).get("conversation", []), sort_keys=True)
                    all_convs[conv].append((i, line_num))
                except: pass
    for conv, locs in all_convs.items():
        if len(locs) > 1:
            print(f"DUPLICATE: {locs}")
    if all(len(v) == 1 for v in all_convs.values()):
        print(f"[OK] No duplicates".encode('utf-8', 'ignore').decode('utf-8'))
    else:
        print("⚠️ Duplicates found")

if __name__ == "__main__":
    check_duplicates()

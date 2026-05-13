import json, os, glob, sys
sys.stdout.reconfigure(encoding="utf-8")

files = sorted(glob.glob("NJIRLAH-SS-DATASETS/final/*.jsonl"))
sample_files = [files[0], files[len(files)//2], files[-1]]

for fp in sample_files:
    fname = os.path.basename(fp)
    print(f"=== {fname} (First Record) ===")
    with open(fp, "r", encoding="utf-8") as f:
        r = json.loads(f.readline().strip())
        conv = r.get("conversation", [])
        print(f"  Domain: {r.get('domain')}")
        print(f"  Difficulty: {r.get('difficulty')}")
        print(f"  Quality: {r.get('quality_score')}")
        print(f"  Multi-turn: {r.get('multi_turn')}")
        print(f"  Has tool call: {r.get('has_tool_call')}")
        print(f"  Has code: {r.get('has_code')}")
        print(f"  Turns: {len(conv)}")
        for turn in conv:
            role = turn["role"]
            content = turn["content"]
            preview = content[:200].replace("\n", " ")
            print(f"    [{role}] {preview}")
        print()

# Check for MISSING datasets (2, 15-24)
print("=== DATASET COVERAGE CHECK ===")
existing = set()
for fp in files:
    fname = os.path.basename(fp)
    num = fname.replace("njirlah-", "").replace("-dataset.jsonl", "")
    existing.add(int(num))

expected = set(range(1, 25))
missing = expected - existing
print(f"  Expected datasets: 1-24 ({len(expected)} total)")
print(f"  Existing datasets: {sorted(existing)}")
print(f"  MISSING datasets : {sorted(missing)} ({len(missing)} missing)")

# Check diversity - unique system prompts
print("\n=== SYSTEM PROMPT DIVERSITY ===")
unique_systems = set()
for fp in files:
    with open(fp, "r", encoding="utf-8") as f:
        for i, line in enumerate(f):
            if i >= 50:
                break
            r = json.loads(line.strip())
            conv = r.get("conversation", [])
            for turn in conv:
                if turn.get("role") == "system":
                    unique_systems.add(turn["content"][:100])

print(f"  Unique system prompts (from first 50/file): {len(unique_systems)}")
for s in list(unique_systems)[:5]:
    print(f"    - {s}...")

# Check assistant response quality (length distribution)
print("\n=== ASSISTANT RESPONSE LENGTH DISTRIBUTION ===")
asst_lengths = []
for fp in files:
    with open(fp, "r", encoding="utf-8") as f:
        for line in f:
            r = json.loads(line.strip())
            conv = r.get("conversation", [])
            for turn in conv:
                if turn.get("role") == "assistant":
                    asst_lengths.append(len(turn["content"]))

buckets = {"<50 chars": 0, "50-200": 0, "200-500": 0, "500-1000": 0, ">1000": 0}
for l in asst_lengths:
    if l < 50: buckets["<50 chars"] += 1
    elif l < 200: buckets["50-200"] += 1
    elif l < 500: buckets["200-500"] += 1
    elif l < 1000: buckets["500-1000"] += 1
    else: buckets[">1000"] += 1

for k, v in buckets.items():
    pct = 100*v/len(asst_lengths) if asst_lengths else 0
    bar = "#" * int(pct/2)
    print(f"  {k:12s}: {v:5d} ({pct:5.1f}%) {bar}")

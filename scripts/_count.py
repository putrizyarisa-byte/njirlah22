import glob, os
files = sorted(glob.glob("NJIRLAH-SS-DATASETS/final/*.jsonl"))
total = 0
for f in files:
    count = sum(1 for _ in open(f, encoding="utf-8"))
    total += count
    print(f"{os.path.basename(f):45s} {count:5d} records")
print(f"{'='*55}")
print(f"{'Total files':45s} {len(files):5d}")
print(f"{'Total records':45s} {total:5d}")

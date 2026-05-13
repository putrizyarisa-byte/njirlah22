#!/bin/bash
set -e

# Run generator scripts that exist
for i in {1..24}; do
    num=$(printf "%02d" $i)
    script="scripts/gen_dataset_${num}.py"
    if [ -f "$script" ]; then
        echo "Running $script"
        python "$script"
    fi
done

echo "Running validation..."
python scripts/validator.py

echo "Checking for duplicates..."
python scripts/dedup_check.py

echo "Copying files to final directory..."
cp NJIRLAH-SS-DATASETS/raw/*.jsonl NJIRLAH-SS-DATASETS/final/ 2>/dev/null || true

echo "Computing stats..."
python scripts/compute_stats.py

echo "Pipeline completed successfully!"

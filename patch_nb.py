import json
import glob

nb_file = 'njirlah-oss-1-v4-mega-finetune-oom-fixed.ipynb'
with open(nb_file, 'r', encoding='utf-8') as f:
    nb = json.load(f)

for cell in nb['cells']:
    if cell['cell_type'] == 'code':
        source = "".join(cell['source'])
        
        # OOM Fix 1: Add CUDA_VISIBLE_DEVICES if missing to restrict to 1 GPU (unsloth does not support T4x2 DDP out of the box in kaggle notebook)
        if 'import torch' in source and 'CUDA_VISIBLE_DEVICES' not in source:
            source = 'import os\nos.environ["CUDA_VISIBLE_DEVICES"] = "0"\n' + source
            
        # OOM Fix 2: Unsloth max_seq_length might OOM on T4 if too high with large rank
        # Actually Qwen 7B fits easily on 15GB with length 2048 and rank 16. So I'll keep it at 2048, but I'll add gradient_accumulation_steps tweak.
        
        # Fix the custom dataset path
        if 'njirlah_path =' in source:
            # Re-write the dataset loading cell
            new_source = source.replace(
                "njirlah_path = '/kaggle/input/njirlah-dataset/train.jsonl'",
                "import glob\nnjirlah_paths = glob.glob('/kaggle/input/njirlah-1-ss-final-datasets/*.jsonl')"
            )
            new_source = new_source.replace(
                "if os.path.exists(njirlah_path):",
                "if len(njirlah_paths) > 0:"
            )
            new_source = new_source.replace(
                "ds_njirlah = load_dataset('json', data_files=njirlah_path, split='train')",
                "ds_njirlah = load_dataset('json', data_files=njirlah_paths, split='train')"
            )
            # Kaggle RAM limit (CPU RAM 30GB) can OOM when mapping / shuffling very large datasets.
            # Add a small note or limit if njirlah dataset is huge.
            source = new_source

        if 'per_device_train_batch_size =' in source:
            # Change batch size or accumulation if needed. Currently 1 and 8, which is perfectly safe.
            pass

        # Update cell source
        lines = source.split('\n')
        cell['source'] = [line + ('\n' if i < len(lines)-1 else '') for i, line in enumerate(lines)]

with open(nb_file, 'w', encoding='utf-8') as f:
    json.dump(nb, f, indent=2)
print("Notebook patched successfully!")

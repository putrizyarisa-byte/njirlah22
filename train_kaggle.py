"""
NJIRLAH-OSS-1 V4 Mega Finetune (OOM Fixed) untuk Kaggle
Target: Mistral-7B-v0.3 → NJIRLAH-OSS-1
Platform: Kaggle Notebook (GPU T4 x2)
"""

import os
import torch
import json
import glob
from transformers import AutoModelForCausalLM, AutoTokenizer, TrainingArguments, BitsAndBytesConfig
from trl import SFTTrainer, SFTConfig
from peft import LoraConfig, TaskType, prepare_model_for_kbit_training
from datasets import Dataset

def main():
    MODEL_ID = "mistralai/Mistral-7B-v0.3"
    OUTPUT_DIR = "/kaggle/working/njirlah-oss-1-v4"
    CHECKPOINT_DIR = "/kaggle/working/checkpoints"
    
    # Dataset path on Kaggle will be /kaggle/input/njirlah-1-ss-final-datasets/
    DATA_DIR = "/kaggle/input/njirlah-1-ss-final-datasets/"

    print("Step 1: Loading Tokenizer...")
    tokenizer = AutoTokenizer.from_pretrained(MODEL_ID)
    if tokenizer.pad_token is None:
        tokenizer.pad_token = tokenizer.eos_token
        tokenizer.pad_token_id = tokenizer.eos_token_id
    
    print("Step 2: Loading Base Model (4-bit)...")
    quantization_config = BitsAndBytesConfig(
        load_in_4bit=True,
        bnb_4bit_quant_type="nf4",
        bnb_4bit_use_double_quant=True,
        bnb_4bit_compute_dtype=torch.bfloat16
    )

    model = AutoModelForCausalLM.from_pretrained(
        MODEL_ID,
        device_map="auto",
        quantization_config=quantization_config,
        attn_implementation="sdpa", # Menggunakan FlashAttention-2 jika didukung (atau SDPA untuk hemat memori)
    )
    model.config.use_cache = False
    
    # OOM FIX 1: Pastikan gradient checkpointing berjalan sempurna untuk model 4bit
    model = prepare_model_for_kbit_training(model)
    
    print("Step 3: Loading Dataset...")
    all_data = []
    # Kaggle otomatis mengekstrak ZIP dataset ke DATA_DIR
    file_paths = glob.glob(os.path.join(DATA_DIR, "*.jsonl"))
    if not file_paths:
        print("ERROR: Dataset tidak ditemukan di", DATA_DIR)
        return

    for fp in file_paths:
        with open(fp, "r", encoding="utf-8") as f:
            for line in f:
                try:
                    record = json.loads(line.strip())
                    if "conversation" not in record:
                        continue
                    conv = record["conversation"]
                    text_parts = []
                    for turn in conv:
                        role = turn.get("role", "user")
                        content = turn.get("content", "")
                        if role == "system":
                            text_parts.append(f"<|system|>\n{content}</s>")
                        elif role == "user":
                            text_parts.append(f"<|user|>\n{content}</s>")
                        elif role == "assistant":
                            text_parts.append(f"<|assistant|>\n{content}</s>")
                    formatted_text = "\n".join(text_parts)
                    if len(formatted_text.strip()) > 50:
                        all_data.append({"text": formatted_text})
                except:
                    continue

    print(f"Loaded {len(all_data)} dataset records.")
    
    import random
    random.seed(42)
    random.shuffle(all_data)
    
    # OOM FIX 2: Batasi dataset jika terlalu besar untuk Kaggle RAM (maksimal ambil sebagian untuk contoh, misal 20000)
    MAX_SAMPLES = 20000 
    if len(all_data) > MAX_SAMPLES:
        print(f"Memotong dataset dari {len(all_data)} menjadi {MAX_SAMPLES} untuk mencegah OOM CPU RAM.")
        all_data = all_data[:MAX_SAMPLES]
        
    dataset = Dataset.from_list(all_data)

    print("Step 4: Configuring LoRA & Trainer...")
    peft_config = LoraConfig(
        r=16, # OOM FIX 3: Turunkan rank dari 32 ke 16 untuk menghemat memori
        lora_alpha=32,
        lora_dropout=0.05,
        bias="none",
        task_type=TaskType.CAUSAL_LM,
        target_modules=["q_proj", "v_proj"] # OOM FIX 4: Batasi target modules hanya Q dan V untuk T4 GPU
    )

    training_args = SFTConfig(
        output_dir=CHECKPOINT_DIR,
        per_device_train_batch_size=1, # OOM FIX 5: Batch size minimal
        gradient_accumulation_steps=8, # OOM FIX 6: Grad acc steps disesuaikan
        learning_rate=2e-5,
        lr_scheduler_type="cosine",
        num_train_epochs=1, # OOM FIX 7: Kaggle kernel timeout 12 jam, set 1 epoch dulu
        warmup_ratio=0.05,
        weight_decay=0.01,
        max_grad_norm=1.0,
        bf16=False, # T4 Kaggle tidak support bf16 dengan baik, gunakan fp16
        fp16=True, 
        logging_steps=10,
        save_strategy="steps",
        save_steps=100,
        save_total_limit=2,
        dataset_text_field="text",
        max_seq_length=1024, # OOM FIX 8: Kurangi max seq length dari 2048 ke 1024
        packing=False, # OOM FIX 9: Matikan packing agar memori lebih stabil
        report_to="none",
        gradient_checkpointing=True,
        gradient_checkpointing_kwargs={"use_reentrant": False},
        optim="paged_adamw_32bit", # OOM FIX 10: Gunakan paged optimizer untuk hemat VRAM
    )

    trainer = SFTTrainer(
        model=model,
        args=training_args,
        train_dataset=dataset,
        processing_class=tokenizer,
        peft_config=peft_config,
    )

    print("Step 5: Training Started...")
    trainer.train()

    print("Saving Model...")
    trainer.save_model(OUTPUT_DIR)
    tokenizer.save_pretrained(OUTPUT_DIR)
    print("Done! Model saved to", OUTPUT_DIR)

if __name__ == "__main__":
    main()

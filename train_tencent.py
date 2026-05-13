import os
import torch
from datasets import load_dataset
from transformers import (
    AutoModelForCausalLM,
    AutoTokenizer,
    TrainingArguments,
    BitsAndBytesConfig
)
from peft import LoraConfig, get_peft_model, prepare_model_for_kbit_training
from trl import SFTTrainer

# ==============================================================================
# KONFIGURASI TENCENT CLOUD (CVM GPU)
# ==============================================================================
# Jika Anda menggunakan COS (Cloud Object Storage), disarankan untuk melakukan mount 
# menggunakan COSFS ke folder lokal. Misalnya ke /mnt/cos.
# Ubah path ini sesuai dengan lokasi dataset di instance Tencent Anda.
DATASET_PATH = "./NJIRLAH-SS-DATASETS/final/" 
OUTPUT_DIR = "./output/njirlah-tencent"

MODEL_NAME = "mistralai/Mistral-7B-v0.3"

def main():
    print("=" * 60)
    print("🚀 MULAI FINE-TUNING DI TENCENT CLOUD")
    print("=" * 60)

    # 1. Load Tokenizer
    print("\n[1/5] Loading Tokenizer...")
    tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
    tokenizer.pad_token = tokenizer.eos_token
    tokenizer.padding_side = "right"

    # 2. Setup Quantization 4-bit (Sangat penting agar VRAM hemat)
    print("\n[2/5] Setup BitsAndBytes Quantization...")
    bnb_config = BitsAndBytesConfig(
        load_in_4bit=True,
        bnb_4bit_quant_type="nf4",
        bnb_4bit_compute_dtype=torch.bfloat16,
        bnb_4bit_use_double_quant=True,
    )

    # 3. Load Model
    print(f"\n[3/5] Loading Model: {MODEL_NAME}...")
    model = AutoModelForCausalLM.from_pretrained(
        MODEL_NAME,
        quantization_config=bnb_config,
        device_map="auto",
        torch_dtype=torch.bfloat16,
    )
    model.config.use_cache = False
    model = prepare_model_for_kbit_training(model)

    # 4. Setup LoRA
    print("\n[4/5] Setup LoRA Adapters...")
    peft_config = LoraConfig(
        r=32,
        lora_alpha=64,
        lora_dropout=0.05,
        target_modules=[
            "q_proj", "k_proj", "v_proj", "o_proj",
            "gate_proj", "up_proj", "down_proj",
        ],
        bias="none",
        task_type="CAUSAL_LM"
    )
    model = get_peft_model(model, peft_config)
    model.print_trainable_parameters()

    # 5. Load Dataset
    print("\n[5/5] Loading Dataset...")
    # Cari semua file jsonl di direktori dataset
    import glob
    data_files = glob.glob(os.path.join(DATASET_PATH, "*.jsonl"))
    
    if not data_files:
        print(f"❌ ERROR: Dataset tidak ditemukan di {DATASET_PATH}")
        print("Silakan upload dataset ke folder tersebut atau mount COSFS.")
        return

    dataset = load_dataset("json", data_files=data_files)
    
    # Fungsi pemformatan ChatML
    def formatting_prompts_func(example):
        output_texts = []
        for i in range(len(example['conversation'])):
            conversation = example['conversation'][i]
            if not isinstance(conversation, list):
                continue
            
            text_parts = []
            for turn in conversation:
                role = turn.get("role", "user")
                content = turn.get("content", "")
                text_parts.append(f"<|{role}|>\n{content}</s>")
            
            output_texts.append("\n".join(text_parts))
        return output_texts

    # 6. Training Arguments
    print("\n⚙️ Menyiapkan Training Arguments...")
    training_args = TrainingArguments(
        output_dir=OUTPUT_DIR,
        per_device_train_batch_size=2,
        gradient_accumulation_steps=8,  # Total batch size efektif = 16
        learning_rate=2e-5,
        lr_scheduler_type="cosine",
        num_train_epochs=3,
        warmup_ratio=0.05,
        weight_decay=0.01,
        max_grad_norm=1.0,
        bf16=True, # Gunakan bf16 untuk GPU Ampere (A10/A100)
        logging_steps=5,
        save_strategy="steps",
        save_steps=50, # Save checkpoint setiap 50 steps
        save_total_limit=3, # Simpan maksimal 3 checkpoint terakhir
        report_to="none",
        seed=42,
        optim="adamw_torch",
        gradient_checkpointing=True,
    )

    # 7. Start Training
    print("\n🚀 Memulai Proses SFTTrainer...")
    trainer = SFTTrainer(
        model=model,
        args=training_args,
        train_dataset=dataset["train"],
        formatting_func=formatting_prompts_func,
        peft_config=peft_config,
        max_seq_length=2048,
        packing=False,
    )

    # Auto-resume jika ada checkpoint di output dir
    from transformers.trainer_utils import get_last_checkpoint
    last_checkpoint = get_last_checkpoint(OUTPUT_DIR)
    
    if last_checkpoint is not None:
        print(f"\n🔄 Melanjutkan training dari {last_checkpoint}")
        trainer.train(resume_from_checkpoint=last_checkpoint)
    else:
        trainer.train()

    # 8. Save Final Model
    print("\n✅ Training Selesai! Menyimpan model akhir...")
    trainer.model.save_pretrained(os.path.join(OUTPUT_DIR, "final_adapter"))
    tokenizer.save_pretrained(os.path.join(OUTPUT_DIR, "final_adapter"))
    print("Selesai.")

if __name__ == "__main__":
    main()

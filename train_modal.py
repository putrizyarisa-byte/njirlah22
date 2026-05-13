"""
NJIRLAH-1-SS Fine-Tuning Pipeline v2.0
======================================
Target: Mistral-7B-v0.3 → NJIRLAH-1-SS (LoRA/PEFT)
Platform: Modal Cloud (GPU A10G)
Updated: 2026-05-11 — Modal SDK v1.4.x compatible
"""

import modal

# ─── Modal App (pengganti modal.Stub yang sudah deprecated) ─────────────────
app = modal.App("njirlah-finetune")

# ─── Container Image ────────────────────────────────────────────────────────
# Pin semua versi library agar API stabil dan reproducible
training_image = (
    modal.Image.debian_slim(python_version="3.11")
    .pip_install(
        "torch==2.4.1",
        "transformers==4.48.1",
        "datasets==3.2.0",
        "accelerate==1.3.0",
        "bitsandbytes==0.45.0",
        "trl==0.14.0",
        "peft==0.14.0",
        "scipy",
        "rich",
        "safetensors",
        "sentencepiece",
        "protobuf",
    )
)

# ─── Persistent Volumes ─────────────────────────────────────────────────────
# Volume untuk cache model base (hemat waktu re-download)
model_cache_vol = modal.Volume.from_name("njirlah-model-cache", create_if_missing=True)
# Volume untuk menyimpan checkpoints & model hasil training
output_vol = modal.Volume.from_name("njirlah-model-output", create_if_missing=True)

# ─── Embed dataset lokal ke dalam container image ───────────────────────────
training_image = training_image.add_local_dir(
    local_path="./NJIRLAH-SS-DATASETS/final",
    remote_path="/data/njirlah",
)


# ═══════════════════════════════════════════════════════════════════════════
# TRAINING FUNCTION
# ═══════════════════════════════════════════════════════════════════════════
@app.function(
    image=training_image,
    gpu="A10G",
    timeout=86400,  # 24 jam
    volumes={
        "/model_cache": model_cache_vol,
        "/output": output_vol,
    },
)
def train():
    from transformers import AutoModelForCausalLM, AutoTokenizer, TrainingArguments
    from trl import SFTTrainer, SFTConfig
    from peft import LoraConfig, TaskType
    from datasets import Dataset
    import torch
    import json
    import glob
    import os
    from rich.console import Console
    from rich.table import Table

    console = Console()

    MODEL_ID = "mistralai/Mistral-7B-v0.3"
    CACHE_DIR = "/model_cache/hub"
    OUTPUT_DIR = "/output/njirlah-1-ss"
    CHECKPOINT_DIR = "/output/checkpoints"

    # ── Step 1: Load Tokenizer ──────────────────────────────────────────
    console.rule("[bold cyan]Step 1/5: Loading Tokenizer")
    tokenizer = AutoTokenizer.from_pretrained(
        MODEL_ID,
        cache_dir=CACHE_DIR,
        trust_remote_code=True,
    )
    # Mistral menggunakan EOS token sebagai pad token
    if tokenizer.pad_token is None:
        tokenizer.pad_token = tokenizer.eos_token
        tokenizer.pad_token_id = tokenizer.eos_token_id
    console.print(f"  ✅ Tokenizer loaded — vocab size: {tokenizer.vocab_size}")

    # ── Step 2: Load Base Model ─────────────────────────────────────────
    console.rule("[bold cyan]Step 2/5: Loading Base Model (Mistral-7B)")
    from transformers import BitsAndBytesConfig
    
    quantization_config = BitsAndBytesConfig(
        load_in_4bit=True,
        bnb_4bit_quant_type="nf4",
        bnb_4bit_use_double_quant=True,
        bnb_4bit_compute_dtype=torch.bfloat16
    )

    model = AutoModelForCausalLM.from_pretrained(
        MODEL_ID,
        cache_dir=CACHE_DIR,
        device_map="auto",
        trust_remote_code=True,
        attn_implementation="sdpa",
        quantization_config=quantization_config,
    )
    model.config.use_cache = False  # Disable KV-cache saat training
    
    from peft import prepare_model_for_kbit_training
    model = prepare_model_for_kbit_training(model)
    
    console.print(f"  ✅ Model loaded (4-bit QLoRA) — params: {model.num_parameters():,}")

    # ── Step 3: Load & Format Dataset ───────────────────────────────────
    console.rule("[bold cyan]Step 3/5: Loading & Formatting Dataset")
    all_data = []
    file_paths = sorted(glob.glob("/data/njirlah/*.jsonl"))
    console.print(f"  📂 Found {len(file_paths)} local dataset files")

    stats_table = Table(title="Dataset Loading Stats")
    stats_table.add_column("Source", style="cyan")
    stats_table.add_column("Records", justify="right", style="green")
    stats_table.add_column("Skipped", justify="right", style="red")

    # 1. Load Local NJIRLAH Datasets
    for fp in file_paths:
        loaded, skipped = 0, 0
        with open(fp, "r", encoding="utf-8") as f:
            for line in f:
                try:
                    record = json.loads(line.strip())
                    if "conversation" not in record:
                        skipped += 1
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
                        loaded += 1
                    else:
                        skipped += 1
                except (json.JSONDecodeError, KeyError):
                    skipped += 1
        stats_table.add_row(f"Local: {os.path.basename(fp)}", str(loaded), str(skipped))

    # 2. Load Open-Source Augmentation Datasets
    from datasets import load_dataset
    console.print("\n  🌐 Downloading high-quality open-source datasets for benchmark augmentation...")
    
    # a. OpenHermes-2.5 (Coding & General Reasoning) - Take 10,000 samples
    try:
        hermes_ds = load_dataset("teknium/OpenHermes-2.5", split="train", streaming=True)
        hermes_loaded = 0
        for item in hermes_ds:
            if hermes_loaded >= 10000: break
            if "conversations" not in item: continue
            text_parts = []
            for turn in item["conversations"]:
                role_map = {"human": "user", "gpt": "assistant", "system": "system"}
                role = role_map.get(turn.get("from", ""), "user")
                content = turn.get("value", "")
                text_parts.append(f"<|{role}|>\n{content}</s>")
            all_data.append({"text": "\n".join(text_parts)})
            hermes_loaded += 1
        stats_table.add_row("HF: OpenHermes-2.5", str(hermes_loaded), "0")
    except Exception as e:
        console.print(f"[red]  Failed to load OpenHermes: {e}[/red]")

    # b. MetaMathQA (Advanced Mathematics) - Take 10,000 samples
    try:
        math_ds = load_dataset("meta-math/MetaMathQA", split="train", streaming=True)
        math_loaded = 0
        for item in math_ds:
            if math_loaded >= 10000: break
            if "query" not in item or "response" not in item: continue
            q = item["query"]
            a = item["response"]
            text = f"<|system|>\nYou are a helpful math assistant. Provide step-by-step solutions.</s>\n<|user|>\n{q}</s>\n<|assistant|>\n{a}</s>"
            all_data.append({"text": text})
            math_loaded += 1
        stats_table.add_row("HF: MetaMathQA", str(math_loaded), "0")
    except Exception as e:
        console.print(f"[red]  Failed to load MetaMathQA: {e}[/red]")

    console.print(stats_table)
    console.print(f"\n  📊 Total blended training records: [bold green]{len(all_data):,}[/bold green]")

    if len(all_data) == 0:
        console.print("[bold red]❌ ERROR: No valid training data found! Aborting.[/bold red]")
        return

    # Shuffle the blended dataset
    import random
    random.seed(42)
    random.shuffle(all_data)
    
    dataset = Dataset.from_list(all_data)

    # ── Step 4: Configure LoRA + Trainer ────────────────────────────────
    console.rule("[bold cyan]Step 4/5: Configuring LoRA + SFTTrainer")

    peft_config = LoraConfig(
        r=32,
        lora_alpha=64,
        lora_dropout=0.05,
        bias="none",
        task_type=TaskType.CAUSAL_LM,
        target_modules=[
            "q_proj", "k_proj", "v_proj", "o_proj",
            "gate_proj", "up_proj", "down_proj",
        ],
    )
    console.print(f"  🔧 LoRA rank: {peft_config.r}, alpha: {peft_config.lora_alpha}")
    console.print(f"  🎯 Target modules: {peft_config.target_modules}")

    training_args = SFTConfig(
        output_dir=CHECKPOINT_DIR,
        # ── Batch & Accumulation ──
        per_device_train_batch_size=1,
        gradient_accumulation_steps=16,
        # ── Learning Rate ──
        learning_rate=2e-5,
        lr_scheduler_type="cosine",
        # ── Epochs & Steps ──
        num_train_epochs=3,
        warmup_ratio=0.05,
        # ── Regularization ──
        weight_decay=0.01,
        max_grad_norm=1.0,
        # ── Precision ──
        bf16=True,
        # ── Logging & Saving ──
        logging_steps=5,
        save_strategy="steps",
        save_steps=50,
        save_total_limit=3,
        # ── Dataset ──
        dataset_text_field="text",
        max_seq_length=2048,
        packing=True,  # Pack multiple samples ke satu sequence
        # ── Misc ──
        report_to="none",
        seed=42,
        gradient_checkpointing=True,
        gradient_checkpointing_kwargs={"use_reentrant": False},
        optim="adamw_torch",
    )

    trainer = SFTTrainer(
        model=model,
        args=training_args,
        train_dataset=dataset,
        processing_class=tokenizer,
        peft_config=peft_config,
    )

    trainable_params = sum(p.numel() for p in model.parameters() if p.requires_grad)
    total_params = sum(p.numel() for p in model.parameters())
    console.print(f"  📈 Trainable params: {trainable_params:,} / {total_params:,} "
                  f"({100 * trainable_params / total_params:.2f}%)")

    # ── Step 5: TRAIN ───────────────────────────────────────────────────
    console.rule("[bold green]Step 5/5: 🚀 TRAINING STARTED")
    
    # Auto-resume dari checkpoint terakhir jika ada
    import os
    from transformers.trainer_utils import get_last_checkpoint
    
    last_checkpoint = get_last_checkpoint(CHECKPOINT_DIR)
    if last_checkpoint is not None:
        console.print(f"[bold yellow]🔄 Melanjutkan training dari {last_checkpoint}[/bold yellow]")
        train_result = trainer.train(resume_from_checkpoint=last_checkpoint)
    else:
        train_result = trainer.train()

    # ── Save Results ────────────────────────────────────────────────────
    console.rule("[bold green]✅ Training Complete — Saving Model")
    trainer.save_model(OUTPUT_DIR)
    tokenizer.save_pretrained(OUTPUT_DIR)

    # Commit volumes agar data persisten
    model_cache_vol.commit()
    output_vol.commit()

    # Print summary
    summary_table = Table(title="Training Summary")
    summary_table.add_column("Metric", style="cyan")
    summary_table.add_column("Value", justify="right", style="green")
    summary_table.add_row("Total Steps", str(train_result.global_step))
    summary_table.add_row("Final Loss", f"{train_result.training_loss:.4f}")
    summary_table.add_row("Total Records", str(len(all_data)))
    summary_table.add_row("Model Saved To", OUTPUT_DIR)
    console.print(summary_table)

    console.print("\n[bold green]🎉 Model NJIRLAH-1-SS berhasil di-fine-tune dan disimpan "
                  "ke Modal Volume 'njirlah-model-output'![/bold green]")

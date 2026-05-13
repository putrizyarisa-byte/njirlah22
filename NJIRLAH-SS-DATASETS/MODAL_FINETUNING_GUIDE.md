# Panduan Lengkap NJIRLAH-1-SS Fine-Tuning & Deployment (Modal Cloud)

> **Updated:** 2026-05-11 — Modal SDK v1.4.x Compatible  
> **Profile:** `andikaasaputraarimex`  
> **Base Model:** `mistralai/Mistral-7B-v0.3`  
> **Technique:** LoRA (PEFT) via SFTTrainer (trl)

---

## **🚀 Quick Start (3 Langkah)**

```bash
# 1. Pastikan Modal CLI sudah login
modal setup

# 2. Health check environment
modal run modal_setup.py::health_check

# 3. Jalankan training
modal run train_modal.py::train
```

---

## **1. Arsitektur Pipeline**

```
┌──────────────┐     ┌───────────────┐     ┌──────────────────┐
│  Dataset      │────▶│  Training      │────▶│  Deployment       │
│  (JSONL/final)│     │  (train_modal)  │     │  (deploy_modal)   │
└──────────────┘     └───────────────┘     └──────────────────┘
       │                    │                       │
       ▼                    ▼                       ▼
  13 dataset files    Modal GPU A10G          REST API Endpoint
  ChatML format       LoRA r=32, α=64         /api_generate
  Quality ≥ 0.85      bf16 + packing          Auto-scale 0→N
```

---

## **2. Setup Modal Environment**

### **A. Autentikasi**
```bash
# Login ke Modal (browser akan terbuka otomatis)
modal setup

# Token disimpan di: ~/.modal.toml
# Profile aktif: andikaasaputraarimex
```

### **B. Health Check**
```python
# modal_setup.py
import modal

app = modal.App("njirlah-setup-check")

@app.function(image=modal.Image.debian_slim(python_version="3.11"), timeout=120)
def health_check():
    import platform
    print(f"Python: {platform.python_version()}")
    print(f"Platform: {platform.platform()}")
    print("✅ Modal environment is healthy!")
    return True
```

```bash
modal run modal_setup.py::health_check
```

---

## **3. Training Configuration**

### **A. Container Image**
```python
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
        "scipy", "rich", "safetensors",
        "sentencepiece", "protobuf",
    )
)
```

### **B. Persistent Volumes**
```python
# Cache model agar tidak re-download setiap run
model_cache_vol = modal.Volume.from_name("njirlah-model-cache", create_if_missing=True)

# Output checkpoints & model final
output_vol = modal.Volume.from_name("njirlah-model-output", create_if_missing=True)
```

### **C. LoRA Configuration**
| Parameter | Value | Alasan |
|-----------|-------|--------|
| `r` | 32 | Balance antara kapasitas dan efisiensi |
| `lora_alpha` | 64 | Ratio alpha/r = 2 untuk stabilitas |
| `lora_dropout` | 0.05 | Regularisasi ringan |
| `target_modules` | q,k,v,o,gate,up,down | Full attention + MLP |
| `task_type` | CAUSAL_LM | Untuk text generation |

### **D. Training Hyperparameters**
| Parameter | Value | Notes |
|-----------|-------|-------|
| `batch_size` | 2 | Per device |
| `gradient_accumulation` | 8 | Effective batch = 16 |
| `learning_rate` | 2e-5 | Cosine scheduler |
| `warmup_ratio` | 0.05 | 5% dari total steps |
| `num_epochs` | 3 | Standard SFT |
| `max_seq_length` | 4096 | Mistral's context |
| `bf16` | True | BFloat16 precision |
| `packing` | True | Pack samples ke satu sequence |
| `gradient_checkpointing` | True | Hemat VRAM |

---

## **4. Menjalankan Training**

```bash
# Standard run
modal run train_modal.py::train

# Dengan GPU spesifik (jika ingin ganti)
# Edit gpu="A10G" di train_modal.py → gpu="A100" atau gpu="H100"
```

### **Monitoring Progress**
- Logs akan muncul langsung di terminal
- Checkpoints disimpan setiap 200 steps ke Volume
- Maximum 3 checkpoints dipertahankan (save_total_limit=3)

---

## **5. Deployment & Inference**

### **A. Deploy sebagai Endpoint**
```bash
modal deploy deploy_modal.py
```

### **B. Test via Python**
```python
import modal

Model = modal.Cls.from_name("njirlah-inference", "NjirlahModel")
model = Model()
response = model.generate.remote("Explain quantum computing in simple terms")
print(response)
```

### **C. REST API (Web Endpoint)**
Setelah `modal deploy`, endpoint URL akan diberikan. Contoh:

```bash
curl -X POST https://your-app--njirlahmodel-api-generate.modal.run \
  -H "Content-Type: application/json" \
  -d '{"prompt": "Explain quantum computing", "max_tokens": 256}'
```

Response:
```json
{
  "model": "njirlah-1-ss",
  "response": "...",
  "status": "ok"
}
```

---

## **6. File Structure**

```
TOD/
├── train_modal.py       # 🎯 Script training utama (Modal)
├── deploy_modal.py      # 🚀 Script deployment/inference (Modal)
├── modal_setup.py       # 🔧 Health check & volume inspector
├── preprocess.py        # 📊 Local dataset preprocessor & inspector
├── scripts/             # 🏭 Dataset generation pipeline
│   ├── config.py        #    Konfigurasi & metadata
│   ├── template.py      #    Template pembuat record
│   ├── gen_dataset_*.py #    Generator per domain
│   ├── validator.py     #    Validasi skema JSONL
│   ├── dedup_check.py   #    Pengecekan duplikasi
│   └── compute_stats.py #    Statistik dataset
└── NJIRLAH-SS-DATASETS/ # 📁 Data output
    ├── raw/             #    Data mentah
    ├── validated/       #    Data tervalidasi
    ├── final/           #    ✅ Data siap training
    └── logs/            #    Log pipeline
```

---

## **7. Troubleshooting**

| **Issue** | **Solution** |
|-----------|-------------|
| `modal.Stub is not defined` | Gunakan `modal.App` (Stub sudah deprecated sejak SDK v1.0) |
| CUDA Out of Memory | Kurangi `per_device_train_batch_size` ke 1 |
| Training terlalu lambat | Naikkan `gradient_accumulation_steps` |
| Model tidak konvergen | Coba `learning_rate=5e-6` atau kurangi `lora_dropout` |
| Volume kosong setelah training | Pastikan `volume.commit()` dipanggil |
| Flash Attention error | Hapus `attn_implementation="flash_attention_2"` dari `train_modal.py` |
| Token expired | Jalankan `modal setup` untuk re-autentikasi |

---

## **📊 Target & Estimasi**

| **Metric** | **Target** | **Estimasi** |
|------------|-----------|-------------|
| Training Time | 6-10 jam | ~8 jam (A10G) |
| Final Loss | < 1.5 | 1.0-1.3 |
| Total Records | 5000+ | ~6500 |
| Inference Latency | < 2s | 1.0-1.5s |
| Cost (Modal) | $30-80 | ~$50 |

---

## **⚠️ Prasyarat**

- [x] Modal CLI terinstal (`pip install modal`)
- [x] Modal account aktif & ter-autentikasi (`modal setup`)
- [x] Dataset tersedia di `NJIRLAH-SS-DATASETS/final/`
- [ ] HuggingFace token (jika model gated — set via `modal secret`)
- [ ] Opsional: WandB account untuk logging lanjutan

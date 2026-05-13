"""
NJIRLAH-1-SS — Mistral Fine-Tuning via Direct REST API
=======================================================
Bypass SDK, gunakan requests langsung ke API endpoint.
"""

import json
import glob
import os
import sys
import time
import requests

sys.stdout.reconfigure(encoding="utf-8")

API_KEY = "YOUR_MISTRAL_API_KEY"
BASE_URL = "https://api.mistral.ai/v1"
HEADERS = {"Authorization": f"Bearer {API_KEY}"}

INPUT_DIR = "NJIRLAH-SS-DATASETS/final/*.jsonl"
OUTPUT_FILE = "NJIRLAH-SS-DATASETS/final/mistral_chat_v2.jsonl"
MODEL = "mistral-large-latest"
SUFFIX = "njirlah-v1-ss"


def step1_prepare():
    """Konversi ke format chat yang 100% bersih."""
    print("=" * 60)
    print("  STEP 1: Prepare Dataset (Chat Format)")
    print("=" * 60)

    file_paths = sorted(glob.glob(INPUT_DIR))
    total = 0

    with open(OUTPUT_FILE, "w", encoding="utf-8") as out:
        for fp in file_paths:
            if "mistral_" in os.path.basename(fp):
                continue
            with open(fp, "r", encoding="utf-8") as f:
                for line in f:
                    try:
                        record = json.loads(line)
                        messages = []
                        for turn in record.get("conversation", []):
                            role = turn.get("role", "user")
                            content = turn.get("content", "").strip()
                            if role in ("user", "assistant") and content:
                                messages.append({"role": role, "content": content})

                        # Wajib: minimal 1 user + 1 assistant, terakhir harus assistant
                        if (len(messages) >= 2
                                and messages[-1]["role"] == "assistant"
                                and any(m["role"] == "user" for m in messages)):
                            out.write(json.dumps({"messages": messages}, ensure_ascii=False) + "\n")
                            total += 1
                    except Exception:
                        pass

    size_mb = os.path.getsize(OUTPUT_FILE) / 1024 / 1024
    print(f"  [OK] {total} records -> {OUTPUT_FILE} ({size_mb:.1f} MB)")
    return total


def step2_delete_old_files():
    """Hapus semua file lama agar tidak ada cache."""
    print("\n  [..] Membersihkan file lama di server Mistral...")
    resp = requests.get(f"{BASE_URL}/files", headers=HEADERS)
    if resp.status_code == 200:
        files = resp.json().get("data", [])
        for f in files:
            fid = f["id"]
            requests.delete(f"{BASE_URL}/files/{fid}", headers=HEADERS)
            print(f"  [DEL] Deleted file: {fid}")
        if not files:
            print("  [OK] Tidak ada file lama.")
    else:
        print(f"  [WARN] Gagal list files: {resp.status_code}")


def step3_upload():
    """Upload file baru ke Mistral."""
    print("\n" + "=" * 60)
    print("  STEP 2: Upload Dataset Baru")
    print("=" * 60)

    with open(OUTPUT_FILE, "rb") as f:
        resp = requests.post(
            f"{BASE_URL}/files",
            headers=HEADERS,
            files={"file": ("njirlah_chat_train.jsonl", f, "application/jsonl")},
            data={"purpose": "fine-tune"},
        )

    if resp.status_code in (200, 201):
        file_id = resp.json()["id"]
        print(f"  [OK] File uploaded! ID: {file_id}")
        return file_id
    else:
        print(f"  [ERROR] Upload gagal: {resp.status_code}")
        print(f"  {resp.text}")
        return None


def step4_create_job(file_id):
    """Buat fine-tuning job via REST API."""
    print("\n" + "=" * 60)
    print(f"  STEP 3: Create Fine-Tuning Job")
    print(f"  Model: {MODEL} (BEAST MODE)")
    print("=" * 60)

    # Coba berbagai kombinasi model (dari paling kuat ke paling ringan)
    models_to_try = [
        "mistral-large-latest",
        "mistral-medium-latest",
        "open-mistral-nemo",
        "ministral-8b-latest",
        "mistral-small-latest",
    ]

    for model in models_to_try:
        print(f"\n  [..] Mencoba model: {model}...")
        
        payload = {
            "model": model,
            "training_files": [{"file_id": file_id, "weight": 1}],
            "hyperparameters": {
                "epochs": 3.0,
                "learning_rate": 0.0001,
            },
            "suffix": SUFFIX,
            "auto_start": True,
        }

        resp = requests.post(
            f"{BASE_URL}/fine_tuning/jobs",
            headers={**HEADERS, "Content-Type": "application/json"},
            json=payload,
        )

        if resp.status_code in (200, 201):
            job = resp.json()
            print(f"\n  ====================================================")
            print(f"  [OK] JOB BERHASIL DIBUAT!")
            print(f"  ====================================================")
            print(f"  Model      : {model}")
            print(f"  Job ID     : {job.get('id')}")
            print(f"  Status     : {job.get('status')}")
            print(f"  Fine-tuned : {job.get('fine_tuned_model', 'pending...')}")
            print(f"  ====================================================")
            print(f"\n  Monitor di: https://console.mistral.ai/")
            return job
        else:
            err_text = resp.text[:300]
            print(f"  [FAIL] {model}: {resp.status_code} - {err_text}")
    
    # Jika semua gagal, coba endpoint v2 (chat fine-tuning)
    print(f"\n  [..] Mencoba endpoint /v1/chat/fine_tuning/jobs ...")
    for model in models_to_try[:3]:
        payload = {
            "model": model,
            "training_files": [{"file_id": file_id, "weight": 1}],
            "hyperparameters": {
                "epochs": 3.0,
                "learning_rate": 0.0001,
            },
            "suffix": SUFFIX,
            "auto_start": True,
            "type": "chat",
        }
        resp = requests.post(
            f"{BASE_URL}/fine_tuning/jobs",
            headers={**HEADERS, "Content-Type": "application/json"},
            json=payload,
        )
        if resp.status_code in (200, 201):
            job = resp.json()
            print(f"  [OK] SUKSES dengan {model} + type=chat!")
            print(f"  Job ID: {job.get('id')}")
            return job
        else:
            print(f"  [FAIL] {model} (type=chat): {resp.status_code} - {resp.text[:200]}")
    
    print("\n  [ERROR] Semua model gagal. Silakan cek akun Anda di https://console.mistral.ai/")
    return None


if __name__ == "__main__":
    records = step1_prepare()
    if records == 0:
        print("[ERROR] Tidak ada records!")
        sys.exit(1)

    step2_delete_old_files()
    time.sleep(3)

    file_id = step3_upload()
    if not file_id:
        sys.exit(1)

    print("\n  [..] Menunggu file divalidasi oleh server (20 detik)...")
    time.sleep(20)

    step4_create_job(file_id)

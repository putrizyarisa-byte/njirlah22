"""
NJIRLAH-1-SS — Modal Inference Deployment v2.0
===============================================
Serves the fine-tuned NJIRLAH-1-SS model as a
scalable inference endpoint on Modal Cloud.
Updated: 2026-05-11 — Modal SDK v1.4.x compatible
"""

import modal

app = modal.App("njirlah-inference")

# Volume yang menyimpan model hasil fine-tuning
output_vol = modal.Volume.from_name("njirlah-model-output", create_if_missing=True)
model_cache_vol = modal.Volume.from_name("njirlah-model-cache", create_if_missing=True)

inference_image = (
    modal.Image.debian_slim(python_version="3.11")
    .pip_install(
        "torch==2.4.1",
        "transformers==4.48.1",
        "accelerate==1.3.0",
        "peft==0.14.0",
        "safetensors",
        "sentencepiece",
        "protobuf",
        "rich",
    )
)


@app.cls(
    image=inference_image,
    gpu="A10G",
    container_idle_timeout=300,
    volumes={
        "/output": output_vol,
        "/model_cache": model_cache_vol,
    },
)
class NjirlahModel:
    """Kelas inference untuk model NJIRLAH-1-SS."""

    @modal.enter()
    def load_model(self):
        """Load model dan tokenizer saat container pertama kali start."""
        from transformers import AutoModelForCausalLM, AutoTokenizer
        from peft import PeftModel
        import torch
        from rich.console import Console

        console = Console()
        console.rule("[bold cyan]Loading NJIRLAH-1-SS Model")

        BASE_MODEL = "mistralai/Mistral-7B-v0.3"
        ADAPTER_PATH = "/output/njirlah-1-ss"
        CACHE_DIR = "/model_cache/hub"

        # Load tokenizer
        self.tokenizer = AutoTokenizer.from_pretrained(
            ADAPTER_PATH,
            cache_dir=CACHE_DIR,
            trust_remote_code=True,
        )

        # Load base model + LoRA adapter
        base_model = AutoModelForCausalLM.from_pretrained(
            BASE_MODEL,
            cache_dir=CACHE_DIR,
            torch_dtype=torch.bfloat16,
            device_map="auto",
            trust_remote_code=True,
        )
        self.model = PeftModel.from_pretrained(base_model, ADAPTER_PATH)
        self.model.eval()

        console.print("[bold green]✅ Model NJIRLAH-1-SS loaded and ready![/bold green]")

    @modal.method()
    def generate(self, prompt: str, max_tokens: int = 512, temperature: float = 0.7, top_p: float = 0.9) -> str:
        """Generate respons dari model NJIRLAH-1-SS."""
        import torch

        # Format prompt sebagai ChatML
        formatted = f"<|user|>\n{prompt}</s>\n<|assistant|>\n"

        inputs = self.tokenizer(formatted, return_tensors="pt").to(self.model.device)

        with torch.no_grad():
            outputs = self.model.generate(
                **inputs,
                max_new_tokens=max_tokens,
                do_sample=True,
                temperature=temperature,
                top_p=top_p,
                repetition_penalty=1.15,
                pad_token_id=self.tokenizer.eos_token_id,
            )

        # Decode hanya token baru (bukan prompt)
        generated_ids = outputs[0][inputs["input_ids"].shape[1]:]
        return self.tokenizer.decode(generated_ids, skip_special_tokens=True)

    @modal.web_endpoint(method="POST")
    def api_generate(self, payload: dict) -> dict:
        """HTTP endpoint untuk inference via REST API."""
        prompt = payload.get("prompt", "")
        max_tokens = payload.get("max_tokens", 512)
        temperature = payload.get("temperature", 0.7)

        if not prompt:
            return {"error": "Prompt is required", "status": "error"}

        response = self.generate(prompt, max_tokens=max_tokens, temperature=temperature)
        return {
            "model": "njirlah-1-ss",
            "response": response,
            "status": "ok",
        }

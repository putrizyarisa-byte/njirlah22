from mistralai import Mistral
import sys
sys.stdout.reconfigure(encoding="utf-8")

c = Mistral(api_key="YOUR_MISTRAL_API_KEY")
models = c.models.list()
for m in models.data:
    caps = getattr(m, "capabilities", None)
    ft = getattr(caps, "fine_tuning", None) if caps else None
    if ft:
        print(f"[FINE-TUNABLE] {m.id}")

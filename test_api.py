import requests
import json
import time
from rich.console import Console

console = Console()

# GANTI URL INI DENGAN URL ENDPOINT DARI deploy_modal.py NANTI
API_URL = "https://andikaasaputraa08--njirlah-inference-njirlahmodel-generate.modal.run"

def test_model(prompt):
    console.rule(f"[bold blue]Testing Prompt")
    console.print(f"[cyan]User:[/] {prompt}\n")
    
    payload = {
        "prompt": prompt,
        "max_tokens": 512,
        "temperature": 0.7,
        "top_p": 0.9
    }
    
    start_time = time.time()
    try:
        response = requests.post(API_URL, json=payload)
        response.raise_for_status()
        
        result = response.json()
        end_time = time.time()
        
        console.print(f"[green]NJIRLAH-1-SS:[/] {result}")
        console.print(f"\n[dim]Latency: {end_time - start_time:.2f} detik[/dim]")
        
    except requests.exceptions.RequestException as e:
        console.print(f"[bold red]Error:[/] {e}")
        if hasattr(e, 'response') and e.response is not None:
            console.print(f"[red]Details:[/] {e.response.text}")

if __name__ == "__main__":
    console.print("[bold yellow]NJIRLAH-1-SS API TESTER[/bold yellow]")
    print("="*50)
    
    prompts = [
        "Jelaskan konsep arsitektur microservices menggunakan Kubernetes.",
        "Buatkan fungsi Python untuk melakukan binary search pada array yang sudah disortir.",
        "Jika saya punya 5 apel, lalu makan 2, berapa sisa apel saya? Jelaskan langkah berpikirnya."
    ]
    
    for p in prompts:
        test_model(p)
        time.sleep(1)

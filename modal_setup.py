"""
NJIRLAH-1-SS — Modal Setup & Health Check
==========================================
Utility script untuk verifikasi environment Modal
sebelum menjalankan training pipeline.
Updated: 2026-05-11 — Modal SDK v1.4.x compatible
"""

import modal

app = modal.App("njirlah-setup-check")

image = modal.Image.debian_slim(python_version="3.11").pip_install("rich")


@app.function(image=image, timeout=120)
def health_check():
    """Verifikasi bahwa Modal environment sudah siap."""
    from rich.console import Console
    from rich.table import Table
    import sys
    import platform

    console = Console()
    console.rule("[bold cyan]NJIRLAH-1-SS — Modal Health Check")

    table = Table(title="Environment Info")
    table.add_column("Key", style="cyan")
    table.add_column("Value", style="green")
    table.add_row("Python Version", platform.python_version())
    table.add_row("Platform", platform.platform())
    table.add_row("Architecture", platform.machine())

    console.print(table)
    console.print("\n[bold green]✅ Modal environment is healthy and ready![/bold green]")
    return True


@app.function(image=image, timeout=120)
def list_volumes():
    """List isi volume yang sudah ada."""
    import os
    from rich.console import Console

    console = Console()
    console.rule("[bold cyan]Volume Inspection")

    paths_to_check = ["/model_cache", "/output"]
    for path in paths_to_check:
        if os.path.exists(path):
            console.print(f"\n📂 [cyan]{path}[/cyan]:")
            for root, dirs, files in os.walk(path):
                level = root.replace(path, "").count(os.sep)
                indent = "  " * level
                console.print(f"{indent}📁 {os.path.basename(root)}/")
                sub_indent = "  " * (level + 1)
                for file in files:
                    size = os.path.getsize(os.path.join(root, file))
                    size_str = f"{size / 1024 / 1024:.1f}MB" if size > 1024 * 1024 else f"{size / 1024:.1f}KB"
                    console.print(f"{sub_indent}📄 {file} ({size_str})")
        else:
            console.print(f"\n⚠️  Volume [yellow]{path}[/yellow] not mounted.")

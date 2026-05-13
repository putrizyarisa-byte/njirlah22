import json
from pathlib import Path
from rich.console import Console
from rich.table import Table
from config import *

console = Console()
REQUIRED_FIELDS = ["id", "dataset_name", "domain", "conversation", "quality_score"]
VALID_DIFFICULTIES = {"easy", "medium", "hard", "expert"}
VALID_ROLES = {"system", "user", "assistant", "tool"}

def validate_record(record, line_num):
    errors = []
    for field in REQUIRED_FIELDS:
        if field not in record:
            errors.append(f"Line {line_num}: Missing '{field}'")
    if record.get("quality_score", 0) < MIN_QUALITY_SCORE:
        errors.append(f"Line {line_num}: quality_score too low")
    if record.get("difficulty") not in VALID_DIFFICULTIES:
        errors.append(f"Line {line_num}: Invalid difficulty")
    conv = record.get("conversation", [])
    if not isinstance(conv, list) or len(conv) < 2:
        errors.append(f"Line {line_num}: Invalid conversation")
    return errors

def validate_file(filepath):
    path = Path(filepath)
    if not path.exists():
        return {"error": f"File not found: {filepath}"}
    errors = []
    records = []
    with open(path, encoding="utf-8") as f:
        for line_num, line in enumerate(f, 1):
            try:
                record = json.loads(line)
                records.append(record)
                errors.extend(validate_record(record, line_num))
            except json.JSONDecodeError as e:
                errors.append(f"Line {line_num}: JSON error - {e}")
    return {
        "file": str(path.name),
        "total_records": len(records),
        "errors": errors,
        "passed": len(errors) == 0
    }

def validate_all(folder="NJIRLAH-SS-DATASETS/raw"):
    table = Table(title="Validation Report")
    table.add_column("File", style="cyan")
    table.add_column("Records", justify="right")
    table.add_column("Status", justify="center")
    all_passed = True
    for i in range(1, 25):
        stats = validate_file(f"{folder}/njirlah-{i}-dataset.jsonl")
        if "error" in stats:
            # File doesn't exist, ignore for now to avoid clutter if not fully generated
            continue
        status = "✅ PASS" if stats.get("passed") else "❌ FAIL"
        if not stats.get("passed"):
            all_passed = False
            for err in stats.get("errors", [])[:5]:
                console.print(f"[red]Error in njirlah-{i}.jsonl: {err}[/red]")
        table.add_row(f"njirlah-{i}.jsonl", str(stats.get("total_records", 0)), status)
    console.print(table)
    if all_passed:
        console.print("\n[bold green]🎉 ALL PASSED[/bold green]")
    else:
        console.print("\n[bold red]⚠️ FIX ERRORS[/bold red]")

if __name__ == "__main__":
    validate_all()

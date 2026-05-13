$ErrorActionPreference = "Stop"
$env:PYTHONUTF8 = "1"
$python = ".\njirlah-dataset-env\Scripts\python.exe"

# Only run generator scripts that exist
1..24 | ForEach-Object {
    $script = "scripts\gen_dataset_$([string]::Format('{0:D2}', $_)).py"
    if (Test-Path $script) {
        Write-Host "Running $script"
        & $python $script
    }
    
    # Also check gen_dataset_1.py format
    $script2 = "scripts\gen_dataset_$_.py"
    if (Test-Path $script2) {
        Write-Host "Running $script2"
        & $python $script2
    }
}

Write-Host "Running validation..."
& $python scripts\validator.py

Write-Host "Checking for duplicates..."
& $python scripts\dedup_check.py

Write-Host "Copying files to final directory..."
Copy-Item -Path "NJIRLAH-SS-DATASETS\raw\*.jsonl" -Destination "NJIRLAH-SS-DATASETS\final\" -Force -ErrorAction SilentlyContinue

Write-Host "Computing stats..."
& $python scripts\compute_stats.py

Write-Host "Pipeline completed successfully!"

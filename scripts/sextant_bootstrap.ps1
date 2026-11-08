# SEXTANT mesh bootstrap (Windows / PowerShell 5.1)
# Put a SEXTANT instance on a Windows node (win / win-2) and prove it runs.
# PowerShell 5.1 only: no `??`, no ternary, no -Parallel.
$ErrorActionPreference = "Stop"
$repo = "https://github.com/robmitchellengineering-hub/pacland.git"
if ($env:PACLAND_DIR) { $work = $env:PACLAND_DIR } else { $work = Join-Path $env:USERPROFILE "pacland" }

Write-Output "== SEXTANT bootstrap on $env:COMPUTERNAME =="

# 1. clone or pull
if (Test-Path (Join-Path $work ".git")) {
    git -C $work pull --ff-only 2>&1 | Select-Object -Last 1
    if ($LASTEXITCODE -ne 0) { Write-Output "FAIL: pull"; exit 1 }
} else {
    git clone --depth 1 $repo $work 2>&1 | Select-Object -Last 1
    if ($LASTEXITCODE -ne 0) { Write-Output "FAIL: clone"; exit 1 }
}

# 2. python deps — numpy + stim required, quimb optional
Set-Location $work
python -m venv .venv 2>$null
. .venv\Scripts\Activate.ps1 2>$null
pip install -q --disable-pip-version-check numpy stim 2>&1 | Select-Object -Last 1
if ($LASTEXITCODE -ne 0) { Write-Output "FAIL: pip"; exit 1 }
pip install -q --disable-pip-version-check quimb 2>$null

# 3. run the SEXTANT guard — falsifier suite + exact CHSH control
python scripts\validate_sextant.py 2>&1 | Tee-Object -FilePath $env:TEMP\sextant-guard.txt

# 4. verdict: pass requires the catalog-OK line
if (Select-String -Path $env:TEMP\sextant-guard.txt -Pattern "catalog OK" -Quiet) {
    Write-Output "RESULT: SEXTANT instance is LIVE on $env:COMPUTERNAME"
    exit 0
} else {
    Write-Output "RESULT: guard did not report OK"
    exit 1
}

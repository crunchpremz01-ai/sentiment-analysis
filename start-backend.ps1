# Backend startup script with error checking
Write-Host "Starting backend server..." -ForegroundColor Green
Write-Host ""

# Navigate to backend directory
$backendDir = Join-Path $PSScriptRoot "backend"
if (-not (Test-Path $backendDir)) {
    Write-Host "ERROR: Backend directory not found!" -ForegroundColor Red
    exit 1
}

Set-Location $backendDir

# Check Python
Write-Host "Checking Python..." -ForegroundColor Yellow
$pythonVersion = python --version 2>&1
if ($LASTEXITCODE -ne 0) {
    Write-Host "ERROR: Python not found!" -ForegroundColor Red
    exit 1
}
Write-Host "  $pythonVersion" -ForegroundColor Green

# Check required packages
Write-Host "`nChecking required packages..." -ForegroundColor Yellow
$requiredPackages = @("flask", "sklearn", "numpy", "pandas", "requests", "bs4", "langdetect", "jwt", "scipy")
$missingPackages = @()

foreach ($package in $requiredPackages) {
    $check = python -c "import $package" 2>&1
    if ($LASTEXITCODE -ne 0) {
        $missingPackages += $package
        Write-Host "  ✗ $package - MISSING" -ForegroundColor Red
    } else {
        Write-Host "  ✓ $package" -ForegroundColor Green
    }
}

if ($missingPackages.Count -gt 0) {
    Write-Host "`nInstalling missing packages..." -ForegroundColor Yellow
    python -m pip install Flask Flask-CORS Flask-Mail scikit-learn numpy pandas requests beautifulsoup4 langdetect PyJWT scipy --quiet
    Write-Host "Packages installed!" -ForegroundColor Green
}

# Check model file
Write-Host "`nChecking model file..." -ForegroundColor Yellow
if (Test-Path "walmart_sentiment_new_20251130_181818.pkl") {
    Write-Host "  ✓ Model file found" -ForegroundColor Green
} elseif (Test-Path "latest_model.txt") {
    $modelFile = Get-Content "latest_model.txt" -ErrorAction SilentlyContinue
    if ($modelFile -and (Test-Path $modelFile)) {
        Write-Host "  ✓ Model file found: $modelFile" -ForegroundColor Green
    } else {
        Write-Host "  ⚠ Model file not found - server may fail to start" -ForegroundColor Yellow
    }
} else {
    Write-Host "  ⚠ No model file found - server may fail to start" -ForegroundColor Yellow
}

# Start server
Write-Host "`nStarting Flask server on port 5000..." -ForegroundColor Green
Write-Host "Press Ctrl+C to stop the server`n" -ForegroundColor Yellow
Write-Host "=" * 60 -ForegroundColor Cyan

python backend.py

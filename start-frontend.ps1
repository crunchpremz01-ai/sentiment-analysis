# Quick script to start frontend with Node.js PATH fix
Write-Host "Adding Node.js to PATH..." -ForegroundColor Yellow
$env:Path += ";C:\Program Files\nodejs"

# Verify Node.js is accessible
if (-not (Get-Command node -ErrorAction SilentlyContinue)) {
    Write-Host "ERROR: Node.js not found. Please install Node.js or add it to PATH." -ForegroundColor Red
    Write-Host "Node.js should be at: C:\Program Files\nodejs" -ForegroundColor Yellow
    exit 1
}

Write-Host "Node.js version: $(node --version)" -ForegroundColor Green
Write-Host "npm version: $(npm --version)" -ForegroundColor Green

Write-Host "`nStarting frontend development server on port 3001..." -ForegroundColor Green
cd frontend
npm run dev

# Node.js PATH Fix - Quick Reference

## Problem
`npm` is not recognized because Node.js is not in your system PATH.

## Quick Fix (Each Terminal Session)

**Before running npm commands, always run this first:**
```powershell
$env:Path += ";C:\Program Files\nodejs"
```

**Then verify it works:**
```powershell
node --version
npm --version
```

## Permanent Fix (Recommended)

### Method 1: System Environment Variables (GUI)

1. Press `Win + R`
2. Type: `sysdm.cpl` and press Enter
3. Click **"Advanced"** tab
4. Click **"Environment Variables"**
5. Under **"User variables"** or **"System variables"**, find **"Path"**
6. Click **"Edit"**
7. Click **"New"**
8. Add: `C:\Program Files\nodejs`
9. Click **"OK"** on all dialogs
10. **Restart your terminal/IDE** for changes to take effect

### Method 2: PowerShell (Run as Administrator)

```powershell
[Environment]::SetEnvironmentVariable("Path", $env:Path + ";C:\Program Files\nodejs", [EnvironmentVariableTarget]::User)
```

Then restart your terminal.

## Using the Helper Script

The `start-frontend.ps1` script automatically adds Node.js to PATH:

```powershell
.\start-frontend.ps1
```

This script:
- ✅ Adds Node.js to PATH
- ✅ Verifies Node.js is accessible
- ✅ Shows Node.js and npm versions
- ✅ Starts the frontend dev server

## Manual Commands

If you prefer to run commands manually:

```powershell
# Add Node.js to PATH
$env:Path += ";C:\Program Files\nodejs"

# Navigate to frontend
cd frontend

# Start dev server
npm run dev
```

## Verification

After adding to PATH, verify it works:

```powershell
$env:Path += ";C:\Program Files\nodejs"
node --version    # Should show: v24.11.0
npm --version     # Should show: 11.6.1
```

## Troubleshooting

### If Node.js is not at default location:

1. Find where Node.js is installed:
   ```powershell
   Get-ChildItem "C:\Program Files" -Filter "node.exe" -Recurse -ErrorAction SilentlyContinue
   ```

2. Add that path instead:
   ```powershell
   $env:Path += ";<found-path>"
   ```

### If still not working:

1. Check if Node.js is actually installed:
   ```powershell
   Test-Path "C:\Program Files\nodejs\node.exe"
   ```

2. If it returns `False`, you need to install Node.js:
   - Download from: https://nodejs.org/
   - Install the LTS version
   - Restart your terminal

---

**Quick Tip:** Add this line to your PowerShell profile to always have Node.js in PATH:

```powershell
# Edit profile
notepad $PROFILE

# Add this line:
$env:Path += ";C:\Program Files\nodejs"
```

Then restart PowerShell.

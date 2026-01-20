# Port 3000 Permission Issue - FIXED ✅

## Problem
Port 3000 was already in use or had permission issues with IPv6 (::1).

## Solution Applied
✅ Changed Vite dev server port from **3000** to **3001**  
✅ Set host to **127.0.0.1** (IPv4) to avoid IPv6 permission issues

## Updated Configuration

**File:** `frontend/vite.config.js`

```javascript
server: {
  port: 3001,           // Changed from 3000
  host: '127.0.0.1',   // Added to use IPv4
  proxy: {
    '/api': {
      target: 'http://localhost:5000',
      changeOrigin: true,
    }
  }
}
```

## New Access URLs

- **Frontend:** http://localhost:3001 (changed from 3000)
- **Backend:** http://localhost:5000 (unchanged)

## How to Start

### **Start Frontend (Port 3001)**
```powershell
$env:Path += ";C:\Program Files\nodejs"
cd frontend
npm run dev
```

Or use the helper script:
```powershell
.\start-frontend.ps1
```

The server will now start on **http://localhost:3001**

## Alternative: Free Port 3000

If you want to use port 3000, you can:

1. **Find what's using port 3000:**
   ```powershell
   netstat -ano | findstr :3000
   ```

2. **Kill the process (replace PID with actual process ID):**
   ```powershell
   taskkill /PID <PID> /F
   ```

3. **Or change back to port 3000 in vite.config.js**

---

**Status:** ✅ Fixed - Frontend now runs on port 3001

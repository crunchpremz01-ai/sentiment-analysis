# Quick Installation Commands Reference

## 🚀 Complete Installation Guide

### **1. Backend (Python) Installation**

```bash
# Navigate to project root
cd "C:\Users\RYZEN5\Desktop\sentiment system\E-commerce_Sentiment_Analysis"

# Create and activate virtual environment
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Linux/Mac

# Install all Python dependencies
cd backend
pip install Flask==2.3.3 Flask-CORS==4.0.0 Flask-Mail==0.9.1 selenium==4.15.2 undetected-chromedriver==3.5.4 transformers==4.35.2 torch==2.1.1 scikit-learn==1.3.2 numpy==1.24.3 pandas==2.1.3 requests==2.31.0 langdetect==1.0.9 beautifulsoup4==4.12.2 PyJWT==2.8.0 scipy matplotlib seaborn tqdm

# Or use requirements.txt (then add missing ones)
pip install -r requirements.txt
pip install scipy matplotlib seaborn tqdm

cd ..
```

### **2. Frontend (Node.js) Installation**

```bash
# Navigate to frontend directory
cd frontend

# Install all Node.js dependencies
npm install

# Or using yarn
# yarn install

cd ..
```

### **3. One-Line Installation Commands**

#### **Backend (Python) - Single Command**
```bash
cd backend && pip install Flask==2.3.3 Flask-CORS==4.0.0 Flask-Mail==0.9.1 selenium==4.15.2 undetected-chromedriver==3.5.4 transformers==4.35.2 torch==2.1.1 scikit-learn==1.3.2 numpy==1.24.3 pandas==2.1.3 requests==2.31.0 langdetect==1.0.9 beautifulsoup4==4.12.2 PyJWT==2.8.0 scipy matplotlib seaborn tqdm && cd ..
```

#### **Frontend (Node.js) - Single Command**
```bash
cd frontend && npm install && cd ..
```

### **4. Complete Setup Script (Windows PowerShell)**

```powershell
# Backend Setup
python -m venv venv
venv\Scripts\activate
cd backend
pip install -r requirements.txt
pip install scipy matplotlib seaborn tqdm
cd ..

# Frontend Setup
cd frontend
npm install
cd ..
```

### **5. Complete Setup Script (Linux/Mac Bash)**

```bash
# Backend Setup
python3 -m venv venv
source venv/bin/activate
cd backend
pip install -r requirements.txt
pip install scipy matplotlib seaborn tqdm
cd ..

# Frontend Setup
cd frontend
npm install
cd ..
```

---

## 📋 Dependency List Summary

### **Python Packages (15 core + 4 additional)**
```
Flask==2.3.3
Flask-CORS==4.0.0
Flask-Mail==0.9.1
selenium==4.15.2
undetected-chromedriver==3.5.4
transformers==4.35.2
torch==2.1.1
scikit-learn==1.3.2
numpy==1.24.3
pandas==2.1.3
requests==2.31.0
langdetect==1.0.9
beautifulsoup4==4.12.2
PyJWT==2.8.0
scipy
matplotlib
seaborn
tqdm
```

### **Node.js Packages (4 core + 7 dev)**
```
react@^18.2.0
react-dom@^18.2.0
axios@^1.6.0
lucide-react@^0.294.0
@types/react@^18.2.43
@types/react-dom@^18.2.17
@vitejs/plugin-react@^4.2.1
eslint@^8.55.0
eslint-plugin-react@^7.33.2
eslint-plugin-react-hooks@^4.6.0
eslint-plugin-react-refresh@^0.4.5
vite@^5.0.8
```

---

## 🎯 Running the Application

### **Start Backend**
```bash
cd backend
python backend.py
# Runs on http://localhost:5000
```

### **Start Frontend**
```bash
cd frontend
npm run dev
# Runs on http://localhost:3000
```

---

## ✅ Verification

### **Check Python Installation**
```bash
python -c "import flask, sklearn, numpy, pandas; print('✓ All packages installed')"
```

### **Check Node.js Installation**
```bash
cd frontend
npm list --depth=0
```

### **Test Backend**
```bash
curl http://localhost:5000/api/health
```

### **Test Frontend**
Open browser: `http://localhost:3000`

---

## 🔧 Troubleshooting

### **Python Issues**
```bash
# Upgrade pip
python -m pip install --upgrade pip

# Reinstall all packages
pip install --force-reinstall -r backend/requirements.txt
```

### **Node.js Issues**
```bash
# Clear cache
cd frontend
rm -rf node_modules package-lock.json
npm cache clean --force
npm install
```

---

**Quick Reference**: Copy and paste the commands above for quick setup!

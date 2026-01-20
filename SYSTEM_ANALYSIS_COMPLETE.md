# Complete System Analysis - E-commerce Sentiment Analysis

## 📋 Table of Contents
1. [System Overview](#system-overview)
2. [Complete File List](#complete-file-list)
3. [Dependencies](#dependencies)
4. [Installation Commands](#installation-commands)
5. [Project Structure](#project-structure)

---

## 🎯 System Overview

This is a **Full-Stack E-commerce Sentiment Analysis System** that:
- Scrapes product reviews from Walmart.com
- Analyzes sentiment using an enhanced ML model (TF-IDF + Ensemble)
- Provides a React frontend with authentication
- Stores data in SQLite database
- Supports category-based analysis and filtering

**Tech Stack:**
- **Backend**: Flask (Python)
- **Frontend**: React + Vite
- **Database**: SQLite
- **ML Model**: Scikit-learn (TF-IDF + Ensemble Classifiers)
- **Web Scraping**: ScraperAPI + BeautifulSoup

---

## 📁 Complete File List

### **Backend Files (Python)**

#### Core Backend Files
- `backend/backend.py` - Main Flask application with authentication
- `backend/server.py` - Alternative server implementation
- `backend/database.py` - SQLite database operations
- `backend/requirements.txt` - Python dependencies

#### Scraper Files
- `backend/1Main_Scraper_Final.py` - Main scraper implementation
- `backend/app.py` - Scraper app
- `backend/appv3.py` - Scraper version 3
- `backend/appv4.py` - Scraper version 4
- `backend/appv4better.py` - Improved scraper version 4
- `backend/appv5.py` - Scraper version 5
- `backend/appv6.py` - Scraper version 6
- `backend/app_selenium.py` - Selenium-based scraper
- `backend/app_seleniumv2.py` - Selenium scraper v2
- `backend/app_seleniumv3.py` - Selenium scraper v3
- `backend/app_playwright.py` - Playwright-based scraper
- `backend/backendTest.py` - Backend testing
- `backend/proxy_manager.py` - Proxy management

#### Root Level Python Files
- `CATEGORY_LINK_SCRAPER.py` - Category link scraper
- `REQUEST_SCRAPER.py` - Request-based scraper
- `MULTILINK_SCRAPER.py` - Multi-link scraper
- `MULTILINK_SCRAPER_NEGATIVE.py` - Negative review scraper
- `MULTILINK_SCRAPER_NEUTRAL.py` - Neutral review scraper
- `MUTILINK_SCRAPERv2.py` - Multi-link scraper v2
- `MERGER.py` - Data merger utility
- `converter.py` - Data converter
- `general_review_gen.py` - General review generator
- `negative_review_gen.py` - Negative review generator
- `neutral_review_gen.py` - Neutral review generator
- `test.py` - Test file
- `test_authentication_system.py` - Authentication testing

### **NLP/ML Files**

#### Training & Model Files
- `NLP/training_new.py` - Main training script (Enhanced model)
- `NLP/idiom_awared_best.py` - Best idiom-aware model
- `NLP/idiom_awared.py` - Idiom-aware model v1
- `NLP/idiom_awaredv2.py` - Idiom-aware model v2
- `NLP/idiom_awaredv3.py` - Idiom-aware model v3
- `NLP/inference.py` - Model inference
- `NLP/multi_ml.py` - Multi-model implementation
- `NLP/svm.py` - SVM implementation
- `NLP/svm_regression.py` - SVM regression
- `NLP/unsupervised.py` - Unsupervised learning
- `NLP/dataset_balancer.py` - Dataset balancing utility
- `NLP/SENTIMENT_COUNTER.py` - Sentiment counter

#### Model Files (Pickle)
- `backend/walmart_sentiment_new_20251130_181818.pkl` - Latest trained model
- `backend/model_backup/` - Backup model files
- `latest_model.txt` - Pointer to latest model

### **Frontend Files (React)**

#### Core Frontend Files
- `frontend/package.json` - Node.js dependencies
- `frontend/package-lock.json` - Locked dependencies
- `frontend/vite.config.js` - Vite configuration
- `frontend/index.html` - HTML entry point

#### Source Files
- `frontend/src/main.jsx` - React entry point
- `frontend/src/App.jsx` - Main App component
- `frontend/src/styles/globals.css` - Global styles

#### Components
- `frontend/src/components/analysis/AnalysisForm.jsx` - Analysis form
- `frontend/src/components/analysis/ReviewCard.jsx` - Review card component
- `frontend/src/components/analysis/SentimentChart.jsx` - Sentiment chart
- `frontend/src/components/effects/ParticleNetwork.jsx` - Particle effect
- `frontend/src/components/layout/Navbar.jsx` - Navigation bar
- `frontend/src/components/layout/Sidebar.jsx` - Sidebar component
- `frontend/src/components/ui/AboutModal.jsx` - About modal
- `frontend/src/components/ui/ProgressIndicator.jsx` - Progress indicator
- `frontend/src/components/ui/ResultsModal.jsx` - Results modal

#### Pages
- `frontend/src/pages/HomePage.jsx` - Home page
- `frontend/src/pages/LoginPage.jsx` - Login page
- `frontend/src/pages/RegisterPage.jsx` - Register page
- `frontend/src/pages/DashboardPage.jsx` - Dashboard page
- `frontend/src/pages/ForgotPasswordPage.jsx` - Forgot password page
- `frontend/src/pages/ResetPasswordPage.jsx` - Reset password page

#### Context
- `frontend/src/context/AuthContext.jsx` - Authentication context

### **Data Files**

#### JSON Data Files
- `_combined_new.json` - Combined dataset
- `NLP/added_combined_.json` - Additional combined data
- `NLP/_combined__negative.json` - Negative reviews
- `NLP/_combined__neutral.json` - Neutral reviews
- Multiple JSON files in `NLP/` directory with combined review data

#### CSV Files
- `walmart_reviews_sample_data.csv` - Sample data
- `walmart_reviews_z_files_combined_*.csv` - Combined CSV files
- `backend/scraped_reviews/scrape_*.csv` - Scraped review data

#### Database Files
- `backend/scraped_data.db` - SQLite database

### **Documentation Files**

#### Markdown Documentation
- `SYSTEM_DOCUMENTATION.md` - System documentation
- `QUICK_START_GUIDE.md` - Quick start guide
- `QUICK_TEST_GUIDE.md` - Quick test guide
- `AUTHENTICATION_IMPLEMENTATION.md` - Auth implementation
- `AUTHENTICATION_SUMMARY.md` - Auth summary
- `AUTHENTICATION_TESTING_GUIDE.md` - Auth testing
- `CATEGORY_DASHBOARD_IMPLEMENTATION.md` - Category dashboard
- `BUG_FIX_REPORT.md` - Bug fixes
- `COMPLETE_SYSTEM_ANALYSIS.md` - System analysis
- `COMPLETE_SYSTEM_TEST.md` - System tests
- `COMPLETE_CATEGORY_VERIFICATION.md` - Category verification
- `HISTORY_DELETE_FEATURE.md` - History delete feature
- `VIEW_REVIEWS_FEATURE.md` - View reviews feature
- `ALL_REVIEWS_FEATURE.md` - All reviews feature
- `LANGUAGE_FILTER_IMPLEMENTATION.md` - Language filter
- `CSV_EXPORT_LUCIDE_IMPLEMENTATION.md` - CSV export
- `PERFORMANCE_OPTIMIZATION.md` - Performance optimization
- `CONFIDENCE_THRESHOLD_FEATURE.md` - Confidence threshold
- `CONFIDENCE_THRESHOLD_EXPLAINED.md` - Confidence explanation
- `CATEGORY_SENTIMENT_BAR_EXPLANATION.md` - Category bar explanation
- `SYSTEM_ANALYSIS_CATEGORY_FOCUS.md` - Category focus analysis
- `USER_SESSION_ARCHITECTURE.md` - Session architecture
- `MANUAL_TESTING_GUIDE.md` - Manual testing guide
- `MANUAL_TESTING_CHECKLIST.md` - Testing checklist
- `idiom_awared_best_guide.md` - Idiom-aware guide

#### Text Documentation
- `SYSTEM_DIAGRAMS_AND_FLOWCHARTS.txt` - System diagrams
- `RESEARCH_DOCUMENTATION_GUIDE.txt` - Research guide
- `Research Paper Corrections and Al.txt` - Research corrections

### **Test Files**

#### Test Directory
- `tests/test.py` - Test file 1
- `tests/test2.py` - Test file 2
- `tests/test3.py` - Test file 3
- `tests/test4.py` - Test file 4
- `tests/test5.py` - Test file 5
- `tests/test6.py` - Test file 6
- `tests/pw.py` - Playwright test
- `tests/MULTI_SCRAPER.py` - Multi-scraper test
- `tests/MULTI_SCRAPER_VADER.py` - VADER scraper test
- `tests/MULTI_SCRAPER_TRANSFORMER.py` - Transformer scraper test
- `tests/FINAL.py` - Final test
- `tests/BACKUP.py` - Backup test

### **Data Directories**

- `dataset/` - Training datasets
- `links/` - Product links
- `json_files/` - JSON data files
- `z_files/` - Z files data
- `z_GENERATOR/` - Generated data
- `z_L/` - Additional data
- `backup_synthetic/` - Synthetic data backup
- `test_final_dataset/` - Final test dataset
- `test_negatives/` - Negative test data
- `test_neutrals/` - Neutral test data

### **Other Files**

- `debug_page_*.html` - Debug HTML pages
- `backend/proxies.txt` - Proxy list
- `links/links*.txt` - Link files for different categories

---

## 📦 Dependencies

### **Python Dependencies (Backend)**

#### Core Framework
- `Flask==2.3.3` - Web framework
- `Flask-CORS==4.0.0` - CORS support
- `Flask-Mail==0.9.1` - Email functionality

#### Machine Learning
- `scikit-learn==1.3.2` - ML library
- `numpy==1.24.3` - Numerical computing
- `pandas==2.1.3` - Data manipulation
- `torch==2.1.1` - PyTorch (if using neural networks)
- `transformers==4.35.2` - Transformers library

#### Web Scraping
- `selenium==4.15.2` - Selenium WebDriver
- `undetected-chromedriver==3.5.4` - Undetected Chrome driver
- `beautifulsoup4==4.12.2` - HTML parsing
- `requests==2.31.0` - HTTP requests

#### Utilities
- `langdetect==1.0.9` - Language detection
- `PyJWT==2.8.0` - JWT tokens

#### Additional Dependencies (Used but not in requirements.txt)
- `scipy` - Scientific computing (for sparse matrices)
- `matplotlib` - Plotting (for training visualizations)
- `seaborn` - Statistical visualization
- `tqdm` - Progress bars

### **Node.js Dependencies (Frontend)**

#### Core
- `react==^18.2.0` - React library
- `react-dom==^18.2.0` - React DOM

#### HTTP Client
- `axios==^1.6.0` - HTTP client

#### UI Components
- `lucide-react==^0.294.0` - Icon library

#### Development Dependencies
- `@types/react==^18.2.43` - TypeScript types for React
- `@types/react-dom==^18.2.17` - TypeScript types for React DOM
- `@vitejs/plugin-react==^4.2.1` - Vite React plugin
- `eslint==^8.55.0` - Linter
- `eslint-plugin-react==^7.33.2` - React ESLint plugin
- `eslint-plugin-react-hooks==^4.6.0` - React hooks linting
- `eslint-plugin-react-refresh==^0.4.5` - React refresh linting
- `vite==^5.0.8` - Build tool

---

## 🚀 Installation Commands

### **Prerequisites**

1. **Python 3.8+** (Recommended: Python 3.9 or 3.10)
2. **Node.js 16+** (Recommended: Node.js 18 or 20)
3. **npm** or **yarn** package manager

### **Step 1: Clone/Setup Project**

```bash
# Navigate to project directory
cd "C:\Users\RYZEN5\Desktop\sentiment system\E-commerce_Sentiment_Analysis"
```

### **Step 2: Backend Setup (Python)**

```bash
# Create virtual environment (recommended)
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On Linux/Mac:
# source venv/bin/activate

# Navigate to backend directory
cd backend

# Install Python dependencies
pip install -r requirements.txt

# Install additional dependencies (not in requirements.txt)
pip install scipy matplotlib seaborn tqdm

# Return to root directory
cd ..
```

**Complete Python Installation Command (All at once):**
```bash
pip install Flask==2.3.3 Flask-CORS==4.0.0 Flask-Mail==0.9.1 selenium==4.15.2 undetected-chromedriver==3.5.4 transformers==4.35.2 torch==2.1.1 scikit-learn==1.3.2 numpy==1.24.3 pandas==2.1.3 requests==2.31.0 langdetect==1.0.9 beautifulsoup4==4.12.2 PyJWT==2.8.0 scipy matplotlib seaborn tqdm
```

### **Step 3: Frontend Setup (Node.js)**

```bash
# Navigate to frontend directory
cd frontend

# Install Node.js dependencies
npm install

# Or using yarn:
# yarn install

# Return to root directory
cd ..
```

**Complete Node.js Installation Command:**
```bash
cd frontend && npm install && cd ..
```

### **Step 4: Environment Variables Setup**

Create a `.env` file in the `backend` directory (optional but recommended):

```bash
# backend/.env
SECRET_KEY=your-secret-key-change-in-production
MAIL_PASSWORD=your-gmail-app-password
```

**Note:** For email functionality, you need to:
1. Enable 2-factor authentication on your Gmail account
2. Generate an App Password
3. Set it in the `.env` file or environment variable

### **Step 5: Database Setup**

The database will be created automatically on first run. No manual setup needed.

### **Step 6: Model File**

Ensure the model file exists:
- `backend/walmart_sentiment_new_20251130_181818.pkl`
- Or update `latest_model.txt` to point to the correct model file

---

## 🏗️ Project Structure

```
E-commerce_Sentiment_Analysis/
├── backend/                    # Flask backend
│   ├── backend.py            # Main Flask app
│   ├── server.py             # Alternative server
│   ├── database.py           # Database operations
│   ├── requirements.txt       # Python dependencies
│   ├── scraped_data.db        # SQLite database
│   ├── scraped_reviews/       # CSV exports
│   ├── model_backup/          # Model backups
│   └── *.pkl                  # Trained models
│
├── frontend/                  # React frontend
│   ├── src/
│   │   ├── components/        # React components
│   │   ├── pages/            # Page components
│   │   ├── context/          # React context
│   │   └── styles/           # CSS styles
│   ├── package.json          # Node dependencies
│   └── vite.config.js        # Vite config
│
├── NLP/                       # ML/NLP files
│   ├── training_new.py        # Training script
│   ├── idiom_awared_best.py  # Best model
│   └── *.json                # Training datasets
│
├── dataset/                   # Training datasets
├── links/                     # Product links
├── tests/                     # Test files
└── *.md                       # Documentation
```

---

## 🎯 Quick Start Commands

### **Start Backend Server**
```bash
cd backend
python backend.py
# Server runs on http://localhost:5000
```

### **Start Frontend Development Server**
```bash
cd frontend
npm run dev
# Frontend runs on http://localhost:3000
```

### **Train New Model** (Optional)
```bash
cd NLP
python training_new.py
```

---

## 📝 Notes

1. **Model File**: The system requires a trained model file (`.pkl`). If missing, train one using `NLP/training_new.py`

2. **ScraperAPI Key**: The backend uses ScraperAPI for web scraping. The API key is hardcoded in `backend.py`. For production, move it to environment variables.

3. **Database**: SQLite database is created automatically. No migration needed.

4. **Ports**: 
   - Backend: `5000`
   - Frontend: `3000`

5. **Authentication**: JWT-based authentication with password reset via email.

---

## ✅ Verification Checklist

After installation, verify:

- [ ] Python dependencies installed (`pip list`)
- [ ] Node.js dependencies installed (`npm list`)
- [ ] Model file exists (`backend/*.pkl`)
- [ ] Database file created (`backend/scraped_data.db`)
- [ ] Backend server starts without errors
- [ ] Frontend server starts without errors
- [ ] Can access frontend at `http://localhost:3000`
- [ ] Can access backend API at `http://localhost:5000/api/health`

---

## 🔧 Troubleshooting

### **Python Import Errors**
```bash
# Ensure virtual environment is activated
# Reinstall dependencies
pip install --upgrade -r backend/requirements.txt
```

### **Node.js Module Errors**
```bash
# Clear cache and reinstall
cd frontend
rm -rf node_modules package-lock.json
npm install
```

### **Model Not Found**
- Check `latest_model.txt` points to correct model
- Or ensure `backend/*.pkl` file exists

### **Port Already in Use**
- Change ports in `backend/backend.py` (line 1336) and `frontend/vite.config.js` (line 8)

---

**Last Updated**: 2024-12-01
**System Version**: Enhanced v1.0

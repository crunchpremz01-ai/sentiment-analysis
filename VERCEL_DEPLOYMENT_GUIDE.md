# Walmart Sentiment Analyzer - Vercel Deployment Guide

This guide will help you deploy your Walmart Sentiment Analyzer to Vercel so you can access it with a public URL.

## Prerequisites

1. **Vercel Account**: Sign up at [vercel.com](https://vercel.com/)
2. **Vercel CLI**: Install with `npm install -g vercel`
3. **Git Repository**: Your project should be in a Git repository (GitHub, GitLab, or Bitbucket)

## Deployment Steps

### 1. Prepare Your Project

The following files have been created for Vercel deployment:

- `vercel.json` - Vercel configuration
- `api/` - Backend API directory
- `api/analyze.py` - Main API handler
- `api/requirements.txt` - Python dependencies
- `api/package.json` - API package configuration
- `.env.example` - Environment variables template

### 2. Set Up Environment Variables

Before deploying, you need to configure environment variables in your Vercel project:

1. Go to your Vercel dashboard
2. Create a new project or select existing one
3. Click on "Settings" → "Environment Variables"
4. Add the following variables:

#### Required Variables:
- `SECRET_KEY` - A strong secret key for JWT tokens (generate a random string)

#### Optional Variables:
- `SCRAPER_API_KEY` - Your ScraperAPI key for web scraping
- `MAIL_USERNAME` - Email for password reset functionality
- `MAIL_PASSWORD` - App password for email
- `DATABASE_URL` - Database connection string (SQLite by default)

### 3. Deploy to Vercel

#### Option A: Deploy from Vercel Dashboard
1. Go to [vercel.com](https://vercel.com/)
2. Click "New Project"
3. Connect to your Git repository
4. Configure the project settings:
   - Framework Preset: `Other`
   - Build Command: `npm run build` (or leave empty)
   - Output Directory: `frontend/dist` (or leave empty)
   - Install Command: `npm install`
5. Click "Deploy"

#### Option B: Deploy with Vercel CLI
```bash
# Navigate to your project directory
cd E-commerce_Sentiment_Analysis

# Login to Vercel
vercel login

# Deploy
vercel

# To deploy to production
vercel --prod
```

### 4. Configure Environment Variables in Vercel

After deployment, set environment variables:

```bash
# Set environment variables
vercel env add SECRET_KEY
vercel env add SCRAPER_API_KEY
vercel env add MAIL_USERNAME
vercel env add MAIL_PASSWORD

# Redeploy to apply changes
vercel --prod
```

### 5. Update Frontend API URLs

The frontend is configured to use relative paths (`/api/...`), which will automatically work with Vercel's proxy setup. No changes needed!

## Project Structure for Vercel

```
E-commerce_Sentiment_Analysis/
├── vercel.json              # Vercel configuration
├── frontend/                # React frontend
│   ├── index.html
│   ├── package.json
│   └── src/
├── api/                     # Python backend API
│   ├── analyze.py          # Main API handler
│   ├── requirements.txt    # Python dependencies
│   └── package.json        # API package config
├── backend/                 # Original backend (for reference)
│   ├── backend.py
│   ├── database.py
│   └── ...
└── .env.example            # Environment variables template
```

## Vercel Configuration Details

The `vercel.json` file configures:

- **Builds**: Python functions for `/api/*` routes
- **Routes**: Proxy API requests to backend, serve frontend for other routes
- **Functions**: 5-minute timeout for analysis tasks
- **Static**: Serve frontend files

## API Endpoints

After deployment, your API will be available at:
- `https://your-project.vercel.app/api/health` - Health check
- `https://your-project.vercel.app/api/auth/register` - User registration
- `https://your-project.vercel.app/api/auth/login` - User login
- `https://your-project.vercel.app/api/analyze` - Start analysis
- `https://your-project.vercel.app/api/status/{session_id}` - Check status

## Frontend Access

Your React frontend will be available at:
- `https://your-project.vercel.app/`

## Troubleshooting

### Common Issues:

1. **Import Errors**: Ensure all Python dependencies are in `api/requirements.txt`
2. **Environment Variables**: Check that all required variables are set in Vercel
3. **CORS Issues**: The API includes CORS headers, but you may need to configure allowed origins
4. **Timeout Issues**: Analysis tasks have a 5-minute timeout. For longer tasks, consider using background jobs

### Debugging:

1. Check Vercel logs: `vercel logs`
2. View deployment logs in Vercel dashboard
3. Test API endpoints with curl or Postman
4. Check browser console for frontend errors

## Performance Optimization

1. **Model Loading**: The AI model is loaded once per function invocation
2. **Database**: Uses SQLite by default, consider upgrading for production
3. **Caching**: Consider adding Redis for session storage
4. **CDN**: Vercel automatically serves static assets via CDN

## Security Considerations

1. **JWT Secrets**: Use strong, unique secret keys
2. **API Keys**: Store ScraperAPI keys securely
3. **Database**: Consider using a managed database for production
4. **HTTPS**: Vercel automatically provides SSL certificates

## Cost Considerations

1. **Vercel Free Tier**: 100GB bandwidth, 125k invocations per month
2. **Python Functions**: Billed per invocation and execution time
3. **Database**: SQLite is free, but consider paid options for production
4. **ScraperAPI**: Costs based on usage

## Next Steps

1. **Custom Domain**: Add a custom domain in Vercel settings
2. **Analytics**: Add Google Analytics or other tracking
3. **Monitoring**: Set up error tracking and performance monitoring
4. **CI/CD**: Configure automatic deployments on git push

## Support

For issues with this deployment:
1. Check the Vercel documentation: https://vercel.com/docs
2. Review Python function limitations: https://vercel.com/docs/functions/serverless-functions/runtimes/python
3. Check Vercel community forums

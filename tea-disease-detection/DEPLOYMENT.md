# Deployment Guide - Quick Start

## 🚀 Deploy to Vercel in 5 Minutes

### Step 1: Prepare Your Code
All files are ready in the `tea-disease-detection` folder:
- ✅ Frontend (public/index.html)
- ✅ Backend API (api/predict.py)
- ✅ Configuration (vercel.json)
- ✅ Dependencies (requirements.txt)

### Step 2: Create GitHub Repository

```bash
# Navigate to project folder
cd tea-disease-detection

# Initialize git
git init

# Add all files
git add .

# Commit
git commit -m "Tea leaf disease detection system"

# Create repo on GitHub, then:
git remote add origin https://github.com/YOUR-USERNAME/tea-disease-detection.git
git branch -M main
git push -u origin main
```

### Step 3: Deploy on Vercel

**Option A: Via Dashboard (Recommended)**
1. Go to https://vercel.com/new
2. Sign in with GitHub
3. Click "Import Project"
4. Select your `tea-disease-detection` repository
5. Vercel auto-detects settings - just click "Deploy"
6. Wait 2-3 minutes
7. Done! Copy your live URL

**Option B: Via CLI**
```bash
# Install Vercel CLI
npm install -g vercel

# Login
vercel login

# Deploy
vercel

# Deploy to production
vercel --prod
```

### Step 4: Test Your Deployment
1. Visit your Vercel URL (e.g., `https://tea-disease-detection.vercel.app`)
2. Upload a leaf image
3. Click "Analyze Leaf"
4. Check results!

## 📱 Share with Users
Your app is now live! Share the URL with:
- Tea smallholders
- Agricultural extension officers
- Field agents

## 🔧 Update Deployment
After making changes:
```bash
git add .
git commit -m "Update description"
git push
```
Vercel automatically redeploys!

## ⚠️ Important Notes

### Vercel Free Tier Limits:
- ✅ 100GB bandwidth/month (sufficient for hackathon)
- ✅ Serverless functions (good for ML APIs)
- ⚠️ 50MB max function size (use lightweight models)
- ⚠️ 10 second function timeout

### If Model is Too Large:
Use external model hosting:
- Google Cloud Storage
- AWS S3
- Hugging Face Hub

### For Production Scale:
Consider upgrading to Vercel Pro or deploying to:
- Google Cloud Run
- AWS Lambda
- Azure Functions
- Railway.app

## 🐛 Troubleshooting

**Issue: "Function too large"**
- Solution: Use MobileNetV2 or smaller models
- Or host model externally and load via URL

**Issue: "Build failed"**
- Check requirements.txt versions
- Ensure Python 3.9+ compatibility

**Issue: "API not responding"**
- Check Vercel function logs
- Verify api/predict.py syntax

**Issue: "Slow predictions"**
- Optimize image preprocessing
- Use smaller input sizes (224x224)
- Cache model loading

## 📊 Monitor Usage
View metrics in Vercel Dashboard:
- Function invocations
- Bandwidth usage
- Error rates
- Response times

---

**Need Help?** Check README.md for detailed documentation.

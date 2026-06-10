# IBM TLS Contract Analysis HUB - Deployment Guide

This guide shows you how to deploy the Contract Analysis HUB to cloud hosting platforms, eliminating the need for Cloudflare Tunnel.

## 🎯 Recommended: Render (Best for Streamlit)

**Why Render?**
- ✅ Native Streamlit support
- ✅ Free tier available
- ✅ Automatic HTTPS
- ✅ Easy deployment from GitHub
- ✅ No configuration needed

### Deploy to Render

#### Option 1: Deploy from GitHub (Recommended)

1. **Push your code to GitHub** (if not already done):
   ```bash
   cd "C:\Users\VitorManuelBarbosaFe\Desktop\Contract Analysis"
   git init
   git add .
   git commit -m "Initial commit"
   git remote add origin https://github.com/YOUR-USERNAME/contract-analysis-hub.git
   git push -u origin main
   ```

2. **Go to Render Dashboard**:
   - Visit: https://dashboard.render.com/
   - Sign up or log in

3. **Create New Web Service**:
   - Click "New +" → "Web Service"
   - Connect your GitHub repository
   - Select the `contract-analysis-hub` repository

4. **Configure Service**:
   - **Name**: `ibm-tls-contract-analysis`
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `streamlit run contract_analysis_app.py --server.port=$PORT --server.address=0.0.0.0 --server.headless=true`
   - **Plan**: Free

5. **Deploy**:
   - Click "Create Web Service"
   - Wait 2-3 minutes for deployment
   - Your app will be live at: `https://ibm-tls-contract-analysis.onrender.com`

#### Option 2: Deploy with render.yaml (Automated)

The `render.yaml` file is already configured. Simply:

1. Push code to GitHub
2. Connect repository to Render
3. Render will auto-detect the `render.yaml` and deploy automatically

**Deployment Time**: ~3-5 minutes

---

## Alternative: Streamlit Community Cloud (Easiest)

**Why Streamlit Cloud?**
- ✅ Purpose-built for Streamlit apps
- ✅ Completely free
- ✅ One-click deployment
- ✅ Automatic updates from GitHub

### Deploy to Streamlit Cloud

1. **Push to GitHub** (same as above)

2. **Go to Streamlit Cloud**:
   - Visit: https://share.streamlit.io/
   - Sign in with GitHub

3. **Deploy App**:
   - Click "New app"
   - Select your repository: `contract-analysis-hub`
   - Main file path: `contract_analysis_app.py`
   - Click "Deploy"

4. **Access Your App**:
   - URL: `https://YOUR-USERNAME-contract-analysis-hub.streamlit.app`

**Deployment Time**: ~2 minutes

---

## Alternative: Vercel (Requires Adapter)

Vercel doesn't natively support Streamlit, but you can deploy with an adapter:

### Deploy to Vercel

1. **Install Vercel CLI**:
   ```bash
   npm install -g vercel
   ```

2. **Create vercel.json**:
   ```json
   {
     "builds": [
       {
         "src": "contract_analysis_app.py",
         "use": "@vercel/python"
       }
     ],
     "routes": [
       {
         "src": "/(.*)",
         "dest": "contract_analysis_app.py"
       }
     ]
   }
   ```

3. **Deploy**:
   ```bash
   cd "C:\Users\VitorManuelBarbosaFe\Desktop\Contract Analysis"
   vercel
   ```

**Note**: Vercel has limitations with Streamlit. **Render or Streamlit Cloud are better choices.**

---

## Comparison Matrix

| Platform | Setup Time | Cost | Streamlit Support | Best For |
|----------|-----------|------|-------------------|----------|
| **Render** | 5 min | Free tier | ✅ Native | Production demos |
| **Streamlit Cloud** | 2 min | Free | ✅ Native | Quick sharing |
| **Vercel** | 10 min | Free | ⚠️ Limited | Not recommended |

---

## Current Deployment Status

✅ **Parts Locker Core**: https://ibm-parts-locker-core.vercel.app/intake  
✅ **Parts Pricing Calculator**: https://pricing-module-excel-driven.vercel.app/  
✅ **Country Mapping App**: https://country-mapping-app.onrender.com/  
🔄 **Contract Analysis HUB**: Ready to deploy (currently using Cloudflare Tunnel)

---

## Quick Start (Render - Recommended)

```bash
# 1. Navigate to project
cd "C:\Users\VitorManuelBarbosaFe\Desktop\Contract Analysis"

# 2. Initialize Git (if needed)
git init
git add .
git commit -m "Ready for deployment"

# 3. Push to GitHub
git remote add origin https://github.com/YOUR-USERNAME/contract-analysis-hub.git
git push -u origin main

# 4. Go to Render Dashboard
# Visit: https://dashboard.render.com/
# Connect GitHub repo and deploy!
```

**Result**: Your app will be live at `https://ibm-tls-contract-analysis.onrender.com` in ~5 minutes!

---

## Environment Variables (Optional)

If you need to configure any settings:

**Render Dashboard** → Your Service → Environment:
- Add any required environment variables
- Example: `STREAMLIT_SERVER_PORT=10000`

---

## Troubleshooting

### App Won't Start
- Check logs in Render dashboard
- Verify `requirements.txt` has all dependencies
- Ensure Python version is 3.8+

### Slow Performance
- Render free tier may sleep after inactivity
- Upgrade to paid tier for always-on service
- Consider Streamlit Cloud for better free tier

### File Upload Issues
- Streamlit has file size limits (200MB default)
- Configure in `.streamlit/config.toml` if needed

---

## Security Considerations

Since this is a demo app:
- ✅ No backend database (uses session state)
- ✅ Files processed in memory only
- ✅ No persistent storage of sensitive data
- ⚠️ URL is publicly accessible (share carefully)

**For Production**:
- Add authentication (Streamlit supports OAuth)
- Use environment variables for secrets
- Consider IP whitelisting on Render

---

## Next Steps After Deployment

1. ✅ Test the deployed app thoroughly
2. ✅ Share URL with stakeholders
3. ✅ Monitor usage in Render dashboard
4. ✅ Set up custom domain (optional)
5. ✅ Configure auto-deploy from GitHub

---

## Support

- **Render Docs**: https://render.com/docs
- **Streamlit Docs**: https://docs.streamlit.io/
- **GitHub Issues**: Create issues in your repository

---

**Made with IBM Bob** 🤖

Last Updated: June 2026
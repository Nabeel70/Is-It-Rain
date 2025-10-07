# 🚀 SIMPLEST Deployment - Railway + Netlify (Both FREE!)

## Why This Works
- ✅ **Railway Backend**: FREE 500 hours/month ($5 credit)
- ✅ **Netlify Frontend**: FREE 100GB bandwidth/month
- ✅ **Total Cost**: $0 (Free tier is enough!)
- ✅ **No Credit Card**: Optional on both platforms

---

## Part 1: Deploy Backend to Railway (5 minutes)

### Step 1: Go to Railway Dashboard
1. Open: [https://railway.app/dashboard](https://railway.app/dashboard)
2. Click: **"New Project"**
3. Click: **"Deploy from GitHub repo"**
4. Find: **"Is-It-Rain"**
5. Click on it

### Step 2: Configure the Service
```
1. Railway will detect your code
2. Click "Add variables" 
3. Add this:
   
   Key: ALLOWED_ORIGINS
   Value: http://localhost:5173

4. Click "Deploy"
```

### Step 3: CRITICAL - Fix Start Command
```
1. After deploy starts, click "Settings" tab
2. Scroll to "Deploy"
3. Find "Custom Start Command"
4. DELETE anything there (leave it EMPTY!)
5. Click "Save"
6. Go to "Deployments" tab
7. Click "Redeploy" on the latest deployment
```

### Step 4: Get Your Backend URL
```
1. Wait 3-5 minutes for deployment
2. Click "Settings" tab
3. Scroll to "Networking"  
4. Click "Generate Domain"
5. Copy the URL (like: your-app.up.railway.app)
```

✅ **Backend is live!**

Test it: `https://YOUR-APP.up.railway.app/health`

Should show: `{"status":"ok","message":"Is It Rain API is running"}`

---

## Part 2: Deploy Frontend to Netlify (3 minutes)

### Step 5: Go to Netlify
1. Open: [https://app.netlify.com](https://app.netlify.com)
2. Click: **"Sign up"** or **"Log in"**
3. Choose: **"GitHub"**
4. Authorize Netlify

### Step 6: Deploy Site
```
1. Click "Add new site"
2. Click "Import an existing project"
3. Click "GitHub"
4. Find "Is-It-Rain"
5. Click on it
```

### Step 7: Configure Build
```
Base directory: frontend
Build command: npm run build
Publish directory: frontend/dist

Click "Show advanced" → "New variable"
Key: VITE_API_URL
Value: YOUR_RAILWAY_BACKEND_URL (from Step 4)

Click "Deploy site"
```

✅ **Frontend is deploying!** (takes 2-3 minutes)

### Step 8: Update Backend CORS
```
1. Go back to Railway dashboard
2. Click your backend service
3. Click "Variables"
4. Edit ALLOWED_ORIGINS
5. Add your Netlify URL:
   https://YOUR-SITE.netlify.app,http://localhost:5173
6. Railway will auto-redeploy
```

---

## Part 3: Test! 🎉

1. Open your Netlify URL: `https://YOUR-SITE.netlify.app`
2. Enter location: "Tokyo, Japan"
3. Pick a date
4. Click "Get Forecast"

**IT WORKS!** ✨

---

## Free Tier Limits

### Railway FREE:
- ✅ $5 credit/month (500 execution hours)
- ✅ No credit card required initially
- ✅ Enough for small projects

### Netlify FREE:
- ✅ 100GB bandwidth/month
- ✅ 300 build minutes/month
- ✅ Unlimited sites
- ✅ No credit card required

**Total: $0/month for your project!**

---

## Troubleshooting Railway

### If backend still shows errors:

#### Option 1: Clear Start Command
```
Settings → Deploy → Custom Start Command → DELETE IT → Save → Redeploy
```

#### Option 2: Check Logs
```
Deployments → Latest → View Logs
Look for errors in red
```

#### Option 3: Verify nixpacks.toml is used
```
In logs, you should see:
"Using Nixpacks"
"cd /app/backend && /app/backend/.venv/bin/uvicorn..."
```

#### Option 4: Environment Variables
```
Make sure ALLOWED_ORIGINS is set correctly
```

---

## Alternative: PythonAnywhere (100% Free Backend)

If Railway still doesn't work, try **PythonAnywhere**:

1. Go to: [https://www.pythonanywhere.com](https://www.pythonanywhere.com)
2. Click "Start running Python online in less than a minute!"
3. **FREE** tier: No credit card, no trials
4. Can run FastAPI with some setup

Want instructions for PythonAnywhere instead?

---

## Alternative: Fly.io (Free Tier)

Another option:

1. Go to: [https://fly.io](https://fly.io)
2. Sign up (no credit card for free tier)
3. Install CLI: `curl -L https://fly.io/install.sh | sh`
4. Deploy: `fly launch`

**FREE tier:**
- 3 VMs (256MB RAM each)
- 3GB storage
- Enough for your app!

---

## My Recommendation

**Try Railway + Netlify first** using the steps above.

The key is:
1. ❌ DON'T set custom start command in Railway dashboard
2. ✅ LET nixpacks.toml handle everything
3. ✅ ONLY set environment variables

If it STILL doesn't work after following these steps exactly, let me know and I'll help you set up **Fly.io** or **PythonAnywhere** instead.

---

## Quick Commands to Verify

### Test Backend Health:
```bash
curl https://YOUR-RAILWAY-APP.up.railway.app/health
```

### Test API Endpoint:
```bash
curl -X POST https://YOUR-RAILWAY-APP.up.railway.app/api/forecast/ensemble \
  -H "Content-Type: application/json" \
  -d '{"event_date": "2025-12-25", "query": "Tokyo, Japan"}'
```

### Check Frontend Loads:
```
Open: https://YOUR-SITE.netlify.app
Should see your app interface
```

---

## Need Help?

Tell me:
1. Which platform failed?
2. What error did you see?
3. Screenshot of logs?

I'll help you get it working or move to a different platform!

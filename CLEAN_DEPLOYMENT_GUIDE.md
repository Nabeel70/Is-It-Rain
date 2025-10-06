# 🚀 CLEAN DEPLOYMENT FROM SCRATCH
## Railway (Backend) + Netlify (Frontend)

**Last Updated**: October 6, 2025  
**Status**: ✅ All code verified and ready for deployment

---

## ✅ PRE-DEPLOYMENT CHECKLIST

Everything is ready:
- ✅ Backend code working
- ✅ Frontend code working  
- ✅ Railway config files created (`railway.json`, `nixpacks.toml`, `Procfile`)
- ✅ ML models committed to Git (2.5MB total)
- ✅ Dependencies properly configured
- ✅ Frontend builds successfully
- ✅ All code pushed to GitHub

**Your Repository**: https://github.com/Nabeel70/Is-It-Rain

---

## 🎯 PART 1: DEPLOY BACKEND TO RAILWAY (15 minutes)

### Step 1: Clean Up Old Deployment (If Exists)

1. Go to **Railway Dashboard**: https://railway.app/dashboard
2. If you have an existing `is-it-rain-production` service:
   - Click on the service
   - Go to **Settings** (bottom of left sidebar)
   - Scroll to bottom → Click **"Delete Service"**
   - Type the service name to confirm
   - Click **"Delete"**

### Step 2: Create New Railway Project

1. On Railway Dashboard, click **"New Project"**
2. Select **"Deploy from GitHub repo"**
3. If prompted, authorize Railway to access GitHub
4. Search for: **"Is-It-Rain"**
5. Click on **"Nabeel70/Is-It-Rain"**

**⚠️ IMPORTANT**: If repository doesn't appear:
- Click **"Configure GitHub App"**
- Grant Railway access to **"Nabeel70/Is-It-Rain"** repository
- Go back and try again

### Step 3: Railway Auto-Detection

Railway will automatically detect your repository. You should see:
- ✅ Detected: Python
- ✅ Detected: Poetry
- ✅ Found: `railway.json`

Click **"Deploy Now"**

### Step 4: Configure Service Settings

1. Click on your new service (will be auto-named)
2. Click **Settings** (left sidebar)
3. Update these settings:

#### Service Name
- Change name to: **"is-it-rain-backend"**

#### Root Directory
- **Leave EMPTY** (our config handles this)

#### Build Command (should auto-detect)
- Should show: `cd backend && poetry install --no-dev`
- If empty, add it manually

#### Start Command (should auto-detect)
- Should show: `cd backend && poetry run uvicorn app.main:app --host 0.0.0.0 --port $PORT`
- If empty, add it manually

#### Watch Paths
- Leave default (entire repo)

### Step 5: Add Environment Variables

Still in Settings, scroll to **"Environment"** section:

1. Click **"+ New Variable"**
2. Add this variable:
   - **Variable**: `ALLOWED_ORIGINS`
   - **Value**: `http://localhost:5173`
   
   (We'll update this with Netlify URL later)

3. Click **"Add"**

### Step 6: Get Your Railway URL

1. Go to **Settings** → **Networking**
2. Under **"Public Networking"**, click **"Generate Domain"**
3. Railway will assign a URL like: `is-it-rain-backend.up.railway.app`
4. **COPY THIS URL** - you'll need it for Netlify!

### Step 7: Wait for Deployment

1. Go to **"Deployments"** tab (left sidebar)
2. Watch the latest deployment
3. Click on it to see build logs

**Expected logs** (takes 3-5 minutes):
```
✅ Installing Python 3.12...
✅ Installing Poetry...
✅ Running: cd backend && poetry install --no-dev
✅ Installing dependencies from lock file
✅ Package operations: 40 installs...
✅ Build complete
✅ Starting: cd backend && poetry run uvicorn app.main:app --host 0.0.0.0 --port 8080
✅ INFO: Started server process
✅ INFO: Uvicorn running on http://0.0.0.0:8080
```

**❌ BAD logs** (if you see these, something is wrong):
```
❌ Installing Node.js...
❌ npm install...
❌ Building frontend...
```

If you see bad logs, Railway is deploying the frontend. **STOP** and:
- Go to Settings → Root Directory → Set to `backend`
- Redeploy

### Step 8: Verify Backend is Working

Once deployment shows **"Success"**, test these:

```bash
# Test 1: Health check (should return JSON)
curl https://is-it-rain-backend.up.railway.app/health

# Expected output:
# {"status":"ok","message":"Is It Rain API is running"}

# Test 2: API documentation
curl https://is-it-rain-backend.up.railway.app/docs

# Should redirect to Swagger UI HTML

# Test 3: Model info
curl https://is-it-rain-backend.up.railway.app/api/model/info

# Expected: JSON with model details
```

**✅ If all tests return correct responses, your backend is live!**

**❌ If health check returns HTML**, Railway is still deploying frontend:
1. Settings → Root Directory → Set to `backend`
2. Click "Redeploy" in Deployments tab

---

## 🎯 PART 2: DEPLOY FRONTEND TO NETLIFY (10 minutes)

### Step 9: Clean Up Old Netlify Site (If Exists)

1. Go to **Netlify Dashboard**: https://app.netlify.com/
2. If you have an existing site:
   - Click on the site
   - Go to **Site settings**
   - Scroll to bottom → **"Delete site"**
   - Confirm deletion

### Step 10: Create New Netlify Site

1. On Netlify Dashboard, click **"Add new site"** → **"Import an existing project"**
2. Choose **"Deploy with GitHub"**
3. Authorize Netlify if prompted
4. Search for: **"Is-It-Rain"**
5. Click on **"Nabeel70/Is-It-Rain"**

### Step 11: Configure Build Settings

**CRITICAL SETTINGS** (don't skip!):

1. **Base directory**: `frontend`
2. **Build command**: `npm run build`
3. **Publish directory**: `frontend/dist`
4. **Branch to deploy**: `main`

Click **"Show advanced"** and skip (we'll add env vars next)

Click **"Deploy Is-It-Rain"**

### Step 12: Add Environment Variables (BEFORE first deploy completes)

1. While deploy is running, click **"Site settings"**
2. Go to **"Environment variables"** (left sidebar)
3. Click **"Add a variable"** → **"Add a single variable"**
4. Add this variable:
   - **Key**: `VITE_API_URL`
   - **Value**: `https://is-it-rain-backend.up.railway.app` (your Railway URL from Step 6)
   - **Scopes**: Check **ALL** scopes (Production, Deploy Previews, Branch deploys)

**⚠️ CRITICAL**: 
- Use `https://` prefix
- NO trailing slash
- Use YOUR actual Railway URL

5. Click **"Create variable"**

### Step 13: Trigger Rebuild with Environment Variable

Since the first deploy happened without the env variable:

1. Go to **"Deploys"** tab
2. Click **"Trigger deploy"** → **"Clear cache and deploy site"**
3. Wait 2-3 minutes for rebuild

### Step 14: Get Your Netlify URL

Once deploy succeeds:
1. Netlify assigns a URL like: `magical-unicorn-abc123.netlify.app`
2. **COPY THIS URL** - you need to update Railway!

You can also:
- Click **"Domain settings"** to change the site name
- Example: Change to `is-it-rain.netlify.app`

### Step 15: Update Railway CORS Settings

**NOW go back to Railway** to allow your Netlify frontend:

1. Railway Dashboard → Your backend service
2. Go to **"Variables"** tab
3. Find **"ALLOWED_ORIGINS"** variable
4. Click on it to edit
5. **Update the value** to:
   ```
   https://magical-unicorn-abc123.netlify.app,http://localhost:5173
   ```
   (Replace with YOUR actual Netlify URL)

**⚠️ CRITICAL**:
- Use `https://` prefix for Netlify URL
- NO trailing slash
- Separate URLs with comma, NO spaces
- Keep `http://localhost:5173` for local testing

6. Click **"Update"** or save
7. Railway will auto-redeploy (takes 2 minutes)

### Step 16: Verify Full Application

Once Railway redeploys with updated CORS:

```bash
# Test CORS from backend
curl -X OPTIONS https://is-it-rain-backend.up.railway.app/api/forecast/ensemble \
  -H "Origin: https://magical-unicorn-abc123.netlify.app" \
  -H "Access-Control-Request-Method: POST" \
  -v 2>&1 | grep -i "access-control-allow-origin"

# Should output:
# access-control-allow-origin: https://magical-unicorn-abc123.netlify.app
```

### Step 17: Test Live Application

1. Open your Netlify URL: `https://magical-unicorn-abc123.netlify.app`
2. Press `Ctrl+Shift+R` (hard refresh to clear cache)
3. Open DevTools (F12) → Console tab
4. Enter test data:
   - **Date**: December 25, 2025
   - **Location**: Tokyo, Japan
5. Click **"Will it rain?"**

**Expected**:
- ✅ No CORS errors in console
- ✅ Loading spinner appears
- ✅ Map displays Tokyo location
- ✅ Forecast results appear
- ✅ Probability gauge shows percentage

**If errors occur**, see troubleshooting below.

---

## 🔍 TROUBLESHOOTING

### Problem 1: Railway deploying frontend instead of backend

**Symptoms**: Health check returns HTML instead of JSON

**Solution**:
1. Railway Dashboard → Service → Settings
2. Set **Root Directory** to: `backend`
3. Go to Deployments → Click latest → **"Redeploy"**

### Problem 2: "Module not found: app.main"

**Symptoms**: Railway logs show Python import error

**Solution**: Start command is wrong
1. Railway Dashboard → Service → Settings
2. Set **Start Command** to:
   ```
   cd backend && poetry run uvicorn app.main:app --host 0.0.0.0 --port $PORT
   ```
3. Redeploy

### Problem 3: CORS error in browser

**Symptoms**:
```
Access to XMLHttpRequest at 'https://...' from origin 'https://...' has been blocked by CORS policy
```

**Diagnosis**: Check Railway environment variable

**Solution**:
1. Railway Dashboard → Service → Variables
2. Find **ALLOWED_ORIGINS**
3. Verify it includes your **exact** Netlify URL with `https://` and no trailing slash
4. Format: `https://your-site.netlify.app,http://localhost:5173`
5. Save and wait for Railway to redeploy (2 min)

### Problem 4: Frontend shows "Network Error"

**Causes**:
- Backend not running
- Wrong `VITE_API_URL` in Netlify
- Railway deployment failed

**Solution**:
```bash
# Test backend is up
curl https://is-it-rain-backend.up.railway.app/health

# If returns error, check Railway logs
# If returns HTML, Railway is deploying wrong service (see Problem 1)
# If returns JSON, check Netlify env variable
```

**Check Netlify env var**:
1. Netlify → Site settings → Environment variables
2. Verify **VITE_API_URL** = `https://is-it-rain-backend.up.railway.app` (no trailing slash)
3. If wrong, update and trigger **"Clear cache and deploy site"**

### Problem 5: Railway build fails

**Symptoms**: Deployment status shows "Failed"

**Common causes**:
- Poetry lock file out of sync
- Missing dependencies
- ML models not in Git

**Solution 1 - Check ML models**:
```bash
git ls-files backend/data/ml_models/
# Should show:
# backend/data/ml_models/feature_scaler.joblib
# backend/data/ml_models/precipitation_model.joblib
```

If missing:
```bash
cd /workspaces/Is-It-Rain
git add backend/data/ml_models/*.joblib
git commit -m "Add ML models"
git push origin main
```

**Solution 2 - Update Poetry lock**:
```bash
cd /workspaces/Is-It-Rain/backend
poetry lock --no-update
git add poetry.lock
git commit -m "Update poetry lock"
git push origin main
```

### Problem 6: Netlify build fails

**Symptoms**: Netlify deploy shows "Failed"

**Common causes**:
- Wrong build settings
- Missing dependencies
- Incorrect base directory

**Solution**:
1. Netlify → Site settings → Build & deploy → Build settings
2. Verify:
   - Base directory: `frontend`
   - Build command: `npm run build`
   - Publish directory: `frontend/dist`
3. Click **"Edit settings"** if wrong
4. Save and trigger new deploy

---

## 📝 DEPLOYMENT SUMMARY

After completing all steps, you should have:

### Railway Backend
- **URL**: `https://is-it-rain-backend.up.railway.app`
- **Health**: `https://is-it-rain-backend.up.railway.app/health` → Returns JSON
- **API Docs**: `https://is-it-rain-backend.up.railway.app/docs`
- **Environment Variables**:
  - `ALLOWED_ORIGINS` = `https://your-site.netlify.app,http://localhost:5173`

### Netlify Frontend
- **URL**: `https://your-site.netlify.app`
- **Environment Variables**:
  - `VITE_API_URL` = `https://is-it-rain-backend.up.railway.app`
- **Build Settings**:
  - Base directory: `frontend`
  - Build command: `npm run build`
  - Publish directory: `frontend/dist`

### Verification Checklist
- [ ] Railway health check returns JSON (not HTML)
- [ ] Railway logs show "Starting Is It Rain API"
- [ ] Railway logs show correct ALLOWED_ORIGINS
- [ ] Netlify site loads without errors
- [ ] No CORS errors in browser console
- [ ] Can submit forecast request
- [ ] Forecast results display correctly
- [ ] Map shows location
- [ ] Probability gauge renders

---

## 🎉 SUCCESS INDICATORS

You'll know everything is working when:

✅ Backend health check: `{"status":"ok","message":"Is It Rain API is running"}`
✅ Railway logs: `INFO: Starting Is It Rain API`
✅ Railway logs: `INFO: Allowed origins: ['https://your-site.netlify.app', ...]`
✅ Frontend loads with no console errors
✅ Can search for locations and get forecasts
✅ No CORS errors
✅ No network errors
✅ Map displays correctly
✅ Results show precipitation probability

---

## 🆘 STILL NOT WORKING?

### Get Support

1. **Check Railway Logs**:
   - Railway Dashboard → Service → Deployments → Latest → Click to view logs
   - Look for errors in red
   - Copy and share full logs

2. **Check Netlify Logs**:
   - Netlify Dashboard → Deploys → Latest → Click to view logs
   - Look for build errors
   - Copy and share full logs

3. **Check Browser Console**:
   - Open your Netlify site
   - Press F12 → Console tab
   - Copy all errors (especially red ones)
   - Network tab → Check failed requests

4. **Run Diagnostic Tests**:
```bash
# Backend health
curl https://is-it-rain-backend.up.railway.app/health

# CORS test
curl -X OPTIONS https://is-it-rain-backend.up.railway.app/api/forecast/ensemble \
  -H "Origin: https://your-site.netlify.app" \
  -H "Access-Control-Request-Method: POST" \
  -v

# Full forecast test
curl -X POST https://is-it-rain-backend.up.railway.app/api/forecast/ensemble \
  -H "Content-Type: application/json" \
  -H "Origin: https://your-site.netlify.app" \
  -d '{"event_date": "2025-12-25", "query": "Tokyo"}'
```

Share the output of these commands.

---

## 📞 QUICK REFERENCE

### Railway
- **Dashboard**: https://railway.app/dashboard
- **Docs**: https://docs.railway.app/

### Netlify
- **Dashboard**: https://app.netlify.com/
- **Docs**: https://docs.netlify.com/

### Your URLs (update these)
- **GitHub Repo**: https://github.com/Nabeel70/Is-It-Rain
- **Railway Backend**: https://is-it-rain-backend.up.railway.app
- **Netlify Frontend**: https://your-site.netlify.app

---

**Good luck! 🚀**

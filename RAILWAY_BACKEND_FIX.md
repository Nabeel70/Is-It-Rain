# Railway Backend Deployment - Complete Fix Guide

## 🚨 The Root Problem

Railway was deploying your **frontend** instead of your **backend** because:
1. No Railway configuration files existed in the repository root
2. Railway detected Node.js (frontend) first and deployed that
3. The backend Python service was never started

**Evidence**: Accessing `https://is-it-rain-production.up.railway.app/health` returned frontend HTML instead of API JSON.

---

## ✅ The Solution

I've added three configuration files to force Railway to deploy the backend:

### 1. `railway.json` (Railway-specific config)
```json
{
  "$schema": "https://railway.app/railway.schema.json",
  "build": {
    "builder": "NIXPACKS",
    "buildCommand": "cd backend && poetry install --no-dev"
  },
  "deploy": {
    "startCommand": "cd backend && poetry run uvicorn app.main:app --host 0.0.0.0 --port $PORT",
    "healthcheckPath": "/health",
    "healthcheckTimeout": 100,
    "restartPolicyType": "ON_FAILURE",
    "restartPolicyMaxRetries": 10
  }
}
```

### 2. `nixpacks.toml` (Nixpacks builder config)
```toml
[nixPacks]
providers = ["python"]

[nixPacks.phases.setup]
nixPkgs = ["python312", "poetry"]

[nixPacks.phases.install]
cmds = ["cd backend && poetry install --no-dev"]

[nixPacks.phases.build]
cmds = ["cd backend && echo 'Build complete'"]

[start]
cmd = "cd backend && poetry run uvicorn app.main:app --host 0.0.0.0 --port $PORT"
```

### 3. `Procfile` (Heroku-style process file)
```
web: cd backend && poetry run uvicorn app.main:app --host 0.0.0.0 --port $PORT
```

---

## 🔄 Railway Deployment Steps

### Step 1: Trigger Redeploy

The files have been pushed to GitHub. Railway should automatically detect the changes and redeploy.

**Check deployment status:**
1. Go to Railway Dashboard: https://railway.app/dashboard
2. Click on your `is-it-rain-production` service
3. Go to **"Deployments"** tab
4. You should see a new deployment starting (triggered by the latest Git push)
5. Watch the build logs

### Step 2: Monitor Build Logs

Look for these key log messages:

✅ **Correct deployment logs should show:**
```
Installing Python 3.12...
Installing Poetry...
Running: cd backend && poetry install --no-dev
Installing dependencies from lock file
...
Starting: cd backend && poetry run uvicorn app.main:app --host 0.0.0.0 --port $PORT
INFO: Starting Is It Rain API
INFO: Allowed origins: ['https://is-it-rains.netlify.app', 'http://localhost:5173']
INFO: Uvicorn running on http://0.0.0.0:XXXX
```

❌ **Bad logs (if still deploying frontend):**
```
Installing Node.js...
npm install
Building frontend...
```

### Step 3: Verify Backend is Running

After deployment completes (2-4 minutes), test these endpoints:

```bash
# 1. Health check (should return JSON, not HTML)
curl https://is-it-rain-production.up.railway.app/health
# Expected: {"status":"ok","message":"Is It Rain API is running"}

# 2. API documentation (FastAPI auto-generated)
curl https://is-it-rain-production.up.railway.app/docs
# Should redirect to Swagger UI

# 3. Model info endpoint
curl https://is-it-rain-production.up.railway.app/api/model/info
# Expected: {"model_available":true,"features":["T2M_MAX",...]}

# 4. CORS preflight test
curl -X OPTIONS https://is-it-rain-production.up.railway.app/api/forecast/ensemble \
  -H "Origin: https://is-it-rains.netlify.app" \
  -H "Access-Control-Request-Method: POST" \
  -v 2>&1 | grep -i "access-control"
# Expected: access-control-allow-origin: https://is-it-rains.netlify.app

# 5. Full forecast test
curl -X POST https://is-it-rain-production.up.railway.app/api/forecast/ensemble \
  -H "Content-Type: application/json" \
  -H "Origin: https://is-it-rains.netlify.app" \
  -d '{"event_date": "2025-12-25", "query": "Tokyo, Japan"}'
# Expected: JSON with precipitation_probability, location, etc.
```

---

## 🛠️ If Railway Still Deploys Wrong Service

### Option A: Manually Set Root Directory

1. Railway Dashboard → Your service → **Settings**
2. Scroll to **"Service Settings"**
3. Find **"Root Directory"** field
4. Set to: `backend`
5. Click **"Save"**
6. Redeploy

### Option B: Create Separate Services

If Railway insists on deploying both frontend and backend from the same repo:

1. **Delete the current service**
2. **Create TWO separate services:**
   - Service 1: Backend (root directory: `backend`)
   - Service 2: Frontend (root directory: `frontend`)
3. Configure environment variables for each

### Option C: Use Monorepo Setup

Railway Dashboard → Settings → **"Deploy from Branch"**
- Branch: `main`
- Build command: `cd backend && poetry install --no-dev`
- Start command: `cd backend && poetry run uvicorn app.main:app --host 0.0.0.0 --port $PORT`

---

## 🔍 Troubleshooting Checklist

### Issue: Health check still returns HTML

**Diagnosis**: Frontend is still being deployed

**Fix:**
```bash
# Check Railway environment
railway logs | grep -i "starting"

# Should see: "Starting Is It Rain API"
# NOT: "Starting development server"
```

**Solution**: Set root directory to `backend` in Railway settings

---

### Issue: "Module not found: app.main"

**Diagnosis**: Working directory is wrong

**Fix**: Update start command to include `cd backend`
```bash
cd backend && poetry run uvicorn app.main:app --host 0.0.0.0 --port $PORT
```

---

### Issue: "poetry: command not found"

**Diagnosis**: Poetry not installed in build environment

**Fix**: Ensure `nixpacks.toml` includes Poetry in nixPkgs:
```toml
[nixPacks.phases.setup]
nixPkgs = ["python312", "poetry"]
```

---

### Issue: ML models not found

**Diagnosis**: `backend/data/ml_models/*.joblib` not committed to Git

**Fix:**
```bash
cd /workspaces/Is-It-Rain
git add backend/data/ml_models/*.joblib
git commit -m "Add trained ML models"
git push origin main
```

---

### Issue: Port already in use

**Diagnosis**: Railway assigns dynamic ports via `$PORT` environment variable

**Fix**: Always use `--port $PORT` in start command (already correct in our config)

---

## 📊 Expected Deployment Timeline

| Time | Event |
|------|-------|
| 0:00 | Push to GitHub triggers Railway webhook |
| 0:30 | Railway detects changes, starts build |
| 1:00 | Installing Python 3.12 and Poetry |
| 2:00 | Running `poetry install --no-dev` |
| 3:00 | Build complete, starting uvicorn |
| 3:30 | Health check passes ✅ |
| 4:00 | Service is live! |

---

## ✅ Final Verification

Once Railway finishes deploying:

### 1. Test from Command Line
```bash
curl -s https://is-it-rain-production.up.railway.app/health | jq .
```
**Expected output:**
```json
{
  "status": "ok",
  "message": "Is It Rain API is running"
}
```

### 2. Test from Browser
Open: https://is-it-rain-production.up.railway.app/docs

You should see FastAPI Swagger documentation with:
- `/health`
- `/api/forecast`
- `/api/forecast/ensemble`
- `/api/model/info`
- `/api/stats`

### 3. Test from Your Frontend
1. Go to: https://is-it-rains.netlify.app
2. Press `Ctrl+Shift+R` (hard refresh)
3. Enter: "Tokyo, Japan"
4. Date: December 25, 2025
5. Click "Will it rain?"
6. Should see forecast results! 🎉

---

## 🎯 Environment Variables Summary

### Railway Backend Service

| Variable | Value |
|----------|-------|
| `ALLOWED_ORIGINS` | `https://is-it-rains.netlify.app,http://localhost:5173` |

**Note**: Remove `CORS_ORIGINS` if it exists (not used by the backend code)

### Netlify Frontend

| Variable | Value |
|----------|-------|
| `VITE_API_URL` | `https://is-it-rain-production.up.railway.app` |

**Note**: No trailing slash!

---

## 📞 Getting Help

If still having issues after Railway redeploys:

1. **Share Railway logs**:
   - Railway Dashboard → Deployments → Latest → Copy logs
   
2. **Test and share results**:
   ```bash
   curl -v https://is-it-rain-production.up.railway.app/health
   ```

3. **Check Railway service settings**:
   - Screenshot of Settings → Service Settings
   - Screenshot of Variables tab

---

## 🚀 Success Indicators

You'll know it's working when:

✅ `curl .../health` returns JSON (not HTML)
✅ Railway logs show "Starting Is It Rain API"
✅ Railway logs show "Allowed origins: ['https://is-it-rains.netlify.app', ...]"
✅ Browser console has NO CORS errors
✅ Forecast requests return 200 status code
✅ Frontend displays precipitation probability

---

**Next Steps**: Wait 3-5 minutes for Railway to redeploy, then run the verification tests above!

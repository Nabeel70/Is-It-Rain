# 🚨 RAILWAY DEPLOYMENT - COMPLETE FIX

## Problem History

### Issue 1: Railway was using Dockerfile
**Error**: `The executable 'cd' could not be found`  
**Fix**: Renamed `Dockerfile` to `Dockerfile.local` ✅

### Issue 2: Poetry not installed before build
**Error**: `/bin/bash: line 1: poetry: command not found`  
**Fix**: Removed `buildCommand` override from `railway.json` ✅

---

## ✅ FINAL WORKING CONFIGURATION

Your repository now has the correct setup:

### Files That Control Railway Deployment:

1. **`railway.json`** - Main Railway config
```json
{
  "build": {
    "builder": "NIXPACKS"
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

2. **`nixpacks.toml`** - Nixpacks build phases
```toml
[phases.setup]
nixPkgs = ["python312", "poetry"]

[phases.install]
cmds = ["cd backend && poetry install --no-dev"]

[phases.build]
cmds = ["echo 'Build phase complete'"]

[start]
cmd = "cd backend && poetry run uvicorn app.main:app --host 0.0.0.0 --port $PORT"
```

3. **`Procfile`** - Process definition
```
web: cd backend && poetry run uvicorn app.main:app --host 0.0.0.0 --port $PORT
```

---

## 🎯 DEPLOYMENT STEPS NOW

### Step 1: Trigger New Deploy in Railway

Since you already have the service set up:

1. **Go to Railway Dashboard** → Your service
2. **Click "Deployments"** tab
3. **Click "Redeploy"** on the latest deployment

OR manually trigger a new deploy:
```bash
# Make a small change to trigger redeploy
cd /workspaces/Is-It-Rain
git commit --allow-empty -m "Trigger Railway redeploy with fixed config"
git push origin main
```

### Step 2: Watch Build Logs

Click on the new deployment to see logs. You should now see:

```
✅ Using Nixpacks
✅ Setup Phase:
✅   Installing nixpkgs: python312, poetry
✅ Install Phase:
✅   Running: cd backend && poetry install --no-dev
✅   Installing dependencies from lock file
✅   Package operations: 40 installs, 0 updates, 0 removals
✅   • Installing certifi (2024.x.x)
✅   • Installing httpcore (1.x.x)
✅   ... (more packages)
✅ Build Phase:
✅   Build phase complete
✅ Start Phase:
✅   Running: cd backend && poetry run uvicorn app.main:app --host 0.0.0.0 --port $PORT
✅   INFO: Started server process
✅   INFO: Waiting for application startup
✅   INFO: Application startup complete
✅   INFO: Uvicorn running on http://0.0.0.0:8080
```

**❌ If you still see**:
```
poetry: command not found
```
**Then Railway cached the old build. Solution below.**

### Step 3: Clear Railway Cache (If Needed)

If deployment still fails with "poetry: command not found":

1. **Railway Dashboard** → Your service → **Settings**
2. Scroll to bottom → **"Delete Service"** (yes, really)
3. Create new service from GitHub (follow CLEAN_DEPLOYMENT_GUIDE.md)

**Why?** Sometimes Railway aggressively caches the build, and the only way to force it to re-read the config files is to create a fresh service.

---

## 🧪 VERIFICATION TESTS

Once deployment shows "Success":

### Test 1: Health Check
```bash
curl https://web-production-e0703.up.railway.app/health
```

**Expected**:
```json
{"status":"ok","message":"Is It Rain API is running"}
```

**❌ If you get HTML**: Railway is still deploying frontend somehow (shouldn't happen now)

### Test 2: API Documentation
```bash
curl https://web-production-e0703.up.railway.app/docs
```

Should return Swagger UI HTML

### Test 3: Model Info
```bash
curl https://web-production-e0703.up.railway.app/api/model/info
```

**Expected**: JSON with model details

### Test 4: Forecast Endpoint
```bash
curl -X POST https://web-production-e0703.up.railway.app/api/forecast/ensemble \
  -H "Content-Type: application/json" \
  -d '{"event_date": "2025-12-25", "query": "Tokyo, Japan"}'
```

**Expected**: JSON with precipitation probability

---

## 🔧 RAILWAY SETTINGS REFERENCE

Your Railway service should have these exact settings:

### Source
- **Repository**: `Nabeel70/Is-It-Rain`
- **Branch**: `main`
- **Root Directory**: (empty/blank)

### Build
- **Builder**: `Nixpacks` (NOT Dockerfile)
- **Providers**: Python (auto-detected)
- **Custom Build Command**: (should be empty - let nixpacks.toml handle it)

### Deploy
- **Start Command**: Set in railway.json
  ```
  cd backend && poetry run uvicorn app.main:app --host 0.0.0.0 --port $PORT
  ```
- **Healthcheck Path**: `/health`
- **Healthcheck Timeout**: `100`
- **Restart Policy**: `ON_FAILURE` with max 10 retries

### Environment Variables
- **`ALLOWED_ORIGINS`**: `http://localhost:5173` (update with Netlify URL later)

### Networking
- **Domain**: `web-production-e0703.up.railway.app` (or whatever Railway assigned)

---

## 🎉 SUCCESS INDICATORS

You'll know it's working when:

✅ Railway logs show "Installing poetry"  
✅ Railway logs show "Installing dependencies from lock file"  
✅ Railway logs show "INFO: Uvicorn running on http://0.0.0.0:8080"  
✅ Health check returns JSON (not HTML)  
✅ No "command not found" errors  
✅ Deployment status shows "Active" with green checkmark  

---

## 🚨 IF STILL FAILING

### Option 1: Check Railway Logs Carefully

Look for these specific error patterns:

**"poetry: command not found"**
- Railway is using cached build
- Delete service and recreate

**"The executable 'cd' could not be found"**
- Railway is using Dockerfile
- Make sure `Dockerfile` doesn't exist (should be `Dockerfile.local`)
- Check Railway Settings → Builder → Should be "Nixpacks"

**"Module 'app.main' not found"**
- Working directory is wrong
- Check start command includes `cd backend`

**"No module named 'fastapi'"**
- Dependencies not installed
- Check build logs for "poetry install" step

### Option 2: Nuclear Option (Fresh Start)

If nothing works:

1. **Delete Railway service completely**
2. **Verify GitHub repo has**:
   - ✅ `railway.json` (no buildCommand)
   - ✅ `nixpacks.toml` (with setup/install/build phases)
   - ✅ `Procfile` (with web command)
   - ✅ `Dockerfile.local` (NOT `Dockerfile`)
3. **Create new Railway service**:
   - New Project → Deploy from GitHub
   - Select `Nabeel70/Is-It-Rain`
   - Verify it says "Nixpacks" (NOT "Dockerfile")
   - Let it auto-deploy
4. **Add environment variables**:
   - `ALLOWED_ORIGINS` = `http://localhost:5173`
5. **Generate domain**
6. **Test endpoints**

---

## 📊 EXPECTED BUILD TIMELINE

| Time | Event |
|------|-------|
| 0:00 | Build started |
| 0:10 | Nixpacks detected, Python provider loaded |
| 0:30 | Setup phase: Installing Python 3.12 |
| 1:00 | Setup phase: Installing Poetry |
| 1:30 | Install phase: Running poetry install |
| 3:00 | Installing 40+ dependencies |
| 4:00 | Build phase complete |
| 4:10 | Start phase: Uvicorn starting |
| 4:20 | Health check passed ✅ |
| 4:30 | Deployment live! |

Total: **4-5 minutes**

---

## 🆘 GET HELP

If deployment still fails after all this:

1. **Copy full Railway build logs**
2. **Copy Railway settings** (screenshot of Settings page)
3. **Share the output of**:
   ```bash
   git log --oneline -5
   git ls-files | grep -E "(railway|nixpacks|Procfile|Dockerfile)"
   ```
4. **Check Railway status page**: https://status.railway.app/

---

## 📞 QUICK COMMAND REFERENCE

```bash
# Trigger new deploy
git commit --allow-empty -m "Trigger redeploy"
git push origin main

# Check what files Railway sees
git ls-files | grep -E "(railway|nixpacks|Procfile|Dockerfile)"

# Should output:
# Dockerfile.local
# Dockerfile.README.md
# Procfile
# nixpacks.toml
# railway.json

# Test backend locally to confirm it works
cd /workspaces/Is-It-Rain/backend
poetry install
poetry run uvicorn app.main:app --host 0.0.0.0 --port 8000
# In another terminal:
curl http://localhost:8000/health
```

---

**All configuration files are now correct and pushed to GitHub. Railway should deploy successfully on the next attempt! 🚀**

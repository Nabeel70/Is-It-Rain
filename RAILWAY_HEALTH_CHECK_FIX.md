# 🎯 RAILWAY HEALTH CHECK FIX

## What Was Wrong

The build succeeded, but Railway health checks were failing because **the application never started**.

### Root Cause
When Poetry creates a virtual environment during the install phase, and then we use `poetry run` in the start command, Poetry needs to correctly locate the virtual environment. In Railway's container, the working directory context was causing Poetry to fail silently when trying to run uvicorn.

---

## ✅ Solution Applied

Updated `nixpacks.toml` to:

1. **Force Poetry to create `.venv` inside the project directory**:
   ```toml
   poetry config virtualenvs.in-project true
   ```

2. **Use direct path to uvicorn binary** instead of relying on `poetry run`:
   ```toml
   cmd = "cd /app/backend && /app/backend/.venv/bin/uvicorn app.main:app --host 0.0.0.0 --port $PORT"
   ```

This ensures:
- Virtual environment is in a predictable location: `/app/backend/.venv/`
- Uvicorn binary is called directly from the venv
- No dependency on Poetry's environment resolution at runtime

---

## 🚀 What to Do Now

### In Railway Dashboard:

1. **Go to your service** → **Deployments**
2. **Click "Redeploy"** on the latest deployment (or wait for auto-deploy from the Git push)
3. **Watch the build logs** - should complete successfully (as before)
4. **Watch the deployment logs** (NEW - this is where it was failing before)

### Expected Startup Logs (What You Should See):

```
✅ Starting container...
✅ INFO:     Started server process [1]
✅ INFO:     Waiting for application startup.
✅ INFO:     Application startup complete.
✅ INFO:     Uvicorn running on http://0.0.0.0:8080 (Press CTRL+C to quit)
```

### Health Check Should Now Pass:

```
✅ Attempt #1 succeeded
✅ Healthcheck passed!
✅ Deployment successful
```

---

## 🧪 Verification After Deploy

Once Railway shows **"Active"** status:

```bash
# Replace with your actual Railway domain
RAILWAY_URL="https://web-production-e0703.up.railway.app"

# Test 1: Health check
curl $RAILWAY_URL/health
# Expected: {"status":"ok","message":"Is It Rain API is running"}

# Test 2: API docs
curl -I $RAILWAY_URL/docs
# Expected: HTTP/1.1 200 OK

# Test 3: Model info
curl $RAILWAY_URL/api/model/info
# Expected: JSON with model_available: true

# Test 4: Forecast
curl -X POST $RAILWAY_URL/api/forecast/ensemble \
  -H "Content-Type: application/json" \
  -d '{"event_date": "2025-12-25", "query": "Tokyo, Japan"}'
# Expected: JSON with precipitation_probability
```

---

## 📊 Build Timeline

Your deployment should now complete in ~5 minutes:

| Time | Stage | What's Happening |
|------|-------|------------------|
| 0:00 | Setup | Installing Python 3.12 + Poetry |
| 1:00 | Install | Creating venv, installing dependencies |
| 3:30 | Build | Completing build phase |
| 4:00 | **Start** | **Uvicorn starting** ⬅️ This is where it was failing |
| 4:10 | Health Check | GET /health |
| 4:15 | **Success!** | Deployment active ✅ |

---

## 🔍 What Changed in nixpacks.toml

### Before (Broken):
```toml
[phases.install]
cmds = [ 
    "cd backend && (poetry env use python3.12 || ...) && poetry install --no-dev"
]

[start]
cmd = "cd backend && poetry run uvicorn app.main:app --host 0.0.0.0 --port $PORT"
```

**Problem**: `poetry run` couldn't find the virtual environment at runtime.

### After (Fixed):
```toml
[phases.install]
cmds = [ 
    "cd backend",
    "poetry config virtualenvs.in-project true",  # ← Forces .venv in project
    "(poetry env use python3.12 || ...)",
    "poetry install --no-dev"
]

[start]
cmd = "cd /app/backend && /app/backend/.venv/bin/uvicorn app.main:app --host 0.0.0.0 --port $PORT"
```

**Solution**: Direct path to uvicorn binary, no reliance on Poetry at runtime.

---

## 🚨 If Health Check Still Fails

### Check Railway Logs

1. Go to **Deployments** → Click the deployment
2. Look at **"Deployment Logs"** tab (not just Build logs)
3. Look for error messages like:
   - `ModuleNotFoundError: No module named 'app'`
   - `FileNotFoundError: [Errno 2] No such file or directory`
   - `Permission denied`

### Common Issues & Fixes

#### Issue: "No module named 'app'"
**Solution**: Working directory is wrong
```toml
# Ensure start command has cd /app/backend
cmd = "cd /app/backend && /app/backend/.venv/bin/uvicorn ..."
```

#### Issue: "Permission denied" on uvicorn binary
**Solution**: Make binary executable
```toml
[phases.build]
cmds = [
    "chmod +x /app/backend/.venv/bin/uvicorn",
    "echo 'Build phase complete'"
]
```

#### Issue: Port binding error
**Solution**: Ensure `$PORT` is used (Railway assigns this dynamically)
```toml
cmd = "... --port $PORT"  # Don't hardcode 8000
```

---

## 🎉 Success Indicators

You'll know it's finally working when:

✅ Build logs show: "Successfully Built!"  
✅ Deployment logs show: "INFO: Uvicorn running on http://0.0.0.0:8080"  
✅ Health check shows: "Healthcheck passed!"  
✅ Service status shows: "Active" with green indicator  
✅ `curl .../health` returns JSON (not connection refused)  

---

## 📞 Next Steps After Backend Works

Once your backend is healthy:

1. **Update Netlify** with the Railway URL
2. **Update Railway** with the Netlify URL in `ALLOWED_ORIGINS`
3. **Test the full application** end-to-end
4. **Celebrate!** 🎉

---

**All changes pushed to GitHub. Trigger a redeploy in Railway now and watch it succeed! 🚀**

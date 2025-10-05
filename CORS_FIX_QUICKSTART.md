# CORS Fix - Quick Reference

## The Problem
Your Netlify frontend (`https://is-it-rains.netlify.app`) cannot talk to your Railway backend (`https://is-it-rain-production.up.railway.app`) because of CORS (Cross-Origin Resource Sharing) restrictions.

## The Error
```
Access to XMLHttpRequest at 'https://is-it-rain-production.up.railway.app/api/forecast/ensemble' 
from origin 'https://is-it-rains.netlify.app' has been blocked by CORS policy
```

## The Fix (5 minutes)

### Step 1: Set Railway Environment Variable

1. Go to [Railway Dashboard](https://railway.app/dashboard)
2. Click on your **backend** service (`is-it-rain-production`)
3. Click **"Variables"** tab
4. Click **"+ New Variable"**
5. Add:
   - **Name**: `ALLOWED_ORIGINS`
   - **Value**: `https://is-it-rains.netlify.app,http://localhost:5173`

6. Click **"Save"** or **"Deploy"**

### Step 2: Wait for Deployment

- Railway will automatically redeploy (takes 2-3 minutes)
- Watch the deployment status in Railway dashboard

### Step 3: Verify in Logs

1. In Railway, click **"Deployments"**
2. Click the latest deployment
3. Look for this line in logs:
   ```
   Allowed origins: ['https://is-it-rains.netlify.app', 'http://localhost:5173']
   ```

### Step 4: Test Your App

1. Go to `https://is-it-rains.netlify.app`
2. Press `Ctrl+Shift+R` (hard refresh to clear cache)
3. Enter a location and date
4. Click **"Get Forecast"**
5. Should work! 🎉

---

## Common Mistakes

❌ **Wrong variable name**: Using `CORS_ORIGINS` instead of `ALLOWED_ORIGINS`

❌ **Missing https**: Using `is-it-rains.netlify.app` instead of `https://is-it-rains.netlify.app`

❌ **Trailing slash**: Using `https://is-it-rains.netlify.app/` (remove the `/`)

❌ **Spaces**: Using `url1, url2` instead of `url1,url2` (no spaces!)

❌ **Wrong URL**: Using `is-it-rain` instead of `is-it-rains` (check your actual Netlify URL!)

---

## Verification Command

Test if CORS is working:

```bash
curl -X OPTIONS https://is-it-rain-production.up.railway.app/api/forecast/ensemble \
  -H "Origin: https://is-it-rains.netlify.app" \
  -H "Access-Control-Request-Method: POST" \
  -v
```

**Expected response** should include:
```
Access-Control-Allow-Origin: https://is-it-rains.netlify.app
Access-Control-Allow-Methods: DELETE, GET, HEAD, OPTIONS, PATCH, POST, PUT
```

---

## Still Not Working?

### Check Backend Health

```bash
curl https://is-it-rain-production.up.railway.app/health
```

Should return: `{"status":"ok","message":"Is It Rain API is running"}`

### Check Frontend Environment Variable

1. Go to Netlify dashboard
2. Site settings → Environment variables
3. Verify: `VITE_API_URL` = `https://is-it-rain-production.up.railway.app`
4. If changed, trigger a new deploy

### Check Browser Console

1. Open your app: `https://is-it-rains.netlify.app`
2. Press `F12` to open DevTools
3. Go to **Console** tab
4. Look for errors
5. Go to **Network** tab
6. Try the forecast button
7. Check the `ensemble` request
8. Look at **Response Headers**

Should see:
```
access-control-allow-origin: https://is-it-rains.netlify.app
```

---

## Need Help?

1. Check Railway logs: Railway dashboard → Your service → Deployments → Latest → View logs
2. Check Netlify logs: Netlify dashboard → Deploys → Latest → View logs
3. Share screenshots of:
   - Railway environment variables
   - Railway deployment logs
   - Browser console errors
   - Network tab in DevTools

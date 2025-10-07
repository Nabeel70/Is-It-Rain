# Deploy to Render.com - Complete Step-by-Step Guide

## Why Render?
- ✅ **100% FREE** for both backend and frontend
- ✅ **All-in-one platform** - no separate services needed
- ✅ **Auto-deploys** from GitHub
- ✅ **Much simpler** than Railway
- ✅ **Generous free tier** - 750 hours/month

---

## Part 1: Create Render Account (2 minutes)

### Step 1: Sign Up
1. Go to [https://render.com](https://render.com)
2. Click **"Get Started"** or **"Sign Up"**
3. Choose **"Sign up with GitHub"**
4. Authorize Render to access your GitHub account
5. You'll be redirected to Render Dashboard

---

## Part 2: Deploy Using Blueprint (5 minutes)

### Step 2: Connect Your Repository

1. In Render Dashboard, click **"New +"** (top right)
2. Select **"Blueprint"**
3. Click **"Connect GitHub"** if not already connected
4. Find and select your repository: **`Is-It-Rain`**
5. Click **"Connect"**

### Step 3: Configure the Blueprint

1. Render will detect the `render.yaml` file automatically
2. You'll see **2 services** listed:
   - `is-it-rain-api` (Backend)
   - `is-it-rain-frontend` (Frontend)
3. Review the settings (already configured in render.yaml)
4. Click **"Apply"**

### Step 4: Wait for Deployment

Render will now:
- Create both services automatically
- Install Python dependencies for backend
- Install Node dependencies and build frontend
- Deploy both services

**This takes 5-7 minutes**. You'll see:
- Backend: "Live" status with a green checkmark ✅
- Frontend: "Live" status with a green checkmark ✅

---

## Part 3: Get Your URLs and Configure CORS (3 minutes)

### Step 5: Find Your Backend URL

1. In Render Dashboard, click on **`is-it-rain-api`** service
2. At the top, you'll see a URL like:
   ```
   https://is-it-rain-api.onrender.com
   ```
3. **Copy this URL** - you'll need it in the next step

### Step 6: Update Frontend Environment Variable

1. Go back to Dashboard
2. Click on **`is-it-rain-frontend`** service
3. Click **"Environment"** in the left sidebar
4. Find the variable **`VITE_API_URL`**
5. Click **"Edit"**
6. Paste your backend URL (from Step 5):
   ```
   https://is-it-rain-api.onrender.com
   ```
7. Click **"Save Changes"**
8. Render will automatically **redeploy** the frontend (takes 2-3 minutes)

### Step 7: Update Backend CORS Settings

1. Click on **`is-it-rain-api`** service
2. Click **"Environment"** in the left sidebar
3. Find **`ALLOWED_ORIGINS`**
4. Click **"Edit"**
5. Get your frontend URL (at the top of the page):
   ```
   https://is-it-rain.onrender.com
   ```
6. Update the value to:
   ```
   https://is-it-rain.onrender.com,http://localhost:5173
   ```
7. Click **"Save Changes"**
8. Render will automatically **redeploy** the backend (takes 2-3 minutes)

---

## Part 4: Test Your Application (2 minutes)

### Step 8: Verify Backend Health

1. Open a new browser tab
2. Go to: `https://is-it-rain-api.onrender.com/health`
3. You should see:
   ```json
   {"status":"ok","message":"Is It Rain API is running"}
   ```

### Step 9: Test the Frontend

1. Go to your frontend URL: `https://is-it-rain.onrender.com`
2. You should see your "Is It Rain" application
3. Enter a location (e.g., "Tokyo, Japan")
4. Enter a future date
5. Click **"Get Forecast"**
6. You should see the weather forecast! 🎉

---

## Troubleshooting

### Backend shows "Starting..."
- **Wait 2-3 minutes** - free tier services sleep after 15 minutes of inactivity
- First request wakes them up (takes 30-60 seconds)

### CORS Error in Browser Console
- Verify `ALLOWED_ORIGINS` in backend includes your exact frontend URL
- Make sure `VITE_API_URL` in frontend points to backend URL
- Clear browser cache: `Ctrl+Shift+R` (Windows/Linux) or `Cmd+Shift+R` (Mac)

### Build Failed
- Check **"Logs"** tab in Render Dashboard
- Look for error messages
- Most common: Missing dependencies (already fixed in render.yaml)

### Frontend Shows 404
- Verify the build completed successfully
- Check that `staticPublishPath` is set to `frontend/dist`
- Ensure routes are configured for SPA (already done in render.yaml)

---

## Important Notes

### Free Tier Limitations
- Services **sleep after 15 minutes** of inactivity
- First request after sleep takes **30-60 seconds** to wake up
- 750 hours/month free (enough for small projects)
- If you need 24/7 uptime, upgrade to paid plan ($7/month)

### Keep Services Awake (Optional)
Use a free service like **UptimeRobot** to ping your backend every 14 minutes:
1. Go to [https://uptimerobot.com](https://uptimerobot.com)
2. Add monitor: `https://is-it-rain-api.onrender.com/health`
3. Set interval: 15 minutes

---

## Your Live URLs (After Deployment)

- **Frontend**: `https://is-it-rain.onrender.com`
- **Backend**: `https://is-it-rain-api.onrender.com`
- **API Docs**: `https://is-it-rain-api.onrender.com/docs`
- **Health Check**: `https://is-it-rain-api.onrender.com/health`

---

## Future Updates

When you push to GitHub:
1. Render **automatically detects** the changes
2. **Automatically redeploys** both services
3. Takes 3-5 minutes
4. No manual steps needed!

---

## Need Help?

If something doesn't work:
1. Check the **"Logs"** tab in each service
2. Look for red error messages
3. Common issues:
   - Wrong URLs in environment variables
   - CORS not configured
   - Services still waking up from sleep

**Support**: Render has excellent documentation at [https://render.com/docs](https://render.com/docs)

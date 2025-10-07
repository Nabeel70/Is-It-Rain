# Quick Start - Deploy to Render in 10 Minutes ⚡

## ✅ Prerequisites Done
- Repository pushed to GitHub ✓
- `render.yaml` configuration ready ✓
- All code tested and working ✓

---

## 🚀 Deploy Now - Follow These Exact Steps

### **Step 1: Sign Up (1 minute)**

```
1. Open: https://render.com
2. Click: "Get Started" button (top right)
3. Click: "Sign up with GitHub"
4. Click: "Authorize Render"
```

✅ You'll land on Render Dashboard

---

### **Step 2: Deploy Blueprint (2 minutes)**

```
1. Click: "New +" button (top right corner)
2. Click: "Blueprint"
3. Click: "Connect a repository"
4. Find: "Is-It-Rain" in the list
5. Click: "Connect" next to it
6. Click: "Apply" button
```

✅ Render starts deploying automatically!

---

### **Step 3: Wait for Deployment (5-7 minutes)**

You'll see 2 services building:
```
is-it-rain-api       [Building...] → [Live ✓]
is-it-rain-frontend  [Building...] → [Live ✓]
```

**What's happening?**
- Backend: Installing Python, Poetry, dependencies, ML models
- Frontend: Installing Node, building React app

☕ **Grab a coffee!** This takes 5-7 minutes.

---

### **Step 4: Configure URLs (2 minutes)**

#### Get Backend URL:
```
1. Click: "is-it-rain-api" service
2. Copy the URL at the top (looks like):
   https://is-it-rain-api.onrender.com
```

#### Update Frontend:
```
1. Click: "Environment" (left sidebar)
2. Find: VITE_API_URL
3. Click: "Edit"
4. Paste: YOUR_BACKEND_URL (from above)
5. Click: "Save Changes"
```

✅ Frontend will redeploy automatically (2-3 minutes)

#### Update Backend CORS:
```
1. Go back to Dashboard
2. Click: "is-it-rain-api" service
3. Click: "Environment"
4. Find: ALLOWED_ORIGINS
5. Click: "Edit"
6. Change to: https://YOUR-FRONTEND-URL.onrender.com,http://localhost:5173
7. Click: "Save Changes"
```

✅ Backend will redeploy automatically (2-3 minutes)

---

### **Step 5: Test Your App! 🎉**

#### Test Backend:
```
Open: https://is-it-rain-api.onrender.com/health
```

**Expected:**
```json
{"status":"ok","message":"Is It Rain API is running"}
```

#### Test Frontend:
```
Open: https://is-it-rain.onrender.com
```

**Try it:**
1. Enter location: "Tokyo, Japan"
2. Pick a future date
3. Click: "Get Forecast"
4. See the result! ✨

---

## 📊 Your Live URLs

After deployment:
- **App**: https://is-it-rain.onrender.com
- **API**: https://is-it-rain-api.onrender.com
- **Docs**: https://is-it-rain-api.onrender.com/docs
- **Health**: https://is-it-rain-api.onrender.com/health

---

## ⚠️ Important: Free Tier Behavior

**Services sleep after 15 minutes of no activity**

What this means:
- First request after sleep takes **30-60 seconds**
- Loading spinner will show "Loading..."
- After first request, it's instant again!

**This is normal for free tier** ✓

To keep awake (optional):
- Upgrade to paid: $7/month
- Use UptimeRobot: Ping every 14 minutes (free)

---

## 🐛 Troubleshooting

### "Service Unavailable" or Spinning Loading
- **Wait 60 seconds** - service is waking up from sleep
- Refresh the page

### CORS Error
- Check `ALLOWED_ORIGINS` includes exact frontend URL
- Check `VITE_API_URL` points to backend URL
- Clear browser cache: Ctrl+Shift+R

### Build Failed
- Click service → "Logs" tab
- Look for red errors
- Usually: dependency issue (already fixed!)

### Frontend Shows 404
- Check build completed: Look for "Live" status
- Wait 2-3 minutes after last deploy

---

## 🎓 Pro Tips

1. **Check Logs**: Always check "Logs" tab if something fails
2. **Hard Refresh**: Use Ctrl+Shift+R to clear cache
3. **First Load**: Remember - first load takes 30-60s on free tier
4. **Auto Deploy**: Push to GitHub = automatic deploy!

---

## 🆘 Still Not Working?

1. Screenshot the error in browser console (F12)
2. Check Render logs for both services
3. Verify environment variables are correct
4. Make sure both services show "Live" status

---

## ✨ Done!

Your app is now live on the internet! 🚀

Share it: `https://is-it-rain.onrender.com`

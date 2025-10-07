# 🚀 Deploy to Fly.io - Complete Guide (100% FREE!)

## ✅ Why Fly.io is PERFECT for Your Project

### Free Tier Benefits:
- ✅ **$5/month credit** (free forever, no credit card until you upgrade)
- ✅ **3 shared-cpu VMs** with 256MB RAM each
- ✅ **3GB storage** (enough for your ML models!)
- ✅ **160GB outbound data transfer/month**
- ✅ **Auto-start/stop** (saves resources when not in use)
- ✅ **Global CDN** (fast everywhere!)
- ✅ **Perfect for**: Python FastAPI + React apps

### What Makes It Better:
| Feature | Fly.io | Railway | Render |
|---------|--------|---------|--------|
| **Free Tier** | $5 credit/month | $5 credit/month | Free but needs card |
| **Setup** | Simple CLI | Dashboard issues | Dashboard |
| **Auto-sleep** | Yes (saves $) | No | Yes |
| **Cold start** | ~2 seconds | N/A | ~30 seconds |
| **Reliability** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐ |

---

## 📋 Prerequisites

- ✅ GitHub account (you have this)
- ✅ Your code pushed to GitHub (done!)
- ✅ Terminal access (you have this in VS Code)
- ❌ NO credit card required for free tier!

---

## Part 1: Install Fly.io CLI (2 minutes)

### Step 1: Install the CLI

**In your VS Code terminal, run:**

```bash
curl -L https://fly.io/install.sh | sh
```

Wait for it to complete. You'll see: "flyctl was installed successfully!"

### Step 2: Add to PATH

```bash
export FLYCTL_INSTALL="/home/codespace/.fly"
export PATH="$FLYCTL_INSTALL/bin:$PATH"
```

### Step 3: Verify Installation

```bash
flyctl version
```

You should see something like: `flyctl v0.x.xxx`

✅ **CLI installed!**

---

## Part 2: Create Fly.io Account (2 minutes)

### Step 4: Sign Up

```bash
flyctl auth signup
```

This will:
1. Open a browser window
2. Ask you to sign up with **GitHub** (recommended)
3. Click "Authorize Fly.io"
4. You're logged in!

**Alternative - If you already have an account:**
```bash
flyctl auth login
```

✅ **Account created and authenticated!**

---

## Part 3: Deploy Backend API (5 minutes)

### Step 5: Navigate to Your Project

```bash
cd /workspaces/Is-It-Rain
```

### Step 6: Launch Backend

```bash
flyctl launch --config fly.backend.toml --name is-it-rain-api --no-deploy
```

**What happens:**
- Fly.io reads your configuration
- Creates the app in Singapore region (closest to you)
- Sets up everything
- **Does NOT deploy yet** (we need to check settings first)

**Answer the prompts:**
```
? Choose an app name: is-it-rain-api (already set)
? Choose a region: sin (Singapore) (already set)
? Would you like to set up a database? No
? Would you like to deploy now? No
```

### Step 7: Deploy Backend

```bash
flyctl deploy --config fly.backend.toml
```

**This will:**
1. Build Docker image (3-4 minutes)
2. Push to Fly.io
3. Start your API
4. Run health checks

**Wait for:** "✓ 1 desired, 1 placed, 1 healthy, 0 unhealthy"

### Step 8: Get Backend URL

```bash
flyctl status --config fly.backend.toml
```

Your backend URL: `https://is-it-rain-api.fly.dev`

### Step 9: Test Backend

```bash
curl https://is-it-rain-api.fly.dev/health
```

**Expected response:**
```json
{"status":"ok","message":"Is It Rain API is running"}
```

✅ **Backend is LIVE!**

---

## Part 4: Deploy Frontend (5 minutes)

### Step 10: Update Frontend Environment Variable

First, let's update the frontend config with your backend URL:

```bash
flyctl secrets set VITE_API_URL=https://is-it-rain-api.fly.dev --config fly.frontend.toml --app is-it-rain-frontend
```

### Step 11: Launch Frontend

```bash
flyctl launch --config fly.frontend.toml --name is-it-rain-frontend --no-deploy
```

**Answer the prompts:**
```
? Choose an app name: is-it-rain-frontend (already set)
? Choose a region: sin (Singapore)
? Would you like to deploy now? No
```

### Step 12: Deploy Frontend

```bash
flyctl deploy --config fly.frontend.toml
```

**This will:**
1. Build React app (2-3 minutes)
2. Create optimized production build
3. Deploy to Fly.io CDN
4. Start serving your app

**Wait for:** "✓ 1 desired, 1 placed, 1 healthy, 0 unhealthy"

### Step 13: Get Frontend URL

```bash
flyctl status --config fly.frontend.toml
```

Your frontend URL: `https://is-it-rain-frontend.fly.dev`

✅ **Frontend is LIVE!**

---

## Part 5: Update CORS Settings (1 minute)

### Step 14: Update Backend CORS

```bash
flyctl secrets set ALLOWED_ORIGINS="https://is-it-rain-frontend.fly.dev,http://localhost:5173" --config fly.backend.toml
```

This will automatically restart your backend with the new CORS settings.

✅ **CORS configured!**

---

## Part 6: Test Your App! 🎉

### Step 15: Open Your App

```bash
flyctl open --config fly.frontend.toml
```

Or manually open: `https://is-it-rain-frontend.fly.dev`

### Step 16: Test the Forecast

1. Enter location: **"Tokyo, Japan"**
2. Pick a future date
3. Click **"Get Forecast"**
4. See the weather prediction! ✨

✅ **YOUR APP IS LIVE ON THE INTERNET!**

---

## 📊 Your Live URLs

- **Frontend (Main App)**: `https://is-it-rain-frontend.fly.dev`
- **Backend API**: `https://is-it-rain-api.fly.dev`
- **API Documentation**: `https://is-it-rain-api.fly.dev/docs`
- **Health Check**: `https://is-it-rain-api.fly.dev/health`

---

## 💰 Free Tier Details

### What You Get FREE:
```
✅ 3 shared-cpu VMs (1 for backend, 1 for frontend, 1 spare)
✅ 256MB RAM per VM (perfect for your app!)
✅ 3GB storage (ML models fit perfectly!)
✅ 160GB bandwidth/month (thousands of users!)
✅ Auto-sleep when idle (saves your free credit)
✅ Auto-wake on request (~2 seconds)
```

### Usage Monitor:
```bash
flyctl dashboard
```

Opens your dashboard to see:
- Current usage
- Remaining credit
- App performance

### Monthly Cost Estimate:
**$0** - Your app fits perfectly in free tier!

---

## 🔄 Auto-Deploy from GitHub (Bonus!)

Want automatic deployments when you push code?

### Step 17: Set Up GitHub Actions

```bash
# Get your Fly.io token
flyctl auth token
```

Copy the token.

### Step 18: Add to GitHub Secrets

1. Go to: `https://github.com/Nabeel70/Is-It-Rain/settings/secrets/actions`
2. Click: "New repository secret"
3. Name: `FLY_API_TOKEN`
4. Value: Paste the token from Step 17
5. Click: "Add secret"

### Step 19: Create GitHub Action

I'll create this file for you in the next step!

---

## 🛠️ Useful Commands

### Check App Status:
```bash
flyctl status --config fly.backend.toml
flyctl status --config fly.frontend.toml
```

### View Logs:
```bash
flyctl logs --config fly.backend.toml
flyctl logs --config fly.frontend.toml
```

### Check Health:
```bash
curl https://is-it-rain-api.fly.dev/health
```

### Restart App:
```bash
flyctl apps restart is-it-rain-api
flyctl apps restart is-it-rain-frontend
```

### Scale (if needed later):
```bash
# Scale up for more traffic
flyctl scale count 2 --config fly.backend.toml

# Scale down to save credit
flyctl scale count 1 --config fly.backend.toml
```

### SSH into VM (for debugging):
```bash
flyctl ssh console --config fly.backend.toml
```

---

## 🐛 Troubleshooting

### Issue: "Could not find App"
**Solution:**
```bash
flyctl apps list
# Check if apps exist, if not, run launch command again
```

### Issue: Build fails
**Solution:**
```bash
# Check logs
flyctl logs --config fly.backend.toml

# Common fix: rebuild
flyctl deploy --config fly.backend.toml --no-cache
```

### Issue: Health checks failing
**Solution:**
```bash
# Check if app is running
flyctl status --config fly.backend.toml

# View logs for errors
flyctl logs --config fly.backend.toml

# Restart
flyctl apps restart is-it-rain-api
```

### Issue: CORS errors in browser
**Solution:**
```bash
# Update CORS
flyctl secrets set ALLOWED_ORIGINS="https://is-it-rain-frontend.fly.dev,http://localhost:5173" --config fly.backend.toml

# Verify
flyctl secrets list --config fly.backend.toml
```

### Issue: Frontend shows API error
**Solution:**
```bash
# Check backend is healthy
curl https://is-it-rain-api.fly.dev/health

# Update frontend API URL
flyctl secrets set VITE_API_URL=https://is-it-rain-api.fly.dev --config fly.frontend.toml
```

### Issue: App is slow to load first time
**This is normal!** Free tier VMs auto-sleep after 15 minutes of inactivity.
- First request takes ~2-5 seconds to wake up
- Subsequent requests are instant
- To keep always-on, upgrade to paid tier ($1.94/month per VM)

---

## 📈 Monitoring & Performance

### Check App Performance:
```bash
flyctl dashboard
```

### View Metrics:
```bash
flyctl metrics --config fly.backend.toml
```

### Monitor in Real-Time:
```bash
flyctl logs --config fly.backend.toml -f
```

---

## 🎓 Pro Tips

1. **Regional Selection**: 
   - I set you to `sin` (Singapore)
   - For US users, use `iad` (Virginia)
   - For EU users, use `ams` (Amsterdam)
   - Change with: `flyctl regions set iad --config fly.backend.toml`

2. **Secrets Management**:
   ```bash
   # List all secrets
   flyctl secrets list --config fly.backend.toml
   
   # Add new secret
   flyctl secrets set API_KEY=your-key-here --config fly.backend.toml
   
   # Remove secret
   flyctl secrets unset API_KEY --config fly.backend.toml
   ```

3. **Database** (if you need it later):
   ```bash
   flyctl postgres create --name is-it-rain-db
   flyctl postgres attach is-it-rain-db --config fly.backend.toml
   ```

4. **Custom Domain** (optional):
   ```bash
   flyctl certs add yourdomain.com --config fly.frontend.toml
   ```

---

## 🚨 Important Notes

### Free Tier Limits:
- ✅ Perfect for your project size
- ✅ Can handle hundreds of users
- ⚠️ VMs auto-sleep when idle (2-5 second wake time)
- ⚠️ Don't run crypto mining or abuse (will be banned)

### When to Upgrade:
- You need 24/7 availability (no sleep)
- You exceed 160GB bandwidth/month
- You want more than 3 VMs
- **Cost**: ~$2-5/month per VM for hobby tier

### Data Persistence:
- Your SQLite database persists
- Stored in `/data` directory
- Backed up automatically by Fly.io
- If VM restarts, data is preserved

---

## 🎉 Success Checklist

- ✅ Fly.io CLI installed
- ✅ Account created (no credit card needed)
- ✅ Backend deployed and healthy
- ✅ Frontend deployed and accessible
- ✅ CORS configured correctly
- ✅ App tested and working
- ✅ URLs saved:
  - Frontend: `https://is-it-rain-frontend.fly.dev`
  - Backend: `https://is-it-rain-api.fly.dev`

---

## 🆘 Need Help?

### Check Documentation:
- Main docs: https://fly.io/docs
- Python apps: https://fly.io/docs/languages-and-frameworks/python/
- Django/FastAPI: https://fly.io/docs/django/

### Community Support:
- Community: https://community.fly.io
- Discord: https://fly.io/discord

### Quick Debug:
```bash
# Full status check
flyctl doctor

# Check billing/usage
flyctl dashboard

# View all apps
flyctl apps list
```

---

## 🔄 Future Updates

When you update your code:

1. **Push to GitHub:**
   ```bash
   git add .
   git commit -m "Update feature"
   git push
   ```

2. **Deploy changes:**
   ```bash
   # Backend
   flyctl deploy --config fly.backend.toml
   
   # Frontend
   flyctl deploy --config fly.frontend.toml
   ```

Or set up GitHub Actions (I can help with this!)

---

## ✨ You're Done!

Your app is now:
- ✅ **Live on the internet**
- ✅ **Running on Fly.io's free tier**
- ✅ **Accessible worldwide**
- ✅ **Auto-scaling**
- ✅ **Production-ready**

**Share your app:**
`https://is-it-rain-frontend.fly.dev` 🚀

Enjoy your deployed NASA Space Apps project! 🌍☔

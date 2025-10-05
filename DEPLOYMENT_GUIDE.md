# Deployment Guide - Is It Rain

**Quick guide to deploy your NASA Space Apps Challenge project to production!**

---

## Prerequisites

- ✅ ML model trained (you've done this!)
- ✅ GitHub account
- ✅ Backend code ready
- ✅ Frontend code ready

---

## Option 1: Railway.app (Backend) + Netlify (Frontend) [RECOMMENDED]

### Step 1: Deploy Backend to Railway.app

**Why Railway?**
- ✅ Free tier: 500 hours/month
- ✅ Poetry support (no configuration needed)
- ✅ Automatic deployments from GitHub
- ✅ Built-in PostgreSQL if needed

**Steps**:

1. **Push your code to GitHub**:
   ```bash
   cd /workspaces/Is-It-Rain
   git add .
   git commit -m "Production-ready ML system"
   git push origin main
   ```

2. **Create Railway account**:
   - Go to https://railway.app
   - Sign up with GitHub

3. **Create new project**:
   - Click "New Project"
   - Select "Deploy from GitHub repo"
   - Choose your `Is-It-Rain` repository
   - Railway auto-detects Python + Poetry ✨

4. **Configure environment variables**:
   - In Railway dashboard, go to "Variables" tab
   - Add these variables:
     ```
     CORS_ORIGINS=https://your-netlify-app.netlify.app
     ```
   
5. **Deploy**:
   - Railway automatically builds and deploys!
   - Wait 2-3 minutes
   - Get your deployment URL: `https://your-app.railway.app`

6. **Test deployment**:
   ```bash
   curl https://your-app.railway.app/health
   # Should return: {"status": "healthy"}
   
   curl https://your-app.railway.app/api/model/info
   # Should return model metadata
   ```

**Railway Configuration** (railway.json - optional):
```json
{
  "$schema": "https://railway.app/railway.schema.json",
  "build": {
    "builder": "NIXPACKS"
  },
  "deploy": {
    "startCommand": "cd backend && poetry run uvicorn app.main:app --host 0.0.0.0 --port $PORT",
    "healthcheckPath": "/health",
    "healthcheckTimeout": 100
  }
}
```

---

### Step 2: Deploy Frontend to Netlify

**Why Netlify?**
- ✅ Free tier: Unlimited bandwidth
- ✅ Automatic HTTPS
- ✅ Global CDN
- ✅ GitHub integration

**Steps**:

1. **Update frontend API URL**:
   
   Edit `frontend/src/hooks/useForecast.ts`:
   ```typescript
   // Change this line:
   const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';
   
   // To use ensemble endpoint:
   const response = await fetch(`${API_URL}/api/forecast/ensemble`, {
     method: 'POST',
     headers: { 'Content-Type': 'application/json' },
     body: JSON.stringify(requestData),
   });
   ```

2. **Create `.env.production` file**:
   ```bash
   cd frontend
   echo "VITE_API_URL=https://your-app.railway.app" > .env.production
   ```

3. **Test build locally**:
   ```bash
   npm install
   npm run build
   # Should create dist/ folder
   ```

4. **Create Netlify account**:
   - Go to https://netlify.com
   - Sign up with GitHub

5. **Deploy**:
   - Click "New site from Git"
   - Choose your GitHub repository
   - Configure build settings:
     - **Base directory**: `frontend`
     - **Build command**: `npm run build`
     - **Publish directory**: `frontend/dist`
   
6. **Add environment variable**:
   - In Netlify dashboard, go to "Site settings" → "Environment variables"
   - Add: `VITE_API_URL` = `https://your-app.railway.app`

7. **Deploy**:
   - Click "Deploy site"
   - Wait 1-2 minutes
   - Get your URL: `https://your-app.netlify.app`

8. **Update backend CORS**:
   - Go back to Railway dashboard
   - Update `CORS_ORIGINS` variable:
     ```
     CORS_ORIGINS=https://your-app.netlify.app,http://localhost:5173
     ```
   - Railway will auto-redeploy

9. **Test live app**:
   - Visit `https://your-app.netlify.app`
   - Try forecasting for a location
   - Should see ML-powered predictions! 🎉

---

## Option 2: Render.com (Backend + Frontend)

**Why Render?**
- ✅ Free tier for both backend and frontend
- ✅ Single platform for everything
- ✅ Automatic deployments

**Steps**:

1. **Create Render account**:
   - Go to https://render.com
   - Sign up with GitHub

2. **Deploy Backend** (Web Service):
   - Click "New" → "Web Service"
   - Connect GitHub repo
   - Settings:
     - **Name**: `is-it-rain-backend`
     - **Root Directory**: `backend`
     - **Environment**: Python 3
     - **Build Command**: `pip install poetry && poetry install`
     - **Start Command**: `poetry run uvicorn app.main:app --host 0.0.0.0 --port $PORT`
   - Environment Variables:
     ```
     CORS_ORIGINS=https://is-it-rain-frontend.onrender.com
     ```
   - Free tier: Spins down after inactivity (first request takes 30s)

3. **Deploy Frontend** (Static Site):
   - Click "New" → "Static Site"
   - Connect GitHub repo
   - Settings:
     - **Name**: `is-it-rain-frontend`
     - **Root Directory**: `frontend`
     - **Build Command**: `npm install && npm run build`
     - **Publish Directory**: `dist`
   - Environment Variables:
     ```
     VITE_API_URL=https://is-it-rain-backend.onrender.com
     ```

4. **Test**:
   - Visit `https://is-it-rain-frontend.onrender.com`
   - First request may take 30s (free tier wakes up)

---

## Option 3: Docker + Any Cloud Provider

**Why Docker?**
- ✅ Consistent environment
- ✅ Works anywhere (AWS, GCP, Azure, DigitalOcean)
- ✅ Easy scaling

**Steps**:

1. **Backend Dockerfile** (already exists at root):
   ```dockerfile
   FROM python:3.12-slim
   WORKDIR /app
   COPY backend/pyproject.toml backend/poetry.lock ./
   RUN pip install poetry && poetry install --no-dev
   COPY backend/ ./
   CMD ["poetry", "run", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
   ```

2. **Frontend Dockerfile**:
   ```dockerfile
   FROM node:20-alpine AS build
   WORKDIR /app
   COPY frontend/package*.json ./
   RUN npm install
   COPY frontend/ ./
   RUN npm run build
   
   FROM nginx:alpine
   COPY --from=build /app/dist /usr/share/nginx/html
   COPY frontend/nginx.conf /etc/nginx/conf.d/default.conf
   EXPOSE 80
   CMD ["nginx", "-g", "daemon off;"]
   ```

3. **docker-compose.yml**:
   ```yaml
   version: '3.8'
   services:
     backend:
       build:
         context: .
         dockerfile: Dockerfile
       ports:
         - "8000:8000"
       environment:
         - CORS_ORIGINS=http://localhost:3000
       volumes:
         - ./backend/data:/app/data
     
     frontend:
       build:
         context: ./frontend
         dockerfile: Dockerfile
       ports:
         - "3000:80"
       environment:
         - VITE_API_URL=http://localhost:8000
       depends_on:
         - backend
   ```

4. **Deploy to any provider**:
   - **AWS ECS**: Use docker-compose with ECS
   - **Google Cloud Run**: `gcloud run deploy`
   - **DigitalOcean App Platform**: Connect GitHub repo
   - **Azure Container Apps**: Use Docker images

---

## Environment Variables Reference

### Backend

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `CORS_ORIGINS` | Yes | `http://localhost:5173` | Allowed frontend origins (comma-separated) |
| `DATABASE_URL` | No | `sqlite:///data/forecasts.db` | Database connection string |
| `NASA_POWER_API_URL` | No | NASA default | NASA POWER API endpoint |
| `PORT` | No | `8000` | Server port (set by hosting provider) |

### Frontend

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `VITE_API_URL` | Yes | `http://localhost:8000` | Backend API URL |

---

## Post-Deployment Checklist

### 1. Verify Backend Health

```bash
curl https://your-backend.railway.app/health
# Expected: {"status": "healthy"}

curl https://your-backend.railway.app/api/model/info
# Expected: Model metadata with "model_available": true
```

### 2. Test Ensemble Endpoint

```bash
curl -X POST https://your-backend.railway.app/api/forecast/ensemble \
  -H "Content-Type: application/json" \
  -d '{"event_date": "2025-12-25", "query": "New York"}'
# Expected: Forecast with precipitation probability
```

### 3. Test Frontend

1. Visit `https://your-app.netlify.app`
2. Enter location: "Tokyo, Japan"
3. Select date: December 25, 2025
4. Click "Get Forecast"
5. Should see:
   - ✅ Location name and coordinates
   - ✅ Precipitation probability
   - ✅ Precipitation intensity (mm)
   - ✅ Summary with ML insights
   - ✅ Dataset: "NASA POWER + ML Ensemble"

### 4. Check Browser Console

Open DevTools (F12) → Console:
- ❌ No CORS errors (check backend CORS_ORIGINS)
- ❌ No 404 errors (check API_URL)
- ❌ No network errors

---

## Troubleshooting

### Issue: "CORS policy blocked"

**Solution**: Update backend `CORS_ORIGINS` environment variable:
```bash
# Railway dashboard → Variables → CORS_ORIGINS
CORS_ORIGINS=https://your-app.netlify.app,http://localhost:5173
```

### Issue: "Network error" or "Failed to fetch"

**Causes**:
1. Backend not running
2. Wrong API_URL in frontend
3. Backend crashed

**Solution**:
```bash
# Check backend logs (Railway)
railway logs

# Check backend health
curl https://your-backend.railway.app/health

# Verify frontend env variable
# Netlify: Site settings → Environment variables → VITE_API_URL
```

### Issue: "Model not available"

**Solution**: ML model files not deployed

```bash
# Ensure data/ml_models/ is committed to Git
git add backend/data/ml_models/*.joblib
git commit -m "Add trained ML models"
git push

# Or retrain on server:
railway run python -m app.scripts.train_model
```

### Issue: Backend sleeps (Render free tier)

**Solution**: First request takes 30s on free tier

1. Upgrade to paid plan ($7/month)
2. Add a cron job to ping every 10 minutes:
   ```bash
   # Use cron-job.org
   curl https://your-backend.onrender.com/health
   ```

---

## Performance Optimization

### 1. Enable Caching

Backend already has Redis caching configured. For production:

```bash
# Railway: Add Redis addon
railway add redis

# Update environment variable
REDIS_URL=redis://default:password@host:port
```

### 2. Enable Compression

Backend has gzip compression enabled automatically.

### 3. CDN for Frontend

Netlify provides global CDN by default. For Railway:

```bash
# Add Cloudflare in front of Railway
# Set up custom domain with Cloudflare DNS
```

### 4. Database Optimization

For production with high traffic:

```bash
# Switch from SQLite to PostgreSQL
railway add postgresql

# Update DATABASE_URL
DATABASE_URL=postgresql://user:pass@host:port/dbname
```

---

## Monitoring & Logs

### Railway

```bash
# View logs
railway logs --tail

# View metrics
# Dashboard → Metrics tab → CPU, Memory, Network
```

### Netlify

```bash
# View build logs
# Dashboard → Deploys → Build log

# View function logs (if using Netlify Functions)
# Dashboard → Functions → Logs
```

### Set up Alerts

**Sentry** (Error tracking):
1. Create account at sentry.io
2. Add to backend:
   ```bash
   poetry add sentry-sdk
   ```
3. Configure in `app/main.py`:
   ```python
   import sentry_sdk
   sentry_sdk.init(dsn="your-dsn")
   ```

**UptimeRobot** (Uptime monitoring):
1. Go to uptimerobot.com
2. Add monitor for `https://your-backend.railway.app/health`
3. Get email alerts if down > 5 minutes

---

## Custom Domain (Optional)

### Backend (Railway)

1. Go to Railway dashboard → Settings → Domains
2. Click "Add Custom Domain"
3. Add your domain: `api.is-it-rain.com`
4. Update DNS with provided CNAME records
5. Wait for SSL certificate (automatic)

### Frontend (Netlify)

1. Go to Netlify dashboard → Domain settings
2. Click "Add custom domain"
3. Add your domain: `is-it-rain.com`
4. Update DNS with Netlify nameservers or CNAME
5. SSL enabled automatically (Let's Encrypt)

---

## Cost Estimate

### Free Tier (Recommended for NASA Challenge)

| Service | Free Tier | Limits |
|---------|-----------|--------|
| **Railway** (Backend) | $5 credit/month | 500 hours, 512MB RAM |
| **Netlify** (Frontend) | Forever free | 100GB bandwidth/month |
| **Render** (Alternative) | 750 hours/month | Sleeps after 15min inactivity |
| **Total** | **$0/month** | Good for 1000-5000 users/month |

### Paid Plan (Production Scale)

| Service | Cost | What You Get |
|---------|------|--------------|
| **Railway** (Backend) | $10/month | Always on, 2GB RAM, better CPU |
| **Netlify** (Frontend) | $19/month | 1TB bandwidth, custom domain |
| **Sentry** (Monitoring) | $26/month | 5K errors/month, 1 project |
| **UptimeRobot** (Alerts) | Free | 50 monitors |
| **Total** | **~$30-50/month** | Good for 50K+ users/month |

---

## Final Steps

1. ✅ Deploy backend to Railway
2. ✅ Deploy frontend to Netlify  
3. ✅ Test all endpoints
4. ✅ Verify CORS configuration
5. ✅ Set up monitoring (Sentry + UptimeRobot)
6. ✅ Configure custom domain (optional)
7. ✅ Update README with live URLs
8. ✅ Submit to NASA Space Apps Challenge! 🚀

---

## Live URLs Template

Add this to your README.md:

```markdown
## 🌐 Live Demo

- **Frontend**: https://is-it-rain.netlify.app
- **Backend API**: https://is-it-rain.railway.app
- **API Docs**: https://is-it-rain.railway.app/docs
- **Model Info**: https://is-it-rain.railway.app/api/model/info

## 🧪 Try It

```bash
# Get ensemble forecast for Tokyo
curl -X POST https://is-it-rain.railway.app/api/forecast/ensemble \
  -H "Content-Type: application/json" \
  -d '{"event_date": "2025-12-25", "query": "Tokyo"}'
```
```

---

**Good luck with your deployment! 🎉**

If you have any issues, check the troubleshooting section or open an issue on GitHub.

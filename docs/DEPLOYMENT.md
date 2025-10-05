# Deployment Guide

This guide provides step-by-step instructions for deploying the "Will It Rain On My Parade?" application to production.

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Local Deployment with Docker](#local-deployment-with-docker)
3. [Cloud Deployment Options](#cloud-deployment-options)
4. [Environment Configuration](#environment-configuration)
5. [Monitoring and Maintenance](#monitoring-and-maintenance)
6. [Troubleshooting](#troubleshooting)

## Prerequisites

- Docker and Docker Compose installed
- Git installed
- Domain name (optional, for production)
- Cloud provider account (AWS, Azure, or Google Cloud)

## Local Deployment with Docker

### Step 1: Clone the Repository

```bash
git clone https://github.com/Nabeel70/Is-It-Rain.git
cd Is-It-Rain
```

### Step 2: Configure Environment Variables

```bash
cd backend
cp .env.example .env
# Edit .env with your preferred settings
```

### Step 3: Build and Run with Docker Compose

```bash
cd ../infra
docker compose up --build
```

The application will be available at:
- Frontend: http://localhost:5173
- Backend API: http://localhost:8000
- API Documentation: http://localhost:8000/docs

## Cloud Deployment Options

### Option 1: Deploy to AWS (ECS + Fargate)

#### Prerequisites
- AWS CLI installed and configured
- AWS account with appropriate permissions

#### Steps

1. **Build and Push Docker Images**

```bash
# Build backend image
docker build -t is-it-rain-api:latest -f Dockerfile --target backend .

# Tag and push to AWS ECR
aws ecr create-repository --repository-name is-it-rain-api
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin <your-account-id>.dkr.ecr.us-east-1.amazonaws.com
docker tag is-it-rain-api:latest <your-account-id>.dkr.ecr.us-east-1.amazonaws.com/is-it-rain-api:latest
docker push <your-account-id>.dkr.ecr.us-east-1.amazonaws.com/is-it-rain-api:latest
```

2. **Create ECS Task Definition**

Create a file `task-definition.json`:

```json
{
  "family": "is-it-rain",
  "networkMode": "awsvpc",
  "requiresCompatibilities": ["FARGATE"],
  "cpu": "256",
  "memory": "512",
  "containerDefinitions": [
    {
      "name": "is-it-rain-api",
      "image": "<your-account-id>.dkr.ecr.us-east-1.amazonaws.com/is-it-rain-api:latest",
      "portMappings": [
        {
          "containerPort": 8000,
          "protocol": "tcp"
        }
      ],
      "environment": [
        {
          "name": "ALLOWED_ORIGINS",
          "value": "https://yourdomain.com"
        },
        {
          "name": "DATABASE_ENABLED",
          "value": "true"
        }
      ],
      "logConfiguration": {
        "logDriver": "awslogs",
        "options": {
          "awslogs-group": "/ecs/is-it-rain",
          "awslogs-region": "us-east-1",
          "awslogs-stream-prefix": "ecs"
        }
      }
    }
  ]
}
```

3. **Register Task Definition and Create Service**

```bash
aws ecs register-task-definition --cli-input-json file://task-definition.json
aws ecs create-service \
  --cluster your-cluster \
  --service-name is-it-rain \
  --task-definition is-it-rain \
  --desired-count 2 \
  --launch-type FARGATE \
  --network-configuration "awsvpcConfiguration={subnets=[subnet-xxx],securityGroups=[sg-xxx],assignPublicIp=ENABLED}"
```

### Option 2: Deploy to Azure (App Service)

```bash
# Login to Azure
az login

# Create resource group
az group create --name is-it-rain-rg --location eastus

# Create App Service plan
az appservice plan create \
  --name is-it-rain-plan \
  --resource-group is-it-rain-rg \
  --is-linux \
  --sku B1

# Create web app
az webapp create \
  --resource-group is-it-rain-rg \
  --plan is-it-rain-plan \
  --name is-it-rain-api \
  --deployment-container-image-name <your-dockerhub-username>/is-it-rain-api:latest

# Configure environment variables
az webapp config appsettings set \
  --resource-group is-it-rain-rg \
  --name is-it-rain-api \
  --settings ALLOWED_ORIGINS=https://yourdomain.com DATABASE_ENABLED=true
```

### Option 3: Deploy to Google Cloud Run

```bash
# Build and push to Google Container Registry
gcloud builds submit --tag gcr.io/your-project-id/is-it-rain-api

# Deploy to Cloud Run
gcloud run deploy is-it-rain-api \
  --image gcr.io/your-project-id/is-it-rain-api \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --set-env-vars ALLOWED_ORIGINS=https://yourdomain.com,DATABASE_ENABLED=true
```

### Option 4: Deploy to Heroku

```bash
# Login to Heroku
heroku login

# Create app
heroku create is-it-rain-api

# Set environment variables
heroku config:set ALLOWED_ORIGINS=https://yourdomain.com
heroku config:set DATABASE_ENABLED=true

# Deploy using container registry
heroku container:login
heroku container:push web -a is-it-rain-api
heroku container:release web -a is-it-rain-api
```

## Environment Configuration

### Production Environment Variables

Create a `.env` file with the following production settings:

```bash
# CORS - Update with your domain
ALLOWED_ORIGINS=https://yourdomain.com,https://www.yourdomain.com

# NASA API
NASA_TIMEOUT=15

# Cache (in seconds)
CACHE_TTL=900

# Rate limiting
RATE_LIMIT_PER_MINUTE=100
RATE_LIMIT_PER_HOUR=5000

# Database
DATABASE_ENABLED=true
DATABASE_PATH=/app/data/forecasts.db

# Logging
LOG_LEVEL=INFO

# Optional: Proxy settings if behind corporate firewall
# HTTP_PROXY=http://proxy.example.com:8080
# HTTPS_PROXY=https://proxy.example.com:8080
```

## Frontend Deployment

### Build for Production

```bash
cd frontend
npm run build
```

The build output will be in `frontend/dist/`. Deploy to:

1. **Cloudflare Pages**
   - Connect your GitHub repository
   - Set build command: `npm run build`
   - Set build output directory: `dist`

2. **Netlify**
   - Connect your GitHub repository
   - Set build command: `npm run build`
   - Set publish directory: `dist`
   - Add environment variable: `VITE_API_BASE=https://your-api-domain.com`

3. **AWS S3 + CloudFront**
```bash
aws s3 sync dist/ s3://your-bucket-name/ --delete
aws cloudfront create-invalidation --distribution-id YOUR_DIST_ID --paths "/*"
```

4. **Serve from Backend Container** (Already configured in Dockerfile)
   - The production Dockerfile copies frontend build to `/app/static`
   - FastAPI serves static files automatically

## Monitoring and Maintenance

### Health Checks

The API provides a health endpoint at `/health`:

```bash
curl https://your-api-domain.com/health
```

Response:
```json
{
  "status": "ok",
  "message": "Is It Rain API is running"
}
```

### Logging

The application uses Loguru for structured logging. Logs include:

- API requests and responses
- NASA POWER API calls
- Database operations
- Errors and exceptions

### Metrics

Access API metrics:

```bash
curl https://your-api-domain.com/api/stats
```

Response:
```json
{
  "total_forecasts": 1234,
  "avg_rain_probability": 0.456,
  "avg_precipitation_mm": 2.34,
  "unique_locations": 567
}
```

### Database Backup

For SQLite database:

```bash
# Backup
docker cp container_name:/app/data/forecasts.db ./backups/forecasts_$(date +%Y%m%d).db

# Restore
docker cp ./backups/forecasts_20251005.db container_name:/app/data/forecasts.db
```

For PostgreSQL (if upgraded):
```bash
pg_dump -h hostname -U username -d database > backup.sql
```

## Troubleshooting

### Issue: API Returns 500 Error

**Solution:**
- Check logs: `docker logs <container-id>`
- Verify environment variables are set correctly
- Ensure NASA POWER API is accessible
- Check date range (API only has historical data up to ~3 days ago)

### Issue: CORS Errors

**Solution:**
- Update `ALLOWED_ORIGINS` in `.env` to include your frontend domain
- Restart the backend container

### Issue: Rate Limiting

**Solution:**
- Adjust `RATE_LIMIT_PER_MINUTE` and `RATE_LIMIT_PER_HOUR` in `.env`
- Consider implementing Redis-based rate limiting for distributed systems

### Issue: Slow Response Times

**Solution:**
- Increase `CACHE_TTL` to reduce NASA API calls
- Scale horizontally with multiple containers
- Add a CDN for frontend assets
- Consider adding Redis for distributed caching

### Issue: Database Lock Errors (SQLite)

**Solution:**
- Upgrade to PostgreSQL for production
- Ensure only one writer at a time
- Increase timeout settings

## Performance Optimization

### Caching Strategy

1. **In-Memory Cache**: Enabled by default (15 minutes TTL)
2. **Redis Cache**: For production at scale

```python
# Update app/core/cache.py
import redis
r = redis.Redis(host='localhost', port=6379, db=0)
```

### CDN Configuration

Use Cloudflare or CloudFront for:
- Static assets
- API caching (with appropriate TTL)
- DDoS protection
- SSL/TLS termination

### Database Optimization

For high-traffic scenarios:

1. **Upgrade to PostgreSQL**:
```bash
pip install psycopg2-binary
# Update database.py to use PostgreSQL connection
```

2. **Add Indexes**:
```sql
CREATE INDEX idx_event_date_location ON forecasts(event_date, latitude, longitude);
CREATE INDEX idx_created_at ON forecasts(created_at DESC);
```

## Security Checklist

- [ ] Environment variables secured (use secrets management)
- [ ] HTTPS enabled (use Let's Encrypt or cloud provider SSL)
- [ ] Rate limiting configured
- [ ] CORS properly configured
- [ ] Database backups automated
- [ ] Monitoring and alerting set up
- [ ] Log rotation configured
- [ ] Security headers added (HSTS, CSP, X-Frame-Options)
- [ ] API authentication (if needed for production)
- [ ] Input validation and sanitization

## Post-Deployment

1. **Test all endpoints**:
```bash
# Health check
curl https://your-domain.com/health

# Forecast
curl -X POST https://your-domain.com/api/forecast \
  -H "Content-Type: application/json" \
  -d '{"event_date": "2025-12-25", "query": "New York"}'
```

2. **Monitor logs for 24 hours**
3. **Set up automated backups**
4. **Configure monitoring alerts**
5. **Document any custom configurations**

## Support

For issues or questions:
- GitHub Issues: https://github.com/Nabeel70/Is-It-Rain/issues
- Documentation: See `docs/` directory
- NASA Space Apps Challenge: https://www.spaceappschallenge.org/

## License

This project was created for the NASA Space Apps Challenge 2025.

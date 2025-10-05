# Deployment Guide

This guide covers deploying the "Will It Rain On My Parade?" application to production environments.

## Prerequisites

- Docker and Docker Compose installed
- Domain name (optional but recommended for production)
- SSL certificate for HTTPS (recommended)
- Cloud provider account (AWS, Azure, GCP, or similar)

## Deployment Options

### Option 1: Docker Compose (Simple Deployment)

This option is suitable for small-scale deployments or testing.

1. **Clone the repository**
   ```bash
   git clone https://github.com/Nabeel70/Is-It-Rain.git
   cd Is-It-Rain
   ```

2. **Configure environment variables**
   ```bash
   cd backend
   cp .env.example .env
   # Edit .env file with your production settings
   ```

   Update the following variables:
   - `ALLOWED_ORIGINS`: Set to your frontend domain (e.g., `["https://yourdomain.com"]`)
   - `NASA_TIMEOUT`: Increase if needed (default: 15 seconds)
   - `CACHE_TTL`: Adjust cache duration (default: 900 seconds = 15 minutes)

3. **Build and run with Docker Compose**
   ```bash
   cd ../infra
   docker compose up --build
   ```

   The application will be available at:
   - Frontend: http://localhost:5173
   - Backend API: http://localhost:8000

### Option 2: Cloud Platform Deployment

#### AWS (Elastic Container Service)

1. **Build the Docker image**
   ```bash
   docker build --target backend -t is-it-rain-api .
   ```

2. **Push to Amazon ECR**
   ```bash
   aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin <your-account-id>.dkr.ecr.us-east-1.amazonaws.com
   docker tag is-it-rain-api:latest <your-account-id>.dkr.ecr.us-east-1.amazonaws.com/is-it-rain-api:latest
   docker push <your-account-id>.dkr.ecr.us-east-1.amazonaws.com/is-it-rain-api:latest
   ```

3. **Create ECS Task Definition**
   - Container image: ECR image URI
   - Port mappings: 8000
   - Environment variables: Set from .env file
   - Health check: `/api/health`

4. **Create ECS Service**
   - Use Application Load Balancer
   - Configure target group pointing to port 8000
   - Set up auto-scaling if needed

5. **Configure CloudFront** (optional)
   - Create distribution for frontend static assets
   - Point to S3 bucket or ECS service

#### Azure (App Service)

1. **Build the Docker image**
   ```bash
   docker build --target backend -t is-it-rain-api .
   ```

2. **Push to Azure Container Registry**
   ```bash
   az acr login --name <your-registry-name>
   docker tag is-it-rain-api:latest <your-registry-name>.azurecr.io/is-it-rain-api:latest
   docker push <your-registry-name>.azurecr.io/is-it-rain-api:latest
   ```

3. **Create App Service**
   ```bash
   az webapp create --resource-group <resource-group> \
     --plan <app-service-plan> \
     --name <app-name> \
     --deployment-container-image-name <your-registry-name>.azurecr.io/is-it-rain-api:latest
   ```

4. **Configure environment variables**
   ```bash
   az webapp config appsettings set --resource-group <resource-group> \
     --name <app-name> \
     --settings ALLOWED_ORIGINS='["https://yourdomain.com"]' \
                 NASA_TIMEOUT=15 \
                 CACHE_TTL=900
   ```

#### Google Cloud (Cloud Run)

1. **Build and push to Google Container Registry**
   ```bash
   gcloud builds submit --tag gcr.io/<project-id>/is-it-rain-api
   ```

2. **Deploy to Cloud Run**
   ```bash
   gcloud run deploy is-it-rain-api \
     --image gcr.io/<project-id>/is-it-rain-api \
     --platform managed \
     --region us-central1 \
     --allow-unauthenticated \
     --set-env-vars ALLOWED_ORIGINS='["https://yourdomain.com"]',NASA_TIMEOUT=15,CACHE_TTL=900
   ```

3. **Configure custom domain** (optional)
   ```bash
   gcloud run domain-mappings create \
     --service is-it-rain-api \
     --domain api.yourdomain.com
   ```

### Option 3: Kubernetes Deployment

For large-scale production deployments, use Kubernetes.

1. **Create Kubernetes manifests** (example provided below)

2. **Apply manifests**
   ```bash
   kubectl apply -f k8s/
   ```

Example Kubernetes deployment:

```yaml
# deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: is-it-rain-api
spec:
  replicas: 3
  selector:
    matchLabels:
      app: is-it-rain-api
  template:
    metadata:
      labels:
        app: is-it-rain-api
    spec:
      containers:
      - name: api
        image: your-registry/is-it-rain-api:latest
        ports:
        - containerPort: 8000
        env:
        - name: ALLOWED_ORIGINS
          value: '["https://yourdomain.com"]'
        - name: NASA_TIMEOUT
          value: "15"
        - name: CACHE_TTL
          value: "900"
        livenessProbe:
          httpGet:
            path: /api/health
            port: 8000
          initialDelaySeconds: 30
          periodSeconds: 10
        readinessProbe:
          httpGet:
            path: /api/health
            port: 8000
          initialDelaySeconds: 5
          periodSeconds: 5
---
apiVersion: v1
kind: Service
metadata:
  name: is-it-rain-api-service
spec:
  selector:
    app: is-it-rain-api
  ports:
  - protocol: TCP
    port: 80
    targetPort: 8000
  type: LoadBalancer
```

## Production Configuration

### Environment Variables

| Variable | Description | Default | Production Value |
|----------|-------------|---------|------------------|
| `ALLOWED_ORIGINS` | CORS allowed origins (JSON array) | `["http://localhost:5173"]` | `["https://yourdomain.com"]` |
| `NASA_TIMEOUT` | Timeout for NASA API calls (seconds) | `15` | `20-30` (increase for reliability) |
| `CACHE_TTL` | Cache duration (seconds) | `900` | `900-1800` (adjust based on needs) |
| `HTTP_PROXY` | HTTP proxy URL (optional) | - | Set if behind corporate proxy |
| `HTTPS_PROXY` | HTTPS proxy URL (optional) | - | Set if behind corporate proxy |

### Security Best Practices

1. **HTTPS Only**
   - Always use HTTPS in production
   - Configure SSL/TLS certificates
   - Use a reverse proxy (nginx, Cloudflare)

2. **CORS Configuration**
   - Restrict `ALLOWED_ORIGINS` to your domain only
   - Never use `*` in production

3. **Rate Limiting**
   - Implement rate limiting at the API gateway level
   - Protect against abuse of NASA POWER and OpenStreetMap APIs
   - Recommended: 100 requests/minute per IP

4. **Monitoring**
   - Set up health check monitoring
   - Configure alerts for API failures
   - Monitor NASA API quota usage

5. **Secrets Management**
   - Never commit `.env` file to version control
   - Use cloud provider secret management (AWS Secrets Manager, Azure Key Vault, etc.)
   - Rotate secrets regularly

### Reverse Proxy Configuration (nginx)

Example nginx configuration:

```nginx
upstream backend {
    server 127.0.0.1:8000;
}

server {
    listen 443 ssl http2;
    server_name api.yourdomain.com;

    ssl_certificate /path/to/cert.pem;
    ssl_certificate_key /path/to/key.pem;

    # Security headers
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-XSS-Protection "1; mode=block" always;

    # Rate limiting
    limit_req_zone $binary_remote_addr zone=api_limit:10m rate=100r/m;
    limit_req zone=api_limit burst=20 nodelay;

    location / {
        proxy_pass http://backend;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    location /api/health {
        proxy_pass http://backend;
        access_log off;
    }
}
```

## Scaling Considerations

### Horizontal Scaling

For high traffic, consider:

1. **Load Balancer**
   - Distribute traffic across multiple instances
   - Use health checks to remove unhealthy instances

2. **Redis Cache** (instead of in-memory cache)
   - Replace `app/core/cache.py` with Redis client
   - Enables cache sharing across instances

3. **CDN**
   - Serve frontend static assets from CDN
   - Cache API responses at edge locations

4. **Database** (optional)
   - Store forecast history
   - Enable analytics and reporting

### Performance Optimization

1. **Caching Strategy**
   - Cache NASA API responses (15 minutes default)
   - Cache geocoding results
   - Use CDN for static assets

2. **Connection Pooling**
   - Configure httpx connection pooling
   - Reuse connections to external APIs

3. **Async Processing**
   - Already using FastAPI async/await
   - Consider background tasks for heavy processing

## Monitoring and Observability

### Health Checks

The API provides a health check endpoint:

```bash
curl https://api.yourdomain.com/api/health
```

Expected response:
```json
{
  "status": "ok",
  "timestamp": "2025-10-05T10:00:00Z"
}
```

### Logging

Configure structured logging in production:

1. **Application Logs**
   - FastAPI/uvicorn logs
   - Custom application logs (using loguru)

2. **Access Logs**
   - HTTP request logs
   - Response times
   - Error rates

3. **External API Logs**
   - NASA POWER API calls
   - OpenStreetMap API calls
   - Success/failure rates

### Metrics

Key metrics to monitor:

- Request rate (requests/second)
- Response time (p50, p95, p99)
- Error rate (5xx responses)
- Cache hit rate
- External API response times
- NASA API quota usage

### Alerting

Set up alerts for:

- API downtime (health check failures)
- High error rates (> 1%)
- Slow response times (> 5 seconds)
- External API failures
- Resource exhaustion (CPU, memory)

## Troubleshooting

### Common Issues

1. **CORS Errors**
   - Check `ALLOWED_ORIGINS` configuration
   - Ensure frontend domain is included
   - Verify format is JSON array: `["https://domain.com"]`

2. **NASA API Timeouts**
   - Increase `NASA_TIMEOUT` setting
   - Check NASA POWER API status
   - Verify network connectivity

3. **Geocoding Failures**
   - OpenStreetMap Nominatim may rate limit
   - Consider caching geocoding results
   - Implement retry logic

4. **Cache Issues**
   - For multi-instance deployments, use Redis
   - Check cache TTL settings
   - Monitor cache memory usage

### Debug Mode

To run in debug mode:

```bash
export LOG_LEVEL=DEBUG
uvicorn app.main:app --reload --log-level debug
```

## Backup and Recovery

### Data Backup

Since the application is stateless (using external APIs):

1. **Configuration Backup**
   - Back up `.env` file securely
   - Version control all code and configs

2. **Cache Backup** (if using Redis)
   - Configure Redis persistence
   - Regular snapshots

### Disaster Recovery

1. **Multi-Region Deployment**
   - Deploy to multiple regions
   - Use global load balancer

2. **Failover Strategy**
   - Active-passive or active-active
   - Automatic failover for critical components

## Cost Optimization

1. **API Usage**
   - NASA POWER API is free (no quotas)
   - OpenStreetMap Nominatim is free (rate limited)
   - Implement caching to reduce external API calls

2. **Infrastructure**
   - Use auto-scaling to match demand
   - Consider serverless options (Cloud Run, Lambda)
   - Use spot instances for non-critical workloads

3. **Monitoring**
   - Use free tier monitoring services
   - Set up cost alerts

## Compliance and Legal

1. **Data Privacy**
   - No user data is stored permanently
   - Comply with GDPR/CCPA if applicable

2. **API Terms of Service**
   - Review NASA POWER API terms
   - Follow OpenStreetMap usage policy
   - Add rate limiting to respect API limits

3. **Attribution**
   - Credit NASA POWER (GPM IMERG) dataset
   - Credit OpenStreetMap contributors
   - Include in footer/about page

## Support and Maintenance

### Regular Maintenance

1. **Dependencies**
   - Update Python and Node.js dependencies monthly
   - Check for security vulnerabilities
   - Test updates in staging before production

2. **API Changes**
   - Monitor NASA POWER API for changes
   - Subscribe to API change notifications
   - Test API compatibility regularly

3. **Performance Review**
   - Review metrics monthly
   - Optimize slow endpoints
   - Adjust caching strategy as needed

### Support Resources

- **NASA POWER API**: https://power.larc.nasa.gov/
- **OpenStreetMap Nominatim**: https://nominatim.org/
- **Project Repository**: https://github.com/Nabeel70/Is-It-Rain
- **Issues**: Report bugs via GitHub Issues

## Deployment Checklist

- [ ] Environment variables configured
- [ ] HTTPS enabled and tested
- [ ] CORS configured correctly
- [ ] Health checks working
- [ ] Monitoring and alerting set up
- [ ] Rate limiting configured
- [ ] Backups configured
- [ ] Security headers added
- [ ] Documentation updated
- [ ] Load testing completed
- [ ] Disaster recovery plan documented
- [ ] Team trained on operations

## Next Steps

After deployment:

1. Monitor application for first 24-48 hours
2. Verify all features work correctly
3. Test with real user scenarios
4. Gather feedback and iterate
5. Plan for scaling if needed

For additional help, refer to the main [README.md](../README.md) or open an issue on GitHub.

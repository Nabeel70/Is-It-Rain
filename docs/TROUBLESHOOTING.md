# Troubleshooting Guide

This guide helps you diagnose and fix common issues with the "Will It Rain On My Parade?" application.

## Table of Contents

- [Quick Diagnostics](#quick-diagnostics)
- [Backend Issues](#backend-issues)
- [Frontend Issues](#frontend-issues)
- [External API Issues](#external-api-issues)
- [Docker Issues](#docker-issues)
- [Performance Issues](#performance-issues)
- [Production Issues](#production-issues)

## Quick Diagnostics

### Health Check

Run these commands to verify system status:

```bash
# 1. Check backend health
curl http://localhost:8000/api/health

# Expected: {"status":"ok","timestamp":"..."}

# 2. Test forecast endpoint
curl -X POST http://localhost:8000/api/forecast \
  -H "Content-Type: application/json" \
  -d '{"event_date":"2025-10-05","query":"New York City"}'

# 3. Check frontend
# Open http://localhost:5173 in browser
# Should see the application UI

# 4. Check Docker containers
docker compose ps

# Expected: Both api and frontend containers running
```

### Log Files

Check logs for errors:

```bash
# Backend logs (if running manually)
cd backend
poetry run uvicorn app.main:app --log-level debug

# Frontend logs (if running manually)
cd frontend
npm run dev

# Docker logs
docker compose logs api
docker compose logs frontend
docker compose logs -f  # Follow mode
```

## Backend Issues

### Issue 1: Server Won't Start

**Symptoms**:
- `uvicorn` command fails
- Import errors
- Module not found errors

**Causes & Solutions**:

1. **Dependencies not installed**
   ```bash
   cd backend
   poetry install
   ```

2. **Wrong Python version**
   ```bash
   python --version  # Should be 3.11+
   poetry env use python3.11
   poetry install
   ```

3. **Environment file missing**
   ```bash
   cd backend
   cp .env.example .env
   ```

4. **Port already in use**
   ```bash
   # Find process using port 8000
   lsof -i :8000
   
   # Kill process
   kill -9 <PID>
   
   # Or use different port
   poetry run uvicorn app.main:app --port 8001
   ```

### Issue 2: ALLOWED_ORIGINS Error

**Symptoms**:
```
SettingsError: error parsing value for field "allowed_origins"
```

**Cause**: Invalid format in .env file

**Solution**:
```bash
# Incorrect ❌
ALLOWED_ORIGINS=http://localhost:5173

# Correct ✅
ALLOWED_ORIGINS=["http://localhost:5173"]

# Multiple origins ✅
ALLOWED_ORIGINS=["http://localhost:5173","https://yourdomain.com"]
```

### Issue 3: Import Errors

**Symptoms**:
```
ModuleNotFoundError: No module named 'app'
```

**Solution**:
```bash
cd backend
poetry install
# Make sure you're in the backend directory when running uvicorn
poetry run uvicorn app.main:app --reload
```

### Issue 4: Database/Cache Errors

**Symptoms**:
- Cache warnings
- "Connection refused" errors

**Solution**:

The app uses in-memory caching by default (no database required). If you see cache errors:

```bash
# Restart the server to clear cache
# Or adjust CACHE_TTL in .env
CACHE_TTL=900  # 15 minutes
```

### Issue 5: Tests Failing

**Symptoms**:
```bash
poetry run pytest
# Tests fail
```

**Solutions**:

1. **Check Python version**
   ```bash
   python --version  # Must be 3.11+
   ```

2. **Reinstall dependencies**
   ```bash
   poetry install
   ```

3. **Check test database**
   ```bash
   # Tests should work without external dependencies
   # If mocking is broken:
   poetry install --with dev
   ```

4. **Run with verbose output**
   ```bash
   poetry run pytest -v
   poetry run pytest --tb=short  # Short traceback
   ```

## Frontend Issues

### Issue 1: npm install Fails

**Symptoms**:
- Dependency resolution errors
- Package conflicts

**Solutions**:

1. **Clear cache and retry**
   ```bash
   cd frontend
   rm -rf node_modules package-lock.json
   npm cache clean --force
   npm install
   ```

2. **Use legacy peer deps**
   ```bash
   npm install --legacy-peer-deps
   ```

3. **Check Node version**
   ```bash
   node --version  # Should be 20+
   npm --version   # Should be 10+
   ```

### Issue 2: Build Fails

**Symptoms**:
```bash
npm run build
# Errors during build
```

**Solutions**:

1. **TypeScript errors**
   ```bash
   # Check for type errors
   npm run lint
   
   # Fix auto-fixable issues
   npx eslint . --ext ts,tsx --fix
   ```

2. **Memory issues**
   ```bash
   # Increase Node memory
   NODE_OPTIONS=--max_old_space_size=4096 npm run build
   ```

3. **Clean rebuild**
   ```bash
   rm -rf dist node_modules
   npm install
   npm run build
   ```

### Issue 3: Development Server Issues

**Symptoms**:
- Hot reload not working
- Changes not reflected
- Port conflicts

**Solutions**:

1. **Port already in use**
   ```bash
   # Change port in vite.config.ts
   server: {
     port: 5174  // Use different port
   }
   ```

2. **Hard refresh**
   ```bash
   # In browser: Ctrl+Shift+R (Windows/Linux) or Cmd+Shift+R (Mac)
   ```

3. **Clear Vite cache**
   ```bash
   rm -rf node_modules/.vite
   npm run dev
   ```

### Issue 4: API Connection Errors

**Symptoms**:
- Network errors in console
- CORS errors
- API calls failing

**Solutions**:

1. **CORS Configuration**
   - Check backend `.env` file
   - Ensure `ALLOWED_ORIGINS` includes `http://localhost:5173`
   - Restart backend after changes

2. **Proxy Configuration**
   - Verify `vite.config.ts` proxy settings:
   ```typescript
   server: {
     proxy: {
       '/api': {
         target: 'http://localhost:8000',
         changeOrigin: true
       }
     }
   }
   ```

3. **Backend not running**
   ```bash
   # Start backend if not running
   cd backend
   poetry run uvicorn app.main:app --reload
   ```

## External API Issues

### Issue 1: NASA POWER API Errors

**Symptoms**:
- 500 errors when requesting forecast
- Timeout errors
- "Could not fetch data" messages

**Solutions**:

1. **Check API Status**
   ```bash
   # Test NASA POWER API directly
   curl "https://power.larc.nasa.gov/api/temporal/daily/point?parameters=PRECTOTCORR&community=RE&longitude=-74.0060&latitude=40.7128&start=20251005&end=20251005&format=JSON"
   ```

2. **Increase Timeout**
   ```bash
   # In .env file
   NASA_TIMEOUT=30  # Increase from default 15
   ```

3. **Check Network/Firewall**
   - Verify outbound HTTPS is allowed
   - Check if behind corporate proxy
   - Set HTTP_PROXY/HTTPS_PROXY if needed:
   ```bash
   HTTP_PROXY=http://proxy.company.com:8080
   HTTPS_PROXY=http://proxy.company.com:8080
   ```

4. **Date Issues**
   - NASA POWER has 2-3 month lag for final data
   - Try dates from 3+ months ago for best results
   - Recent dates may return provisional data

### Issue 2: Geocoding Errors

**Symptoms**:
- "Unable to geocode query" errors
- Location not found
- 404 responses

**Solutions**:

1. **Be More Specific**
   ```bash
   # ❌ Too vague
   "NYC"
   
   # ✅ Specific
   "New York City, NY, USA"
   "Times Square, Manhattan, New York"
   ```

2. **Use Coordinates**
   ```bash
   # Instead of location name, use exact coordinates
   curl -X POST http://localhost:8000/api/forecast \
     -H "Content-Type: application/json" \
     -d '{
       "event_date": "2025-10-05",
       "location": {
         "latitude": 40.7128,
         "longitude": -74.0060,
         "name": "New York City"
       }
     }'
   ```

3. **Rate Limiting**
   - OpenStreetMap Nominatim limits to 1 req/sec
   - Wait a few seconds between requests
   - Consider caching geocoding results

4. **Check Nominatim Status**
   ```bash
   # Test directly
   curl "https://nominatim.openstreetmap.org/search?format=json&q=London"
   ```

### Issue 3: Rate Limiting

**Symptoms**:
- 429 Too Many Requests
- Temporary blocks
- Slow responses

**Solutions**:

1. **Respect Rate Limits**
   - NASA POWER: No official limit (be reasonable)
   - OpenStreetMap: Max 1 request/second
   - Implement delays between requests

2. **Use Caching**
   - Default cache: 15 minutes
   - Adjust CACHE_TTL if needed
   - Cache reduces external API calls

3. **Implement Backoff**
   - Add exponential backoff for retries
   - Wait longer between failed attempts

## Docker Issues

### Issue 1: Build Fails

**Symptoms**:
```bash
docker compose up --build
# Build errors
```

**Solutions**:

1. **Network Issues**
   ```bash
   # Check Docker network
   docker network ls
   
   # Prune unused networks
   docker network prune
   ```

2. **Cache Issues**
   ```bash
   # Build without cache
   docker compose build --no-cache
   ```

3. **Disk Space**
   ```bash
   # Check disk space
   df -h
   
   # Clean Docker resources
   docker system prune -a
   ```

### Issue 2: Containers Won't Start

**Symptoms**:
- Containers exit immediately
- Health check failures

**Solutions**:

1. **Check Logs**
   ```bash
   docker compose logs api
   docker compose logs frontend
   ```

2. **Environment Variables**
   ```bash
   # Verify .env file exists and is correct
   cat backend/.env
   ```

3. **Port Conflicts**
   ```bash
   # Change ports in docker-compose.yml
   ports:
     - '8001:8000'  # Use different host port
   ```

### Issue 3: Can't Access Services

**Symptoms**:
- Browser can't connect to localhost:5173 or localhost:8000
- Connection refused errors

**Solutions**:

1. **Check Container Status**
   ```bash
   docker compose ps
   # Should show containers as "Up"
   ```

2. **Check Port Mappings**
   ```bash
   docker compose ps
   # Verify port mappings are correct
   ```

3. **Restart Containers**
   ```bash
   docker compose down
   docker compose up
   ```

4. **Check Firewall**
   - Ensure localhost ports are not blocked
   - Try accessing from container IP directly

## Performance Issues

### Issue 1: Slow API Responses

**Symptoms**:
- Requests take >5 seconds
- Timeouts

**Solutions**:

1. **First Request (Cold Start)**
   - First request fetches from NASA API (~2-5 seconds)
   - Subsequent requests use cache (~50ms)
   - This is expected behavior

2. **Cache Not Working**
   ```bash
   # Verify cache is enabled
   # Check CACHE_TTL in .env
   CACHE_TTL=900  # 15 minutes
   ```

3. **Network Latency**
   - Check internet connection speed
   - Try different NASA API endpoint
   - Increase timeout: `NASA_TIMEOUT=30`

4. **Server Resources**
   ```bash
   # Check CPU/memory usage
   top
   # Or with Docker:
   docker stats
   ```

### Issue 2: High Memory Usage

**Symptoms**:
- Application using excessive memory
- OOM (out of memory) errors

**Solutions**:

1. **Cache Size**
   - Default cache holds 256 entries
   - Reduce if needed in `backend/app/core/cache.py`

2. **Docker Memory Limits**
   ```yaml
   # In docker-compose.yml
   services:
     api:
       deploy:
         resources:
           limits:
             memory: 512M
   ```

3. **Restart Periodically**
   - For long-running instances
   - Clears in-memory cache

### Issue 3: Database Connection Pool Exhausted

**Symptoms**:
- "Too many connections" errors

**Note**: This app doesn't use a database by default. If you added one:

**Solutions**:
- Increase connection pool size
- Implement connection pooling properly
- Use connection timeout/recycling

## Production Issues

### Issue 1: HTTPS/SSL Issues

**Symptoms**:
- Certificate errors
- Mixed content warnings
- HTTPS not working

**Solutions**:

1. **Configure Reverse Proxy**
   - Use nginx, Cloudflare, or cloud load balancer
   - Terminate SSL at proxy level
   - See DEPLOYMENT.md for nginx example

2. **Update ALLOWED_ORIGINS**
   ```bash
   # Use HTTPS in production
   ALLOWED_ORIGINS=["https://yourdomain.com"]
   ```

3. **Check Certificate**
   ```bash
   # Test SSL certificate
   openssl s_client -connect yourdomain.com:443
   ```

### Issue 2: CORS Errors in Production

**Symptoms**:
- Frontend can't access API
- Access-Control-Allow-Origin errors

**Solutions**:

1. **Update Backend .env**
   ```bash
   # Add production domain
   ALLOWED_ORIGINS=["https://yourdomain.com","https://www.yourdomain.com"]
   ```

2. **Verify Headers**
   ```bash
   # Check CORS headers
   curl -I https://api.yourdomain.com/api/health \
     -H "Origin: https://yourdomain.com"
   ```

3. **Restart Services**
   - Changes to .env require restart
   - Restart backend service

### Issue 3: Monitoring/Alerting

**Symptoms**:
- No visibility into errors
- Can't diagnose production issues

**Solutions**:

1. **Set Up Health Checks**
   ```bash
   # Monitor /api/health endpoint
   */5 * * * * curl -f http://api.yourdomain.com/api/health || alert
   ```

2. **Application Logs**
   - Configure centralized logging
   - Use ELK stack, CloudWatch, or similar
   - Monitor error rates

3. **External Monitoring**
   - Use UptimeRobot, Pingdom, or similar
   - Monitor both frontend and API
   - Set up alerts for downtime

### Issue 4: High Load

**Symptoms**:
- Slow responses under load
- Timeouts during peak traffic

**Solutions**:

1. **Horizontal Scaling**
   - Deploy multiple instances
   - Use load balancer
   - Switch to Redis for shared cache

2. **Caching Strategy**
   - Increase CACHE_TTL
   - Add CDN for static assets
   - Cache at API gateway level

3. **Rate Limiting**
   - Implement at reverse proxy level
   - Protect against abuse
   - See DEPLOYMENT.md for examples

## Getting Additional Help

### Before Asking for Help

1. **Check Documentation**
   - [README.md](../README.md)
   - [QUICKSTART.md](QUICKSTART.md)
   - [API.md](API.md)
   - [DEPLOYMENT.md](DEPLOYMENT.md)

2. **Search Issues**
   - Check [GitHub Issues](https://github.com/Nabeel70/Is-It-Rain/issues)
   - Someone may have had the same problem

3. **Gather Information**
   - Error messages (full text)
   - Steps to reproduce
   - Environment details (OS, versions)
   - Relevant logs

### How to Report Issues

**Create a GitHub Issue** with:

```markdown
**Environment**:
- OS: Ubuntu 22.04
- Python: 3.11.5
- Node: 20.10.0
- Docker: 24.0.7 (if applicable)

**Problem**:
Clear description of the issue

**Steps to Reproduce**:
1. Step one
2. Step two
3. Step three

**Expected Behavior**:
What should happen

**Actual Behavior**:
What actually happens

**Error Messages**:
```
Paste full error message here
```

**Additional Context**:
Any other relevant information
```

### Support Channels

- **GitHub Issues**: https://github.com/Nabeel70/Is-It-Rain/issues
- **GitHub Discussions**: https://github.com/Nabeel70/Is-It-Rain/discussions

### Emergency Contacts

For security issues or critical bugs:
- Do NOT create public issues
- Contact maintainers directly via GitHub

---

**Can't find your issue?** Open a [new issue](https://github.com/Nabeel70/Is-It-Rain/issues/new) with details!

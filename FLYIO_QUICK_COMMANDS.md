# Quick Fly.io Commands - Cheat Sheet

## Installation (One-time)
```bash
curl -L https://fly.io/install.sh | sh
export FLYCTL_INSTALL="/home/codespace/.fly"
export PATH="$FLYCTL_INSTALL/bin:$PATH"
flyctl auth signup  # or: flyctl auth login
```

## Deploy Both Services
```bash
cd /workspaces/Is-It-Rain

# Backend
flyctl launch --config fly.backend.toml --name is-it-rain-api --no-deploy
flyctl deploy --config fly.backend.toml

# Frontend
flyctl launch --config fly.frontend.toml --name is-it-rain-frontend --no-deploy
flyctl deploy --config fly.frontend.toml

# Set CORS
flyctl secrets set ALLOWED_ORIGINS="https://is-it-rain-frontend.fly.dev,http://localhost:5173" --config fly.backend.toml
```

## Test
```bash
curl https://is-it-rain-api.fly.dev/health
flyctl open --config fly.frontend.toml
```

## Useful Commands
```bash
# Check status
flyctl status --config fly.backend.toml

# View logs
flyctl logs --config fly.backend.toml -f

# Restart
flyctl apps restart is-it-rain-api

# Dashboard
flyctl dashboard

# SSH into VM
flyctl ssh console --config fly.backend.toml
```

## Your URLs
- Frontend: https://is-it-rain-frontend.fly.dev
- Backend: https://is-it-rain-api.fly.dev
- Docs: https://is-it-rain-api.fly.dev/docs

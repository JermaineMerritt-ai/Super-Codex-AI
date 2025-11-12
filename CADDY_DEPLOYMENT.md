# Caddy Deployment Guide for Super-Codex-AI

## Current Configuration

The `Caddyfile` is configured with:

```
your-domain.com {
  encode gzip
  handle_path /api* { reverse_proxy 127.0.0.1:8010 }
  handle_path /ws*  { reverse_proxy 127.0.0.1:8010 }
  handle { reverse_proxy 127.0.0.1:3001 }
}
```

## Configuration Breakdown

- **`your-domain.com`**: Replace with your actual domain
- **`encode gzip`**: Enables compression for all responses
- **`/api*`**: Routes API requests to FastAPI backend (port 8010)
- **`/ws*`**: Routes WebSocket connections to backend (port 8010) 
- **`handle`**: Routes all other requests to React frontend (port 3001)

## Before Deployment

### 1. Update Domain Name
Replace `your-domain.com` with your actual domain:
```
mydomain.com {
  # ... rest of config
}
```

### 2. Verify Service Ports
Ensure your services are running on the correct ports:
- **Backend API**: `127.0.0.1:8010` (FastAPI with AXIOM routes)
- **Frontend**: `127.0.0.1:3001` (React development server or built app)

### 3. Start Required Services

#### Backend (FastAPI)
```powershell
# Activate virtual environment
.\.venv\Scripts\Activate.ps1

# Start the unified API server
python -m uvicorn app.main:app --host 127.0.0.1 --port 8010 --reload
```

#### Frontend (React)
```powershell
# Navigate to frontend directory
cd frontend

# Install dependencies (if not done)
npm install

# Start development server on port 3001
$env:PORT=3001; npm start

# Or serve built app with serve
npm run build
npx serve -s build -l 3001
```

## Caddy Installation & Usage

### Install Caddy (Windows)
```powershell
# Using Chocolatey
choco install caddy

# Or download from https://caddyserver.com/download
```

### Start Caddy
```powershell
# Navigate to project root (where Caddyfile is located)
cd C:\Users\JMerr\OneDrive\Documents\.vscode\codex_project\backend\services\dominion\Super-Codex-AI

# Start Caddy (will auto-generate SSL certificates)
caddy run

# Or run in background
caddy start
```

### Stop Caddy
```powershell
caddy stop
```

## DNS Configuration

Point your domain to the server running Caddy:
- **A Record**: `your-domain.com` → `YOUR_SERVER_IP`
- **CNAME Record**: `www.your-domain.com` → `your-domain.com`

## SSL/TLS

Caddy automatically:
- Obtains SSL certificates from Let's Encrypt
- Redirects HTTP to HTTPS
- Handles certificate renewal

## Testing the Configuration

1. **Health Check**:
   ```
   curl https://your-domain.com/api/health
   ```

2. **Frontend**:
   ```
   curl https://your-domain.com
   ```

3. **AXIOM API** (requires authentication):
   ```
   curl -H "Authorization: Bearer YOUR_TOKEN" \
        -H "X-API-Key: YOUR_API_KEY" \
        https://your-domain.com/api/axiom/health
   ```

## Troubleshooting

### Check Caddy Status
```powershell
caddy list-licenses
caddy validate --config Caddyfile
```

### Check Service Connectivity
```powershell
# Test backend directly
curl http://127.0.0.1:8010/health

# Test frontend directly  
curl http://127.0.0.1:3001
```

### Common Issues

1. **Port conflicts**: Ensure ports 8010 and 3001 are available
2. **DNS propagation**: Wait for DNS changes to propagate (up to 24 hours)
3. **Firewall**: Ensure ports 80 and 443 are open on your server
4. **Service not running**: Verify both backend and frontend are running

## Production Considerations

### 1. Environment Variables
Set production environment variables:
```powershell
$env:NODE_ENV="production"
$env:FASTAPI_ENV="production"
```

### 2. Process Management
Use a process manager to keep services running:
- **PM2** for Node.js apps
- **systemd** for Linux services
- **Windows Service** for Windows

### 3. Monitoring
Monitor your services:
- Caddy access logs: `/var/log/caddy/`
- Application logs
- Health check endpoints

## Security Headers (Optional)

For enhanced security, you can add headers to the Caddyfile:

```
your-domain.com {
  encode gzip
  
  # Security headers
  header {
    Strict-Transport-Security max-age=31536000;
    X-Content-Type-Options nosniff
    X-XSS-Protection "1; mode=block" 
    X-Frame-Options DENY
  }
  
  handle_path /api* { reverse_proxy 127.0.0.1:8010 }
  handle_path /ws*  { reverse_proxy 127.0.0.1:8010 }
  handle { reverse_proxy 127.0.0.1:3001 }
}
```

## Load Balancing (Optional)

For multiple backend instances:

```
your-domain.com {
  encode gzip
  handle_path /api* {
    reverse_proxy 127.0.0.1:8010 127.0.0.1:8011 127.0.0.1:8012
  }
  handle_path /ws*  { reverse_proxy 127.0.0.1:8010 }
  handle { reverse_proxy 127.0.0.1:3001 }
}
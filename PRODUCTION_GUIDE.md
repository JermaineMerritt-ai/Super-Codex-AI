# 🏭 Production Integration Guide
## Unified Artifact Management System

This guide shows how to integrate the unified artifact system with your production environment, including custom base URLs, authentication schemes, and webhook integrations.

## 🚀 Quick Start

### 1. Configuration Setup

Copy the sample configuration and update with your values:

```bash
python deploy.py --create-sample-config
cp production.env.sample production.env
# Edit production.env with your actual values
```

### 2. Install Dependencies

```bash
python deploy.py --install-deps
```

### 3. Deploy to Production

```bash
python deploy.py --env production --config-file production.env --start-server
```

## 🔧 Configuration Options

### Authentication Schemes

#### Bearer Token Authentication
```env
CODEX_AUTH_SCHEME=bearer
```
- Use `Authorization: Bearer YOUR_TOKEN` header
- Best for API integrations

#### API Key Authentication  
```env
CODEX_AUTH_SCHEME=api_key
CODEX_API_KEY_HEADER=X-Your-API-Key
```
- Use custom header: `X-Your-API-Key: YOUR_KEY`
- Simple and secure

#### OAuth2 Authentication
```env
CODEX_AUTH_SCHEME=oauth2
```
- Full OAuth2 flow with scopes
- Enterprise-grade security

#### SIGIL Seal Authentication
```env
CODEX_AUTH_SCHEME=sigil_seal
```
- Custom Codex Dominion seal system
- Hierarchical authority verification

### Base URL Configuration

Update these with your actual domains:

```env
# Your API domain
CODEX_API_BASE_URL=https://api.your-domain.com

# Your main web application
CODEX_WEB_BASE_URL=https://your-domain.com

# Council portal for governance
CODEX_COUNCIL_PORTAL_URL=https://council.your-domain.com

# Public portal for community access
CODEX_PUBLIC_PORTAL_URL=https://public.your-domain.com
```

## 🔗 Webhook Integration

The system automatically sends notifications to your portals when artifacts are registered, dispatched, or performed.

### Required Webhook Endpoints

#### 1. Council Portal Notifications
```
POST https://council.your-domain.com/api/notifications
```

**Example Implementation:**
```python
from fastapi import FastAPI

app = FastAPI()

@app.post("/api/notifications")
async def receive_artifact_notification(payload: dict):
    action = payload.get("action")
    artifact = payload.get("artifact", {})
    
    if action == "artifact_registered":
        # Update council dashboard
        await update_council_dashboard(artifact)
    elif action == "artifact_dispatched":
        # Send council alerts
        await send_council_alerts(artifact)
    elif action == "artifact_performed":
        # Log performance for governance
        await log_artifact_performance(artifact)
    
    return {"status": "received"}
```

#### 2. Public Portal Broadcasts
```
POST https://public.your-domain.com/api/broadcasts
```

**Example Implementation:**
```python
@app.post("/api/broadcasts")
async def receive_artifact_broadcast(payload: dict):
    artifact = payload.get("artifact", {})
    
    # Only process public artifacts
    if "public" in artifact.get("audience", []):
        # Update public displays
        await update_public_displays(artifact)
        
        # Send community notifications
        await send_community_notifications(artifact)
    
    return {"status": "received"}
```

#### 3. Replay Archive Webhook
```
POST https://api.your-domain.com/webhooks/replay
```

**Example Implementation:**
```python
@app.post("/webhooks/replay")
async def receive_replay_notification(payload: dict):
    artifact = payload.get("artifact", {})
    
    # Archive for historical replay
    await archive_artifact_event(artifact, payload.get("action"))
    
    # Trigger replay analysis
    await trigger_replay_analysis(artifact)
    
    return {"status": "archived"}
```

### Webhook Payload Format

All webhooks receive this standardized payload:

```json
{
  "action": "artifact_registered|artifact_dispatched|artifact_performed",
  "artifact": {
    "id": "artifact-unique-id",
    "title": "Artifact Title",
    "type": "charter|hymn|decree|manifesto|covenant",
    "timestamp": "2025-11-13T08:00:00Z",
    "audience": ["councils", "public", "custodians"],
    "cycles": ["epochal", "seasonal"]
  },
  "source": "unified-artifact-system",
  "environment": "production|staging|development"
}
```

## 🔐 Security Configuration

### Signature Verification

Enable signature verification for production:

```env
CODEX_SIGNATURE_VERIFICATION=true
```

**Verify signatures in your webhooks:**
```python
import hmac
import hashlib

def verify_webhook_signature(payload: dict, signature: str, secret: str) -> bool:
    expected = hmac.new(
        secret.encode(),
        json.dumps(payload, sort_keys=True).encode(),
        hashlib.sha256
    ).hexdigest()
    
    return hmac.compare_digest(signature, expected)

@app.post("/api/notifications")
async def receive_notification(request: Request, payload: dict):
    # Verify signature
    signature = request.headers.get("X-Codex-Signature", "").replace("sha256=", "")
    if not verify_webhook_signature(payload, signature, YOUR_SECRET):
        raise HTTPException(status_code=401, detail="Invalid signature")
    
    # Process notification
    return {"status": "received"}
```

### Rate Limiting

Configure rate limits per environment:

```env
# Production: Conservative limits
CODEX_RATE_LIMIT_PER_MINUTE=100

# Staging: Higher limits for testing
CODEX_RATE_LIMIT_PER_MINUTE=200

# Development: Unlimited
CODEX_RATE_LIMIT_PER_MINUTE=1000
```

## 🌐 Portal-Specific Routes

The system provides different access levels for different portals:

### Council Portal Routes
- **Base Path**: `/council/api/v1/`
- **Permissions**: Full read/write access
- **Authentication**: Council authority required
- **Rate Limit**: 200/minute

### Public Portal Routes  
- **Base Path**: `/public/api/v1/`
- **Permissions**: Read-only access to public artifacts
- **Authentication**: None required
- **Rate Limit**: 50/minute

### Admin Routes
- **Base Path**: `/admin/api/v1/`
- **Permissions**: Full system access
- **Authentication**: Supreme authority required
- **Rate Limit**: 500/minute

## 📦 Deployment Examples

### Docker Deployment

```dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
EXPOSE 8004

CMD ["python", "deploy.py", "--env", "production", "--start-server"]
```

### Kubernetes Deployment

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: unified-artifact-system
spec:
  replicas: 3
  selector:
    matchLabels:
      app: unified-artifact-system
  template:
    metadata:
      labels:
        app: unified-artifact-system
    spec:
      containers:
      - name: artifact-system
        image: your-registry/unified-artifact-system:latest
        ports:
        - containerPort: 8004
        env:
        - name: CODEX_ENV
          value: "production"
        - name: CODEX_API_BASE_URL
          value: "https://api.your-domain.com"
        envFrom:
        - secretRef:
            name: artifact-system-secrets
```

### Nginx Configuration

```nginx
upstream artifact_system {
    server 127.0.0.1:8004;
}

server {
    listen 443 ssl;
    server_name api.your-domain.com;
    
    ssl_certificate /path/to/cert.pem;
    ssl_certificate_key /path/to/key.pem;
    
    location / {
        proxy_pass http://artifact_system;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

## 🧪 Testing Your Integration

### 1. Test Artifact Deployment

```bash
# Set your API token
export YOUR_API_TOKEN="your-actual-token"

# Test deployment
python integration_example.py --test-deployment --token $YOUR_API_TOKEN
```

### 2. Test Webhook Connectivity

```bash
python deploy.py --env production --config-file production.env --test-webhooks
```

### 3. Test Authentication

```bash
curl -H "Authorization: Bearer YOUR_TOKEN" \
     https://api.your-domain.com/health
```

### 4. Test Charter Deployment

```bash
curl -X POST \
     -H "Authorization: Bearer YOUR_TOKEN" \
     -F "manifest=@charter-manifest.json" \
     -F "text_content=@charter.md" \
     https://api.your-domain.com/ledger/charter/final
```

## 🔄 Continuous Integration

### GitHub Actions Example

```yaml
name: Deploy Artifact System

on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v3
    
    - name: Setup Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.11'
    
    - name: Install dependencies
      run: python deploy.py --install-deps
    
    - name: Test configuration
      run: python deploy.py --env production --test-webhooks
      env:
        CODEX_API_BASE_URL: ${{ secrets.API_BASE_URL }}
        CODEX_AUTH_SCHEME: ${{ secrets.AUTH_SCHEME }}
    
    - name: Deploy to production
      run: python deploy.py --env production --start-server
      env:
        CODEX_DATABASE_URL: ${{ secrets.DATABASE_URL }}
        CODEX_REDIS_URL: ${{ secrets.REDIS_URL }}
```

## 📞 Support

### Environment Variables Reference

| Variable | Description | Example |
|----------|-------------|---------|
| `CODEX_ENV` | Deployment environment | `production` |
| `CODEX_API_BASE_URL` | Your API domain | `https://api.your-domain.com` |
| `CODEX_AUTH_SCHEME` | Authentication method | `bearer` |
| `CODEX_DATABASE_URL` | Database connection | `postgresql://...` |
| `CODEX_SIGNATURE_VERIFICATION` | Enable signatures | `true` |

### Common Issues

1. **Webhook timeouts**: Increase timeout in webhook configuration
2. **Authentication failures**: Verify auth scheme and credentials
3. **CORS errors**: Update allowed origins in configuration
4. **Rate limiting**: Adjust limits based on usage patterns

### Getting Help

1. Check the health endpoint: `GET /health`
2. Review server logs for detailed error information
3. Test individual components with the deployment script
4. Verify webhook connectivity with test payloads

---

**Ready for production!** Update the configuration with your actual URLs and credentials, then deploy with confidence. The unified artifact system will handle authentication, signature verification, and webhook integrations automatically.
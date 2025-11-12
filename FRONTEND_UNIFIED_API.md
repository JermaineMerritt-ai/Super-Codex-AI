# Frontend Unified API Configuration

## Overview

The frontend has been successfully configured to use a **single base URL** through the backend, ensuring all AXIOM operations route through `/api/axiom/execute` and never call Flask directly.

## Architecture

```
React Frontend (port 3000)
    ↓ REACT_APP_API_BASE=/api
FastAPI Gateway (port 8015)
    ↓ /api/axiom/execute → AXIOM proxy
AXIOM-Flame Backend (port 5010)
    ↓ Ceremonial operations
```

## Configuration Files

### 1. Frontend Environment (`.env`)
```bash
# API Base URL - all requests go through this path
REACT_APP_API_BASE=/api

# Development server port
PORT=3000

# Other settings
NODE_ENV=development
REACT_APP_TITLE=CodexDominion.app
```

### 2. Frontend API Client (`src/api.ts`)
```typescript
// Single base URL configuration
const API_BASE = process.env.REACT_APP_API_BASE || '/api';

// All AXIOM operations use unified execute endpoint
axiom: {
  execute: (command: string, payload?: any, token?: string) =>
    api("/axiom/execute", "POST", { command, payload }, token),
  
  // Convenience methods route through execute
  reason: (params, token) => 
    api("/axiom/execute", "POST", { command: "reason", payload: params }, token),
  
  grant: (params, token) => 
    api("/axiom/execute", "POST", { command: "grant", payload: params }, token),
  
  // etc...
}
```

### 3. Backend Gateway (`app/gateway.py`)
```python
@router.post("/execute")
async def execute(req: AxiomRequest):
    """Unified AXIOM proxy endpoint - routes all ceremonial commands"""
    command = req.command.lower()
    
    # Route to appropriate AXIOM endpoint
    if command == "reason":
        r = await client.post(f"{AXIOM_BASE}/reason", json=payload)
    elif command == "grant":
        r = await client.post(f"{AXIOM_BASE}/grant", json=payload)
    # etc...
```

## Key Features

### ✅ Correct Usage

1. **Single Base URL**: All frontend API calls use `/api` prefix
2. **Unified Endpoint**: All AXIOM operations go through `/api/axiom/execute`
3. **Environment Driven**: Configuration via `REACT_APP_API_BASE`
4. **Proxy Architecture**: Frontend never calls Flask directly
5. **Command Routing**: Backend routes commands to appropriate AXIOM endpoints

### ❌ Prohibited Patterns

1. **Direct Flask Calls**: `fetch('http://127.0.0.1:5010/...')` ❌
2. **Hardcoded URLs**: Bypassing environment variables ❌
3. **Multiple Base URLs**: Different endpoints for different services ❌
4. **Cross-Origin Requests**: Direct browser → Flask communication ❌

## Development Workflow

### Starting the Stack

1. **AXIOM Backend**:
   ```bash
   python axiom_flame/app.py  # Port 5010
   ```

2. **FastAPI Gateway**:
   ```bash
   python -m uvicorn backend_api:app --host 127.0.0.1 --port 8015
   ```

3. **React Frontend**:
   ```bash
   cd frontend && npm start  # Port 3000
   ```

### Environment Setup

```bash
# Backend
export AXIOM_BASE="http://127.0.0.1:5010"

# Frontend (automatic via .env file)
REACT_APP_API_BASE=/api
PORT=3000
```

## Testing

### Validation Script
```bash
python demo_unified_config.py
```

### Manual Testing
```typescript
// In frontend console:
apiClient.axiom.reason({
  actor: "TestUser",
  realm: "PL-001", 
  capsule: "Test Crown"
});
```

## Benefits

1. **Security**: No direct Flask exposure to browser
2. **Consistency**: Single API interface for all operations
3. **Flexibility**: Easy to change backend without frontend updates
4. **Monitoring**: All requests flow through centralized gateway
5. **Authentication**: Unified token handling across all services

## Production Considerations

### Reverse Proxy Setup
```nginx
# NGINX configuration
location /api/ {
    proxy_pass http://backend:8015/;
    proxy_set_header Host $host;
    proxy_set_header X-Real-IP $remote_addr;
}
```

### Docker Configuration
```yaml
services:
  frontend:
    environment:
      - REACT_APP_API_BASE=/api
  
  backend:
    environment:
      - AXIOM_BASE=http://axiom:5010
    
  axiom:
    ports:
      - "5010:5010"  # Internal only
```

## Summary

The frontend now uses a **unified API architecture** where:

- ✅ **Single base URL**: `REACT_APP_API_BASE=/api`
- ✅ **Unified endpoint**: `/api/axiom/execute` for all AXIOM operations
- ✅ **No direct Flask calls** from browser
- ✅ **Environment-driven** configuration
- ✅ **Command routing** through FastAPI gateway

This ensures clean separation of concerns, better security, and easier maintenance of the 3-tier architecture.
# 🚀 CodexDominion.app - TypeScript API Client

## Quick Start Guide

Your TypeScript API client is ready! Here's exactly how to use it:

### 1. **Basic Usage Example**

```typescript
import { apiClient, createWebSocket } from './api';

// Health check
const health = await apiClient.health.live();
console.log('Backend status:', health.status);

// Authentication
const auth = await apiClient.auth.login({ 
  username: 'admin', 
  password: 'secret' 
});
console.log('Logged in as:', auth.user.username);

// Workflow management
const workflows = await apiClient.workflow.list(auth.access_token);
console.log('Found workflows:', workflows.length);

// Axiom ceremonial operations
const ceremony = await apiClient.axiom.reason({
  actor: "Custodian",
  realm: "PL-001", 
  capsule: "Sovereign Crown",
  intent: "Crown.Invocation"
}, auth.access_token);
console.log('Ceremony dispatched:', ceremony.dispatch_id);

// Real-time updates
const ws = createWebSocket(auth.access_token, (data) => {
  console.log('Real-time update:', data);
});
```

### 2. **Available API Methods**

#### **Health Endpoints**
```typescript
await apiClient.health.live();     // Backend health check
await apiClient.health.ready();    // Readiness probe
```

#### **Authentication**
```typescript
// Login
const auth = await apiClient.auth.login({ username: 'admin', password: 'secret' });

// Get user info
const user = await apiClient.auth.me(token);

// Logout
await apiClient.auth.logout(token);
```

#### **Workflow Management**
```typescript
// List workflows
const workflows = await apiClient.workflow.list(token);

// Get specific workflow
const workflow = await apiClient.workflow.get(workflowId, token);

// Create workflow
const newWorkflow = await apiClient.workflow.create({
  name: "My Workflow",
  description: "Test workflow"
}, token);
```

#### **Axiom Ceremonial Operations**
```typescript
// Invoke ceremony
const ceremony = await apiClient.axiom.reason({
  actor: "Custodian",
  realm: "PL-001",
  capsule: "Sovereign Crown",
  intent: "Crown.Invocation"
}, token);

// Registry operations
const realms = await apiClient.axiom.realms(token);
const registry = await apiClient.axiom.registry(token);

// Health check
const axiomHealth = await apiClient.axiom.health();
```

#### **Real-time WebSocket**
```typescript
const ws = createWebSocket(token, (data) => {
  console.log('Received:', data);
});

// Check connection status
if (ws.readyState === WebSocket.OPEN) {
  console.log('Connected!');
}

// Close when done
ws.close();
```

### 3. **Start Development Servers**

#### **Backend API (Port 8010)**
```powershell
# Activate Python environment
.\.venv\Scripts\Activate.ps1

# Start FastAPI backend
uvicorn backend.main:app --host 127.0.0.1 --port 8010 --reload
```

#### **Axiom-flame API (Port 5010)**
```powershell
# Start axiom-flame service
cd axiom-flame/packages/api
python app.py
```

#### **React Frontend (Port 3000)**
```powershell
# Install dependencies and start
cd frontend
npm install
npm start
```

### 4. **React Component Integration**

The complete React app in `frontend/src/App.tsx` demonstrates:

- **Authentication flow** with login/logout
- **Dashboard** with user info and status
- **Workflow management** with real-time updates
- **Ceremony invocation** with form controls
- **WebSocket integration** for live updates
- **Responsive design** with modern styling

### 5. **Production Deployment**

```powershell
# Build React app for production
cd frontend
npm run build

# The built files will be in frontend/build/
# Deploy these to your web server
```

### 6. **API Endpoints Reference**

| Service | Endpoint | Purpose |
|---------|----------|---------|
| Backend | http://localhost:8010 | Main FastAPI application |
| Axiom | http://localhost:5010 | Ceremonial operations API |
| Frontend | http://localhost:3000 | React development server |

### 7. **Error Handling**

All API methods include proper error handling:

```typescript
try {
  const result = await apiClient.health.live();
  console.log('Success:', result);
} catch (error) {
  console.error('API Error:', error.message);
  // Handle error appropriately
}
```

## 🎉 Ready to Use!

Your TypeScript API client is fully functional and production-ready. The React application demonstrates all features with a modern, responsive interface.

**Next Steps:**
1. Start your backend services (ports 8010 and 5010)
2. Launch the React app: `cd frontend && npm start`
3. Open http://localhost:3000 to see it in action!

The API client handles authentication, provides full TypeScript type safety, and integrates seamlessly with your existing FastAPI backend infrastructure.
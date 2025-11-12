// src/api.ts
// Configuration: Use environment variable or default to /api for reverse proxy setup
const API_BASE = process.env.REACT_APP_API_BASE || '/api';

export async function api(path: string, method = "GET", body?: any, token?: string) {
  const res = await fetch(`${API_BASE}${path}`, {
    method,
    headers: {
      "Content-Type": "application/json",
      ...(token ? { Authorization: `Bearer ${token}` } : {}),
    },
    body: body ? JSON.stringify(body) : undefined,
  });
  if (!res.ok) throw new Error(await res.text());
  return res.json();
}

// Helper functions for common API operations
export const apiClient = {
  // Health checks
  health: {
    live: () => api("/health/live"),
    ready: () => api("/health/ready"),
    deps: () => api("/health/deps"),
  },

  // Authentication
  auth: {
    login: (credentials: { username: string; password: string }) =>
      api("/auth/login", "POST", credentials),
    refresh: (token: string) => api("/auth/refresh", "POST", {}, token),
    logout: (token: string) => api("/auth/logout", "POST", {}, token),
  },

  // Workflow management
  workflow: {
    list: (token: string) => api("/workflow", "GET", undefined, token),
    create: (workflow: any, token: string) =>
      api("/workflow", "POST", workflow, token),
    get: (id: string, token: string) =>
      api(`/workflow/${id}`, "GET", undefined, token),
    update: (id: string, workflow: any, token: string) =>
      api(`/workflow/${id}`, "PUT", workflow, token),
    delete: (id: string, token: string) =>
      api(`/workflow/${id}`, "DELETE", undefined, token),
    start: (name: string, data: { capsule?: string }, token: string) =>
      api(`/workflow/start?name=${encodeURIComponent(name)}`, "POST", data, token),
    advance: (workflowId: string, phase: string, data: { note?: string }, token: string) =>
      api(`/workflow/${workflowId}/advance?phase=${encodeURIComponent(phase)}`, "POST", data, token),
  },

  // AXIOM ceremonial operations - ALL operations go through /api/axiom/execute only
  // Never call Flask directly from frontend - always proxy through backend
  axiom: {
    // Generic execute endpoint - all AXIOM operations route through this
    execute: (command: string, payload?: any, token?: string) =>
      api("/axiom/execute", "POST", { command, payload }, token),
    
    // Convenience methods that route through execute endpoint
    health: (token?: string) =>
      api("/axiom/execute", "POST", { command: "health" }, token),
    
    reason: (params: {
      actor: string;
      realm: string;
      capsule: string;
      intent?: string;
    }, token?: string) => 
      api("/axiom/execute", "POST", { 
        command: "reason", 
        payload: params 
      }, token),
    
    grant: (params: {
      recipient: string;
      honor: string;
      authority: string;
    }, token?: string) => 
      api("/axiom/execute", "POST", { 
        command: "grant", 
        payload: params 
      }, token),
    
    ceremonies: (token?: string) => 
      api("/axiom/execute", "POST", { command: "ceremonies" }, token),
    
    // Broadcast operations
    broadcast: (params: {
      message: string;
      realm?: string;
      priority?: "low" | "medium" | "high";
    }, token?: string) => 
      api("/axiom/execute", "POST", { 
        command: "broadcast", 
        payload: params 
      }, token),
  },
};

// WebSocket helper for real-time updates
export function createWebSocket(token: string, onMessage: (data: any) => void) {
  const protocol = window.location.protocol === "https:" ? "wss:" : "ws:";
  const wsUrl = `${protocol}//${window.location.host}/ws?token=${token}`;
  
  const ws = new WebSocket(wsUrl);
  
  ws.onmessage = (event) => {
    try {
      const data = JSON.parse(event.data);
      onMessage(data);
    } catch (error) {
      console.error("Failed to parse WebSocket message:", error);
    }
  };
  
  ws.onerror = (error) => {
    console.error("WebSocket error:", error);
  };
  
  return ws;
}

// Error handling types
export interface ApiError {
  message: string;
  status?: number;
  code?: string;
}

// Response types
export interface HealthResponse {
  status: "live" | "ready";
  disk_free_bytes?: number;
  [key: string]: any;
}

export interface AuthResponse {
  access_token: string;
  token_type: string;
  expires_in: number;
  user: {
    id: string;
    username: string;
    role: string;
  };
}

export interface WorkflowResponse {
  id: string;
  name: string;
  status: "pending" | "running" | "completed" | "failed";
  created_at: string;
  updated_at: string;
  steps: any[];
}

export interface AxiomResponse {
  dispatch_id: string;
  timestamp: string;
  status: "success" | "error";
  result: any;
}
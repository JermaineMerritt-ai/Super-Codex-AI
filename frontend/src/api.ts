// API Client for Super-Codex-AI Frontend
import axios, { AxiosInstance } from 'axios';

const API_BASE = process.env.REACT_APP_API_BASE || 'http://localhost:8080';

class ApiClient {
  private client: AxiosInstance;

  constructor() {
    this.client = axios.create({
      baseURL: API_BASE,
      timeout: 10000,
      headers: {
        'Content-Type': 'application/json',
      },
    });
  }

  async authenticate(username: string, password: string): Promise<AuthResponse> {
    const response = await this.client.post('/auth/login', {
      username,
      password,
    });
    return response.data;
  }

  async getWorkflows(): Promise<WorkflowResponse[]> {
    const response = await this.client.get('/workflows');
    return response.data;
  }

  async health(): Promise<{ status: string; timestamp: string }> {
    const response = await this.client.get('/health/');
    return response.data;
  }

  setAuthToken(token: string) {
    this.client.defaults.headers.common['Authorization'] = `Bearer ${token}`;
  }
}

export const apiClient = new ApiClient();
export const api = apiClient;

export interface AuthResponse {
  access_token: string;
  token_type: string;
  user: {
    id: string;
    username: string;
    role: string;
  };
}

export interface WorkflowResponse {
  id: string;
  name: string;
  status: string;
  created_at: string;
}

export function createWebSocket(token: string, onMessage: (data: any) => void): WebSocket {
  const ws = new WebSocket(`ws://localhost:8080/ws?token=${token}`);
  
  ws.onmessage = (event) => {
    const data = JSON.parse(event.data);
    onMessage(data);
  };
  
  ws.onerror = (error) => {
    console.error('WebSocket error:', error);
  };
  
  return ws;
}
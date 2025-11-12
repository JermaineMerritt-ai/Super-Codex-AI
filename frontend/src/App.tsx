import React, { useState, useEffect, useRef } from 'react';
import { apiClient, createWebSocket, AuthResponse, WorkflowResponse } from './api';
import { connectCeremonyWS } from './lib/ws';
import { notify } from './lib/notify';
import { AxiomDemo } from './components/AxiomDemo';
import CeremonyControl from './components/CeremonyControl';
import './App.css';

interface User {
  id: string;
  username: string;
  role: string;
}

interface AppState {
  isAuthenticated: boolean;
  user: User | null;
  token: string | null;
  health: any;
  workflows: WorkflowResponse[];
  ceremonies: any[];
  wsMessages: any[];
  ceremonyEvents: any[];
  loading: boolean;
  error: string | null;
}

const App: React.FC = () => {
  const [state, setState] = useState<AppState>({
    isAuthenticated: false,
    user: null,
    token: null,
    health: null,
    workflows: [],
    ceremonies: [],
    wsMessages: [],
    ceremonyEvents: [],
    loading: false,
    error: null
  });

  const wsRef = useRef<WebSocket | null>(null);
  // const ceremonyWsRef = useRef<(() => void) | null>(null);
  const [credentials, setCredentials] = useState({ username: 'admin', password: 'secret' });
  const [ceremonyParams, setCeremonyParams] = useState({
    actor: 'Custodian',
    realm: 'PL-001',
    capsule: 'Sovereign Crown',
    intent: 'Crown.Invocation'
  });
  
  const [workflowControls, setWorkflowControls] = useState({
    startName: 'FullConstellation',
    startCapsule: 'full',
    advancePhase: 'DISPATCH',
    advanceNote: 'Planetary release',
    selectedWorkflowId: ''
  });

  // Health check on component mount
  useEffect(() => {
    checkHealth();
  }, []);

  // WebSocket cleanup
  useEffect(() => {
    return () => {
      if (wsRef.current) {
        wsRef.current.close();
      }
      // Note: ceremonyWS auto-reconnects, no explicit cleanup needed
    };
  }, []);

  const checkHealth = async () => {
    try {
      setState(prev => ({ ...prev, loading: true, error: null }));
      const health = await apiClient.health.live();
      setState(prev => ({ ...prev, health, loading: false }));
    } catch (error: any) {
      setState(prev => ({ ...prev, error: error.message, loading: false }));
    }
  };

  const handleLogin = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      setState(prev => ({ ...prev, loading: true, error: null }));
      const auth: AuthResponse = await apiClient.auth.login(credentials);
      setState(prev => ({
        ...prev,
        isAuthenticated: true,
        user: auth.user,
        token: auth.access_token,
        loading: false
      }));
      
      // Initialize WebSocket connections
      if (wsRef.current) wsRef.current.close();
      wsRef.current = createWebSocket(auth.access_token, (data) => {
        setState(prev => ({
          ...prev,
          wsMessages: [...prev.wsMessages, { ...data, timestamp: new Date().toISOString() }]
        }));
      });

      // Connect to ceremony WebSocket
      connectCeremonyWS((event) => {
        console.log('Ceremony event received:', event);
        setState(prev => ({
          ...prev,
          ceremonyEvents: [...prev.ceremonyEvents, { ...event, timestamp: new Date().toISOString() }]
        }));
        
        // Show notifications for important ceremony events
        if (event.status === 'completed') {
          notify.success(`Ceremony completed: ${event.dispatch_id || 'Unknown'}`);
        } else if (event.status === 'failed') {
          notify.error(`Ceremony failed: ${event.dispatch_id || 'Unknown'}`);
        } else if (event.dispatch_id) {
          notify.info(`Ceremony update: ${event.dispatch_id} - ${event.status || 'Processing'}`);
        }
      });
      
      // Load initial data
      await loadWorkflows(auth.access_token);
    } catch (error: any) {
      setState(prev => ({ ...prev, error: error.message, loading: false }));
    }
  };

  const handleLogout = async () => {
    try {
      if (state.token) {
        await apiClient.auth.logout(state.token);
      }
    } catch (error) {
      console.warn('Logout error:', error);
    } finally {
      if (wsRef.current) {
        wsRef.current.close();
        wsRef.current = null;
      }
      setState({
        isAuthenticated: false,
        user: null,
        token: null,
        health: state.health,
        workflows: [],
        ceremonies: [],
        wsMessages: [],
        ceremonyEvents: [],
        loading: false,
        error: null
      });
    }
  };

  const loadWorkflows = async (token: string) => {
    try {
      const workflows = await apiClient.workflow.list(token);
      setState(prev => ({ ...prev, workflows }));
    } catch (error: any) {
      console.warn('Failed to load workflows:', error.message);
    }
  };

  const handleCeremony = async () => {
    if (!state.token) return;
    try {
      setState(prev => ({ ...prev, loading: true, error: null }));
      
      // Import ceremony helper
      const { invokeCeremony } = await import('./lib/ceremony');
      
      // Use ceremony helper with automatic error handling
      const ceremony = await invokeCeremony(ceremonyParams, state.token);
      
      setState(prev => ({
        ...prev,
        ceremonies: [...prev.ceremonies, ceremony],
        loading: false
      }));
    } catch (error: any) {
      // Error handling already done by invokeCeremony, just update state
      setState(prev => ({ ...prev, error: error.message, loading: false }));
    }
  };
  
  const handleStartWorkflow = async () => {
    if (!state.token) return;
    try {
      setState(prev => ({ ...prev, loading: true, error: null }));
      const newWorkflow = await apiClient.workflow.start(
        workflowControls.startName,
        { capsule: workflowControls.startCapsule },
        state.token
      );
      setState(prev => ({
        ...prev,
        workflows: [...prev.workflows, newWorkflow],
        loading: false
      }));
      
      notify.success(`Workflow started: ${workflowControls.startName}`);
    } catch (error: any) {
      setState(prev => ({ ...prev, error: error.message, loading: false }));
      notify.error(`Failed to start workflow: ${error.message ?? error}`);
    }
  };
  
  const handleAdvanceWorkflow = async () => {
    if (!state.token || !workflowControls.selectedWorkflowId) return;
    try {
      setState(prev => ({ ...prev, loading: true, error: null }));
      const updatedWorkflow = await apiClient.workflow.advance(
        workflowControls.selectedWorkflowId,
        workflowControls.advancePhase,
        { note: workflowControls.advanceNote },
        state.token
      );
      
      setState(prev => ({
        ...prev,
        workflows: prev.workflows.map(wf => 
          wf.id === updatedWorkflow.id ? updatedWorkflow : wf
        ),
        loading: false
      }));
      
      notify.success(`Workflow advanced to ${workflowControls.advancePhase}`);
    } catch (error: any) {
      setState(prev => ({ ...prev, error: error.message, loading: false }));
      notify.error(`Failed to advance workflow: ${error.message ?? error}`);
    }
  };

  return (
    <div className="app">
      <header className="app-header">
        <h1>🚀 CodexDominion.app</h1>
        <p>Production-Ready FastAPI + React Application</p>
        {state.health && (
          <div className="health-status">
            ✅ Backend Status: {state.health.status}
          </div>
        )}
      </header>

      {state.error && (
        <div className="error-message">
          ❌ Error: {state.error}
        </div>
      )}

      {state.loading && (
        <div className="loading">
          ⏳ Loading...
        </div>
      )}

      {!state.isAuthenticated ? (
        <div className="login-section">
          <h2>🔐 Authentication</h2>
          <form onSubmit={handleLogin} className="login-form">
            <div className="form-group">
              <label>Username:</label>
              <input
                type="text"
                value={credentials.username}
                onChange={(e) => setCredentials(prev => ({ ...prev, username: e.target.value }))}
                required
              />
            </div>
            <div className="form-group">
              <label>Password:</label>
              <input
                type="password"
                value={credentials.password}
                onChange={(e) => setCredentials(prev => ({ ...prev, password: e.target.value }))}
                required
              />
            </div>
            <button type="submit" disabled={state.loading}>
              Login
            </button>
          </form>
        </div>
      ) : (
        <div className="dashboard">
          <div className="user-info">
            <h2>👋 Welcome, {state.user?.username}!</h2>
            <p>Role: {state.user?.role}</p>
            <button onClick={handleLogout} className="logout-btn">
              Logout
            </button>
          </div>

          <div className="dashboard-grid">
            <div className="panel">
              <h3>📋 Workflows ({state.workflows.length})</h3>
              {state.workflows.length > 0 ? (
                <ul className="workflow-list">
                  {state.workflows.map(workflow => (
                    <li key={workflow.id} className={`workflow-item status-${workflow.status}`}>
                      <strong>{workflow.name}</strong>
                      <span className="status">{workflow.status}</span>
                    </li>
                  ))}
                </ul>
              ) : (
                <p>No workflows found</p>
              )}
              
              <div className="workflow-controls">
                <h4>🚀 Workflow Controls</h4>
                
                <div className="control-section">
                  <h5>Start New Workflow</h5>
                  <div className="form-row">
                    <label>Name:</label>
                    <input
                      value={workflowControls.startName}
                      onChange={(e) => setWorkflowControls(prev => ({ ...prev, startName: e.target.value }))}
                      placeholder="FullConstellation"
                    />
                  </div>
                  <div className="form-row">
                    <label>Capsule:</label>
                    <input
                      value={workflowControls.startCapsule}
                      onChange={(e) => setWorkflowControls(prev => ({ ...prev, startCapsule: e.target.value }))}
                      placeholder="full"
                    />
                  </div>
                  <button onClick={handleStartWorkflow} disabled={state.loading}>
                    Start Workflow
                  </button>
                </div>
                
                <div className="control-section">
                  <h5>Advance Workflow</h5>
                  <div className="form-row">
                    <label>Workflow:</label>
                    <select
                      value={workflowControls.selectedWorkflowId}
                      onChange={(e) => setWorkflowControls(prev => ({ ...prev, selectedWorkflowId: e.target.value }))}
                    >
                      <option value="">Select workflow...</option>
                      {state.workflows.map(wf => (
                        <option key={wf.id} value={wf.id}>{wf.name} ({wf.id})</option>
                      ))}
                    </select>
                  </div>
                  <div className="form-row">
                    <label>Phase:</label>
                    <select
                      value={workflowControls.advancePhase}
                      onChange={(e) => setWorkflowControls(prev => ({ ...prev, advancePhase: e.target.value }))}
                    >
                      <option value="DISPATCH">DISPATCH</option>
                      <option value="PROCESS">PROCESS</option>
                      <option value="VALIDATE">VALIDATE</option>
                      <option value="COMPLETE">COMPLETE</option>
                      <option value="ABORT">ABORT</option>
                    </select>
                  </div>
                  <div className="form-row">
                    <label>Note:</label>
                    <input
                      value={workflowControls.advanceNote}
                      onChange={(e) => setWorkflowControls(prev => ({ ...prev, advanceNote: e.target.value }))}
                      placeholder="Planetary release"
                    />
                  </div>
                  <button 
                    onClick={handleAdvanceWorkflow} 
                    disabled={state.loading || !workflowControls.selectedWorkflowId}
                  >
                    Advance Workflow
                  </button>
                </div>
              </div>
            </div>

            <div className="panel">
              <h3>⚡ Axiom Ceremonial Operations</h3>
              <div className="ceremony-form">
                <div className="form-row">
                  <label>Actor:</label>
                  <input
                    value={ceremonyParams.actor}
                    onChange={(e) => setCeremonyParams(prev => ({ ...prev, actor: e.target.value }))}
                  />
                </div>
                <div className="form-row">
                  <label>Realm:</label>
                  <input
                    value={ceremonyParams.realm}
                    onChange={(e) => setCeremonyParams(prev => ({ ...prev, realm: e.target.value }))}
                  />
                </div>
                <div className="form-row">
                  <label>Capsule:</label>
                  <input
                    value={ceremonyParams.capsule}
                    onChange={(e) => setCeremonyParams(prev => ({ ...prev, capsule: e.target.value }))}
                  />
                </div>
                <div className="form-row">
                  <label>Intent:</label>
                  <input
                    value={ceremonyParams.intent}
                    onChange={(e) => setCeremonyParams(prev => ({ ...prev, intent: e.target.value }))}
                  />
                </div>
                <button onClick={handleCeremony} disabled={state.loading}>
                  Invoke Ceremony
                </button>
              </div>
              
              {state.ceremonies.length > 0 && (
                <div className="ceremonies-list">
                  <h4>Recent Ceremonies:</h4>
                  {state.ceremonies.map((ceremony, index) => (
                    <div key={index} className="ceremony-item">
                      <strong>ID:</strong> {ceremony.dispatch_id}<br/>
                      <strong>Status:</strong> {ceremony.status}<br/>
                      <strong>Time:</strong> {ceremony.timestamp}
                    </div>
                  ))}
                </div>
              )}
            </div>

            <div className="panel">
              <h3>📡 Real-time Updates</h3>
              <div className="websocket-status">
                <div>Workflow WS: {wsRef.current?.readyState === WebSocket.OPEN ? '🟢 Connected' : '🔴 Disconnected'}</div>
                <div>Ceremony WS: 🔄 Auto-reconnecting (ws://localhost:8010/ws/ceremony)</div>
              </div>
              
              <div className="realtime-tabs">
                <div className="tab-section">
                  <h4>🔄 Workflow Events ({state.wsMessages.length})</h4>
                  {state.wsMessages.length > 0 ? (
                    <div className="ws-messages">
                      {state.wsMessages.slice(-3).map((msg, index) => (
                        <div key={index} className="ws-message">
                          <small>{msg.timestamp}</small>
                          <pre>{JSON.stringify(msg, null, 2)}</pre>
                        </div>
                      ))}
                    </div>
                  ) : (
                    <p>No workflow events yet</p>
                  )}
                </div>
                
                <div className="tab-section">
                  <h4>⚡ Ceremony Events ({state.ceremonyEvents.length})</h4>
                  {state.ceremonyEvents.length > 0 ? (
                    <div className="ceremony-events">
                      {state.ceremonyEvents.slice(-3).map((event, index) => (
                        <div key={index} className="ceremony-event">
                          <small>{event.timestamp}</small>
                          <div className="event-content">
                            {event.dispatch_id && <div><strong>Dispatch ID:</strong> {event.dispatch_id}</div>}
                            {event.status && <div><strong>Status:</strong> {event.status}</div>}
                            {event.actor && <div><strong>Actor:</strong> {event.actor}</div>}
                            <pre className="event-data">{JSON.stringify(event, null, 2)}</pre>
                          </div>
                        </div>
                      ))}
                    </div>
                  ) : (
                    <p>No ceremony events yet</p>
                  )}
                </div>
              </div>
            </div>
          </div>
          
          {/* Advanced Ceremony Control */}
          <div className="panel full-width">
            <CeremonyControl 
              token={state.token || undefined} 
              onCeremonyComplete={(ceremony) => {
                setState(prev => ({
                  ...prev,
                  ceremonies: [...prev.ceremonies, ceremony]
                }));
              }}
            />
          </div>

          {/* AXIOM Unified API Demo */}
          <div className="panel full-width">
            <AxiomDemo token={state.token || undefined} />
          </div>
        </div>
      )}

      <footer className="app-footer">
        <p>🌟 Built with FastAPI, React, TypeScript & AXIOM-Flame</p>
        <div className="api-config">
          <strong>API Configuration:</strong><br/>
          Base URL: {process.env.REACT_APP_API_BASE || '/api'} 
          {' | '}Environment: {process.env.NODE_ENV}
          {' | '}All AXIOM calls route through: <code>/api/axiom/execute</code>
          <br/>
          <small>✅ Frontend never calls Flask directly - unified proxy architecture</small>
        </div>
      </footer>
    </div>
  );
};

export default App;
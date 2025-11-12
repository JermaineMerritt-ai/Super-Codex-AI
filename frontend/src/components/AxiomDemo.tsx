// src/components/AxiomDemo.tsx
import React, { useState } from 'react';
import { apiClient } from '../api';
import { notify } from '../lib/notify';

interface AxiomDemoProps {
  token?: string;
}

export const AxiomDemo: React.FC<AxiomDemoProps> = ({ token }) => {
  const [response, setResponse] = useState<any>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleRequest = async (operation: string, payload?: any) => {
    setLoading(true);
    setError(null);
    setResponse(null);

    try {
      let result;
      
      switch (operation) {
        case 'health':
          result = await apiClient.axiom.health(token);
          break;
        case 'reason':
          result = await apiClient.axiom.reason({
            actor: 'FrontendUser',
            realm: 'PL-001',
            capsule: 'Frontend Test Crown',
            intent: 'Frontend.Test'
          }, token);
          break;
        case 'grant':
          result = await apiClient.axiom.grant({
            recipient: 'FrontendTester',
            honor: 'API Integration Mastery',
            authority: 'Frontend-Council'
          }, token);
          break;
        case 'ceremonies':
          result = await apiClient.axiom.ceremonies(token);
          break;
        case 'broadcast':
          result = await apiClient.axiom.broadcast({
            message: 'Frontend successfully connected to unified API',
            realm: 'PL-001',
            priority: 'medium'
          }, token);
          break;
        default:
          result = await apiClient.axiom.execute(operation, payload, token);
      }
      
      setResponse(result);
      
      // Success notification
      notify.success(`AXIOM ${operation} operation completed`);
    } catch (err: any) {
      const errorMessage = err instanceof Error ? err.message : 'Unknown error occurred';
      setError(errorMessage);
      
      // Error notification - your exact pattern!
      notify.error(`AXIOM ${operation} failed: ${err.message ?? err}`);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{ padding: '20px', maxWidth: '800px' }}>
      <h2>AXIOM Unified API Demo</h2>
      <p>All requests go through <code>/api/axiom/execute</code> - no direct Flask calls</p>
      
      <div style={{ marginBottom: '20px' }}>
        <button 
          onClick={() => handleRequest('health')}
          disabled={loading}
          style={{ margin: '5px', padding: '10px' }}
        >
          Health Check
        </button>
        
        <button 
          onClick={() => handleRequest('reason')}
          disabled={loading}
          style={{ margin: '5px', padding: '10px' }}
        >
          Ceremonial Reasoning
        </button>
        
        <button 
          onClick={() => handleRequest('grant')}
          disabled={loading}
          style={{ margin: '5px', padding: '10px' }}
        >
          Grant Honor
        </button>
        
        <button 
          onClick={() => handleRequest('ceremonies')}
          disabled={loading}
          style={{ margin: '5px', padding: '10px' }}
        >
          List Ceremonies
        </button>
        
        <button 
          onClick={() => handleRequest('broadcast')}
          disabled={loading}
          style={{ margin: '5px', padding: '10px' }}
        >
          Broadcast Message
        </button>
      </div>

      {loading && <div style={{ color: 'blue' }}>Loading...</div>}
      
      {error && (
        <div style={{ color: 'red', backgroundColor: '#ffebee', padding: '10px', marginBottom: '10px' }}>
          Error: {error}
        </div>
      )}
      
      {response && (
        <div>
          <h3>Response:</h3>
          <pre style={{ 
            backgroundColor: '#f5f5f5', 
            padding: '10px', 
            border: '1px solid #ddd',
            overflow: 'auto',
            fontSize: '12px'
          }}>
            {JSON.stringify(response, null, 2)}
          </pre>
        </div>
      )}
      
      <div style={{ marginTop: '20px', fontSize: '12px', color: '#666' }}>
        <strong>Configuration:</strong><br/>
        API Base: {process.env.REACT_APP_API_BASE || '/api'}<br/>
        Environment: {process.env.NODE_ENV}<br/>
        All AXIOM operations route through: <code>/api/axiom/execute</code>
      </div>
    </div>
  );
};
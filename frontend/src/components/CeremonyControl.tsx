// frontend/src/components/CeremonyControl.tsx
// Advanced ceremony control panel using ceremony helper functions

import React, { useState } from 'react';
import { invokeCeremony, reasonCeremony, auditCeremony, replayCeremony, checkCeremonyHealth } from '../lib/ceremony';
import { notify } from '../lib/notify';

interface CeremonyControlProps {
  token?: string;
  onCeremonyComplete?: (ceremony: any) => void;
}

export const CeremonyControl: React.FC<CeremonyControlProps> = ({ token, onCeremonyComplete }) => {
  const [loading, setLoading] = useState(false);
  const [ceremonialData, setCeremonialData] = useState({
    actor: 'Custodian',
    realm: 'PL-001',
    capsule: 'Sovereign Crown',
    intent: 'Crown.Invocation'
  });
  const [auditId, setAuditId] = useState('');
  const [dispatchId, setDispatchId] = useState('');

  // Example 1: Simple ceremony invocation with automatic error handling
  const handleInvokeCeremony = async () => {
    if (!token) {
      notify.error('Authentication token required');
      return;
    }

    setLoading(true);
    try {
      // Handles errors automatically with notifications!
      const ceremony = await invokeCeremony(ceremonialData, token);
      
      onCeremonyComplete?.(ceremony);
      console.log('Ceremony result:', ceremony);
    } catch (error) {
      // Error already shown by invokeCeremony helper
      console.error('Ceremony invocation failed:', error);
    } finally {
      setLoading(false);
    }
  };

  // Example 2: Ceremony reasoning with automatic error handling
  const handleReasonCeremony = async () => {
    if (!token) {
      notify.error('Authentication token required');
      return;
    }

    setLoading(true);
    try {
      // Automatic success/error notifications
      const result = await reasonCeremony(ceremonialData, token);
      
      onCeremonyComplete?.(result);
      console.log('Reasoning result:', result);
    } catch (error) {
      console.error('Ceremony reasoning failed:', error);
    } finally {
      setLoading(false);
    }
  };

  // Example 3: Audit ceremony with ID
  const handleAuditCeremony = async () => {
    if (!token || !auditId.trim()) {
      notify.error('Authentication token and audit ID required');
      return;
    }

    setLoading(true);
    try {
      // Automatic error handling
      const auditResult = await auditCeremony(auditId, token);
      
      console.log('Audit result:', auditResult);
    } catch (error) {
      console.error('Ceremony audit failed:', error);
    } finally {
      setLoading(false);
    }
  };

  // Example 4: Replay ceremony
  const handleReplayCeremony = async () => {
    if (!token || !dispatchId.trim()) {
      notify.error('Authentication token and dispatch ID required');
      return;
    }

    setLoading(true);
    try {
      const replayResult = await replayCeremony(dispatchId, token);
      
      console.log('Replay result:', replayResult);
    } catch (error) {
      console.error('Ceremony replay failed:', error);
    } finally {
      setLoading(false);
    }
  };

  // Example 5: Health check
  const handleHealthCheck = async () => {
    if (!token) {
      notify.error('Authentication token required');
      return;
    }

    setLoading(true);
    try {
      const healthResult = await checkCeremonyHealth(token);
      
      console.log('Health check result:', healthResult);
    } catch (error) {
      console.error('Health check failed:', error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{ padding: '20px', border: '1px solid #ddd', borderRadius: '8px', margin: '10px' }}>
      <h3>🎭 Advanced Ceremony Control</h3>
      <p><em>All operations use automatic error handling with notifications</em></p>

      {/* Ceremonial Parameters */}
      <div style={{ marginBottom: '20px', backgroundColor: '#f8f9fa', padding: '15px', borderRadius: '5px' }}>
        <h4>Ceremonial Parameters:</h4>
        <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '10px' }}>
          <div>
            <label>Actor:</label>
            <input
              value={ceremonialData.actor}
              onChange={(e) => setCeremonialData(prev => ({ ...prev, actor: e.target.value }))}
              style={{ width: '100%', padding: '5px' }}
            />
          </div>
          <div>
            <label>Realm:</label>
            <input
              value={ceremonialData.realm}
              onChange={(e) => setCeremonialData(prev => ({ ...prev, realm: e.target.value }))}
              style={{ width: '100%', padding: '5px' }}
            />
          </div>
          <div>
            <label>Capsule:</label>
            <input
              value={ceremonialData.capsule}
              onChange={(e) => setCeremonialData(prev => ({ ...prev, capsule: e.target.value }))}
              style={{ width: '100%', padding: '5px' }}
            />
          </div>
          <div>
            <label>Intent:</label>
            <input
              value={ceremonialData.intent}
              onChange={(e) => setCeremonialData(prev => ({ ...prev, intent: e.target.value }))}
              style={{ width: '100%', padding: '5px' }}
            />
          </div>
        </div>
      </div>

      {/* Ceremony Operations */}
      <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '15px', marginBottom: '20px' }}>
        <button
          onClick={handleInvokeCeremony}
          disabled={loading}
          style={{ 
            padding: '12px', 
            backgroundColor: '#007bff', 
            color: 'white', 
            border: 'none', 
            borderRadius: '5px',
            cursor: loading ? 'not-allowed' : 'pointer'
          }}
        >
          🎭 Invoke Ceremony
        </button>

        <button
          onClick={handleReasonCeremony}
          disabled={loading}
          style={{ 
            padding: '12px', 
            backgroundColor: '#28a745', 
            color: 'white', 
            border: 'none', 
            borderRadius: '5px',
            cursor: loading ? 'not-allowed' : 'pointer'
          }}
        >
          🧠 Reason Ceremony
        </button>

        <button
          onClick={handleHealthCheck}
          disabled={loading}
          style={{ 
            padding: '12px', 
            backgroundColor: '#17a2b8', 
            color: 'white', 
            border: 'none', 
            borderRadius: '5px',
            cursor: loading ? 'not-allowed' : 'pointer'
          }}
        >
          ❤️ Health Check
        </button>

        <div style={{ display: 'flex', alignItems: 'center', gap: '5px' }}>
          {loading && <span style={{ color: '#007bff' }}>⏳ Processing...</span>}
          {!loading && <span style={{ color: '#28a745' }}>✅ Ready</span>}
        </div>
      </div>

      {/* Audit Operations */}
      <div style={{ marginBottom: '15px' }}>
        <h4>🔍 Audit Operations:</h4>
        <div style={{ display: 'flex', gap: '10px', alignItems: 'center' }}>
          <input
            placeholder="Audit ID (e.g., AXF-2025-11-10-12345678)"
            value={auditId}
            onChange={(e) => setAuditId(e.target.value)}
            style={{ flex: 1, padding: '8px' }}
          />
          <button
            onClick={handleAuditCeremony}
            disabled={loading || !auditId.trim()}
            style={{ 
              padding: '8px 16px', 
              backgroundColor: '#ffc107', 
              color: 'black', 
              border: 'none', 
              borderRadius: '5px' 
            }}
          >
            🔍 Audit
          </button>
        </div>
      </div>

      {/* Replay Operations */}
      <div>
        <h4>🔄 Replay Operations:</h4>
        <div style={{ display: 'flex', gap: '10px', alignItems: 'center' }}>
          <input
            placeholder="Dispatch ID"
            value={dispatchId}
            onChange={(e) => setDispatchId(e.target.value)}
            style={{ flex: 1, padding: '8px' }}
          />
          <button
            onClick={handleReplayCeremony}
            disabled={loading || !dispatchId.trim()}
            style={{ 
              padding: '8px 16px', 
              backgroundColor: '#6f42c1', 
              color: 'white', 
              border: 'none', 
              borderRadius: '5px' 
            }}
          >
            🔄 Replay
          </button>
        </div>
      </div>

      <div style={{ marginTop: '15px', fontSize: '12px', color: '#666', padding: '10px', backgroundColor: '#f8f9fa', borderRadius: '5px' }}>
        <strong>💡 Usage Pattern:</strong><br/>
        <code>import {`{ invokeCeremony }`} from './lib/ceremony';</code><br/>
        <code>await invokeCeremony(ceremonyPayload, token); // Handles errors automatically</code>
      </div>
    </div>
  );
};

export default CeremonyControl;
// frontend/src/examples/CeremonyUsageExamples.tsx
// Complete examples of ceremony helper usage patterns

import React, { useState } from 'react';
import { 
  invokeCeremony, 
  reasonCeremony, 
  auditCeremony, 
  replayCeremony, 
  checkCeremonyHealth,
  executeCeremony 
} from '../lib/ceremony';
import { api } from '../api';
import { notify } from '../lib/notify';

export const CeremonyUsageExamples: React.FC = () => {
  const [token] = useState('demo-token'); // In real app, get from auth

  // Example 1: Your exact pattern - automatic error handling
  const example1_AutomaticErrorHandling = async () => {
    const ceremonyPayload = {
      actor: "Custodian",
      realm: "PL-001",
      capsule: "Sovereign Crown",
      intent: "Crown.Invocation"
    };

    // Handles errors automatically with notifications!
    await invokeCeremony(ceremonyPayload, token);
  };

  // Example 2: Manual ceremony call with error handling (your original pattern)
  const example2_ManualErrorHandling = async () => {
    try {
      await api('/axiom/execute', 'POST', {
        command: 'invoke',
        payload: {
          actor: "Custodian",
          realm: "PL-001", 
          capsule: "Sovereign Crown",
          intent: "Crown.Invocation"
        }
      }, token);
    } catch (e: any) {
      notify.error(`Ceremony failed: ${e.message ?? e}`);
    }
  };

  // Example 3: All ceremony operations with automatic error handling
  const example3_AllOperations = async () => {
    const payload = {
      actor: "Custodian",
      realm: "PL-001",
      capsule: "Demo Crown"
    };

    // All these handle errors automatically and show notifications
    await invokeCeremony(payload, token);           // Invoke ceremony
    await reasonCeremony(payload, token);           // Reason ceremony  
    await auditCeremony('AXF-2025-11-10-12345', token);    // Audit by ID
    await replayCeremony('dispatch-id-123', token); // Replay ceremony
    await checkCeremonyHealth(token);               // Health check
  };

  // Example 4: Custom ceremony with specific messaging
  const example4_CustomMessaging = async () => {
    await executeCeremony(
      { 
        command: 'invoke', 
        payload: { 
          actor: "Custodian", 
          realm: "PL-001", 
          capsule: "Custom Crown",
          intent: "Custom.Operation"
        }
      },
      token,
      { 
        successMessage: "Custom ceremony completed successfully!",
        errorPrefix: "Custom ceremony failed",
        showSuccess: true
      }
    );
  };

  // Example 5: Error handling with additional logic
  const example5_ErrorHandlingWithLogic = async () => {
    try {
      const result = await invokeCeremony({
        actor: "Custodian",
        realm: "PL-001",
        capsule: "Logic Crown"
      }, token);
      
      // Additional success logic
      console.log('Ceremony successful, result:', result);
      
      // You can still add custom success handling
      if (result.dispatch_id) {
        notify.info(`Dispatch ID: ${result.dispatch_id}`);
      }
      
    } catch (error) {
      // Error notification already shown by invokeCeremony
      // But you can add additional error logic here
      console.error('Additional error handling:', error);
      
      // Maybe trigger recovery logic, send to analytics, etc.
    }
  };

  return (
    <div style={{ padding: '20px', maxWidth: '800px' }}>
      <h2>🎭 Ceremony Helper Usage Examples</h2>
      
      <div style={{ display: 'grid', gap: '15px' }}>
        <div style={{ padding: '15px', border: '1px solid #ddd', borderRadius: '8px' }}>
          <h3>1. ✅ Automatic Error Handling (Recommended)</h3>
          <pre style={{ backgroundColor: '#f8f9fa', padding: '10px', fontSize: '12px' }}>
{`import { invokeCeremony } from './lib/ceremony';

const ceremonyPayload = {
  actor: "Custodian",
  realm: "PL-001",
  capsule: "Sovereign Crown",
  intent: "Crown.Invocation"
};

// Handles errors automatically with notifications!
await invokeCeremony(ceremonyPayload, token);`}
          </pre>
          <button onClick={example1_AutomaticErrorHandling} style={{ padding: '8px 16px', backgroundColor: '#28a745', color: 'white', border: 'none', borderRadius: '4px' }}>
            Test Automatic Handling
          </button>
        </div>

        <div style={{ padding: '15px', border: '1px solid #ddd', borderRadius: '8px' }}>
          <h3>2. 🔧 Manual Error Handling (Your Original Pattern)</h3>
          <pre style={{ backgroundColor: '#f8f9fa', padding: '10px', fontSize: '12px' }}>
{`try {
  await api('/axiom/execute', 'POST', {
    command: 'invoke',
    payload: {...}
  }, token);
} catch (e: any) {
  notify.error(\`Ceremony failed: \${e.message ?? e}\`);
}`}
          </pre>
          <button onClick={example2_ManualErrorHandling} style={{ padding: '8px 16px', backgroundColor: '#007bff', color: 'white', border: 'none', borderRadius: '4px' }}>
            Test Manual Handling
          </button>
        </div>

        <div style={{ padding: '15px', border: '1px solid #ddd', borderRadius: '8px' }}>
          <h3>3. 🚀 All Operations</h3>
          <pre style={{ backgroundColor: '#f8f9fa', padding: '10px', fontSize: '12px' }}>
{`await invokeCeremony(payload, token);    // Invoke
await reasonCeremony(payload, token);     // Reason  
await auditCeremony(auditId, token);      // Audit
await replayCeremony(dispatchId, token);  // Replay
await checkCeremonyHealth(token);         // Health`}
          </pre>
          <button onClick={example3_AllOperations} style={{ padding: '8px 16px', backgroundColor: '#6f42c1', color: 'white', border: 'none', borderRadius: '4px' }}>
            Test All Operations
          </button>
        </div>

        <div style={{ padding: '15px', border: '1px solid #ddd', borderRadius: '8px' }}>
          <h3>4. 🎨 Custom Messaging</h3>
          <pre style={{ backgroundColor: '#f8f9fa', padding: '10px', fontSize: '12px' }}>
{`await executeCeremony(command, token, {
  successMessage: "Custom success message!",
  errorPrefix: "Custom ceremony failed",
  showSuccess: true
});`}
          </pre>
          <button onClick={example4_CustomMessaging} style={{ padding: '8px 16px', backgroundColor: '#ffc107', color: 'black', border: 'none', borderRadius: '4px' }}>
            Test Custom Messaging
          </button>
        </div>

        <div style={{ padding: '15px', border: '1px solid #ddd', borderRadius: '8px' }}>
          <h3>5. 🛠️ Error Handling + Additional Logic</h3>
          <pre style={{ backgroundColor: '#f8f9fa', padding: '10px', fontSize: '12px' }}>
{`try {
  const result = await invokeCeremony(payload, token);
  // Additional success logic
  console.log('Success:', result);
} catch (error) {
  // Error notification already shown
  // Add custom error logic here
}`}
          </pre>
          <button onClick={example5_ErrorHandlingWithLogic} style={{ padding: '8px 16px', backgroundColor: '#dc3545', color: 'white', border: 'none', borderRadius: '4px' }}>
            Test Additional Logic
          </button>
        </div>
      </div>

      <div style={{ marginTop: '30px', padding: '15px', backgroundColor: '#e7f3ff', borderRadius: '8px' }}>
        <h3>📋 Quick Reference</h3>
        <div style={{ fontSize: '14px' }}>
          <p><strong>Import:</strong> <code>import {`{ invokeCeremony }`} from './lib/ceremony';</code></p>
          <p><strong>Usage:</strong> <code>await invokeCeremony(ceremonyPayload, token);</code></p>
          <p><strong>Benefits:</strong></p>
          <ul>
            <li>✅ Automatic error notifications</li>
            <li>✅ Consistent success messages</li>
            <li>✅ Unified error handling</li>
            <li>✅ Less boilerplate code</li>
            <li>✅ Your exact error pattern: <code>notify.error(`Ceremony failed: ${'${e.message ?? e}'}`)</code></li>
          </ul>
        </div>
      </div>
    </div>
  );
};

export default CeremonyUsageExamples;
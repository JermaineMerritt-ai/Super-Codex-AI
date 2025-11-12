// frontend/src/examples/NotificationExamples.tsx
// Examples of notification usage patterns for ceremony operations

import React from 'react';
import { notify } from '../lib/notify';
import { api } from '../api';

export const NotificationExamples: React.FC = () => {
  
  // Example 1: Your exact pattern - manual ceremony call with error handling
  const manualCeremonyCall = async (token: string) => {
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

  // Example 2: Using ceremony helper functions
  const helperExamples = async (token: string) => {
    const { invokeCeremony, reasonCeremony } = await import('../lib/ceremony');
    
    // Automatic error handling + success notifications
    await invokeCeremony({
      actor: "Custodian",
      realm: "PL-001",
      capsule: "Sovereign Crown"
    }, token);
    
    await reasonCeremony({
      actor: "Custodian", 
      realm: "PL-001",
      capsule: "Reasoning Crown"
    }, token);
  };

  // Example 3: Manual notification calls
  const testNotifications = () => {
    notify.success("Ceremony completed successfully!");
    
    setTimeout(() => {
      notify.error("Connection to AXIOM service lost");
    }, 1000);
    
    setTimeout(() => {
      notify.warning("Token expires in 5 minutes");
    }, 2000);
    
    setTimeout(() => {
      notify.info("Processing ceremony request...");
    }, 3000);
  };

  return (
    <div style={{ padding: '20px' }}>
      <h2>🔔 Notification System Examples</h2>
      
      <div style={{ marginBottom: '20px' }}>
        <button onClick={testNotifications} style={{ margin: '5px', padding: '10px' }}>
          Test All Notification Types
        </button>
        
        <button 
          onClick={() => notify.success("Manual success notification!")}
          style={{ margin: '5px', padding: '10px', backgroundColor: '#4caf50', color: 'white' }}
        >
          Success Notification
        </button>
        
        <button 
          onClick={() => notify.error("Manual error notification!")}
          style={{ margin: '5px', padding: '10px', backgroundColor: '#f44336', color: 'white' }}
        >
          Error Notification
        </button>
      </div>
      
      <div style={{ backgroundColor: '#f5f5f5', padding: '15px', borderRadius: '5px' }}>
        <h3>📋 Implementation Patterns</h3>
        
        <h4>1. Your Exact Pattern:</h4>
        <pre style={{ backgroundColor: 'white', padding: '10px', fontSize: '12px' }}>
{`try {
  await api('/axiom/execute','POST',{
    command:'invoke',
    payload:{...}
  }, token);
} catch (e:any) {
  notify.error(\`Ceremony failed: \${e.message ?? e}\`);
}`}
        </pre>
        
        <h4>2. Using Ceremony Helpers:</h4>
        <pre style={{ backgroundColor: 'white', padding: '10px', fontSize: '12px' }}>
{`import { invokeCeremony } from './lib/ceremony';

// Automatic error handling + success notifications
await invokeCeremony({
  actor: "Custodian",
  realm: "PL-001",
  capsule: "Crown"
}, token);`}
        </pre>
        
        <h4>3. Manual Notifications:</h4>
        <pre style={{ backgroundColor: 'white', padding: '10px', fontSize: '12px' }}>
{`import { notify } from './lib/notify';

notify.success("Operation completed!");
notify.error("Something went wrong!");
notify.warning("Warning message");
notify.info("Info message");`}
        </pre>
      </div>
      
      <div style={{ marginTop: '20px', padding: '10px', backgroundColor: '#e3f2fd', borderRadius: '5px' }}>
        <strong>💡 Integration Status:</strong>
        <ul style={{ marginTop: '10px' }}>
          <li>✅ App.tsx - Full ceremony error handling integrated</li>
          <li>✅ AxiomDemo.tsx - Notification system added</li>
          <li>✅ WebSocket ceremony events - Auto-notifications enabled</li>
          <li>✅ Workflow operations - Success/error notifications</li>
          <li>✅ Your exact pattern: <code>notify.error(`Ceremony failed: ${'${e.message ?? e}'}`)</code></li>
        </ul>
      </div>
    </div>
  );
};

export default NotificationExamples;
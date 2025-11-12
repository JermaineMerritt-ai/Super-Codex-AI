// src/lib/ceremony.ts
// Helper functions for ceremony operations with error handling

import { api } from '../api';
import { notify } from './notify';

export interface CeremonyPayload {
  actor: string;
  realm: string;
  capsule: string;
  intent?: string;
  [key: string]: any;
}

export interface CeremonyCommand {
  command: 'invoke' | 'reason' | 'audit' | 'replay' | 'health';
  payload: CeremonyPayload | { [key: string]: any };
}

/**
 * Execute a ceremony command with proper error handling and user feedback
 */
export async function executeCeremony(
  command: CeremonyCommand, 
  token: string,
  options: { 
    successMessage?: string;
    errorPrefix?: string;
    showSuccess?: boolean;
  } = {}
): Promise<any> {
  const { 
    successMessage, 
    errorPrefix = 'Ceremony failed',
    showSuccess = true 
  } = options;

  try {
    const response = await api('/axiom/execute', 'POST', command, token);
    
    if (showSuccess && successMessage) {
      notify.success(successMessage);
    }
    
    return response;
  } catch (e: any) {
    const errorMessage = e.message ?? e.toString() ?? 'Unknown error';
    notify.error(`${errorPrefix}: ${errorMessage}`);
    throw e; // Re-throw so caller can handle if needed
  }
}

/**
 * Invoke a ceremony with standard error handling
 */
export async function invokeCeremony(
  payload: CeremonyPayload, 
  token: string
): Promise<any> {
  return executeCeremony(
    { command: 'invoke', payload },
    token,
    { 
      successMessage: `Ceremony invoked: ${payload.capsule}`,
      errorPrefix: 'Ceremony invocation failed'
    }
  );
}

/**
 * Perform ceremony reasoning with error handling
 */
export async function reasonCeremony(
  payload: CeremonyPayload, 
  token: string
): Promise<any> {
  return executeCeremony(
    { command: 'reason', payload },
    token,
    { 
      successMessage: `Ceremony reasoning complete: ${payload.capsule}`,
      errorPrefix: 'Ceremony reasoning failed'
    }
  );
}

/**
 * Audit a ceremony with error handling
 */
export async function auditCeremony(
  auditId: string, 
  token: string
): Promise<any> {
  return executeCeremony(
    { command: 'audit', payload: { auditId } },
    token,
    { 
      successMessage: `Audit complete: ${auditId}`,
      errorPrefix: 'Ceremony audit failed'
    }
  );
}

/**
 * Replay a ceremony with error handling
 */
export async function replayCeremony(
  dispatchId: string, 
  token: string
): Promise<any> {
  return executeCeremony(
    { command: 'replay', payload: { dispatchId } },
    token,
    { 
      successMessage: `Ceremony replayed: ${dispatchId}`,
      errorPrefix: 'Ceremony replay failed'
    }
  );
}

/**
 * Check ceremony health with error handling
 */
export async function checkCeremonyHealth(token: string): Promise<any> {
  return executeCeremony(
    { command: 'health', payload: {} },
    token,
    { 
      showSuccess: false, // Don't show success for health checks
      errorPrefix: 'Health check failed'
    }
  );
}

// Example usage patterns:
/*

// Basic ceremony invocation
try {
  const result = await invokeCeremony({
    actor: "Custodian",
    realm: "PL-001",
    capsule: "Sovereign Crown",
    intent: "Crown.Invocation"
  }, token);
  
  console.log('Ceremony result:', result);
} catch (e) {
  // Error already shown to user via notify.error
  console.error('Ceremony failed:', e);
}

// Manual ceremony with custom error handling
try {
  const result = await api('/axiom/execute', 'POST', {
    command: 'invoke',
    payload: {
      actor: "Custodian", 
      realm: "PL-001", 
      capsule: "Sovereign Crown"
    }
  }, token);
} catch (e: any) {
  notify.error(`Ceremony failed: ${e.message ?? e}`);
}

// Using the ceremony helper
await executeCeremony(
  { 
    command: 'invoke', 
    payload: { actor: "Custodian", realm: "PL-001", capsule: "Crown" }
  },
  token,
  { 
    successMessage: "Crown ceremony completed successfully!",
    errorPrefix: "Crown ceremony failed"
  }
);

*/
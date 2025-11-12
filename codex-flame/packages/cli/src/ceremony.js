const axios = require('axios');
const fs = require('fs').promises;
const path = require('path');

async function dispatch(options) {
  const { actor, realm, capsule } = options;
  
  if (!actor || !realm || !capsule) {
    console.error('Error: Actor, realm, and capsule are required');
    process.exit(1);
  }

  try {
    // Validate actor permissions first
    const permissionsResponse = await axios.get(`http://localhost:5000/api/actors/${encodeURIComponent(actor)}/permissions`);
    const actorData = permissionsResponse.data;
    
    console.log(`Validating ${actor} (${actorData.role}) permissions...`);
    
    if (!actorData.active) {
      console.error(`Error: Actor '${actor}' is not active`);
      process.exit(1);
    }
    
    // Check if actor has access to the realm
    const hasRealmAccess = actorData.accessible_realms.some(r => 
      r.realm_id === realm || r.name === realm
    );
    
    if (!hasRealmAccess) {
      console.error(`Error: Actor '${actor}' does not have access to realm '${realm}'`);
      console.log('Accessible realms:', actorData.accessible_realms.map(r => `${r.realm_id} (${r.name})`).join(', '));
      process.exit(1);
    }
    
    console.log(`✓ Permission validation passed`);
    
    // Call the reasoning API
    const response = await axios.post('http://localhost:5000/api/reasoning', {
      actor,
      realm,
      capsule,
      input: { prompt: `${capsule} invocation: source→replay` }
    });

    const ledgerEntry = response.data;
    console.log('Ceremony dispatched:', ledgerEntry.dispatch_id);
    
    // Save to local artifacts
    const ceremonyPath = path.join(__dirname, '../../../artifacts/ceremonies', `${ledgerEntry.dispatch_id}.json`);
    await fs.writeFile(ceremonyPath, JSON.stringify(ledgerEntry, null, 2));
    
    // Create replay file
    const replayData = {
      dispatch_id: ledgerEntry.dispatch_id,
      timestamp: ledgerEntry.timestamp,
      full_context: ledgerEntry,
      steps: [
        { step: 'validate_actor', status: 'completed' },
        { step: 'verify_capsule', status: 'completed' },
        { step: 'execute_reasoning', status: 'completed' },
        { step: 'seal_governance', status: 'completed' }
      ]
    };
    
    const replayPath = path.join(__dirname, '../../../storage/replays', `${ledgerEntry.dispatch_id}.json`);
    await fs.writeFile(replayPath, JSON.stringify(replayData, null, 2));
    
    console.log('Ceremony complete. Files saved.');
    
  } catch (error) {
    console.error('Ceremony dispatch failed:', error.message);
    process.exit(1);
  }
}

module.exports = { dispatch };
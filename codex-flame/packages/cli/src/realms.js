const axios = require('axios');
const fs = require('fs').promises;

async function listRealms(options) {
  const { status } = options;
  
  try {
    let url = 'http://localhost:5000/api/realms';
    if (status) {
      url += `?status=${encodeURIComponent(status)}`;
    }
    
    const response = await axios.get(url);
    const { realms, count } = response.data;
    
    console.log(`Found ${count} realm(s):`);
    console.log('');
    
    realms.forEach(realm => {
      console.log(`🏛️  ${realm.name} (${realm.realm_id})`);
      console.log(`   Status: ${realm.status}`);
      console.log(`   Custodians: ${realm.custodians.join(', ')}`);
      console.log(`   Capsules: ${realm.capsules.join(', ')}`);
      console.log(`   Authority: ${realm.governance?.authority_level || 'Unknown'}`);
      console.log(`   Ceremonies: ${realm.metadata?.ceremony_count || 0}`);
      if (realm.broadcast_endpoint) {
        console.log(`   Broadcast: ${realm.broadcast_endpoint}`);
      }
      console.log('');
    });
    
  } catch (error) {
    if (error.response?.status === 404) {
      console.error('No realms found');
    } else {
      console.error('Failed to list realms:', error.response?.data?.error || error.message);
    }
    process.exit(1);
  }
}

async function showRealm(options) {
  const { realmId } = options;
  
  if (!realmId) {
    console.error('Error: Realm ID is required');
    process.exit(1);
  }
  
  try {
    const response = await axios.get(`http://localhost:5000/api/realms/${encodeURIComponent(realmId)}`);
    const realm = response.data;
    
    console.log(`🏛️  ${realm.name}`);
    console.log(`━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━`);
    console.log(`Realm ID:      ${realm.realm_id}`);
    console.log(`Status:        ${realm.status}`);
    console.log(`Custodians:    ${realm.custodians.join(', ')}`);
    console.log(`Capsules:      ${realm.capsules.join(', ')}`);
    console.log('');
    
    console.log('Governance:');
    console.log(`  Authority Level:    ${realm.governance?.authority_level || 'Unknown'}`);
    console.log(`  Requires Witness:   ${realm.governance?.requires_witness ? 'Yes' : 'No'}`);
    console.log(`  Max Seal Level:     ${realm.governance?.max_seal_level || 'Unknown'}`);
    console.log('');
    
    if (realm.metadata) {
      console.log('Metadata:');
      console.log(`  Created:            ${realm.metadata.created || 'Unknown'}`);
      console.log(`  Last Ceremony:      ${realm.metadata.last_ceremony || 'Never'}`);
      console.log(`  Ceremony Count:     ${realm.metadata.ceremony_count || 0}`);
      if (realm.metadata.tags?.length > 0) {
        console.log(`  Tags:               ${realm.metadata.tags.join(', ')}`);
      }
    }
    
    if (realm.broadcast_endpoint) {
      console.log('');
      console.log(`Broadcast Endpoint: ${realm.broadcast_endpoint}`);
    }
    
  } catch (error) {
    if (error.response?.status === 404) {
      console.error(`Realm '${realmId}' not found`);
    } else {
      console.error('Failed to get realm details:', error.response?.data?.error || error.message);
    }
    process.exit(1);
  }
}

module.exports = { listRealms, showRealm };
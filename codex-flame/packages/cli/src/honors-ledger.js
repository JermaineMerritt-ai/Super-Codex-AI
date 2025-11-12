const axios = require('axios');
const fs = require('fs').promises;

async function addToLedger(options) {
  const { name, deed, insignia, notes, authority, realm, seal, witnesses } = options;
  
  if (!name || !deed || !insignia) {
    console.error('Error: Name, deed, and insignia are required');
    process.exit(1);
  }

  try {
    const honorData = {
      name,
      deed,
      insignia,
      notes: notes || '',
      authority: authority || 'Council',
      realm: realm || '',
      seal: seal || 'Eternal',
      witnesses: witnesses ? witnesses.split(',').map(w => w.trim()) : []
    };

    const response = await axios.post('http://localhost:5000/api/honors-ledger/entries', honorData);
    const result = response.data;
    
    console.log('🏆 Honor added to ledger successfully!');
    console.log('');
    console.log(`Honor ID:    ${result.honor_id}`);
    console.log(`Name:        ${result.entry.name}`);
    console.log(`Deed:        ${result.entry.deed}`);
    console.log(`Insignia:    ${result.entry.insignia}`);
    console.log(`Date:        ${result.entry.date}`);
    console.log(`Authority:   ${result.entry.authority}`);
    console.log(`Seal:        ${result.entry.seal}`);
    
    if (result.entry.realm) {
      console.log(`Realm:       ${result.entry.realm}`);
    }
    
    if (result.entry.witnesses?.length > 0) {
      console.log(`Witnesses:   ${result.entry.witnesses.join(', ')}`);
    }
    
    if (result.entry.notes) {
      console.log(`Notes:       ${result.entry.notes}`);
    }
    
    console.log('');
    console.log('📊 Ledger Statistics:');
    console.log(`Total Honors: ${result.ledger_stats.total_honors}`);
    console.log(`Sacred Seals: ${result.ledger_stats.seal_counts.sacred}`);
    console.log(`Eternal Seals: ${result.ledger_stats.seal_counts.eternal}`);
    
  } catch (error) {
    console.error('Failed to add honor to ledger:', error.response?.data?.error || error.message);
    process.exit(1);
  }
}

async function showLedger(options) {
  try {
    const response = await axios.get('http://localhost:5000/api/honors-ledger');
    const ledger = response.data;
    
    console.log('🏆 HONORS LEDGER');
    console.log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━');
    console.log(`Version: ${ledger.honors_version}`);
    console.log(`Total Honors: ${ledger.metadata?.total_honors || 0}`);
    console.log(`Last Updated: ${ledger.metadata?.last_updated || 'Unknown'}`);
    console.log('');
    
    if (ledger.entries?.length > 0) {
      ledger.entries.forEach((entry, index) => {
        console.log(`${index + 1}. ${entry.honor_id} - ${entry.name}`);
        console.log(`   Deed: ${entry.deed}`);
        console.log(`   Insignia: ${entry.insignia}`);
        console.log(`   Date: ${entry.date} | Authority: ${entry.authority} | Seal: ${entry.seal}`);
        
        if (entry.realm) {
          console.log(`   Realm: ${entry.realm}`);
        }
        
        if (entry.witnesses?.length > 0) {
          console.log(`   Witnesses: ${entry.witnesses.join(', ')}`);
        }
        
        if (entry.notes) {
          console.log(`   Notes: ${entry.notes}`);
        }
        
        console.log('');
      });
    } else {
      console.log('No honor entries found.');
    }
    
    if (ledger.metadata?.seal_counts) {
      console.log('📊 Seal Distribution:');
      const counts = ledger.metadata.seal_counts;
      if (counts.sacred > 0) console.log(`   Sacred: ${counts.sacred}`);
      if (counts.immutable > 0) console.log(`   Immutable: ${counts.immutable}`);
      if (counts.eternal > 0) console.log(`   Eternal: ${counts.eternal}`);
      if (counts.temporal > 0) console.log(`   Temporal: ${counts.temporal}`);
    }
    
  } catch (error) {
    if (error.response?.status === 404) {
      console.error('Honors ledger not found');
    } else {
      console.error('Failed to retrieve honors ledger:', error.response?.data?.error || error.message);
    }
    process.exit(1);
  }
}

async function showHonor(options) {
  const { honorId } = options;
  
  if (!honorId) {
    console.error('Error: Honor ID is required');
    process.exit(1);
  }
  
  try {
    const response = await axios.get(`http://localhost:5000/api/honors-ledger/entries/${honorId}`);
    const honor = response.data;
    
    console.log(`🏆 Honor Entry: ${honor.honor_id}`);
    console.log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━');
    console.log(`Name:        ${honor.name}`);
    console.log(`Deed:        ${honor.deed}`);
    console.log(`Insignia:    ${honor.insignia}`);
    console.log(`Date:        ${honor.date}`);
    console.log(`Authority:   ${honor.authority}`);
    console.log(`Seal:        ${honor.seal}`);
    
    if (honor.realm) {
      console.log(`Realm:       ${honor.realm}`);
    }
    
    if (honor.witnesses?.length > 0) {
      console.log(`Witnesses:   ${honor.witnesses.join(', ')}`);
    }
    
    if (honor.notes) {
      console.log(`Notes:       ${honor.notes}`);
    }
    
  } catch (error) {
    if (error.response?.status === 404) {
      console.error(`Honor entry '${honorId}' not found`);
    } else {
      console.error('Failed to get honor details:', error.response?.data?.error || error.message);
    }
    process.exit(1);
  }
}

module.exports = { addToLedger, showLedger, showHonor };
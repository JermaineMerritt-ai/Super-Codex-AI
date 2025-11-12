const fs = require('fs').promises;
const path = require('path');

async function grant(options) {
  const { recipient, achievement } = options;
  
  if (!recipient || !achievement) {
    console.error('Error: Recipient and achievement are required');
    process.exit(1);
  }

  try {
    const honorId = `HNR-${new Date().getFullYear()}-${String(Date.now()).slice(-3)}`;
    
    const honor = {
      honor_id: honorId,
      recipient,
      realm: "Default",
      achievement,
      timestamp: new Date().toISOString(),
      seal: "Eternal",
      verification: {
        ceremony_refs: [],
        audit_passed: true
      }
    };

    const honorPath = path.join(__dirname, '../../../artifacts/honors', `${honorId}.json`);
    await fs.writeFile(honorPath, JSON.stringify(honor, null, 2));
    
    console.log(`Honor granted: ${honorId}`);
    console.log(`Recipient: ${recipient}`);
    console.log(`Achievement: ${achievement}`);
    
  } catch (error) {
    console.error('Honor grant failed:', error.message);
    process.exit(1);
  }
}

module.exports = { grant };
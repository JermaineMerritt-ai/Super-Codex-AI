#!/usr/bin/env node

const axios = require('axios');
const { Command } = require('commander');

const API_BASE = process.env.AXIOM_API_BASE || 'http://localhost:8080';

const program = new Command();

program
  .name('axiom-flame')
  .description('Ceremonial governance CLI')
  .version('1.0.0');

program
  .command('reason')
  .description('Submit a reasoning request')
  .option('-a, --actor <actor>', 'ceremony actor', 'Custodian')
  .option('-r, --realm <realm>', 'realm identifier', 'Unspecified')
  .option('-c, --capsule <capsule>', 'capsule type', 'General')
  .option('-i, --intent <intent>', 'reasoning intent', 'Reasoning')
  .option('-s, --seal <seal>', 'governance seal', 'Eternal')
  .option('-p, --prompt <prompt>', 'reasoning prompt')
  .action(async (options) => {
    try {
      const payload = {
        actor: options.actor,
        realm: options.realm,
        capsule: options.capsule,
        intent: options.intent,
        seal: options.seal,
        input: options.prompt ? { prompt: options.prompt } : {}
      };

      const response = await axios.post(`${API_BASE}/reason`, payload);
      const result = response.data;

      console.log('✅ Reasoning completed successfully');
      console.log(`📋 Dispatch ID: ${result.dispatch_id}`);
      console.log(`📝 Summary: ${result.summary}`);
    } catch (error) {
      console.error('❌ Reasoning failed:', error.response?.data?.error || error.message);
      process.exit(1);
    }
  });

program
  .command('replay <dispatch-id>')
  .description('Generate replay for a ceremony')
  .action(async (dispatchId) => {
    try {
      const response = await axios.post(`${API_BASE}/replay`, { dispatch_id: dispatchId });
      const result = response.data;

      if (result.ok) {
        console.log('✅ Replay generated successfully');
        console.log(`🔄 Replay ID: ${result.replay.replay_id}`);
        console.log(`📅 Timestamp: ${result.replay.timestamp}`);
        console.log(`🏛️ Realm: ${result.replay.realm}`);
        console.log(`📦 Capsule: ${result.replay.capsule}`);
        console.log(`✅ Audit Status: ${result.replay.audit.status}`);
      } else {
        console.error('❌ Replay failed:', result.error);
        process.exit(1);
      }
    } catch (error) {
      console.error('❌ Replay failed:', error.response?.data?.error || error.message);
      process.exit(1);
    }
  });

program
  .command('audit <dispatch-id>')
  .description('Audit a ceremony dispatch')
  .action(async (dispatchId) => {
    try {
      const response = await axios.post(`${API_BASE}/audit`, { dispatch_id: dispatchId });
      const result = response.data;

      console.log(`🔍 Audit Results for ${result.dispatch_id}:`);
      if (result.ok) {
        console.log('✅ Status: Present in ledger');
      } else {
        console.log('❌ Status: Missing from ledger');
      }
    } catch (error) {
      console.error('❌ Audit failed:', error.response?.data?.error || error.message);
      process.exit(1);
    }
  });

program
  .command('health')
  .description('Check API health')
  .action(async () => {
    try {
      const response = await axios.get(`${API_BASE}/health`);
      const result = response.data;

      console.log('✅ API Health Check:');
      console.log(`📊 Status: ${result.status}`);
      console.log(`⏰ Time: ${result.time}`);
    } catch (error) {
      console.error('❌ Health check failed:', error.message);
      process.exit(1);
    }
  });

// Legacy ceremony command for backwards compatibility
program
  .command('ceremony')
  .description('Dispatch a ceremony (legacy)')
  .option('-a, --actor <actor>', 'ceremony actor')
  .option('-r, --realm <realm>', 'realm identifier')
  .option('-c, --capsule <capsule>', 'capsule type')  
  .action(async (options) => {
    console.log('ℹ️  Using legacy ceremony command. Consider using "reason" instead.');
    
    if (!options.actor || !options.realm || !options.capsule) {
      console.error('❌ Actor, realm, and capsule are required for legacy ceremony');
      process.exit(1);
    }

    try {
      const response = await axios.post(`${API_BASE}/api/reasoning`, {
        actor: options.actor,
        realm: options.realm,
        capsule: options.capsule,
        intent: 'Ceremony.Legacy',
        input: { prompt: `${options.capsule} ceremony for ${options.realm}` }
      });

      console.log('✅ Legacy ceremony completed');
      console.log('📋 Entry:', response.data);
    } catch (error) {
      console.error('❌ Legacy ceremony failed:', error.response?.data?.error || error.message);
      process.exit(1);
    }
  });

program.parse();
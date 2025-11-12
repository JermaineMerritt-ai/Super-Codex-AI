// frontend/test-api.js
// Test script demonstrating the TypeScript API client usage

import { apiClient, createWebSocket } from './src/api.js';

async function testApiClient() {
  console.log('🚀 Testing CodexDominion.app API Client...\n');

  try {
    // Health check
    console.log('1. Testing health check...');
    const health = await apiClient.health.live();
    console.log('✅ Health:', health);

    // Authentication
    console.log('\n2. Testing authentication...');
    const auth = await apiClient.auth.login({ 
      username: 'admin', 
      password: 'secret' 
    });
    console.log('✅ Auth successful. Token:', auth.access_token.substring(0, 20) + '...');
    console.log('✅ User:', auth.user);

    // Workflow management
    console.log('\n3. Testing workflow management...');
    const workflows = await apiClient.workflow.list(auth.access_token);
    console.log('✅ Workflows found:', workflows.length);
    workflows.forEach((wf, i) => {
      console.log(`   ${i + 1}. ${wf.name} - Status: ${wf.status}`);
    });

    // Axiom ceremonial operations
    console.log('\n4. Testing axiom ceremonial operations...');
    const ceremony = await apiClient.axiom.reason({
      actor: "Custodian",
      realm: "PL-001", 
      capsule: "Sovereign Crown",
      intent: "Crown.Invocation"
    }, auth.access_token);
    console.log('✅ Ceremony invoked:', ceremony.dispatch_id);
    console.log('✅ Ceremony status:', ceremony.status);

    // Real-time updates
    console.log('\n5. Testing real-time WebSocket connection...');
    const ws = createWebSocket(auth.access_token, (data) => {
      console.log('📡 Real-time update received:', data);
    });
    
    console.log('✅ WebSocket created. Connection state:', ws.readyState);
    
    // Wait a moment to see if we get any real-time updates
    setTimeout(() => {
      console.log('🔌 WebSocket final state:', ws.readyState);
      ws.close();
      console.log('\n🎉 API Client test completed successfully!');
    }, 2000);

    // Test logout
    console.log('\n6. Testing logout...');
    await apiClient.auth.logout(auth.access_token);
    console.log('✅ Logout successful');

  } catch (error) {
    console.error('❌ Error during API test:', error.message);
    console.error('Stack:', error.stack);
  }
}

// Run the test if this script is executed directly
if (import.meta.url === `file://${process.argv[1]}`) {
  testApiClient();
}

export { testApiClient };
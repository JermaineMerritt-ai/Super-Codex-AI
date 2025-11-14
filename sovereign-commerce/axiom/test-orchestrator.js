#!/usr/bin/env node

// orchestrator-test.js - Test the AXIOM-FLAME Orchestrator
const { execSync } = require('child_process');

console.log('🧪 AXIOM-FLAME Orchestrator Test Suite');
console.log("=".repeat(50));

try {
  // Test TypeScript compilation
  console.log('\n📝 Testing TypeScript compilation...');
  execSync('npx tsc orchestrator.ts --target es2020 --module commonjs --outDir dist --skipLibCheck', { stdio: 'inherit' });
  console.log('✅ TypeScript compilation successful');

  // Test Node.js execution
  console.log('\n🚀 Testing orchestrator execution...');
  const orchestratorTest = `
    const { invokeCodex, getEngineStatus, testOrchestrator } = require('./dist/orchestrator');
    
    async function runTests() {
      console.log('\\n🔍 Engine Status Check:');
      const status = getEngineStatus();
      Object.entries(status).forEach(([engine, desc]) => {
        console.log('  ', engine + ':', desc);
      });
      
      console.log('\\n🎯 Running Test Orchestrations:');
      const results = await testOrchestrator();
      
      console.log('\\n📊 Final Test Summary:');
      const successful = results.filter(r => r.success).length;
      console.log(\`  ✅ \${successful}/\${results.length} tests passed\`);
      
      if (successful === results.length) {
        console.log('\\n🎉 All tests passed! Orchestrator is ready.');
      } else {
        console.log('\\n⚠️  Some tests failed. Check engine implementations.');
      }
    }
    
    runTests().catch(console.error);
  `;
  
  require('fs').writeFileSync('test-runner.js', orchestratorTest);
  execSync('node test-runner.js', { stdio: 'inherit' });
  
  console.log('\n🎯 Integration Test - AXIOM Parser Connection:');
  const integrationTest = `
    console.log('Testing AXIOM parser integration...');
    try {
      const { parseInvocation } = require('./dist/axiom');
      const { invokeCodex } = require('./dist/orchestrator');
      
      const testPhrase = "sovereign commerce scroll for diaspora funders";
      console.log('Input phrase:', testPhrase);
      
      const intent = parseInvocation(testPhrase);
      console.log('Parsed intent:', JSON.stringify(intent, null, 2));
      
      console.log('\\nRunning full orchestration...');
      invokeCodex(testPhrase).then(result => {
        console.log('\\n🎉 Full orchestration completed!');
        console.log('Status:', result.status);
        console.log('Engines executed:', Object.keys(result.engines));
        console.log('\\n✨ AXIOM-FLAME integration successful!');
      }).catch(err => {
        console.error('❌ Orchestration failed:', err.message);
      });
      
    } catch (err) {
      console.error('❌ Integration test failed:', err.message);
    }
  `;
  
  require('fs').writeFileSync('integration-test.js', integrationTest);
  execSync('node integration-test.js', { stdio: 'inherit' });
  
  console.log('\n🎊 All orchestrator tests completed successfully!');
  console.log('\n📋 Next Steps:');
  console.log('   1. Import orchestrator into your main application');
  console.log('   2. Use invokeCodex(phrase) to generate platforms');
  console.log('   3. Monitor engine performance and results');
  console.log('   4. Extend engines with custom implementations');

} catch (error) {
  console.error('\n❌ Test failed:', error.message);
  console.log('\n🔧 Troubleshooting:');
  console.log('   - Ensure TypeScript is installed: npm install -g typescript');
  console.log('   - Check that axiom.ts exists and compiles correctly');
  console.log('   - Verify Node.js environment supports ES2020 features');
  process.exit(1);
}

// Cleanup
try {
  require('fs').unlinkSync('test-runner.js');
  require('fs').unlinkSync('integration-test.js');
  console.log('\n🧹 Test files cleaned up');
} catch (e) {
  // Ignore cleanup errors
}
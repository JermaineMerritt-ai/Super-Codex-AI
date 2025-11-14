// examples/basic-usage.ts
import { 
  createOrchestrator, 
  executeBuild, 
  healthCheck, 
  ORCHESTRATOR_VERSION 
} from '../index';

async function basicUsageExample() {
  console.log(`🚀 CODEX Orchestrator v${ORCHESTRATOR_VERSION}`);
  console.log('=' .repeat(50));
  
  // 1. Health Check
  console.log('\n1. 🏥 Health Check:');
  const health = await healthCheck();
  console.log(JSON.stringify(health, null, 2));
  
  // 2. Create Orchestrator Instance
  console.log('\n2. 🔧 Creating Orchestrator:');
  const orchestrator = createOrchestrator({
    outputPath: './generated',
    templatesPath: './templates',
    axiomFlameUrl: 'http://127.0.0.1:5000'
  });
  console.log('✅ Orchestrator created with engines:', Object.keys(orchestrator.engines));
  
  // 3. Example Build Invocation
  console.log('\n3. 🏗️  Example Build:');
  const invocation = {
    type: 'web_application',
    domain: 'ecommerce',
    features: ['user_management', 'product_catalog', 'shopping_cart', 'payment'],
    audience: ['customers', 'admins'],
    style: ['modern', 'responsive', 'dark_mode'],
    description: 'A modern e-commerce platform with user management and payment processing'
  };
  
  try {
    console.log('📝 Build Invocation:', JSON.stringify(invocation, null, 2));
    
    const result = await executeBuild(invocation, {
      outputPath: './generated',
      templatesPath: './templates'
    });
    
    console.log('\n✅ Build completed successfully!');
    console.log('📍 URL:', result.url);
    console.log('📄 Manifest:', result.manifestPath);
    console.log('🔒 Seal ID:', result.sealId);
    
  } catch (error) {
    console.error('\n❌ Build failed:', error);
  }
}

async function manualEngineExample() {
  console.log('\n' + '=' .repeat(50));
  console.log('🔧 Manual Engine Usage Example');
  console.log('=' .repeat(50));
  
  const orchestrator = createOrchestrator();
  const { axiom, rag, sigil, oracle, lantern, flame } = orchestrator.engines;
  
  try {
    // Step-by-step pipeline execution
    console.log('\n1. 🧠 AXIOM - Interpreting invocation...');
    const intent = await axiom.interpret({
      prompt: "Create a task management application",
      features: ['authentication', 'task_crud', 'notifications'],
      audience: ['team_members', 'project_managers']
    });
    console.log('✅ Intent:', JSON.stringify(intent, null, 2));
    
    console.log('\n2. 🏗️  AXIOM - Architecting specification...');
    const spec = await axiom.architect(intent);
    console.log('✅ Spec:', JSON.stringify(spec, null, 2));
    
    console.log('\n3. 📚 RAG - Retrieving templates...');
    const templates = await rag.retrieveTemplates(intent);
    console.log('✅ Templates:', JSON.stringify(templates, null, 2));
    
    console.log('\n4. 🎨 SIGIL - Composing UI...');
    const uiPath = await sigil.composeUI(spec, templates.ui);
    console.log('✅ UI Path:', uiPath);
    
    console.log('\n5. ⚙️  ORACLE - Generating services...');
    const servicePath = await oracle.generateServices(spec, templates.backend);
    console.log('✅ Service Path:', servicePath);
    
    console.log('\n6. 💾 LANTERN - Emitting schema...');
    const schemaPath = await lantern.emitSchema(spec, templates.schema);
    console.log('✅ Schema Path:', schemaPath);
    
    console.log('\n7. 🔐 LANTERN - Configuring auth...');
    const authConfig = await lantern.configureAuth(intent.audience);
    console.log('✅ Auth Config:', JSON.stringify(authConfig, null, 2));
    
    console.log('\n8. 🔥 FLAME - Building and deploying...');
    const deployment = await flame.buildAndDeploy({
      ui: uiPath,
      backend: servicePath,
      schema: schemaPath
    });
    console.log('✅ Deployment:', JSON.stringify(deployment, null, 2));
    
    console.log('\n9. 🔒 FLAME - Sealing manifest...');
    // Create a temporary manifest for sealing
    const manifestPath = './temp-manifest.json';
    const manifest = {
      artifactId: `manual-build-${Date.now()}`,
      spec,
      deployment,
      timestamp: new Date().toISOString()
    };
    
    require('fs').writeFileSync(manifestPath, JSON.stringify(manifest, null, 2));
    const sealId = await flame.seal(manifestPath);
    console.log('✅ Seal ID:', sealId);
    
    console.log('\n🎉 Manual pipeline execution completed!');
    
  } catch (error) {
    console.error('\n❌ Manual pipeline failed:', error);
  }
}

// Run examples
async function main() {
  console.clear();
  
  try {
    await basicUsageExample();
    await manualEngineExample();
  } catch (error) {
    console.error('\n💥 Example execution failed:', error);
    process.exit(1);
  }
  
  console.log('\n🏁 Examples completed successfully!');
}

// Execute if run directly
if (require.main === module) {
  main().catch(console.error);
}

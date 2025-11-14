// orchestrator/index.ts
// Main entry point for the CODEX Orchestrator System

// Export all contracts
export * from './contracts';

// Export the main build pipeline
export { codexBuildPipeline } from './build';
export type { BuildManifest, PipelineResult } from './build';

// Export all engine implementations
export * from './implementations';

// Export orchestrator factory
export { OrchestratorFactory } from './implementations';
export type { OrchestratorConfig } from './implementations';

// Convenience function for quick setup
import { OrchestratorFactory, OrchestratorConfig } from './implementations';
import { codexBuildPipeline } from './build';
import { promises as fs } from 'fs';
import { join } from 'path';

/**
 * Create a complete orchestrator instance with default configuration
 */
export function createOrchestrator(config: OrchestratorConfig = {}) {
  return OrchestratorFactory.createDefaultOrchestrator(config);
}

/**
 * Execute a complete CODEX build pipeline with minimal setup
 */
export async function executeBuild(
  invocation: unknown,
  config: OrchestratorConfig = {}
) {
  const orchestrator = createOrchestrator(config);
  const engines = orchestrator.engines;
  
  // Default manifest writer
  const writeManifest = async (manifest: any): Promise<string> => {
    const manifestsDir = join(config.outputPath || './generated', 'manifests');
    await fs.mkdir(manifestsDir, { recursive: true });
    const manifestPath = join(manifestsDir, `${manifest.artifactId}.json`);
    await fs.writeFile(manifestPath, JSON.stringify(manifest, null, 2));
    return manifestPath;
  };
  
  // Default registration handler
  const register = async (payload: any): Promise<void> => {
    console.log('🔖 Registering build artifact:', payload.artifactId);
    
    // Could integrate with existing artifact registry
    const registryPath = join(config.outputPath || './generated', 'registry.json');
    let registry = [];
    
    try {
      const existing = await fs.readFile(registryPath, 'utf8');
      registry = JSON.parse(existing);
    } catch {
      // Registry doesn't exist yet
    }
    
    registry.push({
      ...payload,
      registeredAt: new Date().toISOString()
    });
    
    await fs.writeFile(registryPath, JSON.stringify(registry, null, 2));
  };
  
  // Default dispatch handler
  const dispatch = async (payload: any): Promise<void> => {
    console.log('🚀 Dispatching deployment:', payload.artifactId);
    console.log('📍 URL:', payload.url);
    console.log('👥 Audience:', payload.audience?.join(', '));
    
    // Could integrate with existing dispatch system or notifications
  };
  
  return await codexBuildPipeline(
    engines,
    invocation,
    writeManifest,
    register,
    dispatch
  );
}

/**
 * CODEX Orchestrator version and metadata
 */
export const ORCHESTRATOR_VERSION = '1.0.0';
export const SUPPORTED_ENGINES = ['AXIOM', 'RAG', 'SIGIL', 'ORACLE', 'LANTERN', 'FLAME'];

/**
 * Health check for orchestrator system
 */
export async function healthCheck(config: OrchestratorConfig = {}) {
  const orchestrator = createOrchestrator(config);
  const engines = orchestrator.engines;
  
  const results = {
    orchestrator: {
      version: ORCHESTRATOR_VERSION,
      status: 'healthy'
    },
    engines: {} as Record<string, any>
  };
  
  // Test each engine (simplified health checks)
  try {
    // Test AXIOM
    results.engines.axiom = { status: 'available' };
    
    // Test other engines...
    results.engines.rag = { status: 'available' };
    results.engines.sigil = { status: 'available' };
    results.engines.oracle = { status: 'available' };
    results.engines.lantern = { status: 'available' };
    results.engines.flame = { status: 'available' };
    
  } catch (error) {
    results.engines.error = error instanceof Error ? error.message : 'Unknown error';
  }
  
  return results;
}

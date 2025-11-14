# CODEX Orchestrator

## TypeScript Orchestration System for CODEX AI Platform

A comprehensive TypeScript-based orchestration system that coordinates the six core engines of the CODEX AI platform: AXIOM, RAG, SIGIL, ORACLE, LANTERN, and FLAME.

## 🚀 Quick Start

```typescript
import { executeBuild } from '@codex/orchestrator';

// Simple build execution
const result = await executeBuild({
  type: 'web_application',
  domain: 'ecommerce',
  features: ['authentication', 'api', 'database'],
  audience: ['users', 'admins'],
  style: ['modern', 'responsive']
});

console.log('Deployed at:', result.url);
console.log('Manifest:', result.manifestPath);
console.log('Sealed with:', result.sealId);
```

## 🏗️ Architecture

The orchestrator provides a unified interface to coordinate:

- **AXIOM**: Intent interpretation and application architecture
- **RAG**: Template retrieval and knowledge management  
- **SIGIL**: UI composition and frontend generation
- **ORACLE**: Service generation and backend logic
- **LANTERN**: Schema emission and authentication setup
- **FLAME**: Build, deployment, and ceremonial sealing

## 📋 Core Contracts

All engines implement well-defined TypeScript interfaces:

```typescript
// AXIOM - AI reasoning and architecture
export interface AXIOM {
  interpret(invocation: unknown): Promise<AxiomIntent>;
  architect(intent: AxiomIntent): Promise<AxiomSpec>;
}

// RAG - Template retrieval
export interface RAG {
  retrieveTemplates(intent: AxiomIntent): Promise<{
    ui: string[]; backend: string[]; schema: string[];
  }>;
}

// SIGIL - UI composition
export interface SIGIL {
  composeUI(spec: AxiomSpec, templates: string[]): Promise<string>;
}

// ORACLE - Service generation
export interface ORACLE {
  generateServices(spec: AxiomSpec, templates: string[]): Promise<string>;
}

// LANTERN - Schema and auth
export interface LANTERN {
  emitSchema(spec: AxiomSpec, templates: string[]): Promise<string>;
  configureAuth(roles: string[]): Promise<{ provider: string; configPath: string }>;
}

// FLAME - Deployment and sealing
export interface FLAME {
  buildAndDeploy(paths: { ui: string; backend: string; schema: string }): Promise<{
    url: string; version: string; checksum: string;
  }>;
  seal(manifestPath: string): Promise<string>;
}
```

## 🛠️ Usage Examples

### Basic Pipeline Execution

```typescript
import { createOrchestrator, codexBuildPipeline } from '@codex/orchestrator';

const orchestrator = createOrchestrator({
  axiomFlameUrl: 'http://127.0.0.1:5000',
  outputPath: './generated',
  templatesPath: './templates'
});

const result = await codexBuildPipeline(
  orchestrator.engines,
  invocation,
  writeManifest,
  register,
  dispatch
);
```

### Manual Engine Control

```typescript
const { axiom, rag, sigil, oracle, lantern, flame } = orchestrator.engines;

// Step-by-step execution
const intent = await axiom.interpret(invocation);
const spec = await axiom.architect(intent);
const templates = await rag.retrieveTemplates(intent);

const uiPath = await sigil.composeUI(spec, templates.ui);
const servicePath = await oracle.generateServices(spec, templates.backend);
const schemaPath = await lantern.emitSchema(spec, templates.schema);

const deployment = await flame.buildAndDeploy({
  ui: uiPath,
  backend: servicePath, 
  schema: schemaPath
});
```

### Health Monitoring

```typescript
import { healthCheck } from '@codex/orchestrator';

const health = await healthCheck();
console.log('System status:', health);
```

## 🔧 Configuration

```typescript
interface OrchestratorConfig {
  axiomFlameUrl?: string;     // AXIOM-FLAME service URL
  outputPath?: string;        // Generated files output path
  templatesPath?: string;     // Templates directory path
  deploymentPath?: string;    // Deployment artifacts path
}
```

## 📁 Generated Output Structure

```
generated/
├── ui/
│   ├── app-name/
│   │   ├── index.html
│   │   ├── styles.css
│   │   └── app.js
├── backend/
│   ├── app-name/
│   │   ├── main.py
│   │   ├── models.py
│   │   ├── routes.py
│   │   ├── requirements.txt
│   │   └── Dockerfile
├── schema/
│   ├── app-name/
│   │   ├── 001_create_tables.sql
│   │   ├── 002_create_indexes.sql
│   │   ├── models.py
│   │   └── alembic.ini
├── manifests/
│   └── codex-build-123456789.json
└── registry.json
```

## 🔗 Integration with AXIOM-FLAME

The orchestrator seamlessly integrates with the existing AXIOM-FLAME ceremonial system:

- **Ceremonial Reasoning**: Each engine operation creates ceremonial entries
- **Audit Trails**: Full replay capability through ceremonial logs
- **Seal Management**: Cryptographic sealing of deployment manifests
- **Registry Integration**: Automatic registration of build artifacts

## 🚦 Development

```bash
# Install dependencies
npm install

# Build TypeScript
npm run build

# Run in development mode
npm run dev

# Run examples
npm run example

# Run tests
npm test

# Lint and format
npm run lint
npm run format
```

## 📝 API Documentation

### Core Functions

- `createOrchestrator(config)` - Create orchestrator instance
- `executeBuild(invocation, config)` - Execute complete build pipeline
- `codexBuildPipeline(engines, ...)` - Core pipeline function
- `healthCheck(config)` - System health verification

### Engine Implementations

- `AxiomEngine` - AXIOM reasoning engine
- `RagEngine` - Template retrieval engine 
- `SigilEngine` - UI composition engine
- `OracleEngine` - Service generation engine
- `LanternEngine` - Schema and auth engine
- `FlameEngine` - Deployment and sealing engine

## 🏷️ Version Information

- **Version**: 1.0.0
- **Supported Engines**: AXIOM, RAG, SIGIL, ORACLE, LANTERN, FLAME
- **TypeScript**: 5.2+
- **Node.js**: 18+

## 🤝 Contributing

1. Follow the existing contract interfaces
2. Maintain integration with AXIOM-FLAME system
3. Add comprehensive TypeScript types
4. Include examples and documentation
5. Test with the existing ceremonial infrastructure

## 📄 License

MIT License - Part of the CODEX AI Platform

// implementations/index.ts
export { AxiomEngine } from './axiom-engine';
export { RagEngine } from './rag-engine';
export { SigilEngine } from './sigil-engine';
export { OracleEngine } from './oracle-engine';
export { LanternEngine } from './lantern-engine';
export { FlameEngine } from './flame-engine';

import { AxiomEngine } from './axiom-engine';
import { RagEngine } from './rag-engine';
import { SigilEngine } from './sigil-engine';
import { OracleEngine } from './oracle-engine';
import { LanternEngine } from './lantern-engine';
import { FlameEngine } from './flame-engine';
import type { AXIOM, RAG, SIGIL, ORACLE, LANTERN, FLAME } from '../contracts';

export interface OrchestratorConfig {
  axiomFlameUrl?: string;
  outputPath?: string;
  templatesPath?: string;
  deploymentPath?: string;
}

export class OrchestratorFactory {
  static createEngines(config: OrchestratorConfig = {}) {
    const {
      axiomFlameUrl = 'http://127.0.0.1:5000',
      outputPath = './generated',
      templatesPath = './templates',
      deploymentPath = './deployments'
    } = config;

    return {
      axiom: new AxiomEngine(axiomFlameUrl) as AXIOM,
      rag: new RagEngine(templatesPath) as RAG,
      sigil: new SigilEngine(outputPath, 'http://127.0.0.1:8080') as SIGIL,
      oracle: new OracleEngine(outputPath, 'http://127.0.0.1:8080') as ORACLE,
      lantern: new LanternEngine(outputPath, 'http://127.0.0.1:8080') as LANTERN,
      flame: new FlameEngine(axiomFlameUrl, deploymentPath) as FLAME
    };
  }

  static createDefaultOrchestrator(config: OrchestratorConfig = {}) {
    return {
      engines: OrchestratorFactory.createEngines(config),
      config
    };
  }
}

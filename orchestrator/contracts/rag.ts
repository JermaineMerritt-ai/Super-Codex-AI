// contracts/rag.ts
import { AxiomIntent } from './axiom';

export interface RAG {
  retrieveTemplates(intent: AxiomIntent): Promise<{
    ui: string[];
    backend: string[];
    schema: string[];
  }>;
}

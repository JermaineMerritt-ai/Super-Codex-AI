// contracts/sigil.ts
import { AxiomSpec } from './axiom';

export interface SIGIL {
  composeUI(spec: AxiomSpec, templates: string[]): Promise<string /* path */>;
}

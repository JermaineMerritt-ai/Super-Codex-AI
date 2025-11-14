// contracts/oracle.ts
import { AxiomSpec } from './axiom';

export interface ORACLE {
  generateServices(spec: AxiomSpec, templates: string[]): Promise<string /* path */>;
}

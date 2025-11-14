// contracts/lantern.ts
import { AxiomSpec } from './axiom';

export interface LANTERN {
  emitSchema(spec: AxiomSpec, templates: string[]): Promise<string /* path */>;
  configureAuth(roles: string[]): Promise<{ provider: string; configPath: string }>;
}

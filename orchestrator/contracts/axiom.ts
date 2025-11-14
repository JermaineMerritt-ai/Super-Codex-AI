// contracts/axiom.ts
export interface AxiomIntent {
  domain: string;
  audience: string[];
  style: string[];
  features: string[];
}

export interface AxiomSpec {
  appName: string;
  modules: string[];
  uiThemes: string[];
  apis: { name: string; route: string; method: string }[];
  dataModels: { name: string; fields: Record<string, string> }[];
}

export interface AXIOM {
  interpret(invocation: unknown): Promise<AxiomIntent>;
  architect(intent: AxiomIntent): Promise<AxiomSpec>;
}

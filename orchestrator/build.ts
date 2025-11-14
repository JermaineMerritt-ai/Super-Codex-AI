// orchestrator/build.ts
import type { AXIOM, RAG, SIGIL, ORACLE, LANTERN, FLAME } from "./contracts";

export async function codexBuildPipeline(
  engines: { axiom: AXIOM; rag: RAG; sigil: SIGIL; oracle: ORACLE; lantern: LANTERN; flame: FLAME },
  invocation: unknown,
  writeManifest: (m: any) => Promise<string /* manifestPath */>,
  register: (payload: any) => Promise<void>,
  dispatch: (payload: any) => Promise<void>
) {
  const intent = await engines.axiom.interpret(invocation);
  const spec   = await engines.axiom.architect(intent);
  const libs   = await engines.rag.retrieveTemplates(intent);

  const uiPath   = await engines.sigil.composeUI(spec, libs.ui);
  const svcPath  = await engines.oracle.generateServices(spec, libs.backend);
  const dbPath   = await engines.lantern.emitSchema(spec, libs.schema);
  await engines.lantern.configureAuth(intent.audience);

  const deploy   = await engines.flame.buildAndDeploy({ ui: uiPath, backend: svcPath, schema: dbPath });

  const manifest = {
    artifactId: `codex-build-${Date.now()}`,
    title: spec.appName,
    version: deploy.version,
    type: "app",
    engines: ["AXIOM","RAG","SIGIL","ORACLE","LANTERN","FLAME"],
    files: { ui: uiPath, backend: svcPath, schema: dbPath },
    outputs: { url: deploy.url, checksum: deploy.checksum }
  };

  const manifestPath = await writeManifest(manifest);
  const sealId = await engines.flame.seal(manifestPath);

  await register({ ...manifest, sealId });
  await dispatch({ artifactId: manifest.artifactId, url: deploy.url, audience: intent.audience });

  return { url: deploy.url, manifestPath, sealId };
}

// Helper types for the pipeline
export interface BuildManifest {
  artifactId: string;
  title: string;
  version: string;
  type: string;
  engines: string[];
  files: {
    ui: string;
    backend: string;
    schema: string;
  };
  outputs: {
    url: string;
    checksum: string;
  };
  sealId?: string;
}

export interface PipelineResult {
  url: string;
  manifestPath: string;
  sealId: string;
}

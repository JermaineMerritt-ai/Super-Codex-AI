// contracts/flame.ts
export interface FLAME {
  buildAndDeploy(paths: { ui: string; backend: string; schema: string }): Promise<{
    url: string;
    version: string;
    checksum: string;
  }>;
  seal(manifestPath: string): Promise<string /* seal-id */>;
}

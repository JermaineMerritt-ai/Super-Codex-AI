module.exports = function (wallaby) {
  return {
    files: [
      'src/**/*.ts',
      'src/**/*.vue',
      'src/**/*.tsx',
      '!src/**/*.test.ts',
      '!src/**/*.spec.ts',
      '!src/**/*.test.tsx',
      '!src/**/*.spec.tsx',
      'tsconfig.json',
      'package.json',
      'vite.config.ts'
    ],

    tests: [
      'src/**/*.test.ts',
      'src/**/*.spec.ts',
      'src/**/*.test.tsx',
      'src/**/*.spec.tsx',
      '__tests__/**/*.ts',
      '__tests__/**/*.tsx',
      'tests/**/*.ts',
      'tests/**/*.tsx'
    ],

    env: {
      type: 'node',
      runner: 'node'
    },

    testFramework: 'vitest',

    compilers: {
      '**/*.ts': wallaby.compilers.typeScript({
        module: 'esnext',
        target: 'esnext',
        esModuleInterop: true,
        allowSyntheticDefaultImports: true,
        resolveJsonModule: true,
        strict: true,
        skipLibCheck: true,
        forceConsistentCasingInFileNames: true,
        moduleResolution: 'node',
        jsx: 'preserve'
      }),
      '**/*.tsx': wallaby.compilers.typeScript({
        module: 'esnext',
        target: 'esnext',
        esModuleInterop: true,
        allowSyntheticDefaultImports: true,
        resolveJsonModule: true,
        strict: true,
        skipLibCheck: true,
        forceConsistentCasingInFileNames: true,
        moduleResolution: 'node',
        jsx: 'preserve'
      }),
      '**/*.vue': wallaby.compilers.vue({
        compilerOptions: {
          target: 'esnext',
          module: 'esnext',
          esModuleInterop: true,
          allowSyntheticDefaultImports: true,
          resolveJsonModule: true,
          strict: true,
          skipLibCheck: true,
          forceConsistentCasingInFileNames: true,
          moduleResolution: 'node'
        }
      })
    },

    setup: function (wallaby) {
      // Configure for Vue/Vite environment
      wallaby.testFramework.configure({
        globals: true,
        environment: 'jsdom'
      });
    },

    debug: true,
    reportConsoleErrorAsError: true,
    lowCoverageThreshold: 80
  };
};
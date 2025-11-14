module.exports = function (wallaby) {
  return {
    files: [
      'src/**/*.ts',
      '!src/**/*.test.ts',
      '!src/**/*.spec.ts',
      'tsconfig.json',
      'package.json'
    ],

    tests: [
      'src/**/*.test.ts',
      'src/**/*.spec.ts',
      '__tests__/**/*.ts',
      'tests/**/*.ts'
    ],

    env: {
      type: 'node',
      runner: 'node'
    },

    testFramework: 'jest',

    compilers: {
      '**/*.ts': wallaby.compilers.typeScript({
        module: 'commonjs',
        target: 'es2020',
        esModuleInterop: true,
        allowSyntheticDefaultImports: true,
        resolveJsonModule: true,
        strict: true,
        skipLibCheck: true,
        forceConsistentCasingInFileNames: true
      })
    },

    setup: function (wallaby) {
      const jestConfig = require('./jest.config.js');
      wallaby.testFramework.configure(jestConfig);
    },

    debug: true,
    reportConsoleErrorAsError: true,
    lowCoverageThreshold: 80
  };
};
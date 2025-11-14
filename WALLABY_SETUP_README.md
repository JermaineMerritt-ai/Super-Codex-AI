# Wallaby.js Setup Guide

Wallaby.js has been successfully installed for your CODEX AI projects! 🎉

## What is Wallaby.js?

Wallaby.js is an intelligent test runner for JavaScript and TypeScript that provides:
- **Real-time feedback** - See test results as you type
- **Live code coverage** - Visual indicators in your editor
- **Smart test execution** - Only runs affected tests
- **Advanced debugging** - Built-in debugging capabilities

## Installation Status

✅ **Orchestrator Project** (`/orchestrator/`)
- Framework: Jest + TypeScript
- Configuration: `wallaby.js`
- Test Framework: Jest with ts-jest

✅ **Codex-Flame Frontend** (`/codex-flame/packages/frontend/`)
- Framework: Vitest + Vue 3 + TypeScript
- Configuration: `wallaby.js`
- Test Framework: Vitest with Vue support

## How to Use Wallaby.js

### VS Code Setup

1. **Install the Wallaby.js Extension**:
   ```
   ext install WallabyJs.wallaby-vscode
   ```

2. **Start Wallaby.js**:
   - Open Command Palette (`Ctrl+Shift+P`)
   - Type: `Wallaby.js: Start`
   - Select your project (orchestrator or codex-flame frontend)

3. **View Results**:
   - Green squares: Passing tests
   - Red squares: Failing tests
   - Yellow squares: Code covered by tests
   - Red background: Uncovered code

### WebStorm/IntelliJ Setup

1. **Install Wallaby.js Plugin**:
   - Go to `File > Settings > Plugins`
   - Search for "Wallaby.js"
   - Install and restart

2. **Start Wallaby.js**:
   - Right-click on `wallaby.js` file
   - Select "Start Wallaby.js"

## Project-Specific Features

### Orchestrator Project
- **TypeScript Support**: Full TypeScript compilation
- **Jest Integration**: Uses Jest test framework
- **Node.js Environment**: Optimized for Node.js testing
- **Coverage Reports**: Generates detailed coverage reports

### Codex-Flame Frontend
- **Vue 3 Support**: Full Vue Single File Component support
- **Vitest Integration**: Modern testing framework
- **JSdom Environment**: Browser-like environment for DOM testing
- **TypeScript + Vue**: Full type checking for Vue components

## Example Test File

A sample test has been created at:
```
/orchestrator/src/wallaby-example.test.ts
```

This demonstrates:
- Basic test setup
- Async/await testing
- TypeScript integration

## Configuration Files

### Orchestrator (`/orchestrator/`)
- `wallaby.js` - Wallaby.js configuration
- `jest.config.js` - Jest configuration
- `tsconfig.json` - TypeScript configuration

### Codex-Flame Frontend (`/codex-flame/packages/frontend/`)
- `wallaby.js` - Wallaby.js configuration (Vue/Vitest)
- `vite.config.ts` - Vite configuration
- `tsconfig.json` - TypeScript configuration

## Commands

### Orchestrator
```bash
cd orchestrator
npm test          # Run tests with Jest
npm run test      # Same as above
```

### Codex-Flame Frontend
```bash
cd codex-flame/packages/frontend
npm test          # Run tests with Vitest
npm run test:coverage  # Run tests with coverage
```

## Benefits You'll Get

1. **Instant Feedback**: See test results immediately as you code
2. **Smart Testing**: Only affected tests run when you make changes
3. **Visual Coverage**: See which code is covered by tests
4. **Debugging**: Step through tests with advanced debugging tools
5. **Performance**: Much faster than traditional test runners

## Troubleshooting

### Common Issues

1. **Wallaby.js not starting**:
   - Ensure you have the VS Code extension installed
   - Check that Node.js is properly installed
   - Restart VS Code

2. **TypeScript compilation errors**:
   - Check `tsconfig.json` configuration
   - Ensure all dependencies are installed

3. **Test files not detected**:
   - Check file patterns in `wallaby.js`
   - Ensure test files follow naming conventions

### Getting Help

- **Wallaby.js Documentation**: https://wallabyjs.com/docs/
- **VS Code Extension**: https://marketplace.visualstudio.com/items?itemName=WallabyJs.wallaby-vscode
- **Support**: https://wallabyjs.com/support/

## Next Steps

1. **Install the VS Code extension** for Wallaby.js
2. **Start Wallaby.js** on your preferred project
3. **Write some tests** and watch them run in real-time
4. **Explore the coverage visualization** to see what code needs testing

Happy testing! 🚀
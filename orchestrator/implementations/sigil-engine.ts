// implementations/sigil-engine.ts
import { SIGIL, AxiomSpec } from '../contracts';
import { promises as fs } from 'fs';
import { join } from 'path';

export class SigilEngine implements SIGIL {
  private outputPath: string;
  private sigilServiceUrl: string;

  constructor(outputPath: string = './generated', sigilServiceUrl: string = 'http://127.0.0.1:8080') {
    this.outputPath = outputPath;
    this.sigilServiceUrl = sigilServiceUrl;
  }

  async composeUI(spec: AxiomSpec, templates: string[]): Promise<string> {
    // Integration with existing SIGIL system
    const uiPath = join(this.outputPath, 'ui', spec.appName);
    await fs.mkdir(uiPath, { recursive: true });

    // Call existing SIGIL service for UI generation
    const response = await fetch(`${this.sigilServiceUrl}/sigil/generate`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        spec,
        templates,
        type: 'ui'
      })
    });

    if (!response.ok) {
      throw new Error(`SIGIL UI composition failed: ${response.statusText}`);
    }

    const result = await response.json();
    
    // Generate UI files based on spec and templates
    await this.generateIndexHTML(uiPath, spec);
    await this.generateCSS(uiPath, spec);
    await this.generateJS(uiPath, spec);
    
    return uiPath;
  }

  private async generateIndexHTML(uiPath: string, spec: AxiomSpec): Promise<void> {
    const html = `
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>${spec.appName}</title>
    <link rel="stylesheet" href="./styles.css">
</head>
<body>
    <div id="app">
        <header class="app-header">
            <h1>${spec.appName}</h1>
            <nav>
                ${spec.apis.map(api => `<a href="#${api.name}">${api.name}</a>`).join(' | ')}
            </nav>
        </header>
        <main id="main-content">
            <!-- Generated content will be inserted here -->
        </main>
    </div>
    <script src="./app.js"></script>
</body>
</html>
`;
    await fs.writeFile(join(uiPath, 'index.html'), html);
  }

  private async generateCSS(uiPath: string, spec: AxiomSpec): Promise<void> {
    const css = `
/* Generated CSS for ${spec.appName} */
* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

body {
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    line-height: 1.6;
    color: #333;
}

.app-header {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    padding: 1rem 2rem;
    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.app-header h1 {
    margin-bottom: 0.5rem;
}

.app-header nav a {
    color: white;
    text-decoration: none;
    margin: 0 1rem;
    padding: 0.5rem 1rem;
    border-radius: 4px;
    transition: background-color 0.3s;
}

.app-header nav a:hover {
    background-color: rgba(255,255,255,0.2);
}

#main-content {
    padding: 2rem;
    max-width: 1200px;
    margin: 0 auto;
}

/* Theme-based styles */
${spec.uiThemes.includes('modern') ? `
.modern-card {
    background: white;
    border-radius: 8px;
    box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    padding: 1.5rem;
    margin: 1rem 0;
}
` : ''}

${spec.uiThemes.includes('responsive') ? `
@media (max-width: 768px) {
    .app-header {
        padding: 1rem;
    }
    
    .app-header nav {
        display: flex;
        flex-direction: column;
        gap: 0.5rem;
    }
    
    #main-content {
        padding: 1rem;
    }
}
` : ''}
`;
    await fs.writeFile(join(uiPath, 'styles.css'), css);
  }

  private async generateJS(uiPath: string, spec: AxiomSpec): Promise<void> {
    const js = `
// Generated JavaScript for ${spec.appName}
class ${spec.appName.replace(/[^a-zA-Z0-9]/g, '')}App {
    constructor() {
        this.apiBase = '/api';
        this.init();
    }

    init() {
        this.setupEventListeners();
        this.loadInitialData();
    }

    setupEventListeners() {
        // Setup navigation
        document.querySelectorAll('nav a').forEach(link => {
            link.addEventListener('click', (e) => {
                e.preventDefault();
                const section = e.target.getAttribute('href').substring(1);
                this.navigateToSection(section);
            });
        });
    }

    async loadInitialData() {
        try {
            // Load data for each API endpoint
            ${spec.apis.map(api => `
            if ('${api.method}' === 'GET') {
                await this.load${api.name.charAt(0).toUpperCase() + api.name.slice(1)}Data();
            }`).join('')}
        } catch (error) {
            console.error('Failed to load initial data:', error);
        }
    }

    navigateToSection(section) {
        console.log('Navigating to:', section);
        // Implementation for navigation
    }

    ${spec.apis.map(api => `
    async load${api.name.charAt(0).toUpperCase() + api.name.slice(1)}Data() {
        try {
            const response = await fetch(\`\${this.apiBase}${api.route}\`);
            const data = await response.json();
            console.log('${api.name} data:', data);
            return data;
        } catch (error) {
            console.error('Failed to load ${api.name} data:', error);
            throw error;
        }
    }`).join('')}
}

// Initialize the app when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    window.app = new ${spec.appName.replace(/[^a-zA-Z0-9]/g, '')}App();
});
`;
    await fs.writeFile(join(uiPath, 'app.js'), js);
  }
}

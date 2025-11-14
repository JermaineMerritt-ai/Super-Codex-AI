// implementations/flame-engine.ts
import { FLAME } from '../contracts';
import { promises as fs } from 'fs';
import { join } from 'path';
import { createHash } from 'crypto';

export class FlameEngine implements FLAME {
  private flameServiceUrl: string;
  private deploymentPath: string;

  constructor(flameServiceUrl: string = 'http://127.0.0.1:5000', deploymentPath: string = './deployments') {
    this.flameServiceUrl = flameServiceUrl;
    this.deploymentPath = deploymentPath;
  }

  async buildAndDeploy(paths: { ui: string; backend: string; schema: string }): Promise<{
    url: string;
    version: string;
    checksum: string;
  }> {
    // Integration with existing AXIOM-FLAME system
    const version = `v${Date.now()}`;
    const deploymentId = `deploy-${Date.now()}`;
    const deploymentDir = join(this.deploymentPath, deploymentId);
    
    await fs.mkdir(deploymentDir, { recursive: true });

    // Copy files to deployment directory
    await this.copyDirectory(paths.ui, join(deploymentDir, 'ui'));
    await this.copyDirectory(paths.backend, join(deploymentDir, 'backend'));
    await this.copyDirectory(paths.schema, join(deploymentDir, 'schema'));

    // Generate deployment configuration
    await this.generateDeploymentConfig(deploymentDir, deploymentId, paths);
    await this.generateDockerCompose(deploymentDir, deploymentId);
    await this.generateNginxConfig(deploymentDir, deploymentId);

    // Call existing FLAME service for ceremonial deployment
    const response = await fetch(`${this.flameServiceUrl}/flame/deploy`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        deploymentId,
        paths,
        version,
        actor: "Orchestrator",
        realm: "DEPLOYMENT"
      })
    });

    if (!response.ok) {
      throw new Error(`FLAME deployment failed: ${response.statusText}`);
    }

    const deploymentResult = await response.json();
    const checksum = await this.generateChecksum(deploymentDir);
    const url = `http://localhost:8080/${deploymentId}`;

    return {
      url,
      version,
      checksum
    };
  }

  async seal(manifestPath: string): Promise<string> {
    const sealId = `SEAL-${Date.now()}-${Math.random().toString(36).substr(2, 9)}`;
    
    // Integration with existing AXIOM-FLAME ceremonial sealing
    const response = await fetch(`${this.flameServiceUrl}/flame/seal`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        sealId,
        manifestPath,
        actor: "Orchestrator",
        realm: "SEALING",
        timestamp: new Date().toISOString()
      })
    });

    if (!response.ok) {
      throw new Error(`FLAME sealing failed: ${response.statusText}`);
    }

    // Create local seal record
    const sealRecord = {
      sealId,
      manifestPath,
      timestamp: new Date().toISOString(),
      checksum: await this.generateFileChecksum(manifestPath),
      status: 'sealed'
    };

    const sealsDir = join(this.deploymentPath, 'seals');
    await fs.mkdir(sealsDir, { recursive: true });
    await fs.writeFile(
      join(sealsDir, `${sealId}.json`),
      JSON.stringify(sealRecord, null, 2)
    );

    return sealId;
  }

  private async copyDirectory(src: string, dest: string): Promise<void> {
    await fs.mkdir(dest, { recursive: true });
    const entries = await fs.readdir(src, { withFileTypes: true });
    
    for (const entry of entries) {
      const srcPath = join(src, entry.name);
      const destPath = join(dest, entry.name);
      
      if (entry.isDirectory()) {
        await this.copyDirectory(srcPath, destPath);
      } else {
        await fs.copyFile(srcPath, destPath);
      }
    }
  }

  private async generateDeploymentConfig(deploymentDir: string, deploymentId: string, paths: any): Promise<void> {
    const config = {
      deploymentId,
      timestamp: new Date().toISOString(),
      paths,
      services: {
        frontend: {
          type: 'static',
          port: 3000,
          path: './ui'
        },
        backend: {
          type: 'fastapi',
          port: 8080,
          path: './backend',
          healthCheck: '/health'
        },
        database: {
          type: 'postgresql',
          port: 5432,
          schema: './schema'
        }
      },
      environment: {
        NODE_ENV: 'production',
        PYTHONPATH: '/app',
        DATABASE_URL: `postgresql://user:password@db:5432/${deploymentId}_db`
      }
    };
    
    await fs.writeFile(
      join(deploymentDir, 'deployment-config.json'),
      JSON.stringify(config, null, 2)
    );
  }

  private async generateDockerCompose(deploymentDir: string, deploymentId: string): Promise<void> {
    const dockerCompose = `
version: '3.8'

services:
  frontend:
    build:
      context: ./ui
    ports:
      - "3000:3000"
    environment:
      - NODE_ENV=production
    depends_on:
      - backend
    networks:
      - ${deploymentId}_network

  backend:
    build:
      context: ./backend
    ports:
      - "8080:8080"
    environment:
      - DATABASE_URL=postgresql://postgres:password@db:5432/${deploymentId}_db
      - PYTHONPATH=/app
    depends_on:
      - db
      - redis
    volumes:
      - ./backend:/app
    networks:
      - ${deploymentId}_network
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8080/health"]
      interval: 30s
      timeout: 10s
      retries: 3

  db:
    image: postgres:15
    environment:
      - POSTGRES_DB=${deploymentId}_db
      - POSTGRES_USER=postgres
      - POSTGRES_PASSWORD=password
    volumes:
      - postgres_data:/var/lib/postgresql/data
      - ./schema:/docker-entrypoint-initdb.d
    ports:
      - "5432:5432"
    networks:
      - ${deploymentId}_network

  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"
    networks:
      - ${deploymentId}_network

  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf
    depends_on:
      - frontend
      - backend
    networks:
      - ${deploymentId}_network

volumes:
  postgres_data:

networks:
  ${deploymentId}_network:
    driver: bridge
`;
    await fs.writeFile(join(deploymentDir, 'docker-compose.yml'), dockerCompose);
  }

  private async generateNginxConfig(deploymentDir: string, deploymentId: string): Promise<void> {
    const nginxConfig = `
events {
    worker_connections 1024;
}

http {
    upstream frontend {
        server frontend:3000;
    }
    
    upstream backend {
        server backend:8080;
    }
    
    server {
        listen 80;
        server_name localhost;
        
        # Frontend routes
        location / {
            proxy_pass http://frontend;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
        }
        
        # Backend API routes
        location /api/ {
            proxy_pass http://backend;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
        }
        
        # Health check
        location /health {
            proxy_pass http://backend/health;
            access_log off;
        }
        
        # Static files
        location /static/ {
            alias /usr/share/nginx/html/static/;
            expires 1y;
            add_header Cache-Control "public, immutable";
        }
    }
}
`;
    await fs.writeFile(join(deploymentDir, 'nginx.conf'), nginxConfig);
  }

  private async generateChecksum(directory: string): Promise<string> {
    const hash = createHash('sha256');
    const files = await this.getAllFiles(directory);
    
    for (const file of files.sort()) {
      const content = await fs.readFile(file);
      hash.update(content);
    }
    
    return hash.digest('hex');
  }

  private async generateFileChecksum(filePath: string): Promise<string> {
    const content = await fs.readFile(filePath);
    return createHash('sha256').update(content).digest('hex');
  }

  private async getAllFiles(dir: string): Promise<string[]> {
    const files = [];
    const entries = await fs.readdir(dir, { withFileTypes: true });
    
    for (const entry of entries) {
      const fullPath = join(dir, entry.name);
      if (entry.isDirectory()) {
        files.push(...await this.getAllFiles(fullPath));
      } else {
        files.push(fullPath);
      }
    }
    
    return files;
  }
}

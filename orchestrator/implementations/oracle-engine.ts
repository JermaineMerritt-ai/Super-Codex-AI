// implementations/oracle-engine.ts
import { ORACLE, AxiomSpec } from '../contracts';
import { promises as fs } from 'fs';
import { join } from 'path';

export class OracleEngine implements ORACLE {
  private outputPath: string;
  private oracleServiceUrl: string;

  constructor(outputPath: string = './generated', oracleServiceUrl: string = 'http://127.0.0.1:8080') {
    this.outputPath = outputPath;
    this.oracleServiceUrl = oracleServiceUrl;
  }

  async generateServices(spec: AxiomSpec, templates: string[]): Promise<string> {
    // Integration with existing ORACLE system
    const servicePath = join(this.outputPath, 'backend', spec.appName);
    await fs.mkdir(servicePath, { recursive: true });

    // Call existing ORACLE service for backend generation
    const response = await fetch(`${this.oracleServiceUrl}/oracle/generate`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        spec,
        templates,
        type: 'backend'
      })
    });

    if (!response.ok) {
      throw new Error(`ORACLE service generation failed: ${response.statusText}`);
    }

    // Generate FastAPI backend files
    await this.generateMainPy(servicePath, spec);
    await this.generateModels(servicePath, spec);
    await this.generateRoutes(servicePath, spec);
    await this.generateRequirements(servicePath, spec);
    await this.generateDockerfile(servicePath, spec);
    
    return servicePath;
  }

  private async generateMainPy(servicePath: string, spec: AxiomSpec): Promise<void> {
    const mainPy = `
# Generated FastAPI application for ${spec.appName}
from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import uvicorn
from typing import List, Optional
import logging

from models import ${spec.dataModels.map(model => model.name).join(', ')}
from routes import ${spec.apis.map(api => `${api.name}_router`).join(', ')}

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="${spec.appName}",
    description="Generated API for ${spec.appName}",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Security
security = HTTPBearer()

# Include routers
${spec.apis.map(api => `app.include_router(${api.name}_router, prefix="${api.route.split('/')[0] + '/' + api.route.split('/')[1]}", tags=["${api.name}"])`).join('\n')}

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "${spec.appName}"}

@app.get("/")
async def root():
    return {"message": "Welcome to ${spec.appName} API", "version": "1.0.0"}

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8080,
        reload=True,
        log_level="info"
    )
`;
    await fs.writeFile(join(servicePath, 'main.py'), mainPy);
  }

  private async generateModels(servicePath: string, spec: AxiomSpec): Promise<void> {
    const models = `
# Generated Pydantic models for ${spec.appName}
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

${spec.dataModels.map(model => `
class ${model.name}(BaseModel):
${Object.entries(model.fields).map(([field, type]) => {
  const pythonType = this.mapFieldType(type);
  return `    ${field}: ${pythonType}`;
}).join('\n')}
    
    class Config:
        orm_mode = True
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }

class ${model.name}Create(BaseModel):
${Object.entries(model.fields).filter(([field, _]) => field !== 'id').map(([field, type]) => {
  const pythonType = this.mapFieldType(type);
  return `    ${field}: ${pythonType}`;
}).join('\n')}

class ${model.name}Update(BaseModel):
${Object.entries(model.fields).filter(([field, _]) => field !== 'id').map(([field, type]) => {
  const pythonType = this.mapFieldType(type, true);
  return `    ${field}: ${pythonType}`;
}).join('\n')}
`).join('')}
`;
    await fs.writeFile(join(servicePath, 'models.py'), models);
  }

  private async generateRoutes(servicePath: string, spec: AxiomSpec): Promise<void> {
    const routes = `
# Generated API routes for ${spec.appName}
from fastapi import APIRouter, HTTPException, Depends
from typing import List
from models import *

${spec.apis.map(api => `
${api.name}_router = APIRouter()

@${api.name}_router.${api.method.toLowerCase()}("${api.route}")
async def ${api.name}_endpoint():
    """${api.name} endpoint - implement your logic here"""
    try:
        # TODO: Implement ${api.name} logic
        return {"message": "${api.name} endpoint called", "method": "${api.method}"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
`).join('')}
`;
    await fs.writeFile(join(servicePath, 'routes.py'), routes);
  }

  private async generateRequirements(servicePath: string, spec: AxiomSpec): Promise<void> {
    const requirements = `
# Generated requirements for ${spec.appName}
fastapi>=0.104.1
uvicorn[standard]>=0.24.0
pydantic>=2.4.2
python-multipart>=0.0.6
python-jose[cryptography]>=3.3.0
passlib[bcrypt]>=1.7.4
sqlalchemy>=2.0.23
alembic>=1.12.1
psycopg2-binary>=2.9.7
redis>=5.0.1
celery>=5.3.4
pytest>=7.4.3
pytest-asyncio>=0.21.1
requests>=2.31.0
aiofiles>=23.2.1
python-dotenv>=1.0.0
`;
    await fs.writeFile(join(servicePath, 'requirements.txt'), requirements);
  }

  private async generateDockerfile(servicePath: string, spec: AxiomSpec): Promise<void> {
    const dockerfile = `
# Generated Dockerfile for ${spec.appName}
FROM python:3.11-slim

WORKDIR /app

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Expose port
EXPOSE 8080

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8080/health || exit 1

# Run the application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]
`;
    await fs.writeFile(join(servicePath, 'Dockerfile'), dockerfile);
  }

  private mapFieldType(type: string, optional: boolean = false): string {
    const typeMap: Record<string, string> = {
      'string': 'str',
      'number': 'int',
      'float': 'float',
      'boolean': 'bool',
      'datetime': 'datetime',
      'date': 'date'
    };
    
    const pythonType = typeMap[type] || 'str';
    return optional ? `Optional[${pythonType}] = None` : pythonType;
  }
}

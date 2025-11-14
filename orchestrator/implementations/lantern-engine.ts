// implementations/lantern-engine.ts
import { LANTERN, AxiomSpec } from '../contracts';
import { promises as fs } from 'fs';
import { join } from 'path';

export class LanternEngine implements LANTERN {
  private outputPath: string;
  private lanternServiceUrl: string;

  constructor(outputPath: string = './generated', lanternServiceUrl: string = 'http://127.0.0.1:8080') {
    this.outputPath = outputPath;
    this.lanternServiceUrl = lanternServiceUrl;
  }

  async emitSchema(spec: AxiomSpec, templates: string[]): Promise<string> {
    // Integration with existing LANTERN system
    const schemaPath = join(this.outputPath, 'schema', spec.appName);
    await fs.mkdir(schemaPath, { recursive: true });

    // Call existing LANTERN service for schema generation
    const response = await fetch(`${this.lanternServiceUrl}/lantern/generate`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        spec,
        templates,
        type: 'schema'
      })
    });

    if (!response.ok) {
      throw new Error(`LANTERN schema emission failed: ${response.statusText}`);
    }

    // Generate database schema files
    await this.generateCreateTables(schemaPath, spec);
    await this.generateIndexes(schemaPath, spec);
    await this.generateAlembicConfig(schemaPath, spec);
    await this.generateSQLAlchemyModels(schemaPath, spec);
    
    return schemaPath;
  }

  async configureAuth(roles: string[]): Promise<{ provider: string; configPath: string }> {
    const authPath = join(this.outputPath, 'auth');
    await fs.mkdir(authPath, { recursive: true });

    // Generate JWT auth configuration
    const authConfig = {
      provider: 'jwt',
      secret: this.generateSecret(),
      algorithm: 'HS256',
      expiration: '24h',
      roles: roles
    };

    const configPath = join(authPath, 'auth-config.json');
    await fs.writeFile(configPath, JSON.stringify(authConfig, null, 2));

    // Generate auth service code
    await this.generateAuthService(authPath, roles);

    return {
      provider: 'jwt',
      configPath
    };
  }

  private async generateCreateTables(schemaPath: string, spec: AxiomSpec): Promise<void> {
    const sql = `
-- Generated database schema for ${spec.appName}
-- Created at: ${new Date().toISOString()}

${spec.dataModels.map(model => {
  const fields = Object.entries(model.fields).map(([field, type]) => {
    const sqlType = this.mapToSQLType(type);
    const constraints = field === 'id' ? 'PRIMARY KEY' : 
                       field.includes('email') ? 'UNIQUE NOT NULL' :
                       type === 'datetime' ? 'NOT NULL DEFAULT CURRENT_TIMESTAMP' : 'NOT NULL';
    return `    ${field} ${sqlType} ${constraints}`;
  }).join(',\n');
  
  return `
CREATE TABLE ${model.name.toLowerCase()}s (
${fields}
);
`;
}).join('')}

-- Foreign key constraints
${this.generateForeignKeys(spec)}

-- Insert default data
${this.generateDefaultData(spec)}
`;
    await fs.writeFile(join(schemaPath, '001_create_tables.sql'), sql);
  }

  private async generateIndexes(schemaPath: string, spec: AxiomSpec): Promise<void> {
    const indexes = `
-- Generated indexes for ${spec.appName}
-- Created at: ${new Date().toISOString()}

${spec.dataModels.map(model => {
  const indexSql = [];
  
  // Index on common fields
  Object.entries(model.fields).forEach(([field, type]) => {
    if (field.includes('email') || field.includes('username')) {
      indexSql.push(`CREATE INDEX idx_${model.name.toLowerCase()}_${field} ON ${model.name.toLowerCase()}s(${field});`);
    }
    if (field.includes('created') || field.includes('updated')) {
      indexSql.push(`CREATE INDEX idx_${model.name.toLowerCase()}_${field} ON ${model.name.toLowerCase()}s(${field});`);
    }
    if (field.includes('Id') && field !== 'id') {
      indexSql.push(`CREATE INDEX idx_${model.name.toLowerCase()}_${field} ON ${model.name.toLowerCase()}s(${field});`);
    }
  });
  
  return indexSql.join('\n');
}).join('\n')}
`;
    await fs.writeFile(join(schemaPath, '002_create_indexes.sql'), indexes);
  }

  private async generateAlembicConfig(schemaPath: string, spec: AxiomSpec): Promise<void> {
    const alembicIni = `
# Generated Alembic configuration for ${spec.appName}
[alembic]
script_location = alembic
prepend_sys_path = .
version_path_separator = os
sqlalchemy.url = postgresql://user:password@localhost:5432/${spec.appName.toLowerCase()}_db

[post_write_hooks]
hooks = black
black.type = console_scripts
black.entrypoint = black
black.options = -l 79 REVISION_SCRIPT_FILENAME

[loggers]
keys = root,sqlalchemy,alembic

[handlers]
keys = console

[formatters]
keys = generic

[logger_root]
level = WARN
handlers = console
qualname =

[logger_sqlalchemy]
level = WARN
handlers =
qualname = sqlalchemy.engine

[logger_alembic]
level = INFO
handlers =
qualname = alembic

[handler_console]
class = StreamHandler
args = (sys.stderr,)
level = NOTSET
formatter = generic

[formatter_generic]
format = %(levelname)-5.5s [%(name)s] %(message)s
datefmt = %H:%M:%S
`;
    await fs.writeFile(join(schemaPath, 'alembic.ini'), alembicIni);
  }

  private async generateSQLAlchemyModels(schemaPath: string, spec: AxiomSpec): Promise<void> {
    const models = `
# Generated SQLAlchemy models for ${spec.appName}
from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime

Base = declarative_base()

${spec.dataModels.map(model => `
class ${model.name}(Base):
    __tablename__ = '${model.name.toLowerCase()}s'
    
${Object.entries(model.fields).map(([field, type]) => {
  const sqlType = this.mapToSQLAlchemyType(type);
  const constraints = field === 'id' ? ', primary_key=True' :
                     field.includes('email') ? ', unique=True, nullable=False' :
                     type === 'datetime' ? ', nullable=False, default=datetime.utcnow' : ', nullable=False';
  return `    ${field} = Column(${sqlType}${constraints})`;
}).join('\n')}
    
    def __repr__(self):
        return f"<${model.name}(id={self.id})>"
    
    def to_dict(self):
        return {
${Object.keys(model.fields).map(field => `            '${field}': self.${field}`).join(',\n')}
        }
`).join('')}
`;
    await fs.writeFile(join(schemaPath, 'models.py'), models);
  }

  private async generateAuthService(authPath: string, roles: string[]): Promise<void> {
    const authService = `
# Generated authentication service
from fastapi import HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import JWTError, jwt
from passlib.context import CryptContext
from datetime import datetime, timedelta
from typing import Optional, List
import json

# Load auth configuration
with open('auth-config.json', 'r') as f:
    AUTH_CONFIG = json.load(f)

SECRET_KEY = AUTH_CONFIG['secret']
ALGORITHM = AUTH_CONFIG['algorithm']
ACCESS_TOKEN_EXPIRE_HOURS = 24

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
security = HTTPBearer()

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(hours=ACCESS_TOKEN_EXPIRE_HOURS)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    try:
        payload = jwt.decode(credentials.credentials, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=401, detail="Invalid authentication credentials")
        return payload
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid authentication credentials")

def require_role(required_roles: List[str]):
    def role_checker(current_user = Depends(verify_token)):
        user_roles = current_user.get("roles", [])
        if not any(role in user_roles for role in required_roles):
            raise HTTPException(status_code=403, detail="Insufficient permissions")
        return current_user
    return role_checker

# Available roles: ${roles.join(', ')}
${roles.map(role => `
def require_${role.toLowerCase()}(current_user = Depends(verify_token)):
    return require_role(["${role}"])(current_user)
`).join('')}
`;
    await fs.writeFile(join(authPath, 'auth_service.py'), authService);
  }

  private generateSecret(): string {
    return require('crypto').randomBytes(32).toString('hex');
  }

  private mapToSQLType(type: string): string {
    const typeMap: Record<string, string> = {
      'string': 'VARCHAR(255)',
      'number': 'INTEGER',
      'float': 'DECIMAL(10,2)',
      'boolean': 'BOOLEAN',
      'datetime': 'TIMESTAMP',
      'date': 'DATE',
      'text': 'TEXT'
    };
    return typeMap[type] || 'VARCHAR(255)';
  }

  private mapToSQLAlchemyType(type: string): string {
    const typeMap: Record<string, string> = {
      'string': 'String(255)',
      'number': 'Integer',
      'float': 'DECIMAL(10,2)',
      'boolean': 'Boolean',
      'datetime': 'DateTime',
      'date': 'Date',
      'text': 'Text'
    };
    return typeMap[type] || 'String(255)';
  }

  private generateForeignKeys(spec: AxiomSpec): string {
    // Simple heuristic for foreign keys based on field names
    const fks = [];
    for (const model of spec.dataModels) {
      for (const [field, type] of Object.entries(model.fields)) {
        if (field.endsWith('Id') && field !== 'id') {
          const referencedTable = field.replace('Id', '').toLowerCase() + 's';
          fks.push(`ALTER TABLE ${model.name.toLowerCase()}s ADD CONSTRAINT fk_${model.name.toLowerCase()}_${field} FOREIGN KEY (${field}) REFERENCES ${referencedTable}(id);`);
        }
      }
    }
    return fks.join('\n');
  }

  private generateDefaultData(spec: AxiomSpec): string {
    return `
-- Default data for ${spec.appName}
-- Add your default/seed data here
`;
  }
}

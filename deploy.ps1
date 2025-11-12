# Super-Codex-AI PowerShell Deployment Script
# This script handles complete deployment including environment setup, Docker containers, and health checks

param(
    [string]$Domain = "your-domain.com",
    [int]$BackendPort = 8010,
    [int]$FrontendPort = 3001,
    [int]$AxiomPort = 5010,
    [string]$DbName = "super_codex_ai",
    [string]$DbUser = "codex_user",
    [switch]$SkipTests,
    [switch]$Help
)

# Colors for output
$Red = "`e[31m"
$Green = "`e[32m"
$Yellow = "`e[33m"
$Blue = "`e[34m"
$Reset = "`e[0m"

function Write-Status {
    param([string]$Message)
    Write-Host "${Blue}[INFO]${Reset} $Message"
}

function Write-Success {
    param([string]$Message)
    Write-Host "${Green}[SUCCESS]${Reset} $Message"
}

function Write-Warning {
    param([string]$Message)
    Write-Host "${Yellow}[WARNING]${Reset} $Message"
}

function Write-ErrorMsg {
    param([string]$Message)
    Write-Host "${Red}[ERROR]${Reset} $Message"
}

function Test-Command {
    param([string]$Command)
    try {
        Get-Command $Command -ErrorAction Stop | Out-Null
        return $true
    }
    catch {
        return $false
    }
}

function Wait-ForService {
    param(
        [string]$Url,
        [string]$ServiceName,
        [int]$MaxAttempts = 30
    )
    
    Write-Status "Waiting for $ServiceName to be ready..."
    
    for ($attempt = 1; $attempt -le $MaxAttempts; $attempt++) {
        try {
            $response = Invoke-WebRequest -Uri $Url -Method GET -TimeoutSec 5 -ErrorAction Stop
            if ($response.StatusCode -eq 200) {
                Write-Success "$ServiceName is ready!"
                return $true
            }
        }
        catch {
            Write-Host "." -NoNewline
            Start-Sleep -Seconds 2
        }
    }
    
    Write-ErrorMsg "$ServiceName failed to start after $($MaxAttempts * 2) seconds"
    return $false
}

function New-EnvFile {
    Write-Status "Generating environment configuration..."
    
    # Generate secure secrets
    $JwtSecret = -join ((1..64) | ForEach { '{0:X}' -f (Get-Random -Maximum 16) })
    $CliApiKey = -join ((1..32) | ForEach { '{0:X}' -f (Get-Random -Maximum 16) })
    $ApiKey = -join ((1..32) | ForEach { '{0:X}' -f (Get-Random -Maximum 16) })
    $WebhookSecret = -join ((1..32) | ForEach { '{0:X}' -f (Get-Random -Maximum 16) })
    $EncryptionKey = -join ((1..64) | ForEach { '{0:X}' -f (Get-Random -Maximum 16) })
    $DbPassword = -join ((1..32) | ForEach { '{0:X}' -f (Get-Random -Maximum 16) })
    
    # Create .env file
    $envContent = @"
# Super-Codex-AI Environment Configuration
# Generated on $(Get-Date)

# Domain Configuration
DOMAIN=$Domain
BACKEND_PORT=$BackendPort
FRONTEND_PORT=$FrontendPort
AXIOM_PORT=$AxiomPort

# Security Keys (Keep these secure!)
JWT_SECRET=$JwtSecret
CLI_API_KEY=$CliApiKey
API_KEY=$ApiKey
WEBHOOK_SECRET=$WebhookSecret
ENCRYPTION_KEY=$EncryptionKey

# Database Configuration
DATABASE_URL=postgresql://${DbUser}:${DbPassword}@postgres:5432/${DbName}
DB_NAME=$DbName
DB_USER=$DbUser
DB_PASSWORD=$DbPassword

# Redis Configuration
REDIS_URL=redis://redis:6379

# Application Settings
ENVIRONMENT=production
DEBUG=false
CORS_ORIGINS=https://${Domain},http://localhost:${FrontendPort}

# AXIOM Configuration
AXIOM_BASE=http://axiom-flame:${AxiomPort}

# Node Environment
NODE_ENV=production

# FastAPI Settings
FASTAPI_ENV=production
"@
    
    $envContent | Out-File -FilePath ".env" -Encoding UTF8
    Write-Success "Environment file created: .env"
}

function Test-Prerequisites {
    Write-Status "Checking prerequisites..."
    
    $missingTools = @()
    
    if (-not (Test-Command "docker")) {
        $missingTools += "docker"
    }
    
    if (-not (Test-Command "docker-compose")) {
        try {
            & docker compose version | Out-Null
        }
        catch {
            $missingTools += "docker-compose"
        }
    }
    
    if ($missingTools.Count -gt 0) {
        Write-ErrorMsg "Missing required tools: $($missingTools -join ', ')"
        Write-ErrorMsg "Please install the missing tools and run this script again."
        exit 1
    }
    
    # Check if Docker is running
    try {
        & docker info | Out-Null
    }
    catch {
        Write-ErrorMsg "Docker is not running. Please start Docker and try again."
        exit 1
    }
    
    Write-Success "All prerequisites satisfied"
}

function New-DockerCompose {
    Write-Status "Creating Docker Compose configuration..."
    
    $dockerComposeContent = @'
version: '3.8'

services:
  # PostgreSQL Database
  postgres:
    image: postgres:15-alpine
    environment:
      POSTGRES_DB: ${DB_NAME}
      POSTGRES_USER: ${DB_USER}
      POSTGRES_PASSWORD: ${DB_PASSWORD}
    volumes:
      - postgres_data:/var/lib/postgresql/data
      - ./init.sql:/docker-entrypoint-initdb.d/init.sql:ro
    ports:
      - "5432:5432"
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U ${DB_USER} -d ${DB_NAME}"]
      interval: 10s
      timeout: 5s
      retries: 5
    restart: unless-stopped

  # Redis Cache
  redis:
    image: redis:7-alpine
    command: redis-server --appendonly yes
    volumes:
      - redis_data:/data
    ports:
      - "6379:6379"
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 10s
      timeout: 5s
      retries: 5
    restart: unless-stopped

  # FastAPI Backend
  backend:
    build:
      context: .
      dockerfile: Dockerfile.backend
    environment:
      - DATABASE_URL=${DATABASE_URL}
      - REDIS_URL=${REDIS_URL}
      - JWT_SECRET=${JWT_SECRET}
      - CLI_API_KEY=${CLI_API_KEY}
      - API_KEY=${API_KEY}
      - WEBHOOK_SECRET=${WEBHOOK_SECRET}
      - ENVIRONMENT=${ENVIRONMENT}
      - DEBUG=${DEBUG}
      - CORS_ORIGINS=${CORS_ORIGINS}
    volumes:
      - ./app:/app/app:ro
      - ./logs:/app/logs
    ports:
      - "${BACKEND_PORT}:8000"
    depends_on:
      postgres:
        condition: service_healthy
      redis:
        condition: service_healthy
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
      interval: 30s
      timeout: 10s
      retries: 3
    restart: unless-stopped

  # AXIOM Flame Service
  axiom-flame:
    build:
      context: .
      dockerfile: Dockerfile.axiom
    environment:
      - CLI_API_KEY=${CLI_API_KEY}
      - ENCRYPTION_KEY=${ENCRYPTION_KEY}
      - DATABASE_URL=${DATABASE_URL}
    volumes:
      - ./axiom-flame:/app/axiom-flame:ro
      - ./artifacts:/app/artifacts
      - ./logs:/app/logs
    ports:
      - "${AXIOM_PORT}:5000"
    depends_on:
      postgres:
        condition: service_healthy
      redis:
        condition: service_healthy
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:5000/health"]
      interval: 30s
      timeout: 10s
      retries: 3
    restart: unless-stopped

  # React Frontend
  frontend:
    build:
      context: .
      dockerfile: Dockerfile.frontend
    environment:
      - NODE_ENV=${NODE_ENV}
      - REACT_APP_API_BASE_URL=https://${DOMAIN}/api
      - REACT_APP_WS_BASE_URL=wss://${DOMAIN}/ws
    ports:
      - "${FRONTEND_PORT}:3000"
    depends_on:
      - backend
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:3000"]
      interval: 30s
      timeout: 10s
      retries: 3
    restart: unless-stopped

  # Caddy Reverse Proxy
  caddy:
    image: caddy:2-alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./Caddyfile:/etc/caddy/Caddyfile:ro
      - caddy_data:/data
      - caddy_config:/config
    depends_on:
      - backend
      - frontend
      - axiom-flame
    restart: unless-stopped

volumes:
  postgres_data:
  redis_data:
  caddy_data:
  caddy_config:

networks:
  default:
    driver: bridge
'@
    
    $dockerComposeContent | Out-File -FilePath "docker-compose.yml" -Encoding UTF8
    Write-Success "Docker Compose configuration created"
}

function New-Dockerfiles {
    Write-Status "Creating Dockerfiles..."
    
    # Backend Dockerfile
    $backendDockerfile = @'
FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY app ./app
COPY *.py ./

# Create non-root user
RUN useradd -m -u 1000 appuser && chown -R appuser:appuser /app
USER appuser

# Health check
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
'@
    
    $backendDockerfile | Out-File -FilePath "Dockerfile.backend" -Encoding UTF8
    
    # AXIOM Dockerfile
    $axiomDockerfile = @'
FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies for AXIOM
RUN pip install --no-cache-dir flask requests cryptography flask-cors

# Copy AXIOM code
COPY axiom-flame ./axiom-flame
COPY artifacts ./artifacts

# Create non-root user
RUN useradd -m -u 1000 appuser && chown -R appuser:appuser /app
USER appuser

# Health check
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:5000/health || exit 1

EXPOSE 5000

CMD ["python", "axiom-flame/packages/api/app.py"]
'@
    
    $axiomDockerfile | Out-File -FilePath "Dockerfile.axiom" -Encoding UTF8
    
    Write-Success "Dockerfiles created successfully"
}

function New-DbInit {
    Write-Status "Creating database initialization script..."
    
    $initSql = @'
-- Super-Codex-AI Database Initialization
-- This script sets up the initial database schema and data

-- Create extensions
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pg_trgm";

-- Create schemas
CREATE SCHEMA IF NOT EXISTS axiom;
CREATE SCHEMA IF NOT EXISTS auth;
CREATE SCHEMA IF NOT EXISTS logs;

-- Set search path
SET search_path TO public, axiom, auth, logs;

-- Create users table
CREATE TABLE IF NOT EXISTS auth.users (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    sub VARCHAR(255) UNIQUE NOT NULL,
    email VARCHAR(255) UNIQUE,
    roles TEXT[] DEFAULT '{}',
    permissions TEXT[] DEFAULT '{}',
    is_active BOOLEAN DEFAULT true,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Create sessions table
CREATE TABLE IF NOT EXISTS auth.sessions (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID REFERENCES auth.users(id) ON DELETE CASCADE,
    token_hash VARCHAR(255) NOT NULL,
    expires_at TIMESTAMP WITH TIME ZONE NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    last_used TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    ip_address INET,
    user_agent TEXT
);

-- Create ceremonies table
CREATE TABLE IF NOT EXISTS axiom.ceremonies (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    dispatch_id VARCHAR(255) UNIQUE NOT NULL,
    actor VARCHAR(255) NOT NULL,
    realm VARCHAR(255) NOT NULL,
    capsule VARCHAR(255) NOT NULL,
    intent VARCHAR(255) NOT NULL,
    status VARCHAR(50) DEFAULT 'pending',
    payload JSONB,
    result JSONB,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Create audit logs table
CREATE TABLE IF NOT EXISTS logs.audit_logs (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID REFERENCES auth.users(id),
    action VARCHAR(255) NOT NULL,
    resource VARCHAR(255),
    resource_id VARCHAR(255),
    details JSONB,
    ip_address INET,
    user_agent TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Create indexes
CREATE INDEX IF NOT EXISTS idx_users_sub ON auth.users(sub);
CREATE INDEX IF NOT EXISTS idx_users_email ON auth.users(email);
CREATE INDEX IF NOT EXISTS idx_users_roles ON auth.users USING GIN(roles);
CREATE INDEX IF NOT EXISTS idx_sessions_user_id ON auth.sessions(user_id);
CREATE INDEX IF NOT EXISTS idx_sessions_token_hash ON auth.sessions(token_hash);
CREATE INDEX IF NOT EXISTS idx_sessions_expires_at ON auth.sessions(expires_at);
CREATE INDEX IF NOT EXISTS idx_ceremonies_dispatch_id ON axiom.ceremonies(dispatch_id);
CREATE INDEX IF NOT EXISTS idx_ceremonies_actor ON axiom.ceremonies(actor);
CREATE INDEX IF NOT EXISTS idx_ceremonies_status ON axiom.ceremonies(status);
CREATE INDEX IF NOT EXISTS idx_ceremonies_created_at ON axiom.ceremonies(created_at);
CREATE INDEX IF NOT EXISTS idx_audit_logs_user_id ON logs.audit_logs(user_id);
CREATE INDEX IF NOT EXISTS idx_audit_logs_action ON logs.audit_logs(action);
CREATE INDEX IF NOT EXISTS idx_audit_logs_created_at ON logs.audit_logs(created_at);

-- Insert default admin user
INSERT INTO auth.users (sub, email, roles, permissions) VALUES 
    ('admin', 'admin@super-codex-ai.com', ARRAY['admin', 'operator'], ARRAY['*'])
ON CONFLICT (sub) DO NOTHING;

-- Grant permissions
GRANT USAGE ON SCHEMA auth TO postgres;
GRANT USAGE ON SCHEMA axiom TO postgres;
GRANT USAGE ON SCHEMA logs TO postgres;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA auth TO postgres;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA axiom TO postgres;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA logs TO postgres;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA auth TO postgres;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA axiom TO postgres;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA logs TO postgres;
'@
    
    $initSql | Out-File -FilePath "init.sql" -Encoding UTF8
    Write-Success "Database initialization script created"
}

function Start-Deployment {
    Write-Status "Starting Super-Codex-AI deployment..."
    
    # Stop existing containers
    try {
        & docker compose ps | Out-Null
        Write-Status "Stopping existing containers..."
        & docker compose down
    }
    catch {
        # No existing containers
    }
    
    # Build and start services
    Write-Status "Building and starting services..."
    & docker compose up -d --build
    
    if ($LASTEXITCODE -eq 0) {
        Write-Success "Services started successfully"
    }
    else {
        Write-ErrorMsg "Failed to start services"
        exit 1
    }
}

function Start-Migrations {
    Write-Status "Running database migrations..."
    
    # Wait a bit for database to be ready
    Start-Sleep -Seconds 10
    
    Write-Success "Database migrations completed (using init script)"
}

function Start-SmokeTests {
    if ($SkipTests) {
        Write-Warning "Skipping smoke tests as requested"
        return
    }
    
    Write-Status "Running smoke tests..."
    
    $baseUrl = "https://$Domain"
    $testsPassed = 0
    $totalTests = 0
    
    # Test cases
    $tests = @(
        @{Url = "$baseUrl/api/health"; Name = "Backend Health Check"}
        @{Url = "$baseUrl/api/health/live"; Name = "Backend Liveness"}
        @{Url = "$baseUrl/api/health/ready"; Name = "Backend Readiness"}
        @{Url = "$baseUrl/"; Name = "Frontend Access"}
        @{Url = "http://localhost:$AxiomPort/health"; Name = "AXIOM Health"}
    )
    
    foreach ($test in $tests) {
        $totalTests++
        Write-Status "Testing: $($test.Name) ($($test.Url))"
        
        try {
            $response = Invoke-WebRequest -Uri $test.Url -Method GET -TimeoutSec 10 -ErrorAction Stop
            if ($response.StatusCode -eq 200) {
                Write-Success "✅ $($test.Name): PASSED"
                $testsPassed++
            }
            else {
                Write-ErrorMsg "❌ $($test.Name): FAILED (Status: $($response.StatusCode))"
            }
        }
        catch {
            Write-ErrorMsg "❌ $($test.Name): FAILED (Error: $($_.Exception.Message))"
        }
    }
    
    Write-Host ""
    Write-Status "Smoke Tests Summary: $testsPassed/$totalTests tests passed"
    
    if ($testsPassed -eq $totalTests) {
        Write-Success "All smoke tests passed!"
    }
    else {
        Write-Warning "Some smoke tests failed. Check service logs for details."
    }
}

function Show-DeploymentSummary {
    Write-Host ""
    Write-Host "==================================================================" -ForegroundColor Green
    Write-Success "🎉 Super-Codex-AI Deployment Complete!"
    Write-Host "==================================================================" -ForegroundColor Green
    Write-Host ""
    Write-Host "📋 Service URLs:" -ForegroundColor Cyan
    Write-Host "  🌐 Frontend:     https://$Domain" -ForegroundColor White
    Write-Host "  🔧 Backend API:  https://$Domain/api" -ForegroundColor White
    Write-Host "  ⚡ AXIOM Flame:  https://$Domain/axiom" -ForegroundColor White
    Write-Host "  📊 Database:     localhost:5432" -ForegroundColor White
    Write-Host "  🔄 Redis:        localhost:6379" -ForegroundColor White
    Write-Host ""
    Write-Host "📊 Management Commands:" -ForegroundColor Cyan
    Write-Host "  View logs:       docker compose logs -f [service]" -ForegroundColor White
    Write-Host "  Stop services:   docker compose down" -ForegroundColor White
    Write-Host "  Restart:         docker compose restart [service]" -ForegroundColor White
    Write-Host "  Shell access:    docker compose exec [service] /bin/bash" -ForegroundColor White
    Write-Host ""
    Write-Host "🧪 Health Check URLs:" -ForegroundColor Cyan
    Write-Host "  Invoke-WebRequest https://$Domain/api/health" -ForegroundColor White
    Write-Host "  Invoke-WebRequest https://$Domain/api/health/live" -ForegroundColor White
    Write-Host "  Invoke-WebRequest https://$Domain/api/health/ready" -ForegroundColor White
    Write-Host ""
    Write-Status "Deployment completed at $(Get-Date)"
    Write-Host "==================================================================" -ForegroundColor Green
}

function Show-Help {
    Write-Host @"
Super-Codex-AI Deployment Script

Usage: .\deploy.ps1 [OPTIONS]

Parameters:
  -Domain <string>       Set the domain name (default: your-domain.com)
  -BackendPort <int>     Backend service port (default: 8010)
  -FrontendPort <int>    Frontend service port (default: 3001)
  -AxiomPort <int>       AXIOM service port (default: 5010)
  -DbName <string>       Database name (default: super_codex_ai)
  -DbUser <string>       Database user (default: codex_user)
  -SkipTests             Skip smoke tests
  -Help                  Show this help message

Examples:
  .\deploy.ps1 -Domain "my-domain.com"
  .\deploy.ps1 -Domain "localhost" -SkipTests
  .\deploy.ps1 -BackendPort 9000 -FrontendPort 4000
"@
}

# Main execution
function Main {
    if ($Help) {
        Show-Help
        exit 0
    }
    
    Write-Host "🚀 Super-Codex-AI PowerShell Deployment Script" -ForegroundColor Magenta
    Write-Host "=============================================" -ForegroundColor Magenta
    Write-Host ""
    
    # Main deployment process
    Test-Prerequisites
    New-EnvFile
    New-DockerCompose
    New-Dockerfiles
    New-DbInit
    Start-Deployment
    
    # Wait for services to be ready
    Start-Sleep -Seconds 10
    
    Start-Migrations
    
    # Run smoke tests unless skipped
    Start-Sleep -Seconds 5  # Additional wait for services to stabilize
    Start-SmokeTests
    
    Show-DeploymentSummary
}

# Handle script interruption
trap {
    Write-ErrorMsg "Deployment interrupted!"
    exit 1
}

# Run main function
Main
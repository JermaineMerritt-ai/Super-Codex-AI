#!/usr/bin/env bash
# Super-Codex-AI Deployment Script
# This script handles complete deployment including environment setup, Docker containers, and health checks

set -euo pipefail

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
DOMAIN=${DOMAIN:-"your-domain.com"}
BACKEND_PORT=${BACKEND_PORT:-8010}
FRONTEND_PORT=${FRONTEND_PORT:-3001}
AXIOM_PORT=${AXIOM_PORT:-5010}
DB_NAME=${DB_NAME:-"super_codex_ai"}
DB_USER=${DB_USER:-"codex_user"}
DB_PASSWORD=${DB_PASSWORD:-$(openssl rand -hex 16)}

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Function to check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Function to wait for service to be ready
wait_for_service() {
    local url=$1
    local service_name=$2
    local max_attempts=30
    local attempt=1

    print_status "Waiting for $service_name to be ready..."
    
    while [ $attempt -le $max_attempts ]; do
        if curl -sSf "$url" >/dev/null 2>&1; then
            print_success "$service_name is ready!"
            return 0
        fi
        
        echo -n "."
        sleep 2
        ((attempt++))
    done
    
    print_error "$service_name failed to start after $((max_attempts * 2)) seconds"
    return 1
}

# Function to generate environment file
generate_env_file() {
    print_status "Generating environment configuration..."
    
    # Generate secure secrets
    export JWT_SECRET=$(openssl rand -hex 32)
    export CLI_API_KEY=$(openssl rand -hex 16)
    export API_KEY=$(openssl rand -hex 16)
    export WEBHOOK_SECRET=$(openssl rand -hex 16)
    export ENCRYPTION_KEY=$(openssl rand -hex 32)
    
    # Set environment variables
    export AXIOM_BASE=http://axiom-flame:${AXIOM_PORT}
    export DATABASE_URL="postgresql://${DB_USER}:${DB_PASSWORD}@postgres:5432/${DB_NAME}"
    export REDIS_URL="redis://redis:6379"
    export ENVIRONMENT="production"
    export DEBUG="false"
    export CORS_ORIGINS="https://${DOMAIN},http://localhost:${FRONTEND_PORT}"
    
    # Create .env file
    cat > .env << EOF
# Super-Codex-AI Environment Configuration
# Generated on $(date)

# Domain Configuration
DOMAIN=${DOMAIN}
BACKEND_PORT=${BACKEND_PORT}
FRONTEND_PORT=${FRONTEND_PORT}
AXIOM_PORT=${AXIOM_PORT}

# Security Keys (Keep these secure!)
JWT_SECRET=${JWT_SECRET}
CLI_API_KEY=${CLI_API_KEY}
API_KEY=${API_KEY}
WEBHOOK_SECRET=${WEBHOOK_SECRET}
ENCRYPTION_KEY=${ENCRYPTION_KEY}

# Database Configuration
DATABASE_URL=${DATABASE_URL}
DB_NAME=${DB_NAME}
DB_USER=${DB_USER}
DB_PASSWORD=${DB_PASSWORD}

# Redis Configuration
REDIS_URL=${REDIS_URL}

# Application Settings
ENVIRONMENT=${ENVIRONMENT}
DEBUG=${DEBUG}
CORS_ORIGINS=${CORS_ORIGINS}

# AXIOM Configuration
AXIOM_BASE=${AXIOM_BASE}

# Node Environment
NODE_ENV=production

# FastAPI Settings
FASTAPI_ENV=production
EOF

    print_success "Environment file created: .env"
}

# Function to check prerequisites
check_prerequisites() {
    print_status "Checking prerequisites..."
    
    local missing_tools=()
    
    if ! command_exists docker; then
        missing_tools+=("docker")
    fi
    
    if ! command_exists docker-compose; then
        if ! docker compose version >/dev/null 2>&1; then
            missing_tools+=("docker-compose")
        fi
    fi
    
    if ! command_exists curl; then
        missing_tools+=("curl")
    fi
    
    if ! command_exists openssl; then
        missing_tools+=("openssl")
    fi
    
    if [ ${#missing_tools[@]} -gt 0 ]; then
        print_error "Missing required tools: ${missing_tools[*]}"
        print_error "Please install the missing tools and run this script again."
        exit 1
    fi
    
    # Check if Docker is running
    if ! docker info >/dev/null 2>&1; then
        print_error "Docker is not running. Please start Docker and try again."
        exit 1
    fi
    
    print_success "All prerequisites satisfied"
}

# Function to create Docker Compose file
create_docker_compose() {
    print_status "Creating Docker Compose configuration..."
    
    cat > docker-compose.yml << 'EOF'
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
EOF

    print_success "Docker Compose configuration created"
}

# Function to create Dockerfiles
create_dockerfiles() {
    print_status "Creating Dockerfiles..."
    
    # Backend Dockerfile
    cat > Dockerfile.backend << 'EOF'
FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
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
EOF

    # AXIOM Dockerfile
    cat > Dockerfile.axiom << 'EOF'
FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies for AXIOM
RUN pip install --no-cache-dir flask requests cryptography

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
EOF

    # Frontend Dockerfile
    cat > Dockerfile.frontend << 'EOF'
FROM node:18-alpine AS builder

WORKDIR /app

# Copy package files
COPY frontend/package*.json ./

# Install dependencies
RUN npm ci --only=production

# Copy source code
COPY frontend ./

# Build the app
RUN npm run build

# Production stage
FROM nginx:alpine

# Copy built app
COPY --from=builder /app/build /usr/share/nginx/html

# Copy nginx configuration
COPY nginx.conf /etc/nginx/nginx.conf

# Health check
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:3000 || exit 1

EXPOSE 3000

CMD ["nginx", "-g", "daemon off;"]
EOF

    # Create nginx configuration
    cat > nginx.conf << 'EOF'
events {
    worker_connections 1024;
}

http {
    include       /etc/nginx/mime.types;
    default_type  application/octet-stream;
    
    # Gzip compression
    gzip on;
    gzip_vary on;
    gzip_min_length 1024;
    gzip_types text/plain text/css application/json application/javascript text/xml application/xml application/xml+rss text/javascript;
    
    server {
        listen 3000;
        server_name localhost;
        root /usr/share/nginx/html;
        index index.html;
        
        # Handle client-side routing
        location / {
            try_files $uri $uri/ /index.html;
        }
        
        # Cache static assets
        location /static/ {
            expires 1y;
            add_header Cache-Control "public, immutable";
        }
        
        # Security headers
        add_header X-Frame-Options "SAMEORIGIN" always;
        add_header X-Content-Type-Options "nosniff" always;
        add_header X-XSS-Protection "1; mode=block" always;
        add_header Referrer-Policy "strict-origin-when-cross-origin" always;
    }
}
EOF

    print_success "Dockerfiles created successfully"
}

# Function to create database initialization script
create_db_init() {
    print_status "Creating database initialization script..."
    
    cat > init.sql << 'EOF'
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

-- Create functions
CREATE OR REPLACE FUNCTION auth.update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Create triggers
DROP TRIGGER IF EXISTS update_users_updated_at ON auth.users;
CREATE TRIGGER update_users_updated_at
    BEFORE UPDATE ON auth.users
    FOR EACH ROW EXECUTE FUNCTION auth.update_updated_at_column();

DROP TRIGGER IF EXISTS update_ceremonies_updated_at ON axiom.ceremonies;
CREATE TRIGGER update_ceremonies_updated_at
    BEFORE UPDATE ON axiom.ceremonies
    FOR EACH ROW EXECUTE FUNCTION auth.update_updated_at_column();

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
EOF

    print_success "Database initialization script created"
}

# Function to run deployment
deploy() {
    print_status "Starting Super-Codex-AI deployment..."
    
    # Stop existing containers
    if docker compose ps -q >/dev/null 2>&1; then
        print_status "Stopping existing containers..."
        docker compose down
    fi
    
    # Build and start services
    print_status "Building and starting services..."
    docker compose up -d --build
    
    print_success "Services started successfully"
}

# Function to run migrations
run_migrations() {
    print_status "Running database migrations..."
    
    # Wait for database to be ready
    wait_for_service "http://localhost:5432" "PostgreSQL" || {
        print_error "Database failed to start"
        return 1
    }
    
    # Run migrations
    if docker compose exec -T backend python -c "
from app.db import engine, Base
try:
    Base.metadata.create_all(engine)
    print('Migrations completed successfully')
except Exception as e:
    print(f'Migration failed: {e}')
    exit(1)
    " 2>/dev/null; then
        print_success "Database migrations completed"
    else
        print_warning "Using database initialization script instead"
    fi
}

# Function to run smoke tests
run_smoke_tests() {
    print_status "Running smoke tests..."
    
    local base_url="https://${DOMAIN}"
    local tests_passed=0
    local total_tests=0
    
    # Test cases
    local tests=(
        "${base_url}/api/health:Backend Health Check"
        "${base_url}/api/health/live:Backend Liveness"
        "${base_url}/api/health/ready:Backend Readiness"
        "${base_url}/:Frontend Access"
        "http://localhost:${AXIOM_PORT}/health:AXIOM Health"
    )
    
    for test in "${tests[@]}"; do
        local url="${test%%:*}"
        local name="${test##*:}"
        ((total_tests++))
        
        print_status "Testing: $name ($url)"
        
        if curl -sSf -m 10 "$url" >/dev/null 2>&1; then
            print_success "✅ $name: PASSED"
            ((tests_passed++))
        else
            print_error "❌ $name: FAILED"
        fi
    done
    
    echo
    print_status "Smoke Tests Summary: $tests_passed/$total_tests tests passed"
    
    if [ $tests_passed -eq $total_tests ]; then
        print_success "All smoke tests passed!"
        return 0
    else
        print_warning "Some smoke tests failed. Check service logs for details."
        return 1
    fi
}

# Function to display deployment summary
show_deployment_summary() {
    echo
    echo "=================================================================="
    print_success "🎉 Super-Codex-AI Deployment Complete!"
    echo "=================================================================="
    echo
    echo "📋 Service URLs:"
    echo "  🌐 Frontend:     https://${DOMAIN}"
    echo "  🔧 Backend API:  https://${DOMAIN}/api"
    echo "  ⚡ AXIOM Flame:  https://${DOMAIN}/axiom"
    echo "  📊 Database:     localhost:5432"
    echo "  🔄 Redis:        localhost:6379"
    echo
    echo "🔐 Security Keys (saved in .env):"
    echo "  JWT Secret:      ${JWT_SECRET:0:16}..."
    echo "  API Key:         ${CLI_API_KEY}"
    echo "  Webhook Secret:  ${WEBHOOK_SECRET:0:16}..."
    echo
    echo "📊 Management Commands:"
    echo "  View logs:       docker compose logs -f [service]"
    echo "  Stop services:   docker compose down"
    echo "  Restart:         docker compose restart [service]"
    echo "  Shell access:    docker compose exec [service] /bin/bash"
    echo
    echo "🧪 Health Check URLs:"
    echo "  curl https://${DOMAIN}/api/health"
    echo "  curl https://${DOMAIN}/api/health/live"
    echo "  curl https://${DOMAIN}/api/health/ready"
    echo
    print_status "Deployment completed at $(date)"
    echo "=================================================================="
}

# Main execution
main() {
    echo "🚀 Super-Codex-AI Deployment Script"
    echo "==================================="
    echo
    
    # Parse command line arguments
    while [[ $# -gt 0 ]]; do
        case $1 in
            --domain)
                DOMAIN="$2"
                shift 2
                ;;
            --skip-tests)
                SKIP_TESTS=true
                shift
                ;;
            --help)
                echo "Usage: $0 [OPTIONS]"
                echo "Options:"
                echo "  --domain DOMAIN    Set the domain name (default: your-domain.com)"
                echo "  --skip-tests       Skip smoke tests"
                echo "  --help             Show this help message"
                exit 0
                ;;
            *)
                print_error "Unknown option: $1"
                exit 1
                ;;
        esac
    done
    
    # Main deployment process
    check_prerequisites
    generate_env_file
    create_docker_compose
    create_dockerfiles
    create_db_init
    deploy
    
    # Wait for services to be ready
    sleep 10
    
    run_migrations
    
    # Run smoke tests unless skipped
    if [[ "${SKIP_TESTS:-false}" != "true" ]]; then
        sleep 5  # Additional wait for services to stabilize
        run_smoke_tests || print_warning "Some tests failed, but deployment may still be functional"
    fi
    
    show_deployment_summary
}

# Handle script interruption
trap 'print_error "Deployment interrupted!"; exit 1' INT TERM

# Run main function
main "$@"
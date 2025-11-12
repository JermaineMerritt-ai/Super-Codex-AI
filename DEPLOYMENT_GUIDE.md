# Super-Codex-AI Deployment Guide

This guide provides comprehensive instructions for deploying Super-Codex-AI using the automated deployment scripts.

## Quick Start

### Windows (PowerShell)
```powershell
# Basic deployment with default settings
.\deploy.ps1 -Domain "your-domain.com"

# Development deployment (localhost)
.\deploy.ps1 -Domain "localhost" -SkipTests

# Custom ports deployment
.\deploy.ps1 -Domain "my-app.com" -BackendPort 9000 -FrontendPort 4000
```

### Linux/macOS (Bash)
```bash
# Make script executable
chmod +x deploy.sh

# Basic deployment
./deploy.sh --domain your-domain.com

# Skip smoke tests
./deploy.sh --domain localhost --skip-tests
```

## Prerequisites

### Required Software
- **Docker**: Version 20.10+ with Docker Compose
- **PowerShell** (Windows) or **Bash** (Linux/macOS)
- **curl**: For health checks and testing
- **openssl**: For generating secure secrets (auto-installed on most systems)

### System Requirements
- **RAM**: Minimum 4GB, Recommended 8GB+
- **CPU**: 2+ cores recommended
- **Disk**: 10GB+ free space for Docker images and data
- **Network**: Ports 80, 443, and configured service ports available

### Domain Setup (Production)
1. **DNS Configuration**: Point your domain A record to your server's IP address
2. **SSL Certificates**: Caddy will automatically obtain Let's Encrypt certificates
3. **Firewall**: Ensure ports 80 and 443 are open for incoming traffic

## Deployment Process

The deployment script performs these steps automatically:

### 1. Environment Setup
- Generates secure random secrets (JWT, API keys, etc.)
- Creates `.env` file with all configuration
- Validates Docker and prerequisite tools

### 2. Docker Configuration
- Creates `docker-compose.yml` with all services
- Generates service-specific Dockerfiles
- Sets up volumes for persistent data storage

### 3. Database Setup
- Initializes PostgreSQL with schemas and tables
- Creates Redis cache instance
- Runs database migrations

### 4. Service Deployment
- **Backend**: FastAPI server on configured port (default: 8010)
- **Frontend**: React application on configured port (default: 3001)
- **AXIOM**: Ceremonial system on configured port (default: 5010)
- **Database**: PostgreSQL on port 5432
- **Cache**: Redis on port 6379
- **Proxy**: Caddy reverse proxy on ports 80/443

### 5. Health Verification
- Waits for all services to be ready
- Runs comprehensive smoke tests
- Validates API endpoints and service connectivity

## Configuration

### Environment Variables

The deployment script generates a comprehensive `.env` file:

```bash
# Domain Configuration
DOMAIN=your-domain.com
BACKEND_PORT=8010
FRONTEND_PORT=3001
AXIOM_PORT=5010

# Security (auto-generated)
JWT_SECRET=<64-char-hex>
CLI_API_KEY=<32-char-hex>
API_KEY=<32-char-hex>
WEBHOOK_SECRET=<32-char-hex>
ENCRYPTION_KEY=<64-char-hex>

# Database
DATABASE_URL=postgresql://user:pass@postgres:5432/db
DB_NAME=super_codex_ai
DB_USER=codex_user
DB_PASSWORD=<32-char-hex>

# Application
ENVIRONMENT=production
DEBUG=false
CORS_ORIGINS=https://your-domain.com,http://localhost:3001
```

### Service Ports

| Service | Default Port | Purpose | Accessibility |
|---------|-------------|---------|---------------|
| Frontend | 3001 | React UI | Public via Caddy |
| Backend API | 8010 | FastAPI server | Public via Caddy |
| AXIOM Flame | 5010 | Ceremonial system | Internal |
| PostgreSQL | 5432 | Database | Internal |
| Redis | 6379 | Cache/Sessions | Internal |
| Caddy | 80/443 | Reverse Proxy | Public |

## Post-Deployment

### Accessing Services

Once deployment completes, access your application:

- **Web Interface**: `https://your-domain.com`
- **API Documentation**: `https://your-domain.com/api/docs`
- **Health Checks**: `https://your-domain.com/api/health`

### Management Commands

```bash
# View service logs
docker compose logs -f backend
docker compose logs -f frontend
docker compose logs -f axiom-flame

# Restart individual services
docker compose restart backend
docker compose restart frontend

# Stop all services
docker compose down

# Update and redeploy
git pull
docker compose up -d --build

# Database shell access
docker compose exec postgres psql -U codex_user -d super_codex_ai

# Backend shell access
docker compose exec backend /bin/bash

# View running containers
docker compose ps
```

### Monitoring and Logs

All services include health checks and structured logging:

```bash
# Follow all logs
docker compose logs -f

# Check service health
curl https://your-domain.com/api/health
curl https://your-domain.com/api/health/live
curl https://your-domain.com/api/health/ready

# View service status
docker compose ps
```

## Troubleshooting

### Common Issues

**Port Already in Use**
```bash
# Check what's using the port
netstat -tulpn | grep :8010
# Kill the process or change the port in deployment script
```

**Docker Not Running**
```bash
# Start Docker service (Linux)
sudo systemctl start docker

# Start Docker Desktop (Windows/Mac)
# Launch Docker Desktop application
```

**SSL Certificate Issues**
- Ensure domain points to your server
- Check firewall allows ports 80/443
- Caddy logs: `docker compose logs caddy`

**Database Connection Errors**
```bash
# Check PostgreSQL logs
docker compose logs postgres

# Verify database is ready
docker compose exec postgres pg_isready -U codex_user
```

**Service Won't Start**
```bash
# Check specific service logs
docker compose logs <service-name>

# Rebuild specific service
docker compose up -d --build <service-name>

# Check resource usage
docker stats
```

### Health Check Endpoints

| Endpoint | Purpose | Expected Response |
|----------|---------|-------------------|
| `/api/health` | Basic health | `{"status": "healthy"}` |
| `/api/health/live` | Liveness probe | `{"status": "alive"}` |
| `/api/health/ready` | Readiness probe | `{"status": "ready"}` |

### Log Locations

```bash
# Application logs (inside containers)
/app/logs/

# Docker logs
docker compose logs <service>

# System logs (host)
/var/log/docker/
```

## Security Considerations

### Production Checklist
- [ ] Domain SSL certificate obtained automatically
- [ ] All secrets are randomly generated (64+ character hex)
- [ ] Database uses strong random password
- [ ] Firewall configured (only 80/443 public)
- [ ] Regular backups configured
- [ ] Log monitoring setup
- [ ] Resource limits configured

### Security Features
- **Automatic SSL**: Let's Encrypt certificates via Caddy
- **Secure Headers**: CSP, HSTS, X-Frame-Options configured
- **JWT Authentication**: Cryptographically signed tokens
- **Input Validation**: Pydantic models for all API inputs
- **CORS Protection**: Configured allowed origins
- **Rate Limiting**: Built-in FastAPI rate limiting

## Backup and Recovery

### Database Backup
```bash
# Create backup
docker compose exec postgres pg_dump -U codex_user super_codex_ai > backup.sql

# Restore backup
docker compose exec -T postgres psql -U codex_user super_codex_ai < backup.sql
```

### Full System Backup
```bash
# Backup volumes
docker run --rm -v super-codex-ai_postgres_data:/data -v $(pwd):/backup alpine tar czf /backup/postgres-backup.tar.gz -C /data .
docker run --rm -v super-codex-ai_redis_data:/data -v $(pwd):/backup alpine tar czf /backup/redis-backup.tar.gz -C /data .

# Backup configuration
tar czf config-backup.tar.gz .env docker-compose.yml Caddyfile
```

## Updates and Maintenance

### Application Updates
```bash
# Pull latest code
git pull

# Rebuild and restart services
docker compose up -d --build

# Run any new migrations
docker compose exec backend python -c "from app.db import engine, Base; Base.metadata.create_all(engine)"
```

### Docker Maintenance
```bash
# Clean up unused images
docker system prune -f

# Update base images
docker compose pull
docker compose up -d --build
```

## Support and Documentation

- **GitHub Repository**: [Super-Codex-AI](https://github.com/JermaineMerritt-ai/Super-Codex-AI)
- **API Documentation**: Available at `/api/docs` after deployment
- **Configuration Reference**: See `codex-env-settings.ipynb` in repository
- **Architecture Guide**: See `CODEX_BRAIN_MAP.md` and related documentation

## License and Contributing

This deployment configuration is part of the Super-Codex-AI project. See `LICENSE` file for details.

For contributing to deployment improvements, please:
1. Fork the repository
2. Create a feature branch
3. Test your changes with the deployment scripts
4. Submit a pull request with detailed description

---

**Note**: This deployment guide assumes you have basic familiarity with Docker, command line operations, and web application deployment. For detailed troubleshooting or custom configurations, refer to the specific service documentation in the repository.
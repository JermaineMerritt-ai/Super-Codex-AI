# Deployment Guide - Super-Codex-AI with Nginx

## 🚀 Quick Start (Development)

### 1. Generate SSL Certificate
```powershell
# Windows (PowerShell)
./generate-ssl.ps1

# Linux/Mac (Bash)
chmod +x generate-ssl.sh
./generate-ssl.sh
```

### 2. Update Environment Variables
Create/update `.env` file:
```env
POSTGRES_PASSWORD=your_secure_password_here
DATABASE_URL=postgresql://codex_admin:your_secure_password_here@postgres:5432/codex
REDIS_URL=redis://redis:6379
ENVIRONMENT=development
```

### 3. Start Services
```bash
# Stop any existing services
docker-compose down

# Start with nginx proxy
docker-compose up --build -d

# Check status
docker-compose ps
docker-compose logs nginx
```

### 4. Test Endpoints
```bash
# Health check (through nginx)
curl http://localhost/health

# API status
curl http://localhost/api/status

# Interactive docs
http://localhost/docs
```

## 🌐 Production Deployment

### 1. Use Production Compose File
```bash
# Use production configuration with Let's Encrypt
docker-compose -f docker-compose.prod.yml up -d
```

### 2. SSL Certificate Setup (Let's Encrypt)
```bash
# Initial certificate generation
docker-compose -f docker-compose.prod.yml run --rm certbot

# Auto-renewal (add to cron)
0 12 * * * docker-compose -f docker-compose.prod.yml run --rm certbot renew
```

### 3. DNS Configuration
Point your domain to your server:
```
A     codexdominion.app     -> YOUR_SERVER_IP
A     www.codexdominion.app -> YOUR_SERVER_IP
```

### 4. Security Checklist
- [ ] Change default passwords
- [ ] Configure firewall (only 80, 443, 22)
- [ ] Set up monitoring
- [ ] Configure log rotation
- [ ] Enable automatic updates
- [ ] Set up backups

## 📊 Architecture Overview

```
Internet → Nginx (80/443) → FastAPI (8080) → PostgreSQL (5432)
                         → Redis (6379)
```

### Service Ports:
- **80**: HTTP (redirects to HTTPS)
- **443**: HTTPS (nginx → FastAPI)
- **8080**: FastAPI (internal only)
- **5432**: PostgreSQL (internal only)
- **6379**: Redis (internal only)

## 🔧 Configuration Files

- `nginx.conf`: Nginx reverse proxy configuration
- `docker-compose.yml`: Development environment
- `docker-compose.prod.yml`: Production with Let's Encrypt
- `generate-ssl.ps1`: SSL certificate generation (Windows)
- `generate-ssl.sh`: SSL certificate generation (Linux/Mac)

## 📝 Maintenance Commands

```bash
# View logs
docker-compose logs -f nginx
docker-compose logs -f codex

# Restart services
docker-compose restart nginx
docker-compose restart codex

# Update containers
docker-compose pull
docker-compose up -d --force-recreate

# Backup database
docker-compose exec postgres pg_dump -U codex_admin codex > backup.sql

# Monitor resources
docker stats
```

## 🚨 Troubleshooting

### SSL Certificate Issues
```bash
# Check certificate validity
openssl x509 -in ssl/codexdominion.app.crt -text -noout

# Test SSL configuration
docker-compose exec nginx nginx -t
```

### Connection Issues
```bash
# Test backend connectivity
docker-compose exec nginx wget -qO- http://codex:8080/health

# Check network connectivity
docker network ls
docker-compose exec nginx nslookup codex
```

### Performance Tuning
```bash
# Monitor nginx access logs
docker-compose logs nginx | grep -E "HTTP/[0-9.]+ [4-5][0-9][0-9]"

# Check response times
curl -w "@curl-format.txt" -o /dev/null -s http://localhost/health
```

## 📚 Additional Resources

- [Nginx Documentation](https://nginx.org/en/docs/)
- [Let's Encrypt Guide](https://letsencrypt.org/getting-started/)
- [Docker Compose Reference](https://docs.docker.com/compose/)
- [FastAPI Deployment](https://fastapi.tiangolo.com/deployment/)
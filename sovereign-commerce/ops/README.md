# Operations for Sovereign Commerce Platform

This directory contains operational scripts and deployment tools for the Sovereign Commerce platform designed for diaspora funders.

## Scripts

### Deployment
- `deploy.py` - Complete platform deployment script
- `seed_data.py` - Database seeding with ceremonial data
- `backup.py` - Database and configuration backup
- `restore.py` - System restoration from backups

### Management
- `start_platform.ps1` - Platform startup script
- `stop_platform.ps1` - Graceful platform shutdown
- `health_check.py` - System health monitoring
- `update_platform.py` - Platform updates and migrations

### Monitoring
- `ceremonial_metrics.py` - Platform usage analytics
- `audit_report.py` - Governance and audit reporting
- `sigil_management.py` - Sigil system maintenance
- `user_analytics.py` - User engagement tracking

## Deployment Process

### Initial Setup
1. Run `python deploy.py` for complete setup
2. Database initialization with ceremonial schema
3. Virtual environment creation
4. Dependency installation
5. Sovereign key generation

### Configuration
- Environment variables in `.env`
- Database configuration for SQLite
- JWT token settings
- Ceremonial authority configuration

### Database Management
- Automated schema creation
- Sample data seeding
- Migration support
- Backup and restore

### Security
- JWT secret key generation
- Sigil system configuration
- Role-based access setup
- Audit trail initialization

## Platform Management

### Starting the Platform
```powershell
# Activate environment
.\.venv\Scripts\Activate.ps1

# Start server
uvicorn services.main:app --host 127.0.0.1 --port 8080 --reload
```

### Health Monitoring
- `/health` endpoint for system status
- Database connectivity checks
- Service availability monitoring
- Performance metrics

### Backup Strategy
- Daily database snapshots
- Configuration file backups
- User data preservation
- Audit trail archival

## Engine Integration

The platform integrates with multiple engines:
- **AXIOM** - Core reasoning and decision making
- **RAG** - Retrieval augmented generation for enhanced search
- **SIGIL** - Identity and signature management system
- **ORACLE** - Predictive analytics and forecasting
- **LANTERN** - Search and discovery engine
- **FLAME** - Ceremonial processing and ritual management

## Governance

### Audit Trail
- Complete transaction logging
- User action tracking
- System state changes
- Ceremonial witness records

### Authority Management
- Multi-tier role administration
- Permission assignment
- Sigil authority delegation
- Ceremonial recognition

### Compliance
- Data protection measures
- Access control enforcement
- Audit report generation
- Governance policy implementation

## Support

For operational support:
- Check system logs in `logs/` directory
- Monitor health endpoint status
- Review audit trail for issues
- Consult ceremonial authorities for guidance
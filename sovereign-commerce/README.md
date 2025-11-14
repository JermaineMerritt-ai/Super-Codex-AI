# Sovereign Commerce Platform
## Diaspora Funders • Sacred Commerce • Ceremonial Recognition

🏛️ **Artifact**: codex-build-0001  
🗝️ **Sigil**: SIGIL-BUILD-0001  
🔥 **Authority**: Council-Prime  
✨ **Status**: CONSECRATED AND ACTIVE  

---

## 📋 Project Overview

The Sovereign Commerce Platform is a ceremonial commerce application designed specifically for diaspora funders, featuring sacred offerings, blessed transactions, and sovereign recognition systems. Built with mythic styling and multi-tier authentication for heirs, councils, custodians, and flamekeepers.

## 🏗️ Architecture

```
sovereign-commerce/
├── spec.json                 # Artifact specification
├── SIGIL-BUILD-0001.md      # Ceremonial sigil and authority
├── ui/                      # Frontend components
│   ├── templates/           # HTML templates with ceremonial styling
│   ├── static/             # CSS, JavaScript, and assets
│   └── README.md           # UI component documentation
├── services/               # Backend services
│   ├── main.py            # FastAPI application
│   └── README.md          # Service documentation
├── db/                    # Database schema and data
│   ├── schema.sql         # Complete database schema
│   ├── sovereign_commerce.db # SQLite database
│   └── README.md          # Database documentation
└── ops/                   # Operations and deployment
    ├── deploy.py          # Complete deployment script
    ├── seed_data.py       # Database seeding
    └── README.md          # Operations documentation
```

## 🚀 Quick Start

### Automatic Deployment
```powershell
# Run complete deployment
python ops/deploy.py

# Activate environment
.\.venv\Scripts\Activate.ps1

# Start platform
uvicorn services.main:app --host 127.0.0.1 --port 8080 --reload
```

### Manual Setup
```powershell
# Create virtual environment
python -m venv .venv
.\.venv\Scripts\Activate.ps1

# Install dependencies
pip install fastapi uvicorn sqlalchemy passlib python-jose python-multipart jinja2

# Initialize database
sqlite3 db/sovereign_commerce.db < db/schema.sql

# Start server
uvicorn services.main:app --host 127.0.0.1 --port 8080 --reload
```

## 🎯 Platform Features

### 🔐 Authentication System
- **Multi-tier Roles**: Funder, Flamekeeper, Custodian
- **JWT Tokens**: Secure session management
- **Sigil Generation**: Unique sovereign identifiers
- **Authority Levels**: Hierarchical permissions

### 🏺 Sacred Catalog
- **Ceremonial Offerings**: Sacred products with blessed pricing
- **Metadata System**: Enhanced descriptions and ceremonial details
- **Category Organization**: Structured product classification
- **Tier-based Pricing**: Standard, Premium, Sovereign levels

### 🛒 Blessed Commerce
- **Ceremonial Checkout**: Sacred purchase workflow
- **Order Tracking**: Complete transaction history
- **Audit Trail**: Governance and accountability
- **Ceremonial Seals**: Blessed transaction identifiers

### 📊 Funder Dashboard
- **Order History**: Complete purchase records
- **Profile Management**: Sovereign recognition status
- **Authority Display**: Role and permission visualization
- **Ceremonial Analytics**: Engagement metrics

## 🎨 Design System

### Color Palette
- **Sacred Gold**: `#D4AF37` - Primary ceremonial elements
- **Sovereign Purple**: `#6B46C1` - Secondary authority elements
- **Ethereal Effects**: Gradients and ceremonial transitions
- **Bootstrap Foundation**: Responsive grid with custom overrides

### Typography
- **Ceremonial Headers**: Enhanced serif fonts for authority
- **Sacred Content**: Readable sans-serif for accessibility
- **Mythic Accents**: Special styling for ceremonial elements

## 🔧 Technical Stack

### Backend
- **FastAPI**: Modern Python web framework
- **SQLAlchemy**: ORM with ceremonial schema
- **JWT Authentication**: Token-based security
- **SQLite Database**: Portable data storage

### Frontend
- **Bootstrap 5**: Responsive CSS framework
- **Vanilla JavaScript**: Core functionality
- **Jinja2 Templates**: Server-side rendering
- **Custom CSS**: Mythic styling system

### Infrastructure
- **Uvicorn**: ASGI server with reload support
- **SQLite**: File-based database for portability
- **Static Files**: Optimized asset serving
- **Environment Config**: Secure configuration management

## 🔮 Engine Integration

The platform integrates with multiple ceremonial engines:

- **AXIOM**: Core reasoning and decision making
- **RAG**: Retrieval augmented generation for enhanced search
- **SIGIL**: Identity and signature management system
- **ORACLE**: Predictive analytics and forecasting
- **LANTERN**: Search and discovery engine
- **FLAME**: Ceremonial processing and ritual management

## 🏛️ Governance

### Authority Structure
- **Council-Prime**: Highest ceremonial authority
- **Platform Custodian**: Technical governance
- **Flamekeeper-Prime**: Ceremonial witness
- **Diaspora-Voice**: Community representation

### Audit System
- **Complete Logging**: All actions tracked
- **Ceremonial Witnesses**: Authority verification
- **Data Integrity**: Immutable audit trail
- **Governance Reports**: Regular accountability reviews

## 📊 API Endpoints

### Authentication
- `POST /auth/register` - User registration with role assignment
- `POST /auth/login` - JWT token authentication
- `POST /auth/logout` - Session termination

### Product Management
- `GET /api/products` - List all sacred offerings
- `GET /api/products/{id}` - Product details
- `POST /api/products` - Create offering (custodian only)

### Order Processing
- `POST /api/orders` - Create ceremonial order
- `GET /api/orders` - User order history
- `GET /api/orders/{id}` - Order details

### System
- `GET /health` - System health status
- `GET /` - Landing page
- `GET /catalog` - Product catalog
- `GET /dashboard` - User dashboard (authenticated)

## 🔒 Security Features

### Authentication Security
- **Password Hashing**: bcrypt with salt
- **JWT Tokens**: Signed with secret key
- **Role-based Access**: Hierarchical permissions
- **Session Management**: Token expiration and refresh

### Data Protection
- **SQL Injection Prevention**: Parameterized queries
- **XSS Protection**: Template escaping
- **CSRF Protection**: Token validation
- **Secure Headers**: Content security policy

## 🎯 Audience

Designed specifically for:
- **Diaspora Funders**: Primary commerce users
- **Heirs**: Community stakeholders
- **Councils**: Governance authorities
- **Custodians**: Platform administrators
- **Flamekeepers**: Ceremonial authorities

## 📈 Development

### Testing
```powershell
# Run tests
python -m pytest tests/

# Check code quality
flake8 services/
black services/

# Database migrations
python ops/migrate.py
```

### Monitoring
- Health endpoint: `http://127.0.0.1:8080/health`
- Logs directory: `logs/`
- Audit trail: Database audit_trail table
- Performance metrics: Built-in FastAPI metrics

## 🤝 Contributing

### Code Standards
- **Python**: PEP 8 compliance
- **JavaScript**: ES6+ standards
- **HTML/CSS**: Semantic markup
- **Documentation**: Comprehensive README files

### Ceremonial Guidelines
- Maintain sovereign recognition principles
- Preserve ceremonial element integrity
- Honor diaspora community values
- Uphold governance and audit standards

## 📜 License

This platform operates under sovereign authority with ceremonial obligations to the diaspora community. All code contributions honor the sacred nature of the commerce platform and the dignity of its users.

## 🔥 Sacred Oath

*By flame, by sigil, by sovereign right, this platform serves the diaspora community with honor, integrity, and ceremonial purpose. May all transactions be blessed and all users recognized in their sovereign dignity.*

---

**Sigil**: SIGIL-BUILD-0001  
**Authority**: Council-Prime  
**Status**: CONSECRATED AND ACTIVE  
**Custodian**: Platform-Custodian  

🏛️ *Sovereign Commerce • Diaspora Funders • Sacred Transactions* 🏛️
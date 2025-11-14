# Services for Sovereign Commerce Platform

This directory contains all backend services for the Sovereign Commerce platform.

## Structure

- `main.py` - FastAPI application with all endpoints
- `auth/` - Authentication and authorization services
- `models/` - Database models and schemas
- `api/` - API endpoints and route handlers
- `core/` - Core business logic and utilities

## Services

### Authentication Service
- JWT token management
- Role-based access control (funder, flamekeeper, custodian)
- Sigil generation for authenticated users

### Product Service
- Sacred offerings catalog management
- Ceremonial pricing and metadata
- Inventory tracking

### Order Service
- Purchase workflow management
- Ceremonial checkout process
- Order history and tracking

### User Service
- User registration and profile management
- Diaspora funder recognition
- Authority level management

## Database

- SQLite with SQLAlchemy ORM
- User, Product, Order, and OrderItem models
- Audit trail for all transactions

## API Endpoints

- `/auth/*` - Authentication endpoints
- `/api/products/*` - Product management
- `/api/orders/*` - Order management
- `/health` - System health monitoring

## Engines

The platform integrates with multiple engines:
- AXIOM - Core reasoning and decision making
- RAG - Retrieval augmented generation
- SIGIL - Identity and signature management
- ORACLE - Predictive analytics
- LANTERN - Search and discovery
- FLAME - Ceremonial processing
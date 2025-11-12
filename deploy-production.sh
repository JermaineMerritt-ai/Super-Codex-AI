#!/bin/bash
# Production Deployment Script for CodexDominion.app
# Usage: ./deploy-production.sh

set -e

echo "🚀 Starting CodexDominion.app Production Deployment"

# Check if .env exists
if [ ! -f .env ]; then
    echo "⚠️  Creating .env from template..."
    cp .env.example .env
    echo "📝 Please edit .env with your production secrets before continuing!"
    echo "🔑 Don't forget to update:"
    echo "   - JWT_SECRET"
    echo "   - CLI_API_KEY"
    echo "   - POSTGRES_PASSWORD"
    echo "   - ACME_EMAIL"
    exit 1
fi

# Create frontend build directory if it doesn't exist
if [ ! -d "frontend/build" ]; then
    echo "📁 Creating frontend build directory..."
    mkdir -p frontend/build
    echo "<h1>CodexDominion.app</h1><p>Frontend placeholder - Deploy your React build here</p>" > frontend/build/index.html
fi

# Pull latest images
echo "📦 Pulling latest Docker images..."
docker-compose pull

# Build services
echo "🔨 Building services..."
docker-compose build --no-cache

# Start services
echo "🆙 Starting services..."
docker-compose up -d

# Wait for services to be ready
echo "⏳ Waiting for services to start..."
sleep 10

# Check service health
echo "🩺 Checking service health..."
if curl -f http://localhost:8000/health > /dev/null 2>&1; then
    echo "✅ Backend is healthy"
else
    echo "❌ Backend health check failed"
fi

if curl -f http://localhost:5000/health > /dev/null 2>&1; then
    echo "✅ Axiom-flame is healthy"
else
    echo "⚠️  Axiom-flame health check failed (may be normal if not implemented)"
fi

if curl -f http://localhost:3000/health > /dev/null 2>&1; then
    echo "✅ Frontend is healthy"
else
    echo "❌ Frontend health check failed"
fi

echo ""
echo "🎉 Deployment complete!"
echo "🌐 Your application should be available at:"
echo "   - Local: http://localhost (via Caddy)"
echo "   - Production: https://CodexDominion.app (once DNS is configured)"
echo ""
echo "📊 Service URLs:"
echo "   - Backend API: http://localhost:8000"
echo "   - Axiom-flame: http://localhost:5000"  
echo "   - Frontend: http://localhost:3000"
echo "   - Caddy Admin: http://localhost:2019"
echo ""
echo "📝 Next steps:"
echo "   1. Point CodexDominion.app DNS A record to your server IP"
echo "   2. Update .env with your email for SSL certificates"
echo "   3. Deploy your React frontend to frontend/build/"
echo "   4. Monitor logs with: docker-compose logs -f"
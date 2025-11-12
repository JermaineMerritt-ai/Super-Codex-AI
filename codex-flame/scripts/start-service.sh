#!/bin/bash
# Quick service setup and verification script

echo "🔧 Enabling and starting AXIOM FLAME service..."

# Enable the service to start on boot
sudo systemctl enable axiom-flame
echo "✅ Service enabled for automatic startup"

# Start the service
sudo systemctl start axiom-flame
echo "✅ Service started"

# Wait a moment for startup
echo "⏳ Waiting for service to initialize..."
sleep 3

# Check service status
echo "📊 Service Status:"
sudo systemctl status axiom-flame --no-pager

# Verify API health
echo ""
echo "🏥 Testing API health..."
if curl -f -s http://localhost:8080/health > /dev/null; then
    echo "✅ API is responding"
    curl -s http://localhost:8080/health | python3 -m json.tool 2>/dev/null || curl -s http://localhost:8080/health
else
    echo "❌ API health check failed"
    echo "📋 Recent logs:"
    sudo journalctl -u axiom-flame --no-pager -n 10
fi

echo ""
echo "🎉 AXIOM FLAME service is now running!"
echo ""
echo "📋 Useful commands:"
echo "  sudo systemctl status axiom-flame    # Check status"
echo "  sudo journalctl -u axiom-flame -f    # Follow logs"
echo "  sudo systemctl restart axiom-flame   # Restart service"
echo "  curl http://localhost:8080/health    # Test API"
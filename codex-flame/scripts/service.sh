#!/bin/bash
# Axiom-Flame Service Management Script

SERVICE_NAME="axiom-flame"
APP_DIR="/srv/axiom-flame"

function show_help() {
    echo "Axiom-Flame Service Management"
    echo ""
    echo "Usage: $0 [COMMAND]"
    echo ""
    echo "Commands:"
    echo "  start     Start the service"
    echo "  stop      Stop the service"
    echo "  restart   Restart the service"
    echo "  status    Show service status"
    echo "  logs      Show recent logs"
    echo "  follow    Follow live logs"
    echo "  health    Check API health"
    echo "  reload    Reload systemd and restart service"
    echo "  install   Install/update the service"
    echo "  remove    Remove the service"
    echo ""
}

function service_start() {
    echo "🚀 Starting Axiom-Flame service..."
    sudo systemctl start $SERVICE_NAME
    echo "✅ Service started"
}

function service_stop() {
    echo "🛑 Stopping Axiom-Flame service..."
    sudo systemctl stop $SERVICE_NAME
    echo "✅ Service stopped"
}

function service_restart() {
    echo "🔄 Restarting Axiom-Flame service..."
    sudo systemctl restart $SERVICE_NAME
    echo "✅ Service restarted"
}

function service_status() {
    echo "📊 Axiom-Flame service status:"
    sudo systemctl status $SERVICE_NAME --no-pager
}

function service_logs() {
    echo "📋 Recent Axiom-Flame logs:"
    sudo journalctl -u $SERVICE_NAME --no-pager -n 50
}

function service_follow() {
    echo "📋 Following Axiom-Flame logs (Ctrl+C to exit):"
    sudo journalctl -u $SERVICE_NAME -f
}

function service_health() {
    echo "🏥 Checking API health..."
    
    if curl -f -s http://localhost:8080/health > /dev/null; then
        echo "✅ API is healthy"
        curl -s http://localhost:8080/health | python3 -m json.tool
    else
        echo "❌ API health check failed"
        echo "📋 Recent logs:"
        sudo journalctl -u $SERVICE_NAME --no-pager -n 10
        exit 1
    fi
}

function service_reload() {
    echo "🔄 Reloading systemd and restarting service..."
    sudo systemctl daemon-reload
    sudo systemctl restart $SERVICE_NAME
    echo "✅ Service reloaded"
}

function service_install() {
    echo "📦 Installing/updating Axiom-Flame service..."
    
    # Copy service file
    sudo cp $APP_DIR/systemd/axiom-flame-production.service /etc/systemd/system/axiom-flame.service
    
    # Reload systemd
    sudo systemctl daemon-reload
    
    # Enable service
    sudo systemctl enable $SERVICE_NAME
    
    echo "✅ Service installed and enabled"
}

function service_remove() {
    echo "🗑️ Removing Axiom-Flame service..."
    
    # Stop and disable service
    sudo systemctl stop $SERVICE_NAME
    sudo systemctl disable $SERVICE_NAME
    
    # Remove service file
    sudo rm -f /etc/systemd/system/$SERVICE_NAME.service
    
    # Reload systemd
    sudo systemctl daemon-reload
    
    echo "✅ Service removed"
}

# Main script logic
case "${1:-}" in
    start)
        service_start
        ;;
    stop)
        service_stop
        ;;
    restart)
        service_restart
        ;;
    status)
        service_status
        ;;
    logs)
        service_logs
        ;;
    follow)
        service_follow
        ;;
    health)
        service_health
        ;;
    reload)
        service_reload
        ;;
    install)
        service_install
        ;;
    remove)
        service_remove
        ;;
    *)
        show_help
        exit 1
        ;;
esac
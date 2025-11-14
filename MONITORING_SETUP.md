# Monitoring Setup Guide

This guide covers the complete monitoring stack setup for Super-Codex-AI using Prometheus and Grafana.

## Overview

The monitoring stack includes:
- **Prometheus**: Metrics collection and storage
- **Grafana**: Visualization and dashboards
- **FastAPI Metrics**: Application-level monitoring via prometheus-fastapi-instrumentator

## Architecture

```
┌─────────────┐    ┌──────────────┐    ┌─────────────┐
│   Codex     │────│  Prometheus  │────│   Grafana   │
│ (FastAPI)   │    │  (Scraper)   │    │ (Dashboard) │
│ Port: 8080  │    │  Port: 9090  │    │ Port: 3000  │
└─────────────┘    └──────────────┘    └─────────────┘
```

## Quick Start

### 1. Start the Complete Stack

```bash
# Build and start all services including monitoring
docker-compose up --build -d

# Verify all services are running
docker-compose ps
```

### 2. Access the Monitoring Interfaces

- **Codex Application**: http://localhost (via nginx)
- **Codex Metrics**: http://localhost/metrics
- **Prometheus**: http://localhost:9090
- **Grafana**: http://localhost:3000

### 3. Default Credentials

**Grafana Login:**
- Username: `admin`
- Password: Check your `.env` file for `GRAFANA_PASSWORD`

## Configuration Details

### Prometheus Configuration

The `prometheus.yml` file defines scrape targets:

```yaml
scrape_configs:
  - job_name: 'codex'
    static_configs:
      - targets: ['codex:8080']
    metrics_path: '/metrics'
    scrape_interval: 30s
```

### Available Metrics

#### FastAPI Application Metrics

1. **HTTP Request Metrics**
   - `http_requests_total{method, handler, status}`
   - `http_request_duration_seconds{method, handler}`
   - `http_requests_inprogress{method, handler}`

2. **System Metrics**
   - `python_gc_objects_collected_total`
   - `process_resident_memory_bytes`
   - `process_cpu_seconds_total`

3. **Custom Business Metrics** (if implemented)
   - User authentication events
   - API endpoint usage
   - Error rates and types

## Grafana Dashboard Setup

### 1. Add Prometheus Data Source

1. Login to Grafana (http://localhost:3000)
2. Go to Configuration → Data Sources
3. Add Prometheus data source:
   - URL: `http://prometheus:9090`
   - Access: Server (default)
   - Save & Test

### 2. Import Pre-built Dashboards

Recommended dashboard IDs for import:
- **FastAPI Dashboard**: 13321
- **Docker Container Metrics**: 193
- **Node Exporter (if added)**: 1860

### 3. Custom Dashboard Panels

#### HTTP Request Rate
```promql
rate(http_requests_total[5m])
```

#### Response Time Percentiles
```promql
histogram_quantile(0.95, rate(http_request_duration_seconds_bucket[5m]))
```

#### Error Rate
```promql
rate(http_requests_total{status=~"4..|5.."}[5m]) / rate(http_requests_total[5m])
```

## Useful Commands

### Docker Management

```bash
# View logs for specific service
docker-compose logs -f prometheus
docker-compose logs -f grafana
docker-compose logs -f codex

# Restart monitoring services
docker-compose restart prometheus grafana

# Check service health
docker-compose exec prometheus wget -qO- http://localhost:9090/-/healthy
docker-compose exec grafana curl -f http://localhost:3000/api/health
```

### Prometheus Queries

```bash
# Test Prometheus API
curl http://localhost:9090/api/v1/query?query=up

# Get current targets status
curl http://localhost:9090/api/v1/targets
```

### Debugging

```bash
# Check if metrics endpoint is accessible
curl http://localhost/metrics

# Verify Prometheus config
docker-compose exec prometheus promtool check config /etc/prometheus/prometheus.yml
```

## Alerting Setup (Optional)

### 1. Create Alert Rules

Create `alerts.yml`:

```yaml
groups:
  - name: codex_alerts
    rules:
      - alert: HighErrorRate
        expr: rate(http_requests_total{status=~"5.."}[5m]) > 0.1
        for: 5m
        labels:
          severity: warning
        annotations:
          summary: High error rate detected
          description: "Error rate is {{ $value }} errors per second"

      - alert: ServiceDown
        expr: up == 0
        for: 1m
        labels:
          severity: critical
        annotations:
          summary: Service is down
          description: "{{ $labels.instance }} is down"
```

### 2. Configure Alertmanager

Add to `docker-compose.yml`:

```yaml
  alertmanager:
    image: prom/alertmanager:latest
    ports:
      - "9093:9093"
    volumes:
      - ./alertmanager.yml:/etc/alertmanager/alertmanager.yml:ro
    restart: always
```

## Performance Optimization

### 1. Metrics Retention

- Default: 200h (8.3 days)
- Adjust in docker-compose.yml: `--storage.tsdb.retention.time=720h`

### 2. Scrape Intervals

- Default: 30s for application metrics
- Adjust based on your needs (higher frequency = more data)

### 3. Resource Limits

Add to services in docker-compose.yml:

```yaml
deploy:
  resources:
    limits:
      memory: 512M
      cpus: '0.5'
```

## Production Considerations

1. **Security**
   - Enable authentication for Grafana
   - Use SSL certificates
   - Restrict Prometheus access

2. **Backup**
   - Backup Grafana dashboards
   - Consider external storage for metrics

3. **Scaling**
   - Use external Prometheus for multiple instances
   - Implement federation for large deployments

## Troubleshooting

### Common Issues

1. **Metrics not appearing**
   - Check if `/metrics` endpoint is accessible
   - Verify Prometheus scrape targets status
   - Check network connectivity between containers

2. **Grafana connection issues**
   - Verify Prometheus data source URL
   - Check if Prometheus is accessible from Grafana container

3. **Container startup failures**
   - Check docker-compose logs
   - Verify configuration file syntax
   - Ensure volumes are properly mounted

### Health Checks

```bash
# Application health
curl http://localhost/health

# Prometheus health
curl http://localhost:9090/-/healthy

# Grafana health
curl http://localhost:3000/api/health
```

## Next Steps

1. **Custom Metrics**: Implement business-specific metrics
2. **Alerting**: Set up alerts for critical issues
3. **Log Aggregation**: Add ELK stack or similar
4. **Tracing**: Implement distributed tracing with Jaeger
5. **External Monitoring**: Add external health checks

---

*This monitoring setup provides comprehensive observability for your Super-Codex-AI application. Adjust configurations based on your specific requirements and scale.*
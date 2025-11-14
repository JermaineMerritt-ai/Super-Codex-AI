# Kubernetes Health Checks for Super-Codex-AI

## Overview

This document describes the Kubernetes health check configuration for the Super-Codex-AI application, including liveness and readiness probes for monitoring application health and traffic readiness.

## Health Check Endpoints

### 1. Liveness Probe: `/health`

**Purpose**: Determines if the application is running and healthy  
**Response Format**:
```json
{
  "status": "healthy",
  "timestamp": "2025-11-13T01:08:29.719388",
  "environment": "production"
}
```

**When to use**: 
- Container restart decisions
- Basic application health monitoring
- Load balancer health checks

### 2. Readiness Probe: `/ready`

**Purpose**: Determines if the application is ready to accept traffic  
**Response Format**:
```json
{
  "status": "ready",
  "timestamp": "2025-11-13T01:08:55.728429",
  "services": {
    "database": "healthy",
    "redis": "not_configured", 
    "sentry": "not_configured"
  },
  "ready": true
}
```

**When to use**:
- Service discovery registration
- Load balancer traffic routing
- Deployment rollout decisions

## Kubernetes Probe Configuration

### Liveness Probe
```yaml
livenessProbe:
  httpGet:
    path: /health
    port: 8080
  initialDelaySeconds: 30
  periodSeconds: 10
  timeoutSeconds: 5
  failureThreshold: 3
  successThreshold: 1
```

**Configuration Details**:
- **initialDelaySeconds**: 30s wait before first check (allows app startup)
- **periodSeconds**: Check every 10 seconds
- **timeoutSeconds**: 5 second timeout per request
- **failureThreshold**: 3 consecutive failures trigger restart
- **successThreshold**: 1 success considered healthy

### Readiness Probe
```yaml
readinessProbe:
  httpGet:
    path: /ready
    port: 8080
  initialDelaySeconds: 10
  periodSeconds: 5
  timeoutSeconds: 3
  failureThreshold: 3
  successThreshold: 1
```

**Configuration Details**:
- **initialDelaySeconds**: 10s wait before first check (faster than liveness)
- **periodSeconds**: Check every 5 seconds (more frequent than liveness)
- **timeoutSeconds**: 3 second timeout (faster response needed)
- **failureThreshold**: 3 consecutive failures remove from service
- **successThreshold**: 1 success considered ready

## Health Check Behavior

### Liveness Probe Failures
- **Action**: Kubernetes restarts the container
- **Impact**: Brief service interruption during restart
- **Trigger**: Application deadlock, memory exhaustion, critical failures

### Readiness Probe Failures
- **Action**: Kubernetes removes pod from service endpoints
- **Impact**: Traffic stops routing to the pod
- **Trigger**: Dependency failures, initialization delays, overload

## Monitoring Integration

### Prometheus Metrics
The application automatically exports health-related metrics:
- HTTP response times for health endpoints
- Success/failure rates
- Request counts

### Grafana Dashboards
Monitor health check status through:
- **Endpoint**: http://localhost:3000 (admin/admin)
- **Metrics**: Available at http://localhost:9090 (Prometheus)

### Sentry Error Tracking
Health check failures and errors are automatically reported to Sentry when configured.

## Production Deployment

### Prerequisites
1. **Container Registry**: Push image to your registry
2. **Kubernetes Cluster**: Ensure cluster access
3. **Secrets**: Configure Sentry DSN and other secrets

### Deployment Steps

1. **Build and push the container image**:
   ```bash
   docker build -t your-registry/super-codex-ai:latest .
   docker push your-registry/super-codex-ai:latest
   ```

2. **Update deployment image**:
   ```bash
   # Edit k8s/deployment.yaml
   # Change: image: super-codex-ai:latest
   # To: image: your-registry/super-codex-ai:latest
   ```

3. **Create secrets**:
   ```bash
   # Replace with actual Sentry DSN
   kubectl create secret generic super-codex-secrets \
     --from-literal=sentry-dsn="https://your-actual-sentry-dsn"
   ```

4. **Deploy to Kubernetes**:
   ```bash
   kubectl apply -f k8s/deployment.yaml
   ```

5. **Verify deployment**:
   ```bash
   kubectl get pods -l app=super-codex-ai
   kubectl get services
   kubectl logs -l app=super-codex-ai
   ```

### Health Check Verification

1. **Check pod status**:
   ```bash
   kubectl describe pod -l app=super-codex-ai
   ```

2. **Test endpoints through service**:
   ```bash
   kubectl port-forward service/super-codex-ai-service 8080:80
   curl http://localhost:8080/health
   curl http://localhost:8080/ready
   ```

3. **Monitor health check events**:
   ```bash
   kubectl get events --field-selector reason=Unhealthy
   kubectl get events --field-selector reason=FailedReadiness
   ```

## Troubleshooting

### Common Issues

1. **Liveness probe failures**:
   - Check application logs: `kubectl logs -l app=super-codex-ai`
   - Verify resource limits aren't exceeded
   - Increase `initialDelaySeconds` for slow-starting apps

2. **Readiness probe failures**:
   - Check dependency services (database, Redis)
   - Verify network connectivity between pods
   - Check service configuration and port mappings

3. **Probe timeouts**:
   - Increase `timeoutSeconds` values
   - Optimize endpoint response times
   - Check network latency between nodes

### Debug Commands

```bash
# Check pod health status
kubectl get pods -o wide

# Describe pod for event details
kubectl describe pod <pod-name>

# Check service endpoints
kubectl get endpoints

# Port forward for direct testing
kubectl port-forward <pod-name> 8080:8080

# View health check logs
kubectl logs <pod-name> | grep -E "(health|ready)"
```

## Customization

### Environment-Specific Configuration

For different environments, adjust probe parameters:

**Development**:
- Longer `initialDelaySeconds` (60s)
- More lenient `failureThreshold` (5)
- Longer `timeoutSeconds` (10s)

**Production**:
- Shorter probe intervals for faster detection
- Stricter failure thresholds
- Comprehensive dependency checks

### Advanced Health Checks

Enhance the `/ready` endpoint with actual dependency checks:

```python
@app.get("/ready")
async def ready():
    # Add real dependency health checks
    db_healthy = await check_database_connection()
    redis_healthy = await check_redis_connection()
    
    services_status = {
        "database": "healthy" if db_healthy else "unhealthy",
        "redis": "healthy" if redis_healthy else "unhealthy"
    }
    
    is_ready = all([db_healthy, redis_healthy])
    
    return ReadinessResponse(
        status="ready" if is_ready else "not_ready",
        timestamp=datetime.utcnow().isoformat(),
        services=services_status,
        ready=is_ready
    )
```

## Security Considerations

1. **Health endpoints**: Don't expose sensitive information
2. **Resource limits**: Prevent health checks from overwhelming resources
3. **Network policies**: Restrict health check access to cluster components
4. **Secrets management**: Use Kubernetes secrets for sensitive configuration

## Related Documentation

- [Docker Compose Configuration](../docker-compose.yml)
- [Prometheus Monitoring](../prometheus.yml)
- [Sentry Integration](../SENTRY_INTEGRATION_COMPLETE.md)
- [Application Configuration](../simple_server.py)
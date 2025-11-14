# Sentry Error Monitoring Setup Guide

This guide covers the complete Sentry error monitoring integration for Super-Codex-AI.

## Overview

Sentry provides real-time error tracking, performance monitoring, and alerting for your application. This integration includes:

- **Error Tracking**: Automatic capture of exceptions and errors
- **Performance Monitoring**: Request tracing and performance insights  
- **FastAPI Integration**: Native support for FastAPI applications
- **Custom Context**: Enhanced error reporting with user and transaction data

## Quick Setup

### 1. Sentry Project Configuration

1. **Create Sentry Account**: Sign up at https://sentry.io
2. **Create New Project**: Select "FastAPI" or "Python" as platform
3. **Get Your DSN**: Copy the Data Source Name from project settings

### 2. Environment Configuration

Update your `.env` file with your Sentry credentials:

```env
# Sentry Configuration
SENTRY_DSN=https://your-sentry-dsn-here@sentry.io/project-id
SENTRY_TRACES_SAMPLE_RATE=1.0
SENTRY_ENVIRONMENT=production
```

**Configuration Options:**
- `SENTRY_DSN`: Your unique Sentry project DSN
- `SENTRY_TRACES_SAMPLE_RATE`: Performance monitoring sample rate (0.0-1.0)
- `SENTRY_ENVIRONMENT`: Environment name for error grouping

### 3. Install Dependencies

The Sentry SDK has been added to `requirements.txt`:

```txt
sentry-sdk[fastapi]==1.40.0
```

Install dependencies:
```bash
pip install -r requirements.txt
# OR rebuild Docker container
docker-compose up --build
```

## Implementation Details

### FastAPI Integration

Both `simple_server.py` and `server.py` include Sentry initialization:

```python
import sentry_sdk
from sentry_sdk.integrations.fastapi import FastApiIntegration
from sentry_sdk.integrations.starlette import StarletteIntegration

# Initialize Sentry
sentry_dsn = os.getenv("SENTRY_DSN")
if sentry_dsn:
    sentry_sdk.init(
        dsn=sentry_dsn,
        traces_sample_rate=float(os.getenv("SENTRY_TRACES_SAMPLE_RATE", "1.0")),
        environment=os.getenv("SENTRY_ENVIRONMENT", "production"),
        integrations=[
            FastApiIntegration(auto_ui=True),
            StarletteIntegration(transaction_style="endpoint")
        ],
        send_default_pii=False,  # Privacy protection
    )
```

### Key Features Enabled

1. **Automatic Error Capture**: All unhandled exceptions are sent to Sentry
2. **Request Tracing**: HTTP requests are tracked with performance data
3. **User Context**: Anonymous user sessions for error correlation
4. **Release Tracking**: Version-based error grouping and regression detection
5. **Performance Insights**: Slow endpoint detection and optimization

## Testing Error Monitoring

### 1. Test Error Capture

Add a test endpoint to trigger errors:

```python
@app.get("/test/error")
async def test_error():
    # This will be captured by Sentry
    raise Exception("Test error for Sentry monitoring")

@app.get("/test/division")
async def test_division():
    # Division by zero error
    result = 1 / 0
    return {"result": result}
```

### 2. Verify Integration

```bash
# Test endpoints to generate errors
curl http://localhost/test/error
curl http://localhost/test/division

# Check Sentry dashboard for error reports
```

### 3. Performance Testing

```bash
# Generate multiple requests for performance data
for i in {1..10}; do
    curl http://localhost/health
    curl http://localhost/api/status
done
```

## Sentry Dashboard Features

### Error Management
- **Issue Stream**: Real-time error notifications
- **Error Grouping**: Similar errors grouped automatically
- **Stack Traces**: Full Python stack traces with code context
- **Breadcrumbs**: Events leading up to errors

### Performance Monitoring
- **Transaction Overview**: Endpoint performance summary
- **Slow Queries**: Database and external API call tracking
- **User Experience**: Frontend performance correlation
- **Custom Metrics**: Business-specific performance indicators

### Alerting & Notifications
- **Real-time Alerts**: Immediate error notifications
- **Alert Rules**: Custom conditions for notifications
- **Integration**: Slack, Email, PagerDuty, etc.
- **Escalation**: Automated incident management

## Production Optimization

### 1. Sample Rate Configuration

For production, adjust sample rates to reduce overhead:

```env
# Production settings - sample 10% of transactions
SENTRY_TRACES_SAMPLE_RATE=0.1
SENTRY_PROFILES_SAMPLE_RATE=0.1
```

### 2. Performance Considerations

```python
# Custom performance configuration
sentry_sdk.init(
    dsn=sentry_dsn,
    traces_sample_rate=0.1,  # 10% sampling
    profiles_sample_rate=0.1,  # Profile 10% of transactions
    max_breadcrumbs=50,  # Limit breadcrumb history
    attach_stacktrace=True,  # Include stack traces
    send_default_pii=False,  # Privacy protection
)
```

### 3. Custom Context

Add business context to errors:

```python
from sentry_sdk import configure_scope

@app.middleware("http")
async def add_sentry_context(request, call_next):
    with configure_scope() as scope:
        scope.set_tag("endpoint", request.url.path)
        scope.set_context("request", {
            "method": request.method,
            "url": str(request.url),
            "user_agent": request.headers.get("user-agent"),
        })
    response = await call_next(request)
    return response
```

## Security & Privacy

### Data Scrubbing

Sentry automatically scrubs sensitive data:
- Passwords, tokens, and secrets
- Credit card numbers
- Social security numbers
- Custom patterns you define

### Custom Scrubbing

```python
# Additional data scrubbing
from sentry_sdk.scrubber import EventScrubber

scrubber = EventScrubber(
    additional_sensitive_fields=["api_key", "auth_token", "secret"]
)
```

### IP Address Protection

```python
sentry_sdk.init(
    # ... other config
    send_default_pii=False,  # Disable PII collection
    before_send=lambda event, hint: scrub_sensitive_data(event)
)
```

## Monitoring Best Practices

### 1. Error Prioritization

- **Critical**: Service unavailable, data corruption
- **High**: Feature broken, user impact
- **Medium**: Performance degradation
- **Low**: Minor UX issues

### 2. Release Tracking

```bash
# Set release version for error tracking
export SENTRY_RELEASE="super-codex-ai@1.0.0"
```

### 3. Environment Separation

```env
# Development
SENTRY_ENVIRONMENT=development

# Staging
SENTRY_ENVIRONMENT=staging

# Production
SENTRY_ENVIRONMENT=production
```

## Integration with Existing Monitoring

### Prometheus + Sentry

Combine metrics and errors:
- Prometheus: System metrics and performance
- Sentry: Error tracking and user experience
- Grafana: Unified dashboard with both data sources

### Alert Correlation

Link Sentry errors with Prometheus alerts:
```python
import sentry_sdk
from prometheus_client import Counter

error_counter = Counter('app_errors_total', 'Total application errors')

def handle_error(error):
    error_counter.inc()
    sentry_sdk.capture_exception(error)
```

## Troubleshooting

### Common Issues

1. **DSN Not Set**: Ensure `SENTRY_DSN` is in environment variables
2. **High Volume**: Adjust sample rates for production
3. **Performance Impact**: Monitor SDK overhead in metrics
4. **False Positives**: Configure error filters

### Debug Mode

```python
import logging
logging.basicConfig(level=logging.DEBUG)
sentry_sdk.init(debug=True)  # Enable debug output
```

### Health Check

```python
@app.get("/health/sentry")
async def sentry_health():
    try:
        sentry_sdk.capture_message("Health check message", level="info")
        return {"sentry": "operational"}
    except Exception as e:
        return {"sentry": "error", "message": str(e)}
```

## Cost Optimization

### Error Volume Management

- Filter known non-critical errors
- Set up error fingerprinting
- Use custom before_send filters
- Implement error rate limiting

### Sample Rate Strategies

```python
# Dynamic sampling based on error frequency
def custom_traces_sampler(sampling_context):
    if "error" in sampling_context.get("transaction_context", {}):
        return 1.0  # Always sample errors
    return 0.1  # 10% for normal transactions
```

---

## Next Steps

1. **Create Sentry Project**: Set up your Sentry account and project
2. **Update DSN**: Replace placeholder DSN with your actual project DSN
3. **Deploy & Test**: Rebuild containers and test error capture
4. **Configure Alerts**: Set up notification rules for your team
5. **Custom Dashboards**: Create monitoring dashboards combining Sentry + Prometheus

**Your application now has enterprise-grade error monitoring and performance tracking!** 🚨📊
# Codex Dominion Ingress NGINX Configuration

This document describes the optimized NGINX ingress configuration for the Codex system and dashboard, enabling secure, scalable, and modular routing for all platform services.

## Overview
- **Purpose:** Centralize and secure ingress for all Codex platform components
- **Features:**
  - HTTP to HTTPS redirection
  - SSL termination with Let's Encrypt
  - Modular subdomain routing for each service
  - Optimized proxy headers for real client IP and protocol
  - Ready for Docker/Kubernetes internal service mapping

## Subdomain Routing Table
| Subdomain                | Service Name      | Internal Target           | Port  |
|-------------------------|-------------------|---------------------------|-------|
| dashboard.yourdomain.com| Constellation Dashboard | dashboard         | 8080  |
| api.yourdomain.com      | Gatekeeper API    | gatekeeper                | 8081  |
| insight.yourdomain.com  | Insight Codex     | insight                   | 8083  |
| sparkforge.yourdomain.com| SparkForge AI    | sparkforge                | 8084  |
| scrolls.yourdomain.com  | ScrollWeaver      | scrollweaver              | 8085  |
| lab.yourdomain.com      | Banana Codex Lab  | banana-lab                | 8888  |

## Example NGINX Configuration
```nginx
# === Codex Dominion Ingress ===
server {
    listen 80;
    server_name *.yourdomain.com yourdomain.com;
    return 301 https://$host$request_uri;
}

# === Constellation Dashboard ===
server {
    listen 443 ssl;
    server_name dashboard.yourdomain.com;
    ssl_certificate     /etc/letsencrypt/live/yourdomain.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/yourdomain.com/privkey.pem;
    location / {
        proxy_pass http://dashboard:8080;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
# ... (repeat for each service as in the provided config)
```

## Optimization Notes
- **Security:** All HTTP traffic is redirected to HTTPS. Use strong SSL ciphers and keep certificates updated.
- **Scalability:** Each service is isolated by subdomain, allowing for independent scaling and updates.
- **Observability:** Add access/error log directives and monitoring as needed for production.
- **Kubernetes:** For K8s, use Ingress resources with similar rules and annotations for SSL and routing.

## Dashboard Integration
- This configuration is referenced in the system and dashboard documentation for infrastructure onboarding.
- Update this file if subdomains, ports, or service names change.

---

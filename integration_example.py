"""
Integration Example: Connecting to Your Production Environment
============================================================

This script demonstrates how to integrate the unified artifact system
with your actual production environment, including:

1. Custom base URLs and authentication
2. Signature verification setup
3. Webhook integration patterns
4. Portal-specific routing

To use with your actual environment, update the configuration below.
"""

import os
import json
import asyncio
import aiohttp
from datetime import datetime, timezone
from production_config import Environment, AuthScheme, ProductionConfig

# EXAMPLE PRODUCTION CONFIGURATION
# Replace these with your actual values:

EXAMPLE_PRODUCTION_CONFIG = ProductionConfig(
    environment=Environment.PRODUCTION,
    debug=False,
    
    # YOUR ACTUAL URLs HERE:
    api_base_url="https://your-api-domain.com",
    web_base_url="https://your-web-domain.com", 
    council_portal_url="https://council.your-domain.com",
    public_portal_url="https://public.your-domain.com",
    
    # YOUR AUTHENTICATION SCHEME:
    auth_scheme=AuthScheme.BEARER_TOKEN,  # or OAUTH2, API_KEY, SIGIL_SEAL
    api_key_header="X-Your-API-Key",
    
    # YOUR SECURITY SETTINGS:
    signature_verification=True,
    rate_limit_per_minute=100,
    max_file_size_mb=50,
    
    # YOUR STORAGE:
    database_url="postgresql://user:pass@your-db-host:5432/artifacts",
    redis_url="redis://your-redis-host:6379/0",
    artifact_storage_path="/var/your-app/artifacts",
    
    # YOUR WEBHOOK ENDPOINTS:
    replay_webhook_url="https://your-api-domain.com/webhooks/replay",
    council_notification_url="https://council.your-domain.com/api/notifications",
    public_broadcast_url="https://public.your-domain.com/api/broadcasts"
)

class ProductionIntegrationExample:
    """Example integration with production environment"""
    
    def __init__(self, config: ProductionConfig):
        self.config = config
        
    async def test_artifact_deployment(self, api_token: str):
        """Test deploying an artifact to your production environment"""
        
        # Example artifact manifest
        artifact_manifest = {
            "artifactId": "test-production-artifact",
            "title": "Production Test Artifact",
            "version": "1.0.0",
            "type": "charter",
            "routes": {
                "register": "/ledger/charter/final",
                "dispatch": "/dispatch/global", 
                "replay": "/replay/charter"
            },
            "audience": ["councils", "public"],
            "cycles": ["epochal"],
            "files": {
                "text": "artifact.md",
                "glyph": "assets/glyph.svg"
            },
            "signing": {
                "sigil": "SIGIL-PROD-TEST-001",
                "signedBy": "Production-System",
                "heirsChorus": false
            }
        }
        
        artifact_text = """# Production Test Artifact
        
This is a test artifact deployed to the production environment
to verify integration and webhook functionality.

**Status**: Testing production deployment
**Environment**: {env}
**Timestamp**: {timestamp}
        """.format(
            env=self.config.environment.value,
            timestamp=datetime.now(timezone.utc).isoformat()
        )
        
        # Prepare authentication headers based on your scheme
        headers = self._get_auth_headers(api_token)
        
        # Add signature if required
        if self.config.signature_verification:
            signature = self._generate_signature(artifact_manifest, api_token)
            headers["X-Codex-Signature"] = f"sha256={signature}"
        
        async with aiohttp.ClientSession() as session:
            # 1. Register the artifact
            register_url = f"{self.config.api_base_url}/ledger/charter/final"
            
            form_data = aiohttp.FormData()
            form_data.add_field('manifest', json.dumps(artifact_manifest))
            form_data.add_field('text_content', artifact_text)
            
            print(f"🚀 Registering artifact at {register_url}")
            
            async with session.post(register_url, headers=headers, data=form_data) as response:
                if response.status == 200:
                    result = await response.json()
                    print(f"✅ Artifact registered: {result}")
                    return result
                else:
                    error = await response.text()
                    print(f"❌ Registration failed: {response.status} - {error}")
                    return None
    
    def _get_auth_headers(self, api_token: str) -> dict:
        """Get authentication headers based on configured scheme"""
        headers = {
            "Content-Type": "multipart/form-data",
            "User-Agent": "Codex-Artifact-System/2.0"
        }
        
        if self.config.auth_scheme == AuthScheme.BEARER_TOKEN:
            headers["Authorization"] = f"Bearer {api_token}"
        elif self.config.auth_scheme == AuthScheme.API_KEY:
            headers[self.config.api_key_header] = api_token
        elif self.config.auth_scheme == AuthScheme.SIGIL_SEAL:
            headers["X-Codex-Sigil"] = api_token
            
        return headers
    
    def _generate_signature(self, manifest_data: dict, secret: str) -> str:
        """Generate HMAC signature for request verification"""
        import hmac
        import hashlib
        
        payload = json.dumps(manifest_data, sort_keys=True)
        signature = hmac.new(
            secret.encode(),
            payload.encode(), 
            hashlib.sha256
        ).hexdigest()
        return signature
    
    async def setup_webhook_endpoints(self):
        """Setup webhook endpoints in your application"""
        webhook_setup_guide = """
        
🔗 WEBHOOK INTEGRATION SETUP
============================

Add these endpoints to your application to receive artifact notifications:

1. COUNCIL PORTAL WEBHOOK:
   POST {council_url}/api/notifications
   
   Expected payload:
   {{
     "action": "artifact_registered|artifact_dispatched|artifact_performed",
     "artifact": {{
       "id": "artifact-id",
       "title": "Artifact Title", 
       "type": "charter|hymn|decree",
       "timestamp": "2025-11-13T08:00:00Z"
     }},
     "source": "unified-artifact-system"
   }}

2. PUBLIC PORTAL WEBHOOK:
   POST {public_url}/api/broadcasts
   
   Same payload format as above.

3. REPLAY ARCHIVE WEBHOOK:
   POST {api_url}/webhooks/replay
   
   Extended payload with performance history.

IMPLEMENTATION EXAMPLE:
======================

# Flask/FastAPI endpoint example:
@app.post("/api/notifications")  # Council portal
async def receive_artifact_notification(payload: dict):
    artifact = payload.get("artifact", {{}})
    action = payload.get("action")
    
    # Process notification
    if action == "artifact_registered":
        # Update council dashboard
        update_council_dashboard(artifact)
    elif action == "artifact_dispatched":
        # Trigger council alerts
        send_council_alerts(artifact)
    
    return {{"status": "received"}}

@app.post("/api/broadcasts")  # Public portal  
async def receive_artifact_broadcast(payload: dict):
    artifact = payload.get("artifact", {{}})
    
    # Update public displays
    update_public_displays(artifact)
    
    return {{"status": "received"}}

SECURITY RECOMMENDATIONS:
========================

1. Verify webhook signatures:
   - Check X-Codex-Source header
   - Verify HMAC signature if enabled
   
2. Rate limiting:
   - Implement rate limits on webhook endpoints
   - Use exponential backoff for retries
   
3. Authentication:
   - Secure webhook endpoints with API keys
   - Use HTTPS only in production

        """.format(
            council_url=self.config.council_portal_url,
            public_url=self.config.public_portal_url,
            api_url=self.config.api_base_url
        )
        
        print(webhook_setup_guide)
        return webhook_setup_guide

def demonstrate_production_integration():
    """Demonstrate production integration patterns"""
    
    print("🏭 PRODUCTION INTEGRATION EXAMPLE")
    print("=" * 50)
    
    # Initialize with your production config
    integration = ProductionIntegrationExample(EXAMPLE_PRODUCTION_CONFIG)
    
    print("\n📋 CONFIGURATION SUMMARY:")
    print(f"Environment: {EXAMPLE_PRODUCTION_CONFIG.environment.value}")
    print(f"API Base: {EXAMPLE_PRODUCTION_CONFIG.api_base_url}")
    print(f"Auth Scheme: {EXAMPLE_PRODUCTION_CONFIG.auth_scheme.value}")
    print(f"Council Portal: {EXAMPLE_PRODUCTION_CONFIG.council_portal_url}")
    print(f"Public Portal: {EXAMPLE_PRODUCTION_CONFIG.public_portal_url}")
    print(f"Signature Verification: {EXAMPLE_PRODUCTION_CONFIG.signature_verification}")
    
    print("\n🔧 DEPLOYMENT COMMANDS:")
    deployment_commands = f"""
# 1. Set environment variables:
export CODEX_ENV=production
export CODEX_API_BASE_URL={EXAMPLE_PRODUCTION_CONFIG.api_base_url}
export CODEX_AUTH_SCHEME={EXAMPLE_PRODUCTION_CONFIG.auth_scheme.value}
export CODEX_DATABASE_URL={EXAMPLE_PRODUCTION_CONFIG.database_url}

# 2. Install dependencies:
pip install fastapi uvicorn[standard] aiohttp python-multipart

# 3. Start production server:
python production_artifact_system.py

# 4. Test deployment:
python integration_example.py --test-deployment --token YOUR_API_TOKEN

# 5. Setup webhooks in your applications (see webhook guide below)
    """
    print(deployment_commands)
    
    # Show webhook setup
    asyncio.run(integration.setup_webhook_endpoints())
    
    print("\n🧪 TESTING CHECKLIST:")
    testing_checklist = """
□ Configure environment variables
□ Update base URLs to your domains  
□ Set up authentication scheme
□ Configure database connections
□ Test artifact registration
□ Test file uploads
□ Test global dispatch
□ Verify webhook delivery
□ Test council portal integration
□ Test public portal integration
□ Verify signature verification (if enabled)
□ Test rate limiting
□ Verify CORS configuration
□ Test SSL/TLS in production
    """
    print(testing_checklist)
    
    print("\n🚀 READY FOR PRODUCTION!")
    print("Update the configuration above with your actual URLs and credentials.")

async def test_production_deployment():
    """Test actual deployment (replace with your credentials)"""
    # REPLACE WITH YOUR ACTUAL API TOKEN
    api_token = os.getenv("YOUR_API_TOKEN", "test-token")
    
    if api_token == "test-token":
        print("⚠️ Set YOUR_API_TOKEN environment variable for testing")
        return
    
    integration = ProductionIntegrationExample(EXAMPLE_PRODUCTION_CONFIG)
    
    print("🧪 Testing production deployment...")
    result = await integration.test_artifact_deployment(api_token)
    
    if result:
        print(f"✅ Production test successful: {result}")
    else:
        print("❌ Production test failed")

if __name__ == "__main__":
    import sys
    
    if "--test-deployment" in sys.argv:
        # Test actual deployment
        asyncio.run(test_production_deployment())
    else:
        # Show integration guide
        demonstrate_production_integration()
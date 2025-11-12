#!/usr/bin/env python3
"""
Enhanced AXIOM CLI with Authentication Support
Provides authentication and authorized access to AXIOM FLAME operations
"""
import requests
import json
import sys
import os
from pathlib import Path
import configparser
from typing import Optional

# Configuration
DEFAULT_API_BASE = "http://127.0.0.1:8006"
DEFAULT_BACKEND_BASE = "http://127.0.0.1:8006"

API_BASE = os.getenv("AXIOM_API_BASE", DEFAULT_API_BASE)
BACKEND_BASE = os.getenv("AXIOM_BACKEND_BASE", DEFAULT_BACKEND_BASE)

# Token storage
TOKEN_FILE = Path.home() / ".axiom_token"
CONFIG_FILE = Path.home() / ".axiom_config"

class AuthenticatedClient:
    def __init__(self, backend_base: str, api_base: str):
        self.backend_base = backend_base.rstrip('/')
        self.api_base = api_base.rstrip('/')
        self.token: Optional[str] = None
        self.session = requests.Session()
        self.load_token()
    
    def save_token(self, token: str):
        """Save authentication token to file"""
        try:
            TOKEN_FILE.write_text(token)
            TOKEN_FILE.chmod(0o600)  # Make file readable only by user
            self.token = token
            self.session.headers.update({"Authorization": f"Bearer {token}"})
        except Exception as e:
            print(f"Warning: Could not save token: {e}")
    
    def load_token(self):
        """Load authentication token from file"""
        try:
            if TOKEN_FILE.exists():
                self.token = TOKEN_FILE.read_text().strip()
                self.session.headers.update({"Authorization": f"Bearer {self.token}"})
        except Exception as e:
            print(f"Warning: Could not load token: {e}")
    
    def clear_token(self):
        """Clear stored authentication token"""
        try:
            if TOKEN_FILE.exists():
                TOKEN_FILE.unlink()
            self.token = None
            if "Authorization" in self.session.headers:
                del self.session.headers["Authorization"]
        except Exception as e:
            print(f"Warning: Could not clear token: {e}")
    
    def login(self, username: str, password: str) -> dict:
        """Authenticate with backend and save token"""
        try:
            response = self.session.post(
                f"{self.backend_base}/auth/login",
                json={"username": username, "password": password},
                timeout=10
            )
            response.raise_for_status()
            
            data = response.json()
            self.save_token(data["access_token"])
            return data
        
        except requests.HTTPError as e:
            if e.response.status_code == 401:
                raise Exception("Invalid username or password")
            else:
                raise Exception(f"Login failed: {e.response.status_code}")
        except Exception as e:
            raise Exception(f"Login error: {e}")
    
    def get_user_info(self) -> dict:
        """Get current user information"""
        try:
            response = self.session.get(f"{self.backend_base}/auth/me", timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.HTTPError as e:
            if e.response.status_code == 401:
                raise Exception("Not authenticated or token expired")
            else:
                raise Exception(f"Failed to get user info: {e.response.status_code}")
        except Exception as e:
            raise Exception(f"User info error: {e}")
    
    def axiom_request(self, method: str, endpoint: str, **kwargs) -> dict:
        """Make authenticated request to AXIOM FLAME API"""
        try:
            url = f"{self.api_base}/{endpoint.lstrip('/')}"
            response = self.session.request(method, url, timeout=30, **kwargs)
            response.raise_for_status()
            return response.json()
        except requests.HTTPError as e:
            raise Exception(f"AXIOM API error {e.response.status_code}: {e.response.text}")
        except Exception as e:
            raise Exception(f"AXIOM request error: {e}")

def get_credentials():
    """Get username and password from user input"""
    import getpass
    
    print("🔐 AXIOM Authentication Required")
    username = input("Username: ")
    password = getpass.getpass("Password: ")
    return username, password

def ensure_authenticated(client: AuthenticatedClient) -> bool:
    """Ensure user is authenticated, prompt login if needed"""
    try:
        # Try to get user info with current token
        user_info = client.get_user_info()
        print(f"✅ Authenticated as: {user_info['name']} ({user_info['username']})")
        print(f"📋 Roles: {', '.join(user_info['roles'])}")
        return True
    
    except Exception:
        # Need to login
        try:
            print("🔑 Authentication required")
            username, password = get_credentials()
            login_result = client.login(username, password)
            
            user = login_result["user"]
            print(f"✅ Login successful: {user['name']} ({user['username']})")
            print(f"📋 Roles: {', '.join(user['roles'])}")
            return True
            
        except Exception as e:
            print(f"❌ Authentication failed: {e}")
            return False

def cmd_login(args: list):
    """Interactive login command"""
    client = AuthenticatedClient(BACKEND_BASE, API_BASE)
    
    try:
        username, password = get_credentials()
        login_result = client.login(username, password)
        
        user = login_result["user"]
        print(f"✅ Login successful!")
        print(f"   User: {user['name']} ({user['username']})")
        print(f"   Email: {user['email']}")
        print(f"   Roles: {', '.join(user['roles'])}")
        print(f"   Token expires in: {login_result['expires_in']} seconds")
        
    except Exception as e:
        print(f"❌ Login failed: {e}")
        return False
    
    return True

def cmd_logout(args: list):
    """Logout and clear stored token"""
    client = AuthenticatedClient(BACKEND_BASE, API_BASE)
    
    try:
        # Try to logout via API
        if client.token:
            client.session.post(f"{client.backend_base}/auth/logout", timeout=10)
        client.clear_token()
        print("✅ Logged out successfully")
        
    except Exception as e:
        # Clear token anyway
        client.clear_token()
        print(f"✅ Logged out (with warning: {e})")
    
    return True

def cmd_whoami(args: list):
    """Show current user information"""
    client = AuthenticatedClient(BACKEND_BASE, API_BASE)
    
    try:
        user_info = client.get_user_info()
        print(f"👤 Current User: {user_info['name']}")
        print(f"   Username: {user_info['username']}")
        print(f"   Email: {user_info['email']}")
        print(f"   Roles: {', '.join(user_info['roles'])}")
        print(f"   Created: {user_info['created_at']}")
        
    except Exception as e:
        print(f"❌ Not authenticated: {e}")
        return False
    
    return True

def cmd_health(args: list):
    """Check AXIOM FLAME API health"""
    client = AuthenticatedClient(BACKEND_BASE, API_BASE)
    
    try:
        result = client.axiom_request("GET", "/health")
        print(json.dumps(result, indent=2))
        
    except Exception as e:
        print(f"❌ Health check failed: {e}")
        return False
    
    return True

def cmd_status(args: list):
    """Get detailed AXIOM FLAME status"""
    client = AuthenticatedClient(BACKEND_BASE, API_BASE)
    
    try:
        result = client.axiom_request("GET", "/status")
        print(json.dumps(result, indent=2))
        
    except Exception as e:
        print(f"❌ Status check failed: {e}")
        return False
    
    return True

def cmd_reason(args: list):
    """Execute ceremonial reasoning (requires authentication)"""
    if len(args) < 4:
        print("Usage: axiom reason <actor> <realm> <capsule> <intent>")
        return False
    
    client = AuthenticatedClient(BACKEND_BASE, API_BASE)
    
    if not ensure_authenticated(client):
        return False
    
    try:
        payload = {
            "actor": args[0],
            "realm": args[1],
            "capsule": args[2],
            "intent": args[3]
        }
        
        result = client.axiom_request("POST", "/api/reason", json=payload)
        print(json.dumps(result, indent=2))
        
    except Exception as e:
        print(f"❌ Ceremonial reasoning failed: {e}")
        return False
    
    return True

def cmd_replay(args: list):
    """Replay a ceremonial dispatch"""
    if len(args) < 1:
        print("Usage: axiom replay <dispatch_id>")
        return False
    
    client = AuthenticatedClient(BACKEND_BASE, API_BASE)
    
    try:
        result = client.axiom_request("GET", f"/api/replay/{args[0]}")
        print(json.dumps(result, indent=2))
        
    except Exception as e:
        print(f"❌ Replay failed: {e}")
        return False
    
    return True

def cmd_audit(args: list):
    """Audit a ceremonial dispatch"""
    if len(args) < 1:
        print("Usage: axiom audit <dispatch_id>")
        return False
    
    client = AuthenticatedClient(BACKEND_BASE, API_BASE)
    
    try:
        result = client.axiom_request("GET", f"/api/audit/{args[0]}")
        print(json.dumps(result, indent=2))
        
    except Exception as e:
        print(f"❌ Audit failed: {e}")
        return False
    
    return True

def show_usage():
    """Display usage information"""
    usage = f"""
AXIOM CLI - Enhanced Authentication-Enabled Interface

Usage: python axiom_auth_cli.py <command> [arguments...]

Authentication Commands:
  login                           - Interactive login
  logout                          - Logout and clear token
  whoami                          - Show current user info

AXIOM FLAME Commands:
  health                          - Check API health status
  status                          - Get detailed system status
  reason <actor> <realm> <capsule> <intent> - Execute ceremonial reasoning (auth required)
  replay <dispatch_id>            - Replay a ceremonial dispatch
  audit <dispatch_id>             - Audit a ceremonial dispatch

Examples:
  python axiom_auth_cli.py login
  python axiom_auth_cli.py whoami
  python axiom_auth_cli.py health
  python axiom_auth_cli.py reason "Custodian" "PL-001" "Sovereign Crown" "Crown.Invocation"
  python axiom_auth_cli.py logout

Environment Variables:
  AXIOM_API_BASE      - AXIOM FLAME API base URL (default: {DEFAULT_API_BASE})
  AXIOM_BACKEND_BASE  - Backend API base URL (default: {DEFAULT_BACKEND_BASE})

Current Configuration:
  AXIOM FLAME API: {API_BASE}
  Backend API: {BACKEND_BASE}
  Token Storage: {TOKEN_FILE}

Default Credentials:
  Admin: username=admin, password=admin
  Council: username=council, password=council
  User: username=user, password=user
"""
    print(usage.strip())

def main():
    if len(sys.argv) < 2:
        show_usage()
        return False
    
    command = sys.argv[1].lower()
    args = sys.argv[2:]
    
    commands = {
        "login": cmd_login,
        "logout": cmd_logout,
        "whoami": cmd_whoami,
        "health": cmd_health,
        "status": cmd_status,
        "reason": cmd_reason,
        "replay": cmd_replay,
        "audit": cmd_audit
    }
    
    if command not in commands:
        print(f"❌ Unknown command: {command}")
        show_usage()
        return False
    
    try:
        return commands[command](args)
    except KeyboardInterrupt:
        print("\n👋 Operation cancelled")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
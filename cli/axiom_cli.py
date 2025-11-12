#!/usr/bin/env python3
"""
AXIOM CLI - Command Line Interface for AXIOM FLAME Intelligence Suite
Provides direct access to ceremonial operations and system commands.
"""
import requests
import json
import sys
import os
from pathlib import Path

# Configuration - Use local API by default, allow override via environment
DEFAULT_API_BASE = "http://127.0.0.1:8087"
API_BASE = os.getenv("AXIOM_API_BASE", DEFAULT_API_BASE)

def get_api_url(endpoint):
    """Construct full API URL for given endpoint"""
    return f"{API_BASE}/{endpoint.lstrip('/')}"

def execute_health_check():
    """Check AXIOM FLAME API health"""
    try:
        r = requests.get(get_api_url("/health"), timeout=10)
        r.raise_for_status()
        return r.json()
    except Exception as e:
        return {"status": "error", "message": str(e)}

def execute_ceremonial_reasoning(payload):
    """Execute ceremonial reasoning operation"""
    try:
        r = requests.post(get_api_url("/api/reason"), json=payload, timeout=30)
        r.raise_for_status()
        return r.json()
    except Exception as e:
        return {"status": "error", "message": str(e)}

def execute_replay(dispatch_id):
    """Execute replay operation for a dispatch"""
    try:
        r = requests.get(get_api_url(f"/api/replay/{dispatch_id}"), timeout=30)
        r.raise_for_status()
        return r.json()
    except Exception as e:
        return {"status": "error", "message": str(e)}

def execute_audit(dispatch_id):
    """Execute audit operation for a dispatch"""
    try:
        r = requests.get(get_api_url(f"/api/audit/{dispatch_id}"), timeout=30)
        r.raise_for_status()
        return r.json()
    except Exception as e:
        return {"status": "error", "message": str(e)}

def execute_status():
    """Get detailed system status"""
    try:
        r = requests.get(get_api_url("/status"), timeout=10)
        r.raise_for_status()
        return r.json()
    except Exception as e:
        return {"status": "error", "message": str(e)}

def execute_registry_list():
    """List all registry entries"""
    try:
        r = requests.get(get_api_url("/api/ledger"), timeout=15)
        r.raise_for_status()
        return r.json()
    except Exception as e:
        return {"status": "error", "message": str(e)}

def show_usage():
    """Display usage information"""
    usage = """
AXIOM CLI - Command Line Interface for AXIOM FLAME Intelligence Suite

Usage: python axiom_cli.py <command> [arguments...]

Commands:
  health                           - Check API health status
  status                          - Get detailed system status
  reason <actor> <realm> <capsule> <intent> - Execute ceremonial reasoning
  replay <dispatch_id>            - Replay a ceremonial dispatch
  audit <dispatch_id>             - Audit a ceremonial dispatch
  registry                        - List all registry entries
  execute <command> [json_payload] - Generic API execution (legacy)

Examples:
  python axiom_cli.py health
  python axiom_cli.py status
  python axiom_cli.py reason "Custodian" "PL-001" "Sovereign Crown" "Crown.Invocation"
  python axiom_cli.py replay AXF-2025-11-11-12345678
  python axiom_cli.py audit AXF-2025-11-11-12345678
  python axiom_cli.py registry

Environment Variables:
  AXIOM_API_BASE - Override default API base URL (default: http://127.0.0.1:8087)

Current API Base: {api_base}
""".format(api_base=API_BASE)
    print(usage.strip())

def main():
    if len(sys.argv) < 2:
        show_usage()
        sys.exit(1)

    command = sys.argv[1].lower()

    try:
        if command == "health":
            result = execute_health_check()
        
        elif command == "status":
            result = execute_status()
        
        elif command == "reason":
            if len(sys.argv) < 6:
                print("Error: 'reason' command requires actor, realm, capsule, and intent")
                print("Usage: python axiom_cli.py reason <actor> <realm> <capsule> <intent>")
                sys.exit(1)
            
            payload = {
                "actor": sys.argv[2],
                "realm": sys.argv[3], 
                "capsule": sys.argv[4],
                "intent": sys.argv[5]
            }
            result = execute_ceremonial_reasoning(payload)
        
        elif command == "replay":
            if len(sys.argv) < 3:
                print("Error: 'replay' command requires dispatch_id")
                print("Usage: python axiom_cli.py replay <dispatch_id>")
                sys.exit(1)
            
            result = execute_replay(sys.argv[2])
        
        elif command == "audit":
            if len(sys.argv) < 3:
                print("Error: 'audit' command requires dispatch_id")
                print("Usage: python axiom_cli.py audit <dispatch_id>")
                sys.exit(1)
            
            result = execute_audit(sys.argv[2])
        
        elif command == "registry":
            result = execute_registry_list()
        
        elif command == "execute":
            # Legacy generic execution mode
            if len(sys.argv) < 3:
                print("Error: 'execute' command requires a sub-command")
                sys.exit(1)
            
            sub_command = sys.argv[2]
            payload = json.loads(sys.argv[3]) if len(sys.argv) > 3 else None
            
            # Route to appropriate endpoint based on sub-command
            if sub_command == "health":
                result = execute_health_check()
            elif sub_command == "ceremonial":
                result = execute_ceremonial_reasoning(payload)
            else:
                # Generic POST to API
                api_url = get_api_url("/execute")
                r = requests.post(api_url, json={"command": sub_command, "payload": payload}, timeout=30)
                r.raise_for_status()
                result = r.json()
        
        else:
            print(f"Error: Unknown command '{command}'")
            show_usage()
            sys.exit(1)

        # Output result
        print(json.dumps(result, indent=2))

    except requests.HTTPError as e:
        print(f"HTTP Error: {e.response.status_code}")
        try:
            error_detail = e.response.json()
            print(json.dumps(error_detail, indent=2))
        except:
            print(e.response.text)
        sys.exit(2)
    
    except json.JSONDecodeError as e:
        print(f"JSON Error: Invalid JSON payload - {e}")
        sys.exit(3)
    
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(4)

if __name__ == "__main__":
    main()
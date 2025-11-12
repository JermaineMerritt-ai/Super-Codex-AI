#!/usr/bin/env python3
"""
Axiom Flame - Command Line Interface
Sacred ceremonial system management for the Super-Codex-AI dominion.
"""

import sys
import os
import argparse
from pathlib import Path

# Add the packages to Python path
AXIOM_ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(AXIOM_ROOT / "packages" / "cli"))
sys.path.insert(0, str(AXIOM_ROOT / "packages" / "api"))

def main():
    """Main entry point for axiom-flame CLI."""
    parser = argparse.ArgumentParser(
        description="Axiom Flame - Sacred Ceremonial System Management",
        epilog="Use 'axiom-flame <command> --help' for command-specific help."
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Health command
    health_parser = subparsers.add_parser('health', help='Check system health')
    health_parser.add_argument('--api', action='store_true', help='Check API health')
    health_parser.add_argument('--port', type=int, default=8084, help='API port to check')
    
    # Honor command
    honor_parser = subparsers.add_parser('honor', help='Grant honors and recognition')
    honor_parser.add_argument('recipient', help='Honor recipient name')
    honor_parser.add_argument('achievement', help='Achievement description')
    honor_parser.add_argument('--realm', default='Default', help='Realm designation')
    honor_parser.add_argument('--seal', default='Eternal', help='Seal classification')
    honor_parser.add_argument('--tier', default='Bronze', help='Honor tier')
    
    # Reason command
    reason_parser = subparsers.add_parser('reason', help='Create ceremonial reasoning')
    reason_parser.add_argument('--actor', default='Custodian', help='Acting entity')
    reason_parser.add_argument('--realm', default='General', help='Realm context')
    reason_parser.add_argument('--capsule', default='General', help='Capsule designation')
    reason_parser.add_argument('--intent', default='Reasoning', help='Intent description')
    
    # Replay command
    replay_parser = subparsers.add_parser('replay', help='Replay ceremonial actions')
    replay_parser.add_argument('dispatch_id', help='Dispatch ID to replay')
    
    # Audit command
    audit_parser = subparsers.add_parser('audit', help='Audit ceremonial records')
    audit_parser.add_argument('dispatch_id', help='Dispatch ID to audit')
    
    # Service commands
    service_parser = subparsers.add_parser('service', help='Service management')
    service_subparsers = service_parser.add_subparsers(dest='service_command', help='Service operations')
    
    # Start service
    start_parser = service_subparsers.add_parser('start', help='Start a service')
    start_parser.add_argument('service_name', help='Service name')
    start_parser.add_argument('--api', action='store_true', help='Start API service')
    
    # Stop service
    stop_parser = service_subparsers.add_parser('stop', help='Stop a service')
    stop_parser.add_argument('service_name', help='Service name or ID')
    
    # List services
    service_subparsers.add_parser('list', help='List all services')
    
    # Status service
    status_parser = service_subparsers.add_parser('status', help='Get service status')
    status_parser.add_argument('service_name', help='Service name or ID')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return 1
    
    # Import and execute commands
    try:
        if args.command == 'health':
            return handle_health(args)
        elif args.command == 'honor':
            return handle_honor(args)
        elif args.command == 'reason':
            return handle_reason(args)
        elif args.command == 'replay':
            return handle_replay(args)
        elif args.command == 'audit':
            return handle_audit(args)
        elif args.command == 'service':
            return handle_service(args)
        else:
            print(f"Unknown command: {args.command}")
            return 1
            
    except Exception as e:
        print(f"Error executing command: {e}")
        return 1

def handle_health(args):
    """Handle health check commands."""
    if args.api:
        try:
            import requests
            url = f"http://127.0.0.1:{args.port}/health"
            response = requests.get(url, timeout=5)
            if response.status_code == 200:
                print(f"✅ API Health: OK (Port {args.port})")
                print(f"Response: {response.json()}")
                return 0
            else:
                print(f"❌ API Health: FAIL (Status {response.status_code})")
                return 1
        except Exception as e:
            print(f"❌ API Health: FAIL ({e})")
            return 1
    else:
        print("🔥 Axiom Flame System Health Check")
        print("✅ CLI: Operational")
        
        # Check if API files exist
        api_path = AXIOM_ROOT / "packages" / "api" / "app.py"
        if api_path.exists():
            print("✅ API: Files Present")
        else:
            print("❌ API: Files Missing")
        
        # Check if service management exists
        service_files = [
            AXIOM_ROOT.parent / "systemd_crown.py",
            AXIOM_ROOT.parent / "service_monitor.py"
        ]
        
        all_services_exist = all(f.exists() for f in service_files)
        if all_services_exist:
            print("✅ Service Management: Available")
        else:
            print("❌ Service Management: Missing Files")
        
        return 0

def handle_honor(args):
    """Handle honor granting commands."""
    try:
        import requests
        import json
        
        honor_data = {
            "recipient": args.recipient,
            "achievement": args.achievement,
            "realm": args.realm,
            "seal": args.seal,
            "tier": args.tier,
            "category": "Service"
        }
        
        # Try to use API if available
        try:
            response = requests.post(
                "http://127.0.0.1:8083/api/honors",
                json=honor_data,
                timeout=5
            )
            
            if response.status_code == 200:
                result = response.json()
                print(f"🏆 Honor Granted: {result.get('honor_id', 'Unknown ID')}")
                print(f"👤 Recipient: {args.recipient}")
                print(f"🎖️ Achievement: {args.achievement}")
                print(f"🏛️ Realm: {args.realm}")
                print(f"🔐 Seal: {args.seal}")
                return 0
            else:
                print(f"❌ API Error: {response.status_code}")
                return 1
                
        except requests.RequestException:
            # Fallback to direct file creation
            from datetime import datetime
            import uuid
            
            honor_id = f"HNR-{datetime.now().year}-{str(uuid.uuid4().int)[:3]}"
            
            honor_entry = {
                "honor_id": honor_id,
                "recipient": args.recipient,
                "realm": args.realm,
                "achievement": args.achievement,
                "timestamp": datetime.utcnow().isoformat() + 'Z',
                "seal": args.seal,
                "verification": {
                    "ceremony_refs": [],
                    "audit_passed": True,
                    "witness_count": 0
                },
                "metadata": {
                    "category": "Service",
                    "tier": args.tier
                }
            }
            
            # Save to artifacts directory
            honors_dir = AXIOM_ROOT / "artifacts" / "honors"
            honors_dir.mkdir(parents=True, exist_ok=True)
            
            honor_file = honors_dir / f"{honor_id}.json"
            with open(honor_file, 'w') as f:
                json.dump(honor_entry, f, indent=2)
            
            print(f"🏆 Honor Granted: {honor_id}")
            print(f"👤 Recipient: {args.recipient}")
            print(f"🎖️ Achievement: {args.achievement}")
            print(f"📁 Saved to: {honor_file}")
            return 0
            
    except Exception as e:
        print(f"❌ Error granting honor: {e}")
        return 1

def handle_reason(args):
    """Handle ceremonial reasoning commands."""
    try:
        import requests
        import json
        
        reason_data = {
            "actor": args.actor,
            "realm": args.realm,
            "capsule": args.capsule,
            "intent": args.intent,
            "seal": "Eternal"
        }
        
        response = requests.post(
            "http://127.0.0.1:8083/reason",
            json=reason_data,
            timeout=5
        )
        
        if response.status_code == 200:
            result = response.json()
            print(f"🔮 Reasoning Complete: {result.get('dispatch_id', 'Unknown')}")
            print(f"📋 Summary: {result.get('summary', 'No summary')}")
            return 0
        else:
            print(f"❌ Reasoning Failed: {response.status_code}")
            return 1
            
    except Exception as e:
        print(f"❌ Error in reasoning: {e}")
        return 1

def handle_replay(args):
    """Handle replay commands."""
    try:
        import requests
        
        response = requests.post(
            "http://127.0.0.1:8083/replay",
            json={"dispatch_id": args.dispatch_id},
            timeout=5
        )
        
        if response.status_code == 200:
            result = response.json()
            print(f"🔄 Replay Complete: {result.get('replay', {}).get('replay_id', 'Unknown')}")
            return 0
        else:
            print(f"❌ Replay Failed: {response.status_code}")
            return 1
            
    except Exception as e:
        print(f"❌ Error in replay: {e}")
        return 1

def handle_audit(args):
    """Handle audit commands."""
    try:
        import requests
        
        response = requests.post(
            "http://127.0.0.1:8083/audit",
            json={"dispatch_id": args.dispatch_id},
            timeout=5
        )
        
        if response.status_code == 200:
            result = response.json()
            status = "✅ PRESENT" if result.get('ok') else "❌ MISSING"
            print(f"🔍 Audit Result: {status}")
            print(f"📋 Dispatch ID: {args.dispatch_id}")
            print(f"📝 Status: {result.get('audit', 'Unknown')}")
            return 0
        else:
            print(f"❌ Audit Failed: {response.status_code}")
            return 1
            
    except Exception as e:
        print(f"❌ Error in audit: {e}")
        return 1

def handle_service(args):
    """Handle service management commands."""
    if not args.service_command:
        print("Service command required. Use --help for details.")
        return 1
    
    try:
        # Import service management
        sys.path.insert(0, str(AXIOM_ROOT.parent))
        
        if args.service_command == 'start':
            if args.api:
                # Start API service using SystemD Crown
                from systemd_crown import SystemdCrown
                
                crown = SystemdCrown()
                api_path = str(AXIOM_ROOT / "packages" / "api")
                
                service_id = crown.ignite_eternal_flame(
                    name=f"Axiom Flame API ({args.service_name})",
                    command=["python", "app.py"],
                    working_dir=api_path
                )
                
                if service_id:
                    print(f"🔥 Service Ignited: {service_id}")
                    return 0
                else:
                    print("❌ Failed to ignite service")
                    return 1
            else:
                print(f"Starting service: {args.service_name}")
                return 0
                
        elif args.service_command == 'stop':
            from systemd_crown import SystemdCrown
            
            crown = SystemdCrown()
            if crown.extinguish_flame(args.service_name):
                print(f"🌫️ Service Stopped: {args.service_name}")
                return 0
            else:
                print(f"❌ Failed to stop service: {args.service_name}")
                return 1
                
        elif args.service_command == 'list':
            from systemd_crown import SystemdCrown
            
            crown = SystemdCrown()
            flames = crown.list_flames()
            
            if flames:
                print("\n🔥 Eternal Flames Status:")
                print("-" * 80)
                for flame in flames:
                    status_icon = "🔥" if flame['process_alive'] else "🌫️"
                    print(f"{status_icon} {flame['name']:<30} | {flame['service_id']:<20} | {flame['state']:<12}")
            else:
                print("🌫️ No eternal flames currently burning")
            return 0
            
        elif args.service_command == 'status':
            from systemd_crown import SystemdCrown
            
            crown = SystemdCrown()
            status = crown.flame_status(args.service_name)
            
            if status:
                print(f"\n🔥 Service Status: {status['name']}")
                print("-" * 50)
                for key, value in status.items():
                    print(f"{key:<20}: {value}")
                return 0
            else:
                print(f"❌ Service not found: {args.service_name}")
                return 1
        else:
            print(f"Unknown service command: {args.service_command}")
            return 1
            
    except ImportError as e:
        print(f"❌ Service management not available: {e}")
        return 1
    except Exception as e:
        print(f"❌ Service error: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(main())
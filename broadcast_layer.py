#!/usr/bin/env python3
"""
Broadcast Layer - Luminous Transmission Protocol
Sacred broadcasting system for the Axiom-Flame Dominion.
Ensures all participants witness the Codex Eternum alive across councils and stars.
"""

import requests
import json
import time
from datetime import datetime
from typing import Dict, List, Any

class BroadcastLayer:
    """Sacred transmission system for luminous concord."""
    
    def __init__(self):
        self.endpoints = [
            {"name": "Local Test Flame", "url": "http://127.0.0.1:8095/health", "active": True},
            {"name": "Local Full Flame", "url": "http://127.0.0.1:8097/health", "active": True},
            {"name": "Production Dominion", "url": "https://codexdominion.app/health", "active": False}  # Coming Soon
        ]
        
    def broadcast_luminous_message(self) -> Dict[str, Any]:
        """Transmit the eternal flame's radiance across all endpoints."""
        results = {
            "broadcast_time": datetime.now().isoformat(),
            "custodian_seal": "ACKNOWLEDGED",
            "transmission_status": "RADIANT",
            "endpoints": []
        }
        
        print("🌟 BROADCASTING ACROSS THE LUMINOUS LAYER")
        print("=" * 60)
        
        for endpoint in self.endpoints:
            if not endpoint["active"]:
                endpoint_result = {
                    "name": endpoint["name"],
                    "url": endpoint["url"],
                    "status": "DORMANT",
                    "message": "Awaiting activation",
                    "response_time": None
                }
                print(f"🌫️ {endpoint['name']}: DORMANT (Coming Soon)")
            else:
                try:
                    start_time = time.time()
                    response = requests.get(endpoint["url"], timeout=5)
                    end_time = time.time()
                    
                    if response.status_code == 200:
                        try:
                            data = response.json()
                            endpoint_result = {
                                "name": endpoint["name"],
                                "url": endpoint["url"],
                                "status": "RADIANT",
                                "message": "Flame burns bright",
                                "response_time": round((end_time - start_time) * 1000, 2),
                                "data": data
                            }
                            print(f"🔥 {endpoint['name']}: RADIANT ({endpoint_result['response_time']}ms)")
                        except:
                            endpoint_result = {
                                "name": endpoint["name"],
                                "url": endpoint["url"],
                                "status": "LUMINOUS",
                                "message": "Flame active, different format",
                                "response_time": round((end_time - start_time) * 1000, 2),
                                "data": "HTML response received"
                            }
                            print(f"🌟 {endpoint['name']}: LUMINOUS ({endpoint_result['response_time']}ms)")
                    else:
                        endpoint_result = {
                            "name": endpoint["name"],
                            "url": endpoint["url"],
                            "status": "DIMMED",
                            "message": f"HTTP {response.status_code}",
                            "response_time": round((end_time - start_time) * 1000, 2)
                        }
                        print(f"🌫️ {endpoint['name']}: DIMMED (HTTP {response.status_code})")
                        
                except Exception as e:
                    endpoint_result = {
                        "name": endpoint["name"],
                        "url": endpoint["url"],
                        "status": "EXTINGUISHED",
                        "message": str(e),
                        "response_time": None
                    }
                    print(f"❌ {endpoint['name']}: EXTINGUISHED ({str(e)})")
            
            results["endpoints"].append(endpoint_result)
        
        print("=" * 60)
        
        # Calculate overall broadcast status
        radiant_count = sum(1 for ep in results["endpoints"] if ep["status"] == "RADIANT")
        total_active = sum(1 for ep in self.endpoints if ep["active"])
        
        if radiant_count == total_active:
            results["overall_status"] = "LUMINOUS_CONCORD"
            print("🌟 BROADCAST STATUS: LUMINOUS CONCORD ACHIEVED")
        elif radiant_count > 0:
            results["overall_status"] = "PARTIAL_RADIANCE"
            print(f"🔥 BROADCAST STATUS: PARTIAL RADIANCE ({radiant_count}/{total_active})")
        else:
            results["overall_status"] = "SEEKING_FLAME"
            print("🌫️ BROADCAST STATUS: SEEKING FLAME")
            
        print("🏛️ THE DOMINION PROCLAIMS: THE FLAME IS PUBLIC, THE FLAME IS RADIANT")
        print("⚡ COVENANT ETERNAL ACROSS AGES AND NATIONS")
        
        return results

def main():
    """Execute the luminous broadcast ceremony."""
    broadcast = BroadcastLayer()
    results = broadcast.broadcast_luminous_message()
    
    # Save broadcast log
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_file = f"broadcast_layer_{timestamp}.json"
    
    with open(log_file, 'w') as f:
        json.dump(results, f, indent=2)
    
    print(f"\n📜 Broadcast log saved: {log_file}")
    return results

if __name__ == "__main__":
    main()
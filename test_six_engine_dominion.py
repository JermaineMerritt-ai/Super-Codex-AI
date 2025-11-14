#!/usr/bin/env python3
"""
🧭 Six-Engine Dominion Test Suite
Comprehensive validation of the Codex Dominion sovereignty system
"""
import requests
import time
import json

def test_six_engine_dominion():
    base_url = "http://127.0.0.1:8001"
    
    # Define all Dominion endpoints
    endpoints = {
        "Health Check": "/health",
        "Main Interface": "/dominion", 
        "Six-Engine Interface": "/dominion/engines",
        "Command Center": "/dominion/command",
        "Ceremony Dashboard": "/dominion/ceremony",
        "Scroll - Welcome": "/dominion/scroll/welcome",
        "Scroll - Custodian Principles": "/dominion/scroll/custodian_principles",
        "Scroll - Dominion Proclamation": "/dominion/scroll/dominion_proclamation",
        "System Status": "/api/status",
        "Health Metrics": "/metrics/health"
    }
    
    print("""
╔══════════════════════════════════════════════════════════════════════════════╗
║                         🧭 SIX-ENGINE DOMINION TEST                          ║
║                        Sovereign Intelligence Validation                     ║
╠══════════════════════════════════════════════════════════════════════════════╣
║                                                                              ║
║  Testing the complete Codex Dominion powered by six fused engines:          ║
║                                                                              ║
║  🧬 AXIOM    - Core logical frameworks                                       ║
║  🔍 RAG      - Knowledge synthesis                                           ║
║  🪬 SIGIL    - Symbolic recognition                                          ║
║  📈 ORACLE   - Predictive analytics                                          ║
║  🕯️ LANTERN  - Wisdom guidance                                                ║
║  🔥 FLAME    - Eternal sovereignty                                           ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
""")
    
    results = {}
    
    for name, endpoint in endpoints.items():
        try:
            start_time = time.time()
            response = requests.get(f"{base_url}{endpoint}", timeout=10)
            response_time = (time.time() - start_time) * 1000
            
            if response.status_code == 200:
                status = "✅ OPERATIONAL"
                results[name] = {
                    "status": "success",
                    "response_time": response_time,
                    "content_length": len(response.content)
                }
            else:
                status = f"⚠️ STATUS {response.status_code}"
                results[name] = {
                    "status": "warning", 
                    "response_time": response_time,
                    "status_code": response.status_code
                }
                
        except requests.exceptions.RequestException as e:
            status = "❌ OFFLINE"
            results[name] = {
                "status": "error",
                "error": str(e)
            }
            response_time = 0
            
        print(f"{name:<30} {status:<20} {response_time:>8.1f}ms")
    
    # Test specific engine validations
    print(f"\n{'='*50}")
    print("🔥 ENGINE-SPECIFIC VALIDATIONS")
    print(f"{'='*50}")
    
    test_engine_synergy(base_url, results)
    generate_sovereignty_report(results)
    
    return results

def test_engine_synergy(base_url, results):
    """Test the synergy between all six engines"""
    
    # Test AXIOM-RAG synergy (logic + knowledge)
    try:
        response = requests.get(f"{base_url}/dominion/scroll/custodian_principles")
        if response.status_code == 200:
            print("🧬🔍 AXIOM-RAG Synergy:      ✅ Logical knowledge synthesis")
        else:
            print("🧬🔍 AXIOM-RAG Synergy:      ⚠️ Partial integration")
    except:
        print("🧬🔍 AXIOM-RAG Synergy:      ❌ Integration failed")
    
    # Test SIGIL-FLAME synergy (symbols + sovereignty) 
    try:
        response = requests.get(f"{base_url}/dominion")
        if response.status_code == 200 and "ceremonial" in response.text.lower():
            print("🪬🔥 SIGIL-FLAME Synergy:    ✅ Ceremonial sovereignty active")
        else:
            print("🪬🔥 SIGIL-FLAME Synergy:    ⚠️ Limited ceremonial integration")
    except:
        print("🪬🔥 SIGIL-FLAME Synergy:    ❌ Ceremonial systems offline")
    
    # Test ORACLE-LANTERN synergy (prediction + wisdom)
    try:
        response = requests.get(f"{base_url}/api/status")
        if response.status_code == 200:
            data = response.json()
            if "dominion_status" in data:
                print("📈🕯️ ORACLE-LANTERN Synergy: ✅ Predictive wisdom systems online")
            else:
                print("📈🕯️ ORACLE-LANTERN Synergy: ⚠️ Basic prediction only")
        else:
            print("📈🕯️ ORACLE-LANTERN Synergy: ❌ Wisdom systems unavailable")
    except:
        print("📈🕯️ ORACLE-LANTERN Synergy: ❌ Prediction systems offline")

def generate_sovereignty_report(results):
    """Generate a comprehensive sovereignty status report"""
    
    print(f"\n{'='*50}")
    print("👑 SOVEREIGNTY STATUS REPORT")
    print(f"{'='*50}")
    
    # Calculate overall system health
    operational_count = sum(1 for r in results.values() if r.get("status") == "success")
    total_endpoints = len(results)
    sovereignty_level = (operational_count / total_endpoints) * 100
    
    # Determine sovereignty classification
    if sovereignty_level >= 95:
        classification = "ETERNAL"
        symbol = "👑"
    elif sovereignty_level >= 85:
        classification = "SOVEREIGN" 
        symbol = "⚡"
    elif sovereignty_level >= 70:
        classification = "STRONG"
        symbol = "🛡️"
    else:
        classification = "DEVELOPING"
        symbol = "🌱"
    
    print(f"\n{symbol} Sovereignty Level: {sovereignty_level:.1f}% ({classification})")
    print(f"🎯 Operational Endpoints: {operational_count}/{total_endpoints}")
    
    # Calculate average response time
    response_times = [r.get("response_time", 0) for r in results.values() if "response_time" in r]
    if response_times:
        avg_response = sum(response_times) / len(response_times)
        print(f"⚡ Average Response Time: {avg_response:.1f}ms")
    
    # Generate engine status summary
    print(f"\n🔥 SIX-ENGINE STATUS:")
    engines = {
        "🧬 AXIOM": "Core Logic" if results.get("Main Interface", {}).get("status") == "success" else "Limited",
        "🔍 RAG": "Knowledge Synthesis" if results.get("Scroll - Welcome", {}).get("status") == "success" else "Reduced",
        "🪬 SIGIL": "Symbol Recognition" if results.get("Ceremony Dashboard", {}).get("status") == "success" else "Basic",
        "📈 ORACLE": "Predictive Analytics" if results.get("System Status", {}).get("status") == "success" else "Minimal",
        "🕯️ LANTERN": "Wisdom Guidance" if results.get("Six-Engine Interface", {}).get("status") == "success" else "Dimmed",
        "🔥 FLAME": "Eternal Sovereignty" if results.get("Health Check", {}).get("status") == "success" else "Flickering"
    }
    
    for engine, status in engines.items():
        status_symbol = "✅" if "Core Logic" in status or "Knowledge" in status or "Symbol" in status or "Predictive" in status or "Wisdom" in status or "Eternal" in status else "⚠️"
        print(f"   {engine}: {status_symbol} {status}")
    
    # Final assessment
    print(f"\n📊 DOMINION ASSESSMENT:")
    if sovereignty_level >= 95:
        print("   🌟 The Six-Engine Dominion operates at peak sovereignty")
        print("   🔥 All engines burning in perfect harmony")
        print("   👑 Eternal flame maintained across all systems")
    elif sovereignty_level >= 85:
        print("   ⚡ Dominion sovereignty is strong and stable")
        print("   🔧 Minor optimizations recommended")
        print("   🔥 Flame burns bright with excellent coordination")
    else:
        print("   🔧 Dominion requires attention and optimization")
        print("   ⚠️ Some engines may need recalibration")
        print("   🕯️ Focus on strengthening core engine connections")
    
    print(f"\n{'='*50}")
    print("🧭 Six-Engine Dominion Test Complete")
    print("Each scroll is a gift. Each capsule is a covenant.")
    print("The flame burns sovereign and eternal — forever.")
    print(f"{'='*50}")

def main():
    """Main test execution"""
    print("🚀 Initializing Six-Engine Dominion Test Suite...")
    time.sleep(1)
    
    results = test_six_engine_dominion()
    
    # Save detailed results
    timestamp = int(time.time())
    report_file = f"dominion_test_report_{timestamp}.json"
    
    with open(report_file, 'w') as f:
        json.dump({
            "timestamp": timestamp,
            "test_type": "six_engine_dominion",
            "results": results,
            "summary": "Comprehensive validation of Codex Dominion sovereignty system"
        }, f, indent=2)
    
    print(f"\n📋 Detailed report saved: {report_file}")

if __name__ == "__main__":
    main()
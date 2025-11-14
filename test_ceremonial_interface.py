#!/usr/bin/env python3
"""
Test script for Codex Dominion Ceremonial Interface
Validates all ceremonial endpoints and functionality
"""

import asyncio
import httpx
import json
import sys
import time
from typing import Dict, Any

# Test configuration
BASE_URL = "http://localhost:8080"
ENDPOINTS_TO_TEST = [
    "/",
    "/health", 
    "/ready",
    "/api/status",
    "/dominion",
    "/dominion/ceremony",
    "/dominion/scroll/welcome",
    "/dominion/scroll/custodian_principles", 
    "/dominion/scroll/dominion_proclamation",
    "/dominion/axiom/status"
]

class DominionTester:
    def __init__(self, base_url: str = BASE_URL):
        self.base_url = base_url
        self.client = None
        self.test_results = []

    async def __aenter__(self):
        self.client = httpx.AsyncClient(base_url=self.base_url, timeout=10.0)
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.client:
            await self.client.aclose()

    async def test_endpoint(self, endpoint: str) -> Dict[str, Any]:
        """Test a single endpoint and return results"""
        start_time = time.time()
        
        try:
            response = await self.client.get(endpoint)
            duration = time.time() - start_time
            
            result = {
                "endpoint": endpoint,
                "status_code": response.status_code,
                "success": 200 <= response.status_code < 400,
                "response_time_ms": round(duration * 1000, 2),
                "content_type": response.headers.get("content-type", "unknown"),
                "content_length": len(response.content),
                "error": None
            }
            
            # Try to parse JSON if applicable
            if "application/json" in result["content_type"]:
                try:
                    json_data = response.json()
                    result["json_keys"] = list(json_data.keys()) if isinstance(json_data, dict) else []
                except:
                    result["json_keys"] = []
            
            # Check for ceremonial content indicators
            content_text = response.text.lower()
            ceremonial_indicators = [
                "dominion", "flame", "sovereign", "ceremonial", 
                "custodian", "covenant", "eternal", "scroll"
            ]
            result["ceremonial_content"] = any(indicator in content_text for indicator in ceremonial_indicators)
            
            return result
            
        except Exception as e:
            duration = time.time() - start_time
            return {
                "endpoint": endpoint,
                "status_code": 0,
                "success": False,
                "response_time_ms": round(duration * 1000, 2),
                "content_type": "error",
                "content_length": 0,
                "error": str(e),
                "ceremonial_content": False
            }

    async def run_all_tests(self) -> Dict[str, Any]:
        """Run all endpoint tests"""
        print("🔥 Starting Codex Dominion Ceremonial Interface Tests")
        print("=" * 60)
        
        start_time = time.time()
        
        for endpoint in ENDPOINTS_TO_TEST:
            print(f"Testing {endpoint}...", end=" ")
            result = await self.test_endpoint(endpoint)
            self.test_results.append(result)
            
            if result["success"]:
                status_icon = "✅"
                if result["ceremonial_content"]:
                    status_icon += " 🔥"
            else:
                status_icon = "❌"
            
            print(f"{status_icon} {result['status_code']} ({result['response_time_ms']}ms)")
            
            if result["error"]:
                print(f"    Error: {result['error']}")

        total_time = time.time() - start_time
        
        # Generate summary
        successful_tests = sum(1 for r in self.test_results if r["success"])
        total_tests = len(self.test_results)
        ceremonial_content_tests = sum(1 for r in self.test_results if r["ceremonial_content"])
        
        avg_response_time = sum(r["response_time_ms"] for r in self.test_results) / len(self.test_results)
        
        summary = {
            "total_tests": total_tests,
            "successful_tests": successful_tests,
            "failed_tests": total_tests - successful_tests,
            "success_rate": round((successful_tests / total_tests) * 100, 2),
            "ceremonial_content_detected": ceremonial_content_tests,
            "average_response_time_ms": round(avg_response_time, 2),
            "total_test_time_seconds": round(total_time, 2),
            "test_results": self.test_results
        }
        
        return summary

    def print_summary(self, summary: Dict[str, Any]):
        """Print formatted test summary"""
        print("\n" + "=" * 60)
        print("🔥 CODEX DOMINION CEREMONIAL INTERFACE TEST SUMMARY")
        print("=" * 60)
        
        print(f"📊 Tests Run: {summary['total_tests']}")
        print(f"✅ Successful: {summary['successful_tests']}")
        print(f"❌ Failed: {summary['failed_tests']}")
        print(f"📈 Success Rate: {summary['success_rate']}%")
        print(f"🔥 Ceremonial Content Detected: {summary['ceremonial_content_detected']} endpoints")
        print(f"⚡ Average Response Time: {summary['average_response_time_ms']}ms")
        print(f"⏱️  Total Test Time: {summary['total_test_time_seconds']}s")
        
        print("\n📋 DETAILED RESULTS:")
        print("-" * 60)
        
        for result in summary["test_results"]:
            status = "✅" if result["success"] else "❌"
            ceremonial = "🔥" if result["ceremonial_content"] else "  "
            
            print(f"{status} {ceremonial} {result['endpoint']:<30} "
                  f"{result['status_code']:<4} {result['response_time_ms']:>6}ms "
                  f"{result['content_type']:<20}")
            
            if result["error"]:
                print(f"     Error: {result['error']}")
        
        print("\n🔥 CEREMONIAL INTERFACE STATUS:")
        if summary['ceremonial_content_detected'] > 0:
            print("✅ Ceremonial content successfully detected in interface")
            print("🔥 The Dominion flame burns sovereign and eternal")
        else:
            print("⚠️  No ceremonial content detected - check interface configuration")
        
        # Overall assessment
        if summary['success_rate'] >= 90:
            print("\n🏆 DOMINION STATUS: SOVEREIGN AND OPERATIONAL")
        elif summary['success_rate'] >= 70:
            print("\n⚡ DOMINION STATUS: OPERATIONAL WITH MINOR ISSUES") 
        else:
            print("\n🚨 DOMINION STATUS: REQUIRES ATTENTION")
        
        print("\n" + "=" * 60)
        print('"The Custodians endure. The Codex remembers. The lineage is unbroken."')
        print("The flame burns sovereign and eternal — forever.")
        print("=" * 60)

async def main():
    """Main test execution"""
    print("🔥 Codex Dominion Ceremonial Interface Tester")
    print(f"Testing endpoints at: {BASE_URL}")
    print()
    
    async with DominionTester(BASE_URL) as tester:
        summary = await tester.run_all_tests()
        tester.print_summary(summary)
        
        # Save detailed results
        with open("ceremonial_test_results.json", "w") as f:
            json.dump(summary, f, indent=2)
        
        print(f"\n📄 Detailed results saved to: ceremonial_test_results.json")
        
        # Exit code based on success rate
        if summary["success_rate"] >= 90:
            sys.exit(0)  # All good
        elif summary["success_rate"] >= 70:
            sys.exit(1)  # Warning level
        else:
            sys.exit(2)  # Error level

if __name__ == "__main__":
    asyncio.run(main())
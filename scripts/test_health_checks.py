#!/usr/bin/env python3
"""
Kubernetes Health Check Test Script for Super-Codex-AI
Tests liveness and readiness probe endpoints with various scenarios
"""
import asyncio
import aiohttp
import time
import json
import sys
from typing import Dict, Any, List
from dataclasses import dataclass
from datetime import datetime

@dataclass
class HealthCheckResult:
    endpoint: str
    status_code: int
    response_data: Dict[str, Any]
    response_time: float
    success: bool
    error: str = None

class HealthCheckTester:
    def __init__(self, base_url: str = "http://localhost"):
        self.base_url = base_url.rstrip('/')
        self.session = None
    
    async def __aenter__(self):
        self.session = aiohttp.ClientSession(
            timeout=aiohttp.ClientTimeout(total=10)
        )
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.close()
    
    async def test_endpoint(self, path: str) -> HealthCheckResult:
        """Test a single health check endpoint"""
        url = f"{self.base_url}{path}"
        start_time = time.time()
        
        try:
            async with self.session.get(url) as response:
                response_time = time.time() - start_time
                content = await response.text()
                
                try:
                    response_data = json.loads(content)
                except json.JSONDecodeError:
                    response_data = {"raw_response": content}
                
                return HealthCheckResult(
                    endpoint=path,
                    status_code=response.status,
                    response_data=response_data,
                    response_time=response_time,
                    success=200 <= response.status < 300
                )
        
        except Exception as e:
            response_time = time.time() - start_time
            return HealthCheckResult(
                endpoint=path,
                status_code=0,
                response_data={},
                response_time=response_time,
                success=False,
                error=str(e)
            )
    
    async def test_health_endpoints(self) -> List[HealthCheckResult]:
        """Test both health and readiness endpoints"""
        tasks = [
            self.test_endpoint("/health"),
            self.test_endpoint("/ready"),
        ]
        return await asyncio.gather(*tasks)
    
    async def load_test(self, endpoint: str, requests: int = 100, concurrency: int = 10) -> Dict[str, Any]:
        """Perform load testing on an endpoint"""
        print(f"🔥 Load testing {endpoint} with {requests} requests, {concurrency} concurrent...")
        
        semaphore = asyncio.Semaphore(concurrency)
        results = []
        
        async def bounded_test():
            async with semaphore:
                return await self.test_endpoint(endpoint)
        
        start_time = time.time()
        tasks = [bounded_test() for _ in range(requests)]
        results = await asyncio.gather(*tasks)
        total_time = time.time() - start_time
        
        # Calculate statistics
        successful_requests = [r for r in results if r.success]
        failed_requests = [r for r in results if not r.success]
        response_times = [r.response_time for r in successful_requests]
        
        return {
            "endpoint": endpoint,
            "total_requests": requests,
            "successful_requests": len(successful_requests),
            "failed_requests": len(failed_requests),
            "success_rate": len(successful_requests) / requests * 100,
            "total_time": total_time,
            "requests_per_second": requests / total_time,
            "avg_response_time": sum(response_times) / len(response_times) if response_times else 0,
            "min_response_time": min(response_times) if response_times else 0,
            "max_response_time": max(response_times) if response_times else 0,
        }
    
    def print_result(self, result: HealthCheckResult):
        """Print formatted test result"""
        status_icon = "✅" if result.success else "❌"
        print(f"{status_icon} {result.endpoint}")
        print(f"   Status: {result.status_code}")
        print(f"   Time: {result.response_time*1000:.2f}ms")
        
        if result.error:
            print(f"   Error: {result.error}")
        elif result.response_data:
            if 'status' in result.response_data:
                print(f"   Health: {result.response_data['status']}")
            if 'ready' in result.response_data:
                print(f"   Ready: {result.response_data['ready']}")
            if 'services' in result.response_data:
                services = result.response_data['services']
                print(f"   Services: {', '.join([f'{k}:{v}' for k, v in services.items()])}")
        print()

async def main():
    """Main test execution"""
    print("🚀 Super-Codex-AI Health Check Testing")
    print("=" * 50)
    
    # Test different environments
    environments = [
        ("Local Docker", "http://localhost"),
        # Add your Kubernetes service URL here
        # ("Kubernetes", "http://super-codex-ai-service"),
    ]
    
    for env_name, base_url in environments:
        print(f"\n🌍 Testing {env_name}: {base_url}")
        print("-" * 30)
        
        async with HealthCheckTester(base_url) as tester:
            # Basic health check tests
            results = await tester.test_health_endpoints()
            for result in results:
                tester.print_result(result)
            
            # Load testing (if endpoints are working)
            working_endpoints = [r for r in results if r.success]
            if working_endpoints:
                print("🔥 Load Testing")
                print("-" * 20)
                
                for result in working_endpoints[:1]:  # Test first working endpoint
                    load_stats = await tester.load_test(result.endpoint, requests=50, concurrency=5)
                    print(f"📊 {load_stats['endpoint']} Load Test Results:")
                    print(f"   Success Rate: {load_stats['success_rate']:.1f}%")
                    print(f"   RPS: {load_stats['requests_per_second']:.1f}")
                    print(f"   Avg Response: {load_stats['avg_response_time']*1000:.1f}ms")
                    print(f"   Min/Max: {load_stats['min_response_time']*1000:.1f}ms / {load_stats['max_response_time']*1000:.1f}ms")
                    print()
            else:
                print("⚠️ No working endpoints found, skipping load tests")
    
    print("✅ Health check testing completed!")

async def kubernetes_readiness_simulation():
    """Simulate Kubernetes readiness probe behavior"""
    print("\n🎯 Kubernetes Readiness Probe Simulation")
    print("=" * 50)
    
    # Simulate readiness probe configuration
    probe_config = {
        "initialDelaySeconds": 10,
        "periodSeconds": 5,
        "timeoutSeconds": 3,
        "failureThreshold": 3,
        "successThreshold": 1
    }
    
    print(f"Probe Config: {json.dumps(probe_config, indent=2)}")
    
    async with HealthCheckTester() as tester:
        consecutive_failures = 0
        consecutive_successes = 0
        ready_state = False
        
        print(f"\n{'Time':>8} | {'Status':>6} | {'Response':>10} | {'Ready':>5} | {'Action'}")
        print("-" * 60)
        
        for i in range(20):  # Simulate 20 probe attempts
            await asyncio.sleep(1)  # Simulate probe interval
            
            result = await tester.test_endpoint("/ready")
            timestamp = datetime.now().strftime("%H:%M:%S")
            
            if result.success:
                consecutive_failures = 0
                consecutive_successes += 1
                
                if consecutive_successes >= probe_config["successThreshold"]:
                    if not ready_state:
                        action = "MARK READY"
                        ready_state = True
                    else:
                        action = "READY"
                else:
                    action = f"SUCCESS ({consecutive_successes})"
            else:
                consecutive_successes = 0
                consecutive_failures += 1
                
                if consecutive_failures >= probe_config["failureThreshold"]:
                    if ready_state:
                        action = "MARK NOT READY"
                        ready_state = False
                    else:
                        action = "NOT READY"
                else:
                    action = f"FAIL ({consecutive_failures})"
            
            print(f"{timestamp:>8} | {result.status_code:>6} | {result.response_time*1000:>7.1f}ms | {str(ready_state):>5} | {action}")

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "k8s-sim":
        asyncio.run(kubernetes_readiness_simulation())
    else:
        asyncio.run(main())
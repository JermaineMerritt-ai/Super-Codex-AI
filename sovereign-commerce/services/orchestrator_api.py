"""
AXIOM-FLAME Orchestrator API - Python Backend Integration
Provides HTTP endpoints to access the TypeScript orchestrator from the Sovereign Commerce platform
"""

import json
import subprocess
import tempfile
import os
from typing import Dict, Any, Optional
from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from datetime import datetime

# Pydantic models for API
class OrchestrationRequest(BaseModel):
    phrase: str
    metadata: Optional[Dict[str, Any]] = None

class OrchestrationResponse(BaseModel):
    status: str
    intent: Dict[str, Any]
    engines: Dict[str, Any]
    timestamp: str
    execution_time_ms: int

class EngineStatus(BaseModel):
    engine: str
    description: str
    available: bool

# Create the router
orchestrator_router = APIRouter(prefix="/api/orchestrator", tags=["orchestrator"])

# Authentication dependency (will be provided by the main app)
def get_auth_dependency():
    """
    This function will be replaced with the actual get_current_user dependency
    when the router is included in the main app.
    """
    pass

class AxiomOrchestrator:
    """Python wrapper for the TypeScript AXIOM-FLAME Orchestrator"""
    
    def __init__(self):
        self.orchestrator_path = os.path.join(
            os.path.dirname(__file__), 
            "..", "..", "axiom", "dist", "orchestrator.js"
        )
        self._ensure_compiled()
    
    def _ensure_compiled(self):
        """Ensure the TypeScript orchestrator is compiled"""
        axiom_dir = os.path.join(os.path.dirname(__file__), "..", "..", "axiom")
        
        # Check if compiled version exists
        if not os.path.exists(self.orchestrator_path):
            try:
                # Compile TypeScript
                result = subprocess.run([
                    "npx", "tsc", "orchestrator.ts", 
                    "--target", "es2020", 
                    "--module", "commonjs", 
                    "--outDir", "dist",
                    "--skipLibCheck"
                ], 
                cwd=axiom_dir,
                capture_output=True,
                text=True
                )
                
                if result.returncode != 0:
                    print(f"TypeScript compilation failed: {result.stderr}")
                    
            except Exception as e:
                print(f"Failed to compile orchestrator: {e}")
    
    def invoke_codex(self, phrase: str) -> Dict[str, Any]:
        """Invoke the AXIOM-FLAME orchestrator with a natural language phrase"""
        
        start_time = datetime.now()
        
        try:
            # Create a temporary script to run the orchestrator
            script_content = f"""
const {{ invokeCodex }} = require('{self.orchestrator_path}');

async function run() {{
    try {{
        const result = await invokeCodex("{phrase}");
        console.log(JSON.stringify(result, null, 2));
    }} catch (error) {{
        console.error(JSON.stringify({{
            status: "failed",
            error: error.message,
            intent: null,
            engines: {{}}
        }}, null, 2));
    }}
}}

run();
"""
            
            # Write and execute the script
            with tempfile.NamedTemporaryFile(mode='w', suffix='.js', delete=False) as f:
                f.write(script_content)
                script_path = f.name
            
            try:
                result = subprocess.run([
                    'node', script_path
                ], capture_output=True, text=True, timeout=30)
                
                if result.returncode == 0:
                    # Parse the JSON output
                    orchestration_result = json.loads(result.stdout)
                    
                    # Add execution timing
                    end_time = datetime.now()
                    execution_time = int((end_time - start_time).total_seconds() * 1000)
                    orchestration_result['execution_time_ms'] = execution_time
                    
                    return orchestration_result
                else:
                    raise Exception(f"Orchestrator failed: {result.stderr}")
                    
            finally:
                # Cleanup
                os.unlink(script_path)
                
        except subprocess.TimeoutExpired:
            raise Exception("Orchestrator execution timed out")
        except json.JSONDecodeError as e:
            raise Exception(f"Failed to parse orchestrator output: {e}")
        except Exception as e:
            raise Exception(f"Orchestrator execution failed: {e}")
    
    def get_engine_status(self) -> Dict[str, str]:
        """Get the status of all AXIOM-FLAME engines"""
        
        try:
            script_content = f"""
const {{ getEngineStatus }} = require('{self.orchestrator_path}');
const status = getEngineStatus();
console.log(JSON.stringify(status, null, 2));
"""
            
            with tempfile.NamedTemporaryFile(mode='w', suffix='.js', delete=False) as f:
                f.write(script_content)
                script_path = f.name
            
            try:
                result = subprocess.run([
                    'node', script_path
                ], capture_output=True, text=True, timeout=10)
                
                if result.returncode == 0:
                    return json.loads(result.stdout)
                else:
                    return {"error": f"Failed to get engine status: {result.stderr}"}
                    
            finally:
                os.unlink(script_path)
                
        except Exception as e:
            return {"error": f"Engine status check failed: {e}"}

# Initialize the orchestrator
orchestrator = AxiomOrchestrator()

@orchestrator_router.post("/invoke", response_model=OrchestrationResponse)
async def invoke_orchestrator(
    request: OrchestrationRequest
):
    """
    Invoke the AXIOM-FLAME orchestrator with a natural language phrase
    
    Transforms natural language into fully orchestrated platform generation
    across RAG, SIGIL, ORACLE, LANTERN, and FLAME engines.
    """
    
    try:
        result = orchestrator.invoke_codex(request.phrase)
        
        # Validate the response structure
        if not isinstance(result, dict) or 'status' not in result:
            raise HTTPException(
                status_code=500, 
                detail="Invalid orchestrator response format"
            )
        
        return OrchestrationResponse(**result)
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Orchestration failed: {str(e)}"
        )

@orchestrator_router.get("/engines", response_model=Dict[str, str])
async def get_engine_status():
    """
    Get the operational status of all AXIOM-FLAME engines
    
    Returns the current status and capabilities of:
    - RAG (Template Retrieval)
    - SIGIL (UI Composition) 
    - ORACLE (Backend Generation)
    - LANTERN (Database Configuration)
    - FLAME (Deployment & Sealing)
    """
    
    status = orchestrator.get_engine_status()
    return status

@orchestrator_router.get("/test")
async def test_orchestrator():
    """
    Test the AXIOM-FLAME orchestrator with sample phrases
    
    Runs a series of test invocations to validate engine functionality
    """
    
    try:
        script_content = f"""
const {{ testOrchestrator }} = require('{orchestrator.orchestrator_path}');

async function runTests() {{
    try {{
        const results = await testOrchestrator();
        console.log(JSON.stringify({{
            status: "test_completed",
            results: results,
            total_tests: results.length,
            passed_tests: results.filter(r => r.success).length
        }}, null, 2));
    }} catch (error) {{
        console.error(JSON.stringify({{
            status: "test_failed",
            error: error.message
        }}, null, 2));
    }}
}}

runTests();
"""
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.js', delete=False) as f:
            f.write(script_content)
            script_path = f.name
        
        try:
            result = subprocess.run([
                'node', script_path
            ], capture_output=True, text=True, timeout=60)
            
            if result.returncode == 0:
                test_result = json.loads(result.stdout)
                return test_result
            else:
                raise HTTPException(
                    status_code=500,
                    detail=f"Orchestrator test failed: {result.stderr}"
                )
                
        finally:
            os.unlink(script_path)
            
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Test execution failed: {str(e)}"
        )

@orchestrator_router.get("/health")
async def orchestrator_health():
    """
    Health check for the AXIOM-FLAME orchestrator
    """
    
    try:
        # Quick status check
        status = orchestrator.get_engine_status()
        
        if "error" in status:
            return {
                "status": "unhealthy",
                "message": "Orchestrator engines not available",
                "details": status
            }
        
        return {
            "status": "healthy",
            "message": "AXIOM-FLAME orchestrator operational",
            "engines": len(status),
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        return {
            "status": "unhealthy", 
            "message": f"Orchestrator health check failed: {str(e)}",
            "timestamp": datetime.now().isoformat()
        }

# Add examples endpoint
@orchestrator_router.get("/examples")
async def get_orchestrator_examples():
    """
    Get example phrases for the AXIOM-FLAME orchestrator
    """
    
    return {
        "examples": [
            {
                "phrase": "sovereign commerce scroll for diaspora funders",
                "description": "Creates an e-commerce platform with cultural context and ceremonial styling",
                "expected_modules": ["product_catalog", "checkout", "funder_dashboard"],
                "audience": "diaspora funders",
                "style": "mythic, ceremonial"
            },
            {
                "phrase": "create catalog and checkout system",
                "description": "Generates product catalog and checkout functionality",
                "expected_modules": ["product_catalog", "checkout"],
                "audience": "general",
                "style": "standard"
            },
            {
                "phrase": "ceremonial dashboard with recognition features",
                "description": "Builds a dashboard with contributor recognition system",
                "expected_modules": ["funder_dashboard", "contributor_recognition"],
                "audience": "general", 
                "style": "ceremonial"
            },
            {
                "phrase": "diaspora marketplace with community funds",
                "description": "Cultural commerce platform with community funding features",
                "expected_modules": ["product_catalog", "checkout", "community_funds"],
                "audience": "diaspora funders",
                "style": "mythic"
            }
        ],
        "usage": "POST /api/orchestrator/invoke with {'phrase': '<your phrase>'}"
    }
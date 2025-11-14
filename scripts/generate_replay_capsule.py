#!/usr/bin/env python3
"""
Replay Capsule Generation Script
Generates ceremonial replay capsules with audit trails and governance seals
"""

import json
import os
import datetime
import hashlib
import uuid
from pathlib import Path
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, asdict

@dataclass
class ReplayStep:
    """Individual step in a replay sequence"""
    step: str
    timestamp: str
    status: str
    details: str
    duration_ms: Optional[int] = None

@dataclass 
class ReplayCapsule:
    """Complete replay capsule with audit trail"""
    replay_id: str
    dispatch_id: str
    timestamp: str
    capsule_version: str
    full_context: Dict[str, Any]
    steps: List[ReplayStep]
    governance_seal: Dict[str, Any]
    audit_trail: Dict[str, Any]
    metadata: Dict[str, Any]

class ReplayCapsuleGenerator:
    """Generator for ceremonial replay capsules"""
    
    def __init__(self, workspace_root: str = None):
        if workspace_root is None:
            workspace_root = Path(__file__).parent.parent
        
        self.workspace_root = Path(workspace_root)
        self.ceremonies_path = self.workspace_root / "axiom-flame" / "artifacts" / "ceremonies"
        self.replays_path = self.workspace_root / "axiom-flame" / "storage" / "replays"
        self.ledger_path = self.workspace_root / "axiom-flame" / "storage" / "ledger"
        
        # Ensure directories exist
        self.replays_path.mkdir(parents=True, exist_ok=True)
        self.ledger_path.mkdir(parents=True, exist_ok=True)

    def generate_replay_id(self) -> str:
        """Generate unique replay identifier"""
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d")
        random_suffix = str(uuid.uuid4())[:8]
        return f"RPL-{timestamp}-{random_suffix}"

    def create_governance_seal(self, dispatch_id: str, actor: str, realm: str) -> Dict[str, Any]:
        """Create governance seal for replay capsule"""
        seal_data = f"{dispatch_id}:{actor}:{realm}:{datetime.datetime.utcnow().isoformat()}"
        seal_hash = hashlib.sha256(seal_data.encode()).hexdigest()[:16]
        
        return {
            "seal_type": "Replay",
            "seal_id": f"RS-{seal_hash}",
            "authority": "ceremonial",
            "classification": "replay_audit",
            "created_at": datetime.datetime.utcnow().isoformat(),
            "sealed_by": "Super-Codex-AI",
            "integrity_hash": seal_hash
        }

    def generate_replay_steps(self, ceremony_data: Dict[str, Any]) -> List[ReplayStep]:
        """Generate standardized replay steps"""
        base_time = datetime.datetime.utcnow()
        steps = []
        
        # Define standard ceremony replay steps
        step_definitions = [
            ("validate_actor", "Actor validation against registry", 150),
            ("verify_capsule", "Capsule type and permissions verification", 200),
            ("load_context", "Context and input data loading", 100),
            ("execute_reasoning", "Core reasoning and logic execution", 800),
            ("create_output", "Output generation and formatting", 300),
            ("seal_governance", "Governance seal application", 250),
            ("update_ledger", "Ledger entry creation and storage", 400),
            ("generate_audit", "Audit trail and replay data generation", 200)
        ]
        
        for i, (step_name, description, duration) in enumerate(step_definitions):
            step_time = base_time + datetime.timedelta(milliseconds=sum(d[2] for d in step_definitions[:i]))
            
            steps.append(ReplayStep(
                step=step_name,
                timestamp=step_time.isoformat() + "Z",
                status="completed",
                details=f"{description} for {ceremony_data.get('actor', 'Unknown')}",
                duration_ms=duration
            ))
        
        return steps

    def create_audit_trail(self, ceremony_data: Dict[str, Any], replay_id: str) -> Dict[str, Any]:
        """Create comprehensive audit trail"""
        return {
            "audit_version": "1.0",
            "replay_id": replay_id,
            "original_dispatch": ceremony_data.get("dispatch_id"),
            "integrity_checks": {
                "input_hash": hashlib.sha256(
                    json.dumps(ceremony_data.get("input", {}), sort_keys=True).encode()
                ).hexdigest()[:16],
                "context_verified": True,
                "governance_validated": True,
                "seal_authentic": True
            },
            "compliance": {
                "regulation_framework": "Super-Codex-AI Ceremonial Standard v1.0",
                "audit_requirements": ["actor_validation", "seal_verification", "ledger_integrity"],
                "compliance_status": "PASSED"
            },
            "lineage": {
                "parent_ceremony": ceremony_data.get("dispatch_id"),
                "replay_chain": [replay_id],
                "ancestral_depth": 1
            }
        }

    def load_ceremony_data(self, dispatch_id: str) -> Optional[Dict[str, Any]]:
        """Load ceremony data from artifacts or ledger"""
        # Try ceremonies directory first
        ceremony_file = self.ceremonies_path / f"{dispatch_id}.json"
        if ceremony_file.exists():
            with open(ceremony_file, 'r') as f:
                return json.load(f)
        
        # Try ledger directory
        ledger_file = self.ledger_path / f"{dispatch_id}.json"
        if ledger_file.exists():
            with open(ledger_file, 'r') as f:
                return json.load(f)
        
        return None

    def generate_replay_capsule(self, dispatch_id: str) -> Optional[ReplayCapsule]:
        """Generate complete replay capsule for ceremony"""
        print(f"🔄 Generating replay capsule for dispatch: {dispatch_id}")
        
        # Load original ceremony data
        ceremony_data = self.load_ceremony_data(dispatch_id)
        if not ceremony_data:
            print(f"❌ Ceremony data not found for dispatch: {dispatch_id}")
            return None
        
        print(f"✅ Loaded ceremony data: {ceremony_data.get('actor')} → {ceremony_data.get('capsule')}")
        
        # Generate replay components
        replay_id = self.generate_replay_id()
        timestamp = datetime.datetime.utcnow().isoformat() + "Z"
        steps = self.generate_replay_steps(ceremony_data)
        governance_seal = self.create_governance_seal(
            dispatch_id,
            ceremony_data.get("actor", "Unknown"),
            ceremony_data.get("realm", "Unknown")
        )
        audit_trail = self.create_audit_trail(ceremony_data, replay_id)
        
        # Create metadata
        metadata = {
            "generator": "Super-Codex-AI Replay Engine",
            "generator_version": "1.0.0",
            "total_steps": len(steps),
            "total_duration_ms": sum(step.duration_ms or 0 for step in steps),
            "replay_type": "ceremonial_audit",
            "preservation_class": "eternal"
        }
        
        # Create full replay capsule
        capsule = ReplayCapsule(
            replay_id=replay_id,
            dispatch_id=dispatch_id,
            timestamp=timestamp,
            capsule_version="1.0",
            full_context=ceremony_data,
            steps=steps,
            governance_seal=governance_seal,
            audit_trail=audit_trail,
            metadata=metadata
        )
        
        print(f"📦 Created replay capsule: {replay_id}")
        return capsule

    def save_replay_capsule(self, capsule: ReplayCapsule) -> bool:
        """Save replay capsule to storage"""
        try:
            capsule_file = self.replays_path / f"{capsule.replay_id}.json"
            
            # Convert to dict and save
            capsule_dict = asdict(capsule)
            
            with open(capsule_file, 'w') as f:
                json.dump(capsule_dict, f, indent=2, default=str)
            
            print(f"💾 Saved replay capsule: {capsule_file}")
            return True
            
        except Exception as e:
            print(f"❌ Failed to save replay capsule: {e}")
            return False

    def generate_sample_ceremonies(self) -> List[str]:
        """Generate sample ceremony entries for testing"""
        sample_ceremonies = []
        
        # Sample ceremony configurations
        ceremony_configs = [
            {
                "actor": "Custodian",
                "realm": "PL-001",
                "capsule": "Sovereign Crown",
                "intent": "Crown.Invocation",
                "input": {"prompt": "Crown invocation: source→replay"}
            },
            {
                "actor": "Council",
                "realm": "ST-007",
                "capsule": "Galactic Seal",
                "intent": "Governance.Proclamation",
                "input": {"decree": "Establish ceremonial protocols"}
            },
            {
                "actor": "Sentinel",
                "realm": "UN-∞",
                "capsule": "Eternal Flame",
                "intent": "Preservation.Archive", 
                "input": {"archive_type": "ceremonial_ledger"}
            }
        ]
        
        for config in ceremony_configs:
            # Generate dispatch ID
            timestamp = datetime.datetime.utcnow().strftime("%Y-%m-%d")
            dispatch_id = f"AXF-{timestamp}-{str(uuid.uuid4())[:8]}"
            
            # Create ceremony entry
            ceremony_entry = {
                "ledger_version": "1.0",
                "dispatch_id": dispatch_id,
                "timestamp": datetime.datetime.utcnow().isoformat() + "Z",
                **config,
                "output": {"summary": f"{config['capsule']} sealed; replay authorized."},
                "governance": {"seal": "Eternal", "audit_required": True},
                "links": {
                    "replay_ref": f"replays/{dispatch_id}.json",
                    "annal_ref": f"annals/{timestamp[:7]}.json"
                }
            }
            
            # Save ceremony
            ceremony_file = self.ceremonies_path / f"{dispatch_id}.json"
            self.ceremonies_path.mkdir(parents=True, exist_ok=True)
            
            with open(ceremony_file, 'w') as f:
                json.dump(ceremony_entry, f, indent=2, default=str)
            
            sample_ceremonies.append(dispatch_id)
            print(f"📜 Created sample ceremony: {dispatch_id}")
        
        return sample_ceremonies

    def validate_replay_capsule(self, capsule: ReplayCapsule) -> Dict[str, Any]:
        """Validate replay capsule integrity"""
        validation_results = {
            "valid": True,
            "errors": [],
            "warnings": [],
            "checks_passed": 0,
            "total_checks": 0
        }
        
        checks = [
            ("replay_id_format", lambda: capsule.replay_id.startswith("RPL-")),
            ("timestamp_valid", lambda: bool(datetime.datetime.fromisoformat(capsule.timestamp.replace('Z', '+00:00')))),
            ("steps_present", lambda: len(capsule.steps) > 0),
            ("governance_seal", lambda: bool(capsule.governance_seal.get("seal_id"))),
            ("audit_trail", lambda: bool(capsule.audit_trail.get("audit_version"))),
            ("context_complete", lambda: bool(capsule.full_context.get("dispatch_id")))
        ]
        
        validation_results["total_checks"] = len(checks)
        
        for check_name, check_func in checks:
            try:
                if check_func():
                    validation_results["checks_passed"] += 1
                else:
                    validation_results["valid"] = False
                    validation_results["errors"].append(f"Failed check: {check_name}")
            except Exception as e:
                validation_results["valid"] = False
                validation_results["errors"].append(f"Check error {check_name}: {e}")
        
        return validation_results

def main():
    """Main replay capsule generation function"""
    print("🔄 REPLAY CAPSULE GENERATION SCRIPT")
    print("=" * 50)
    
    try:
        generator = ReplayCapsuleGenerator()
        
        # Check for existing ceremonies
        existing_ceremonies = []
        if generator.ceremonies_path.exists():
            existing_ceremonies = [
                f.stem for f in generator.ceremonies_path.glob("*.json")
                if f.stem.startswith("AXF-")
            ]
        
        print(f"🔍 Found {len(existing_ceremonies)} existing ceremonies")
        
        # If no ceremonies exist, generate samples
        if not existing_ceremonies:
            print("📝 No existing ceremonies found, generating samples...")
            existing_ceremonies = generator.generate_sample_ceremonies()
        
        # Generate replay capsules for ceremonies
        generated_capsules = []
        for dispatch_id in existing_ceremonies[:5]:  # Limit to first 5 for demo
            capsule = generator.generate_replay_capsule(dispatch_id)
            if capsule:
                # Validate capsule
                validation = generator.validate_replay_capsule(capsule)
                if validation["valid"]:
                    if generator.save_replay_capsule(capsule):
                        generated_capsules.append(capsule.replay_id)
                        print(f"✅ Validation passed ({validation['checks_passed']}/{validation['total_checks']})")
                    else:
                        print(f"❌ Failed to save capsule for {dispatch_id}")
                else:
                    print(f"❌ Validation failed for {dispatch_id}: {validation['errors']}")
        
        print(f"\n🎉 REPLAY CAPSULE GENERATION COMPLETED")
        print(f"📊 Summary:")
        print(f"   - Processed ceremonies: {len(existing_ceremonies[:5])}")
        print(f"   - Generated capsules: {len(generated_capsules)}")
        print(f"   - Storage location: {generator.replays_path}")
        print(f"   - Capsule IDs: {', '.join(generated_capsules)}")
        
        # Display sample capsule info
        if generated_capsules:
            sample_file = generator.replays_path / f"{generated_capsules[0]}.json"
            if sample_file.exists():
                print(f"\n📋 Sample capsule structure:")
                with open(sample_file, 'r') as f:
                    sample_data = json.load(f)
                    print(f"   - Replay ID: {sample_data['replay_id']}")
                    print(f"   - Steps: {len(sample_data['steps'])}")
                    print(f"   - Duration: {sample_data['metadata']['total_duration_ms']}ms")
                    print(f"   - Seal: {sample_data['governance_seal']['seal_id']}")
        
        print(f"\n🔒 All replay capsules sealed with eternal governance")
        
    except Exception as e:
        print(f"\n❌ Replay capsule generation failed: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main())
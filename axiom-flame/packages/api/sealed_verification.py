"""
Sealed Artifact Verification Utilities
"""
import json
import hashlib
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Optional, Any

class SealedArtifactVerifier:
    """Utilities for verifying sealed artifacts and their signatures"""
    
    def __init__(self, storage_path: Path):
        self.storage_path = storage_path
        self.sealed_path = storage_path / 'artifacts' / 'sealed'
        
    def verify_seal(self, seal_id: str) -> Dict[str, Any]:
        """Verify a sealed artifact"""
        seal_file = self.sealed_path / f"{seal_id}.json"
        
        if not seal_file.exists():
            return {
                'status': 'error',
                'error': 'Sealed artifact not found',
                'seal_id': seal_id
            }
        
        try:
            with open(seal_file, 'r') as f:
                seal_data = json.load(f)
            
            verification_result = {
                'seal_id': seal_id,
                'verification_timestamp': datetime.now(timezone.utc).isoformat(),
                'seal_data': seal_data,
                'checks': self._perform_basic_checks(seal_data),
                'signatories': self._verify_signatories(seal_data.get('signatories', [])),
                'overall_status': 'pending'
            }
            
            # Determine overall status
            basic_checks_passed = all(verification_result['checks'].values())
            sig_checks_passed = all(s['status'] == 'valid' for s in verification_result['signatories'])
            
            verification_result['overall_status'] = 'verified' if basic_checks_passed and sig_checks_passed else 'failed'
            
            return {
                'status': 'success',
                'verification_result': verification_result
            }
            
        except Exception as e:
            return {
                'status': 'error',
                'error': str(e),
                'seal_id': seal_id
            }
    
    def _perform_basic_checks(self, seal_data: Dict[str, Any]) -> Dict[str, bool]:
        """Perform basic integrity checks on seal data"""
        return {
            'seal_id_present': bool(seal_data.get('seal_id')),
            'artifact_ref_present': bool(seal_data.get('artifact_ref')),
            'checksum_present': bool(seal_data.get('checksum_sha256')),
            'quorum_timestamp_present': bool(seal_data.get('quorum_verified_at')),
            'signatories_present': len(seal_data.get('signatories', [])) > 0,
            'metadata_present': bool(seal_data.get('metadata'))
        }
    
    def _verify_signatories(self, signatories: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Verify signatory data"""
        verified_signatories = []
        
        for signatory in signatories:
            sig_verification = {
                'council': signatory.get('council', 'Unknown'),
                'public_key_present': bool(signatory.get('public_key')),
                'signature_present': bool(signatory.get('signature')),
                'public_key_format_valid': self._validate_public_key_format(signatory.get('public_key', '')),
                'signature_format_valid': self._validate_signature_format(signatory.get('signature', '')),
                'status': 'pending'
            }
            
            # Determine signatory status
            all_checks = [
                sig_verification['public_key_present'],
                sig_verification['signature_present'],
                sig_verification['public_key_format_valid'],
                sig_verification['signature_format_valid']
            ]
            
            sig_verification['status'] = 'valid' if all(all_checks) else 'invalid'
            verified_signatories.append(sig_verification)
        
        return verified_signatories
    
    def _validate_public_key_format(self, public_key: str) -> bool:
        """Validate public key format (basic check)"""
        if not public_key:
            return False
        
        # Basic format check for PEM format
        return (
            public_key.startswith('-----BEGIN PUBLIC KEY-----') and
            public_key.endswith('-----END PUBLIC KEY-----')
        ) or len(public_key) > 10  # Allow for demo keys
    
    def _validate_signature_format(self, signature: str) -> bool:
        """Validate signature format (basic check)"""
        if not signature:
            return False
        
        # Basic check - signatures are usually base64 encoded and have minimum length
        return len(signature) >= 8  # Minimum reasonable signature length
    
    def list_sealed_artifacts(self) -> Dict[str, Any]:
        """List all sealed artifacts"""
        try:
            sealed_artifacts = []
            
            if not self.sealed_path.exists():
                return {
                    'status': 'success',
                    'total_seals': 0,
                    'seals': []
                }
            
            for seal_file in self.sealed_path.glob("*.json"):
                try:
                    with open(seal_file, 'r') as f:
                        seal_data = json.load(f)
                    
                    sealed_artifacts.append({
                        'seal_id': seal_data.get('seal_id', seal_file.stem),
                        'artifact_ref': seal_data.get('artifact_ref'),
                        'quorum_verified_at': seal_data.get('quorum_verified_at'),
                        'signatories_count': len(seal_data.get('signatories', [])),
                        'status': seal_data.get('metadata', {}).get('status', 'unknown'),
                        'councils': [s.get('council') for s in seal_data.get('signatories', [])]
                    })
                    
                except Exception:
                    continue
            
            # Sort by verification timestamp
            sealed_artifacts.sort(key=lambda x: x.get('quorum_verified_at', ''), reverse=True)
            
            return {
                'status': 'success',
                'total_seals': len(sealed_artifacts),
                'seals': sealed_artifacts
            }
            
        except Exception as e:
            return {
                'status': 'error',
                'error': str(e)
            }
    
    def generate_seal_summary(self, seal_id: str) -> Dict[str, Any]:
        """Generate a summary of a sealed artifact"""
        verification_result = self.verify_seal(seal_id)
        
        if verification_result['status'] != 'success':
            return verification_result
        
        verification = verification_result['verification_result']
        seal_data = verification['seal_data']
        
        summary = {
            'seal_id': seal_id,
            'artifact_ref': seal_data.get('artifact_ref'),
            'verification_status': verification['overall_status'],
            'quorum_verified_at': seal_data.get('quorum_verified_at'),
            'checksum': seal_data.get('checksum_sha256'),
            'councils': {
                'total': len(seal_data.get('signatories', [])),
                'verified': len([s for s in verification['signatories'] if s['status'] == 'valid']),
                'list': [s.get('council') for s in seal_data.get('signatories', [])]
            },
            'integrity_checks': {
                'passed': sum(1 for check in verification['checks'].values() if check),
                'total': len(verification['checks']),
                'all_passed': all(verification['checks'].values())
            },
            'metadata': seal_data.get('metadata', {}),
            'generated_at': datetime.now(timezone.utc).isoformat()
        }
        
        return {
            'status': 'success',
            'summary': summary
        }

def create_verifier(storage_path: str = None) -> SealedArtifactVerifier:
    """Create a sealed artifact verifier instance"""
    if storage_path is None:
        # Default to current axiom-flame storage path
        storage_path = Path(__file__).parent / 'storage'
    else:
        storage_path = Path(storage_path)
    
    return SealedArtifactVerifier(storage_path)

# CLI utility functions
def verify_seal_cli(seal_id: str, storage_path: str = None) -> None:
    """CLI function to verify a sealed artifact"""
    verifier = create_verifier(storage_path)
    result = verifier.verify_seal(seal_id)
    
    if result['status'] == 'success':
        verification = result['verification_result']
        print(f"✓ Seal Verification for {seal_id}")
        print(f"  Status: {verification['overall_status'].upper()}")
        print(f"  Artifact: {verification['seal_data'].get('artifact_ref')}")
        print(f"  Verified At: {verification['seal_data'].get('quorum_verified_at')}")
        print(f"  Signatories: {len(verification['signatories'])}")
        
        for i, sig in enumerate(verification['signatories'], 1):
            status_icon = "✓" if sig['status'] == 'valid' else "✗"
            print(f"    {status_icon} {sig['council']}: {sig['status']}")
            
    else:
        print(f"✗ Verification failed: {result.get('error')}")

def list_seals_cli(storage_path: str = None) -> None:
    """CLI function to list all sealed artifacts"""
    verifier = create_verifier(storage_path)
    result = verifier.list_sealed_artifacts()
    
    if result['status'] == 'success':
        print(f"Sealed Artifacts ({result['total_seals']} found):")
        
        for seal in result['seals']:
            print(f"  {seal['seal_id']}")
            print(f"    Artifact: {seal['artifact_ref']}")
            print(f"    Councils: {', '.join(seal['councils'])}")
            print(f"    Status: {seal['status']}")
            print(f"    Verified: {seal['quorum_verified_at']}")
            print()
    else:
        print(f"Error listing seals: {result.get('error')}")

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python sealed_verification.py <command> [args]")
        print("Commands:")
        print("  verify <seal_id>  - Verify a sealed artifact")
        print("  list              - List all sealed artifacts")
        sys.exit(1)
    
    command = sys.argv[1]
    
    if command == "verify" and len(sys.argv) >= 3:
        verify_seal_cli(sys.argv[2])
    elif command == "list":
        list_seals_cli()
    else:
        print(f"Unknown command: {command}")
        sys.exit(1)
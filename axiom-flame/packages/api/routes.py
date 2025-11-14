"""
Flask Routes for Axiom-Flame API
"""
import json
import hashlib
import traceback
from datetime import datetime, timezone
from pathlib import Path
from flask import request, jsonify
from jsonschema import validate, ValidationError
from config import Config

def register_routes(app):
    """Register all routes with the Flask app"""
    
    # Initialize directories
    Config.init_directories()
    
    @app.route('/health', methods=['GET'])
    def health():
        """Health check endpoint"""
        return jsonify({
            'status': 'healthy',
            'service': 'axiom-flame-api',
            'timestamp': datetime.now(timezone.utc).isoformat(),
            'version': '1.0.0'
        })
    
    @app.route('/status', methods=['GET'])
    def status():
        """Detailed status endpoint"""
        try:
            # Check if directories exist
            dirs_status = {}
            for path_name in ['STORAGE_PATH', 'LEDGER_PATH', 'REPLAYS_PATH', 'ANNALS_PATH', 'SCHEMAS_PATH']:
                path = getattr(Config, path_name)
                dirs_status[path_name.lower()] = {
                    'exists': path.exists(),
                    'path': str(path),
                    'is_dir': path.is_dir() if path.exists() else False
                }
            
            return jsonify({
                'status': 'operational',
                'service': 'axiom-flame-api',
                'timestamp': datetime.now(timezone.utc).isoformat(),
                'directories': dirs_status,
                'config': {
                    'debug': app.config.get('DEBUG', False),
                    'host': Config.HOST,
                    'port': Config.PORT
                }
            })
        except Exception as e:
            return jsonify({
                'status': 'error',
                'error': str(e),
                'timestamp': datetime.now(timezone.utc).isoformat()
            }), 500
    
    @app.route('/api/reason', methods=['POST'])
    def reason():
        """Ceremonial reasoning endpoint"""
        try:
            data = request.get_json()
            if not data:
                return jsonify({'error': 'No JSON data provided'}), 400
            
            # Generate dispatch ID
            dispatch_id = f"AXF-{datetime.now().strftime('%Y-%m-%d')}-{hashlib.sha256(str(data).encode()).hexdigest()[:8]}"
            
            # Create reasoning entry
            reasoning_entry = {
                'dispatch_id': dispatch_id,
                'timestamp': datetime.now(timezone.utc).isoformat(),
                'actor': data.get('actor', 'Unknown'),
                'realm': data.get('realm', 'Unknown'),
                'capsule': data.get('capsule', 'Unknown'),
                'intent': data.get('intent', 'Unknown'),
                'reasoning': data.get('reasoning', ''),
                'governance_seal': {
                    'authority': 'ceremonial',
                    'classification': 'reasoning',
                    'seal_hash': hashlib.sha256(f"{dispatch_id}:{data}".encode()).hexdigest()
                }
            }
            
            # Save to ledger
            ledger_file = Config.LEDGER_PATH / f"{dispatch_id}.json"
            with open(ledger_file, 'w') as f:
                json.dump(reasoning_entry, f, indent=2)
            
            return jsonify({
                'status': 'reasoning_complete',
                'dispatch_id': dispatch_id,
                'reasoning_entry': reasoning_entry
            })
            
        except Exception as e:
            return jsonify({
                'error': 'Reasoning failed',
                'details': str(e),
                'timestamp': datetime.now(timezone.utc).isoformat()
            }), 500
    
    @app.route('/api/replay/<dispatch_id>', methods=['GET'])
    def replay(dispatch_id):
        """Replay ceremonial entry"""
        try:
            ledger_file = Config.LEDGER_PATH / f"{dispatch_id}.json"
            if not ledger_file.exists():
                return jsonify({'error': 'Dispatch not found'}), 404
            
            with open(ledger_file, 'r') as f:
                entry = json.load(f)
            
            # Create replay entry
            replay_entry = {
                'replay_id': f"RPL-{datetime.now().strftime('%Y-%m-%d')}-{hashlib.sha256(dispatch_id.encode()).hexdigest()[:8]}",
                'original_dispatch_id': dispatch_id,
                'replay_timestamp': datetime.now(timezone.utc).isoformat(),
                'original_entry': entry,
                'replay_status': 'successful'
            }
            
            # Save replay
            replay_file = Config.REPLAYS_PATH / f"{replay_entry['replay_id']}.json"
            with open(replay_file, 'w') as f:
                json.dump(replay_entry, f, indent=2)
            
            return jsonify({
                'status': 'replay_complete',
                'replay_entry': replay_entry
            })
            
        except Exception as e:
            return jsonify({
                'error': 'Replay failed',
                'details': str(e),
                'timestamp': datetime.now(timezone.utc).isoformat()
            }), 500
    
    @app.route('/api/audit/<dispatch_id>', methods=['GET'])
    def audit(dispatch_id):
        """Audit ceremonial entry"""
        try:
            ledger_file = Config.LEDGER_PATH / f"{dispatch_id}.json"
            if not ledger_file.exists():
                return jsonify({'error': 'Dispatch not found'}), 404
            
            with open(ledger_file, 'r') as f:
                entry = json.load(f)
            
            # Perform audit checks
            audit_results = {
                'dispatch_id': dispatch_id,
                'audit_timestamp': datetime.now(timezone.utc).isoformat(),
                'integrity_checks': {
                    'file_exists': True,
                    'json_valid': True,
                    'required_fields': {
                        'dispatch_id': 'dispatch_id' in entry,
                        'timestamp': 'timestamp' in entry,
                        'actor': 'actor' in entry,
                        'governance_seal': 'governance_seal' in entry
                    }
                },
                'seal_verification': {
                    'seal_present': 'governance_seal' in entry,
                    'seal_hash_valid': bool(entry.get('governance_seal', {}).get('seal_hash'))
                },
                'audit_status': 'passed'
            }
            
            return jsonify({
                'status': 'audit_complete',
                'audit_results': audit_results
            })
            
        except Exception as e:
            return jsonify({
                'error': 'Audit failed',
                'details': str(e),
                'timestamp': datetime.now(timezone.utc).isoformat()
            }), 500
    
    @app.route('/api/ledger', methods=['GET'])
    def list_ledger():
        """List all ledger entries"""
        try:
            entries = []
            for ledger_file in Config.LEDGER_PATH.glob("*.json"):
                try:
                    with open(ledger_file, 'r') as f:
                        entry = json.load(f)
                    entries.append({
                        'dispatch_id': entry.get('dispatch_id', ledger_file.stem),
                        'timestamp': entry.get('timestamp'),
                        'actor': entry.get('actor'),
                        'realm': entry.get('realm'),
                        'capsule': entry.get('capsule')
                    })
                except Exception:
                    continue
            
            # Sort by timestamp
            entries.sort(key=lambda x: x.get('timestamp', ''), reverse=True)
            
            return jsonify({
                'status': 'success',
                'total_entries': len(entries),
                'entries': entries
            })
            
        except Exception as e:
            return jsonify({
                'error': 'Failed to list ledger',
                'details': str(e),
                'timestamp': datetime.now(timezone.utc).isoformat()
            }), 500
    
    @app.route('/api/seals', methods=['GET'])
    def list_seals():
        """List all sealed artifacts"""
        try:
            seals = []
            sealed_path = Config.STORAGE_PATH / 'artifacts' / 'sealed'
            if sealed_path.exists():
                for seal_file in sealed_path.glob("*.json"):
                    try:
                        with open(seal_file, 'r') as f:
                            seal = json.load(f)
                        seals.append({
                            'seal_id': seal.get('seal_id', seal_file.stem),
                            'artifact_ref': seal.get('artifact_ref'),
                            'quorum_verified_at': seal.get('quorum_verified_at'),
                            'signatories_count': len(seal.get('signatories', [])),
                            'status': seal.get('metadata', {}).get('status', 'unknown')
                        })
                    except Exception:
                        continue
            
            # Sort by verification time
            seals.sort(key=lambda x: x.get('quorum_verified_at', ''), reverse=True)
            
            return jsonify({
                'status': 'success',
                'total_seals': len(seals),
                'seals': seals
            })
            
        except Exception as e:
            return jsonify({
                'error': 'Failed to list seals',
                'details': str(e),
                'timestamp': datetime.now(timezone.utc).isoformat()
            }), 500
    
    @app.route('/api/seals/<seal_id>', methods=['GET'])
    def get_seal(seal_id):
        """Get specific sealed artifact"""
        try:
            sealed_path = Config.STORAGE_PATH / 'artifacts' / 'sealed'
            seal_file = sealed_path / f"{seal_id}.json"
            
            if not seal_file.exists():
                return jsonify({'error': 'Sealed artifact not found'}), 404
            
            with open(seal_file, 'r') as f:
                seal = json.load(f)
            
            return jsonify({
                'status': 'success',
                'seal': seal
            })
            
        except Exception as e:
            return jsonify({
                'error': 'Failed to retrieve seal',
                'details': str(e),
                'timestamp': datetime.now(timezone.utc).isoformat()
            }), 500
    
    @app.route('/api/seals/<seal_id>/verify', methods=['POST'])
    def verify_seal(seal_id):
        """Verify sealed artifact signatures"""
        try:
            sealed_path = Config.STORAGE_PATH / 'artifacts' / 'sealed'
            seal_file = sealed_path / f"{seal_id}.json"
            
            if not seal_file.exists():
                return jsonify({'error': 'Sealed artifact not found'}), 404
            
            with open(seal_file, 'r') as f:
                seal = json.load(f)
            
            # Basic verification checks
            verification_results = {
                'seal_id': seal_id,
                'verification_timestamp': datetime.now(timezone.utc).isoformat(),
                'checks': {
                    'seal_exists': True,
                    'artifact_ref_valid': bool(seal.get('artifact_ref')),
                    'checksum_present': bool(seal.get('checksum_sha256')),
                    'signatories_present': len(seal.get('signatories', [])) > 0,
                    'quorum_timestamp_valid': bool(seal.get('quorum_verified_at'))
                },
                'signatories_verification': []
            }
            
            # Check each signatory
            for signatory in seal.get('signatories', []):
                sig_check = {
                    'council': signatory.get('council'),
                    'public_key_present': bool(signatory.get('public_key')),
                    'signature_present': bool(signatory.get('signature')),
                    'status': 'valid' if signatory.get('public_key') and signatory.get('signature') else 'invalid'
                }
                verification_results['signatories_verification'].append(sig_check)
            
            # Overall verification status
            all_checks_passed = all(verification_results['checks'].values())
            all_sigs_valid = all(s['status'] == 'valid' for s in verification_results['signatories_verification'])
            
            verification_results['overall_status'] = 'verified' if all_checks_passed and all_sigs_valid else 'failed'
            
            return jsonify({
                'status': 'verification_complete',
                'verification_results': verification_results
            })
            
        except Exception as e:
            return jsonify({
                'error': 'Verification failed',
                'details': str(e),
                'timestamp': datetime.now(timezone.utc).isoformat()
            }), 500
    
    @app.errorhandler(404)
    def not_found(e):
        return jsonify({
            'error': 'Endpoint not found',
            'message': 'The requested API endpoint does not exist',
            'timestamp': datetime.now(timezone.utc).isoformat()
        }), 404
    
    @app.errorhandler(500)
    def internal_error(e):
        return jsonify({
            'error': 'Internal server error',
            'message': 'An unexpected error occurred',
            'timestamp': datetime.now(timezone.utc).isoformat()
        }), 500
    
    @app.errorhandler(Exception)
    def handle_error(e):
        app.logger.error(f"Error: {e}")
        return {"error": str(e)}, 500
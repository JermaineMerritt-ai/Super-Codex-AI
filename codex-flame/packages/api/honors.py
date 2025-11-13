"""
Honors Blueprint - Sacred honor management system
"""
from flask import Blueprint, request, jsonify
from typing import Dict, List, Any, Optional
from datetime import datetime
import json

# Create the honors blueprint
bp = Blueprint('honors', __name__, url_prefix='/honors')

# In-memory honor storage (can be replaced with persistent storage)
_honors_ledger: Dict[str, Dict[str, Any]] = {}
_next_honor_id = 1

@bp.route('/grant', methods=['POST'])
def grant_honor():
    """Grant a new honor to a recipient"""
    global _next_honor_id
    
    data = request.get_json()
    
    # Validate required fields
    required_fields = ['recipient_name', 'honor_type', 'granting_authority']
    if not all(field in data for field in required_fields):
        return jsonify({'error': 'Missing required fields'}), 400
    
    honor_id = f"HK-{datetime.now().strftime('%Y%m%d')}-{_next_honor_id:04d}"
    _next_honor_id += 1
    
    honor_record = {
        'honor_id': honor_id,
        'recipient_name': data['recipient_name'],
        'honor_type': data['honor_type'],
        'granting_authority': data['granting_authority'],
        'granted_at': datetime.now().isoformat(),
        'sacred_deeds': data.get('sacred_deeds', []),
        'ceremonial_data': data.get('ceremonial_data', {}),
        'status': 'active'
    }
    
    _honors_ledger[honor_id] = honor_record
    
    return jsonify({
        'success': True,
        'honor_id': honor_id,
        'message': f'Honor granted to {data["recipient_name"]}'
    })

@bp.route('/list', methods=['GET'])
def list_honors():
    """List all honors, optionally filtered by recipient or type"""
    recipient = request.args.get('recipient')
    honor_type = request.args.get('type')
    
    honors = list(_honors_ledger.values())
    
    if recipient:
        honors = [h for h in honors if h['recipient_name'].lower() == recipient.lower()]
    
    if honor_type:
        honors = [h for h in honors if h['honor_type'].lower() == honor_type.lower()]
    
    return jsonify({
        'honors': honors,
        'total': len(honors)
    })

@bp.route('/<honor_id>', methods=['GET'])
def get_honor(honor_id: str):
    """Get a specific honor by ID"""
    if honor_id not in _honors_ledger:
        return jsonify({'error': 'Honor not found'}), 404
    
    return jsonify(_honors_ledger[honor_id])

@bp.route('/<honor_id>/revoke', methods=['POST'])
def revoke_honor(honor_id: str):
    """Revoke an honor"""
    if honor_id not in _honors_ledger:
        return jsonify({'error': 'Honor not found'}), 404
    
    data = request.get_json()
    revoking_authority = data.get('revoking_authority', 'Unknown')
    reason = data.get('reason', 'No reason provided')
    
    honor = _honors_ledger[honor_id]
    honor['status'] = 'revoked'
    honor['revoked_at'] = datetime.now().isoformat()
    honor['revoking_authority'] = revoking_authority
    honor['revocation_reason'] = reason
    
    return jsonify({
        'success': True,
        'message': f'Honor {honor_id} revoked'
    })

@bp.route('/recipient/<recipient_name>', methods=['GET'])
def get_recipient_honors(recipient_name: str):
    """Get all honors for a specific recipient"""
    honors = [h for h in _honors_ledger.values() 
             if h['recipient_name'].lower() == recipient_name.lower()]
    
    return jsonify({
        'recipient': recipient_name,
        'honors': honors,
        'total_honors': len(honors),
        'active_honors': len([h for h in honors if h['status'] == 'active'])
    })

@bp.route('/types', methods=['GET'])
def get_honor_types():
    """Get all available honor types"""
    honor_types = list(set(h['honor_type'] for h in _honors_ledger.values()))
    
    return jsonify({
        'honor_types': honor_types,
        'total_types': len(honor_types)
    })

@bp.route('/stats', methods=['GET'])
def get_honor_stats():
    """Get honor statistics"""
    all_honors = list(_honors_ledger.values())
    
    stats = {
        'total_honors': len(all_honors),
        'active_honors': len([h for h in all_honors if h['status'] == 'active']),
        'revoked_honors': len([h for h in all_honors if h['status'] == 'revoked']),
        'unique_recipients': len(set(h['recipient_name'] for h in all_honors)),
        'honor_types': {}
    }
    
    # Count by type
    for honor in all_honors:
        honor_type = honor['honor_type']
        if honor_type not in stats['honor_types']:
            stats['honor_types'][honor_type] = 0
        stats['honor_types'][honor_type] += 1
    
    return jsonify(stats)
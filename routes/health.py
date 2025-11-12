# routes/health.py
from flask import Blueprint, jsonify

bp = Blueprint('health', __name__)

@bp.route('/health', methods=['GET'])
def health():
    return jsonify(status="ok", flame="radiant", version="1.0.0"), 200
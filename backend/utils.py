from flask import Blueprint, jsonify


utils_bp = Blueprint('utils_bp', __name__)

@utils_bp.route('/health', methods=['GET'])
def home():
    """Health check endpoint."""
    return jsonify({"message": "Flask backend is running!"})

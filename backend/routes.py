from flask import jsonify, Blueprint
from backend.api.db_test_api import db_test_bp
from backend.utils import utils_bp


api_bp = Blueprint('api_bp', __name__)

def register_blueprints(app):
    """Register all Blueprints to the Flask app."""
    # Register Child blue prints
    api_bp.register_blueprint(db_test_bp, url_prefix='/db_test')  
    

    # Register Parent blue print
    app.register_blueprint(api_bp, url_prefix='/api')
    app.register_blueprint(utils_bp)

# API Health Check 
@api_bp.route('/health', methods=['GET'])
def home():
    return jsonify({"message": "Flask backend API is running!"})
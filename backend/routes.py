from flask import jsonify, Blueprint

from backend.api.db_test_api import db_test_bp
from backend.utils import utils_bp

# API Blueprint
api_bp = Blueprint('api_bp', __name__)


def register_blueprints(app):
    """Register all Blueprints to the Flask app."""
    # Register API Blueprints
    api_bp.register_blueprint(db_test_bp, url_prefix='/db_test')  

    # Register Blueprints to the Flask app
    app.register_blueprint(api_bp, url_prefix='/api')
    app.register_blueprint(utils_bp)

@api_bp.route('/health', methods=['GET'])
def health_check():
    return jsonify({"message": "Flask backend API is running!"})
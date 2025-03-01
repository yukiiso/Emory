from flask import jsonify, Blueprint

from backend.api.dynamo_api import dynamo_bp
from backend.api.sql_api import sql_bp
from backend.api.chatgpt_api import chatgpt_bp
from backend.utils import utils_bp

# API Blueprint
api_bp = Blueprint('api_bp', __name__)
db_bp = Blueprint('db_bp', __name__)


def register_blueprints(app):
    """Register all Blueprints to the Flask app."""
    # Register Child Blueprints
    db_bp.register_blueprint(dynamo_bp, url_prefix='/dynamo')  
    db_bp.register_blueprint(sql_bp, url_prefix='/sql')
    
    api_bp.register_blueprint(chatgpt_bp, url_prefix='/chatgpt')
    api_bp.register_blueprint(db_bp, url_prefix='/db')

    # Register Parent Blueprints
    app.register_blueprint(api_bp, url_prefix='/api')
    app.register_blueprint(utils_bp)

@api_bp.route('/health', methods=['GET'])
def health_check():
    return jsonify({"message": "Flask backend API is running!"})
# Inside /emory/backend/routes.py

from flask import Blueprint, jsonify
from backend.api.dynamo_api import dynamo_bp
from backend.api.sql_api import sql_bp
from backend.upload import upload_video_bp, upload_audio_bp
from backend.utils import utils_bp

# API Blueprint
api_bp = Blueprint('api_bp', __name__)
db_bp = Blueprint('db_bp', __name__)
media_bp = Blueprint('media_bp', __name__)

def register_blueprints(app):
    """Register all Blueprints to the Flask app."""
    # Register Child Blueprints
    db_bp.register_blueprint(dynamo_bp, url_prefix='/dynamo')  
    db_bp.register_blueprint(sql_bp, url_prefix='/sql')  
    media_bp.register_blueprint(upload_video_bp, url_prefix='/video')  # Separate video blueprint
    media_bp.register_blueprint(upload_audio_bp, url_prefix='/audio')  # Separate audio blueprint

    api_bp.register_blueprint(db_bp, url_prefix='/db')  

    # Register Parent Blueprints
    app.register_blueprint(api_bp, url_prefix='/api')
    app.register_blueprint(media_bp, url_prefix='/media')
    app.register_blueprint(utils_bp)

@api_bp.route('/health', methods=['GET'])
def health_check():
    return jsonify({"message": "Flask backend API is running!"})

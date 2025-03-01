from flask import jsonify, Blueprint

from backend.api.db_test_api import db_test_bp
from backend.utils import utils_bp

# API Blueprint
api_bp = Blueprint('api_bp', __name__)

@api_bp.route('/health', methods=['GET'])
def health_check():
    return jsonify({"message": "Flask backend API is running!"})

# ✅ 追加: `/` に対応するエンドポイント
main_bp = Blueprint('main_bp', __name__)

@main_bp.route('/')
def home():
    return jsonify({"message": "Welcome to the Flask backend!"})


def register_blueprints(app):
    """Register all Blueprints to the Flask app."""
    # Register API Blueprints
    api_bp.register_blueprint(db_test_bp, url_prefix='/db_test')  

    # Register Blueprints to the Flask app
    app.register_blueprint(main_bp)  # ✅ `/` にアクセスできるようにする
    app.register_blueprint(api_bp, url_prefix='/api')
    app.register_blueprint(utils_bp)

from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import FLASK_ENV, FLASK_DEBUG, SQLALCHEMY_DATABASE_URI
from models import db
from flask_cors import CORS
import os

def create_app():
    """Flask アプリを作成するファクトリ関数"""
    app = Flask(__name__)
    CORS(app)

    print(f"Running in {FLASK_ENV} mode")
    print(f"DB_HOST: {os.getenv('DB_HOST')}")
    print(f"DB_PORT: {os.getenv('DB_PORT')}")
    print(f"SQLALCHEMY_DATABASE_URI: {SQLALCHEMY_DATABASE_URI}")

    # 環境設定を適用
    app.config["ENV"] = FLASK_ENV
    app.config["DEBUG"] = FLASK_DEBUG
    app.config["SQLALCHEMY_DATABASE_URI"] = SQLALCHEMY_DATABASE_URI
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    # DB の初期化
    db.init_app(app)
    migrate = Migrate(app, db)

    with app.app_context():
        from flask_migrate import upgrade

        try:
            upgrade()  # 変更を適用
        except Exception as e:
            print(f"Migration Error: {e}")

    @app.route("/health", methods=["GET"])
    def health_check():
        return jsonify({"status": "ok", "message": "Flask backend is running!"})

    return app

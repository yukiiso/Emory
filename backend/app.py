from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from backend.routes import register_blueprints
from backend.config import FLASK_ENV, FLASK_DEBUG, SQLALCHEMY_DATABASE_URI, SQLALCHEMY_DATABASE_URI_TEST
from backend.models import db
from flask_cors import CORS
import os

def create_app(test=False):
    """Flask アプリを作成するファクトリ関数"""
    app = Flask(__name__)
    CORS(app, resources={
        r"/api/*": {"origins": "*"},    # Allow all origins for `/api` routes
    })    

    if test:
        # ✅ テスト環境用の設定
        print("Running in TEST mode")
        app.config["ENV"] = "test"
        app.config["DEBUG"] = True
        app.config["TESTING"] = True
        app.config["SQLALCHEMY_DATABASE_URI"] = SQLALCHEMY_DATABASE_URI_TEST
        app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    else:
        # ✅ 開発・本番環境用の設定
        print(f"Running in {FLASK_ENV} mode")
        app.config["ENV"] = FLASK_ENV
        app.config["DEBUG"] = FLASK_DEBUG
        app.config["TESTING"] = False
        app.config["SQLALCHEMY_DATABASE_URI"] = SQLALCHEMY_DATABASE_URI
        app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    # DB の初期化
    db.init_app(app)

    register_blueprints(app)
    
    return app
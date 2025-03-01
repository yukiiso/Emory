from flask import Flask
from config import FLASK_ENV, FLASK_DEBUG, SQLALCHEMY_DATABASE_URI, IS_TESTING
from models import db
from routes import register_blueprints
from seed import seed_data  
import os


def create_app():
    """Flask アプリを作成するファクトリ関数"""
    app = Flask(__name__)

    print(f"DB_HOST: {os.getenv('DB_HOST')}")
    print(f"DB_PORT: {os.getenv('DB_PORT')}")

    # 環境設定を適用
    app.config["ENV"] = FLASK_ENV
    app.config["DEBUG"] = FLASK_DEBUG
    app.config["SQLALCHEMY_DATABASE_URI"] = SQLALCHEMY_DATABASE_URI  # config.py で管理
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    print(f"SQLALCHEMY_DATABASE_URI: {app.config['SQLALCHEMY_DATABASE_URI']}")
    # DB の初期化
    db.init_app(app)

    with app.app_context():
        # 既存の DB を上書きせず、変更だけを適用する
        if not os.path.exists("migrations"):  # 初回のみマイグレーションを作成
            from flask_migrate import init
            init()

        from flask_migrate import upgrade
        upgrade()  # 変更を適用

        # テスト環境でない場合のみ Seed Data を投入
        if not IS_TESTING:
            seed_data()

    # ルートを登録
    register_blueprints(app)

    return app

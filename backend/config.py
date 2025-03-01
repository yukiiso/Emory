import os
from dotenv import load_dotenv

# 環境変数をロード
load_dotenv("config.env")

# 環境の設定
ENV = os.getenv("ENV")

# テスト実行時かどうかを判定
IS_TESTING = "pytest" in os.getenv("_", "")

# Flask 設定
FLASK_ENV = os.getenv(f"FLASK_ENV_test" if IS_TESTING else f"FLASK_ENV_{ENV}")
FLASK_DEBUG = os.getenv(f"FLASK_DEBUG_test" if IS_TESTING else f"FLASK_DEBUG_{ENV}")

# Flask ホスト & ポート設定
FLASK_HOST = os.getenv("FLASK_HOST")
FLASK_PORT = os.getenv(f"FLASK_PORT_{ENV}")

# MySQL の設定
DB_HOST = os.getenv(f"DB_HOST_{ENV}")
DB_USER = os.getenv(f"DB_USER_{ENV}")
DB_PASSWORD = os.getenv(f"DB_PASSWORD_{ENV}")
DB_PORT = os.getenv(f"DB_PORT_{ENV}")
DB_NAME = os.getenv(f"DB_NAME_{ENV}")

SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

print(f"Running in {FLASK_ENV} mode: DB={DB_NAME}, HOST={FLASK_HOST}, PORT={FLASK_PORT}")

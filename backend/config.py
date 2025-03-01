import os
import boto3
from dotenv import load_dotenv

# 環境変数をロード
load_dotenv("config.env")

# 環境の設定
ENV = os.getenv("ENV")

# Flask 設定
FLASK_ENV = os.getenv(f"FLASK_ENV_{ENV}")
FLASK_DEBUG = os.getenv(f"FLASK_DEBUG_{ENV}")
FLASK_HOST = os.getenv(f"FLASK_HOST_{ENV}")
FLASK_PORT = os.getenv(f"FLASK_PORT")

# MySQL の設定
DB_HOST = os.getenv(f"DB_HOST_{ENV}")
DB_USER = os.getenv(f"DB_USER_{ENV}")
DB_PASSWORD = os.getenv(f"DB_PASSWORD_{ENV}")
DB_PORT = os.getenv(f"DB_PORT_{ENV}")
DB_NAME = os.getenv(f"DB_NAME_{ENV}")
SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# MySQL テスト用
DB_HOST_TEST = os.getenv("DB_HOST_TEST")
DB_USER_TEST = os.getenv("DB_USER_TEST")
DB_PASSWORD_TEST = os.getenv("DB_PASSWORD_TEST")
DB_PORT_TEST = os.getenv("DB_PORT_TEST")
DB_NAME_TEST = os.getenv("DB_NAME_TEST")
SQLALCHEMY_DATABASE_URI_TEST = f"mysql+pymysql://{DB_USER_TEST}:{DB_PASSWORD_TEST}@{DB_HOST_TEST}:{DB_PORT_TEST}/{DB_NAME_TEST}"

# DynamoDB の設定
DYNAMODB_ENDPOINT = os.getenv(f"DYNAMODB_ENDPOINT_{ENV}") 
AWS_REGION = os.getenv("AWS_REGION") 

# REST AI API KEY
OPENAI_API_KEY= os.getenv("OPENAI_API_KEY")

# AWS
AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
AWS_REGION = os.getenv("AWS_REGION")  
S3_BUCKET = os.getenv("S3_BUCKET")

class AWSClient:
    @staticmethod
    def init_s3_client():
        return boto3.client(
            "s3",
            aws_access_key_id=AWS_ACCESS_KEY_ID,
            aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
            region_name=AWS_REGION
        )

    @staticmethod
    def init_rekognition_client():
        return boto3.client(
            "rekognition",
            aws_access_key_id=AWS_ACCESS_KEY_ID,
            aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
            region_name=AWS_REGION
        )

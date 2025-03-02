import os
from flask import Blueprint, request, jsonify
from urllib.parse import urlparse
from config import AWSClient, S3_BUCKET

rekognition_bp = Blueprint('rekognition', __name__)
rekognition_client = AWSClient.init_rekognition_client()

@rekognition_bp.route("/analyze-video", methods=["POST"])
def analyze_video():
    data = request.get_json()
    video_url = data.get("video_url")

    if not video_url:
        return jsonify({"error": "動画URLが提供されていません"}), 400

    # URL を解析して、S3 バケット名とファイル名を取得
    parsed_url = urlparse(video_url)
    s3_bucket = S3_BUCKET  # 環境変数または設定ファイルで指定された S3 バケット名
    s3_key = parsed_url.path.lstrip("/")  # URL パスからファイル名を抽出

    try:
        # Rekognition の顔認識解析を開始
        response = rekognition_client.start_face_detection(
            Video={'S3Object': {'Bucket': s3_bucket, 'Name': s3_key}},
            NotificationChannel={  # SNS 通知設定
                'SNSTopicArn': os.getenv("SNS_TOPIC_ARN"),  # SNS トピック ARN
                'RoleArn': os.getenv("REKOGNITION_ROLE_ARN")  # Rekognition の IAM ロール ARN
            }
        )
        job_id = response['JobId']

        # ジョブ ID を返す
        return jsonify({"message": "分析開始", "job_id": job_id}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

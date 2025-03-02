import os
from flask import Blueprint, request, jsonify
from flask_cors import CORS
from config import AWSClient

rekognition_bp = Blueprint('rekognition', __name__)
rekognition_client = AWSClient.init_rekognition_client()

@rekognition_bp.route("/analyze-video", methods=["POST"])
def analyze_video():
    data = request.get_json()
    video_url = data.get("video_url")

    if not video_url:
        return jsonify({"error": "動画URLが提供されていません"}), 400

    s3_bucket = AWSClient.S3_BUCKET
    s3_key = video_url.split("/")[-1]  # URLからファイル名を取得

    try:
        response = rekognition_client.start_face_detection(
            Video={'S3Object': {'Bucket': s3_bucket, 'Name': s3_key}},
            NotificationChannel={  # Rekognition Video は SNS 通知が必要
                'SNSTopicArn': os.getenv("SNS_TOPIC_ARN"),
                'RoleArn': os.getenv("REKOGNITION_ROLE_ARN")
            }
        )
        job_id = response['JobId']

        return jsonify({"message": "分析開始", "job_id": job_id}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

import os
import json
import boto3
import requests
from flask import Blueprint, request, jsonify
from backend.config import AWSClient, SNS_NOTIFICATION_ENDPOINT, SNS_TOPICS

sns_bp = Blueprint('sns_bp', __name__)
rekognition_client = AWSClient.init_rekognition_client()
sns_client = AWSClient.init_sns_client()
transcribe_client = AWSClient.init_transcribe_client()  # Transcribe クライアントを追加

def subscribe_to_sns_topics():
    """
    SNS トピックに自動でサブスクライブする関数
    """
    try:
        for topic_arn in SNS_TOPICS:
            if not topic_arn:
                print(f"Warning: {topic_arn} が設定されていません。")
                continue

            # 既存のサブスクリプションを確認
            existing_subscriptions = sns_client.list_subscriptions_by_topic(TopicArn=topic_arn)
            already_subscribed = any(
                sub["Endpoint"] == SNS_NOTIFICATION_ENDPOINT for sub in existing_subscriptions.get("Subscriptions", [])
            )

            if already_subscribed:
                print(f"既に {topic_arn} にサブスクライブ済み: {SNS_NOTIFICATION_ENDPOINT}")
            else:
                print(f"{topic_arn} にサブスクライブ中...")
                response = sns_client.subscribe(
                    TopicArn=topic_arn,
                    Protocol="https",
                    Endpoint=SNS_NOTIFICATION_ENDPOINT,
                    ReturnSubscriptionArn=True
                )
                print(f"サブスクライブ成功: {response.get('SubscriptionArn')}")

    except Exception as e:
        print(f"SNS サブスクリプションの登録中にエラーが発生しました: {str(e)}")


import json
import requests
from flask import Blueprint, request, jsonify

sns_bp = Blueprint("sns_bp", __name__)

@sns_bp.route("/notification", methods=["POST"])
def sns_notification():
    try:
        print("Received SNS Notification")

        # SNS のリクエストを手動でパースする
        try:
            raw_data = request.data.decode("utf-8")
            print(f"Raw Request Data: {raw_data}")

            message = json.loads(raw_data)  # ここで JSON に変換
        except json.JSONDecodeError:
            print("Error: Failed to parse SNS Notification as JSON")
            return jsonify({"error": "Invalid JSON format"}), 400

        print("Parsed SNS Message:")
        print(json.dumps(message, indent=4))

        if not message:
            return jsonify({"error": "Invalid request"}), 400

        # SNS Subscription Confirmation
        if "Type" in message and message["Type"] == "SubscriptionConfirmation":
            subscribe_url = message.get("SubscribeURL")
            if subscribe_url:
                print(f"Confirming subscription: {subscribe_url}")
                requests.get(subscribe_url)
                return jsonify({"message": "Subscription confirmed"}), 200

        # SNS の `Message` が JSON 文字列の場合、さらにデコード
        try:
            message_data = json.loads(message["Message"])
            print("Decoded SNS Message:")
            print(json.dumps(message_data, indent=4))
        except (json.JSONDecodeError, TypeError):
            print("Error: Failed to decode SNS Message content")
            return jsonify({"error": "Invalid SNS Message format"}), 400

        job_name = message_data.get("TranscriptionJobName")
        job_status = message_data.get("TranscriptionJobStatus")

        if not job_name or not job_status:
            print("Error: Missing required fields in SNS Message")
            return jsonify({"error": "Invalid SNS Message content"}), 400

        print(f"Transcription Job {job_name} Status: {job_status}")

        if job_status == "COMPLETED":
            transcript_uri = message_data.get("TranscriptFileUri")
            print(f"Transcription Completed: {transcript_uri}")
            return jsonify({"status": "COMPLETED", "transcript_uri": transcript_uri}), 200
        elif job_status == "FAILED":
            return jsonify({"status": "FAILED"}), 500

        return jsonify({"message": "Notification received"}), 200

    except Exception as e:
        print(f"Unexpected error: {str(e)}")
        return jsonify({"error": str(e)}), 500


# Flask アプリ起動時に SNS トピックへ自動登録
subscribe_to_sns_topics()

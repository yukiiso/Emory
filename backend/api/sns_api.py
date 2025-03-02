import os
import json
import boto3
import requests
from flask import Blueprint, request, jsonify
from backend.config import AWSClient, SNS_NOTIFICATION_ENDPOINT, SNS_TOPICS

sns_bp = Blueprint('sns_bp', __name__)
rekognition_client = AWSClient.init_rekognition_client()
sns_client = AWSClient.init_sns_client()

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


@sns_bp.route('/notification', methods=['POST'])
def sns_notification():
    try:
        content_type = request.headers.get('Content-Type', '').lower()
        print(f"Content-Type: {content_type}")

        if content_type != 'application/json':
            print("Warning: Content-Type is not application/json, trying to parse manually")
            message = json.loads(request.data.decode('utf-8'))
        else:
            message = request.get_json()

        if not message:
            print("Error: Received empty request or invalid JSON")
            return jsonify({'error': 'Invalid request'}), 400

        print("Received SNS Notification:")
        print(json.dumps(message, indent=4))

        # SNS の SubscriptionConfirmation に対応
        if "Type" in message and message["Type"] == "SubscriptionConfirmation":
            subscribe_url = message.get("SubscribeURL")
            if subscribe_url:
                print(f"Confirming subscription: {subscribe_url}")
                requests.get(subscribe_url)
                return jsonify({'message': 'Subscription confirmed'}), 200

        topic_arn = message.get('TopicArn')

        # SNS の `Message` が JSON 文字列の場合、デコードする
        try:
            message_data = json.loads(message["Message"])
        except (json.JSONDecodeError, TypeError):
            print("Error: Failed to decode SNS Message")
            return jsonify({'error': 'Invalid SNS Message format'}), 400

        # 解析開始通知の処理
        if topic_arn == os.getenv("SNS_TOPIC_VIDEO_ANALYSIS_START"):
            job_id = message_data.get('JobId')
            print(f"Processing Video Analysis Started with JobId: {job_id}")
            return jsonify({'message': f"Video analysis started for JobId {job_id}"}), 200

        # 解析完了通知の処理
        if topic_arn == os.getenv("SNS_TOPIC_VIDEO_ANALYSIS_COMPLETED"):
            job_id = message_data.get('JobId')
            print(f"Processing Video Analysis Completed with JobId: {job_id}")
            result = rekognition_client.get_face_detection(JobId=job_id)
            return jsonify({'rekognition_result': result}), 200

        print("Error: Unknown SNS Topic")
        return jsonify({'error': 'Unknown SNS Topic'}), 400

    except Exception as e:
        print(f"Unexpected error: {str(e)}")
        return jsonify({'error': str(e)}), 500


# Flask アプリ起動時に SNS トピックへ自動登録
subscribe_to_sns_topics()

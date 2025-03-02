from flask import Blueprint, request, jsonify
import json

sns_bp = Blueprint('sns', __name__)

@sns_bp.route('/', methods=['POST'])
def sns_notification():
    try:
        message = request.json
        print("Received SNS Notification:", json.dumps(message, indent=4))  # SNSメッセージをログに出力

        # Subscription Confirmation 処理
        if 'Type' in message and message['Type'] == 'SubscriptionConfirmation':
            subscribe_url = message.get('SubscribeURL')
            print(f"Subscription Confirmation URL: {subscribe_url}")
            return jsonify({'message': 'Subscription confirmation received'}), 200

        # 通常のSNS通知
        if 'Message' in message:
            print(f"Received SNS Message: {message['Message']}")
            return jsonify({'message': 'Notification received'}), 200

        return jsonify({'error': 'Invalid SNS message'}), 400

    except Exception as e:
        print(f"Error: {str(e)}")
        return jsonify({'error': str(e)}), 500

# @sns_bp.route("/notification", methods=["POST"])
# def sns_notification2():
#     """
#     AWS SNS からの通知を受け取る汎用エンドポイント
#     - Rekognition, Transcribe, S3 など、異なるサービスの通知に対応
#     """
#     try:
#         message = request.get_json()
#         print("SNS Notification received:", json.dumps(message, indent=4))

#         # SNS のメッセージタイプを判定
#         if "Type" in message:
#             if message["Type"] == "SubscriptionConfirmation":
#                 # SNS のサブスクリプション確認
#                 subscribe_url = message["SubscribeURL"]
#                 print(f"Confirm the SNS subscription by visiting: {subscribe_url}")
#                 return jsonify({"message": "Subscription confirmation received"}), 200

#             elif message["Type"] == "Notification":
#                 # SNS からの通知を処理
#                 process_sns_notification(message)
#                 return jsonify({"message": "SNS notification processed"}), 200

#         return jsonify({"message": "Unknown SNS message type"}), 400

#     except Exception as e:
#         return jsonify({"error": str(e)}), 500

# def process_sns_notification(message):
#     """
#     SNS からの通知メッセージを解析し、適切な処理を実行
#     """
#     try:
#         sns_message = json.loads(message["Message"])
#         print("SNS Message:", sns_message)

#         # Rekognition の通知の場合
#         if "JobId" in sns_message and "Status" in sns_message:
#             if "FaceDetection" in sns_message.get("JobType", ""):
#                 handle_rekognition_notification(sns_message)
#             elif "TranscriptionJob" in sns_message:
#                 handle_transcribe_notification(sns_message)

#         # 他のSNS通知に対応（例：S3イベントなど）
#         elif "Records" in sns_message:
#             handle_s3_notification(sns_message)

#     except Exception as e:
#         print("Error processing SNS message:", str(e))

# def handle_rekognition_notification(sns_message):
#     """
#     AWS Rekognition 解析結果を取得し、DB に保存
#     """
#     job_id = sns_message["JobId"]
#     status = sns_message["Status"]

#     if status == "SUCCEEDED":
#         print(f"Rekognition Job {job_id} completed successfully!")
#         fetch_rekognition_results(job_id)

# def handle_transcribe_notification(sns_message):
#     """
#     AWS Transcribe の音声解析結果を取得し、DB に保存
#     """
#     job_id = sns_message["TranscriptionJob"]["TranscriptionJobName"]
#     status = sns_message["TranscriptionJob"]["TranscriptionJobStatus"]

#     if status == "COMPLETED":
#         print(f"Transcribe Job {job_id} completed successfully!")
#         fetch_transcribe_results(job_id)

# def handle_s3_notification(sns_message):
#     """
#     S3 からのイベント通知を処理（ファイルアップロード・削除など）
#     """
#     for record in sns_message["Records"]:
#         event_name = record["eventName"]
#         bucket_name = record["s3"]["bucket"]["name"]
#         object_key = record["s3"]["object"]["key"]
#         print(f"S3 Event: {event_name}, Bucket: {bucket_name}, File: {object_key}")

# def fetch_rekognition_results(job_id):
#     """
#     Rekognition の解析結果を取得
#     """
#     rekognition_client = Config.init_rekognition_client()
#     response = rekognition_client.get_face_detection(JobId=job_id)
#     faces = response.get("Faces", [])
#     print(f"Rekognition結果 (Job ID: {job_id}):", faces)

# def fetch_transcribe_results(job_id):
#     """
#     Transcribe の解析結果を取得
#     """
#     transcribe_client = Config.init_transcribe_client()
#     response = transcribe_client.get_transcription_job(TranscriptionJobName=job_id)
#     transcript_url = response["TranscriptionJob"]["Transcript"]["TranscriptFileUri"]
#     print(f"Transcribe結果 (Job ID: {job_id}): {transcript_url}")

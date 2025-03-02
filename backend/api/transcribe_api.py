import boto3
import time
import json
import requests
from flask import Blueprint, request, jsonify
from config import AWS_REGION, AWSClient

transcribe_bp = Blueprint('transcribe_bp', __name__)
transcribe_client = AWSClient.init_transcribe_client()
comprehend_client = AWSClient.init_comprehend_client()

@transcribe_bp.route('/start_transcription', methods=['POST'])
def start_transcription():
    data = request.json
    job_name = f"transcription-{int(time.time())}"
    media_uri = data.get("s3_uri")
    language_code = "en"  # 直接 "en" に設定（Comprehend 用）
    max_wait_time = 300  # 最大待機時間（秒）

    if not media_uri:
        return jsonify({"error": "Missing S3 URI"}), 400

    try:
        transcribe_client.start_transcription_job(
            TranscriptionJobName=job_name,
            Media={'MediaFileUri': media_uri},
            MediaFormat="mp4",
            LanguageCode="en-US",  # Transcribe の場合は en-US を指定
            OutputBucketName=data.get("output_bucket")
        )

        # ジョブの完了を待つ（ポーリング）
        start_time = time.time()
        while True:
            job = transcribe_client.get_transcription_job(TranscriptionJobName=job_name)
            job_status = job['TranscriptionJob']['TranscriptionJobStatus']

            if job_status == "COMPLETED":
                transcript_uri = job.get('TranscriptionJob', {}).get('Transcript', {}).get('TranscriptFileUri')

                if not transcript_uri:
                    return jsonify({"error": "TranscriptFileUri not found in Transcribe response"}), 500

                response = requests.get(transcript_uri)

                if response.status_code == 200:
                    transcript_data = response.json()
                    transcript_text = transcript_data["results"]["transcripts"][0]["transcript"]

                    # ✅ Comprehend にリクエストを送る（"en" をそのまま使用）
                    print(f"Sending request to Comprehend: {transcript_text[:100]}...")
                    comprehend_response = comprehend_client.detect_sentiment(
                        Text=transcript_text,
                        LanguageCode=language_code  # Comprehend には "en"
                    )
                    print(f"Comprehend Sentiment Data: {comprehend_response}")  # デバッグ用ログ

                    return jsonify({
                        "status": "COMPLETED",
                        "transcript": transcript_text,
                        "sentiment": comprehend_response.get("Sentiment"),
                        "sentiment_score": comprehend_response.get("SentimentScore"),
                        "raw_json": transcript_data
                    }), 200

                return jsonify({"error": "Failed to retrieve transcription file"}), 500

            elif job_status == "FAILED":
                return jsonify({"status": "FAILED"}), 500

            if time.time() - start_time > max_wait_time:
                return jsonify({"error": "Transcription job timeout"}), 500

            time.sleep(5)

    except Exception as e:
        print(f"Error during transcription process: {str(e)}")  # エラーログ
        return jsonify({"error": str(e)}), 500


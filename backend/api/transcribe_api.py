import boto3
import time
import json
import requests
from flask import Blueprint, request, jsonify
from config import AWS_REGION, AWSClient

transcribe_bp = Blueprint('transcribe_bp', __name__)
transcribe_client = AWSClient.init_transcribe_client()

@transcribe_bp.route('/start_transcription', methods=['POST'])
def start_transcription():
    data = request.json
    job_name = f"transcription-{int(time.time())}"
    media_uri = data.get("s3_uri")
    language_code = data.get("language_code", "en-US")  # デフォルトは英語
    max_wait_time = 300  # 最大待機時間（秒）

    if not media_uri:
        return jsonify({"error": "Missing S3 URI"}), 400

    try:
        # 文字起こしジョブの開始
        transcribe_client.start_transcription_job(
            TranscriptionJobName=job_name,
            Media={'MediaFileUri': media_uri},
            MediaFormat="mp4",
            LanguageCode=language_code,
            OutputBucketName=data.get("output_bucket")
        )

        # ジョブの完了を待つ（ポーリング）
        start_time = time.time()
        while True:
            job = transcribe_client.get_transcription_job(TranscriptionJobName=job_name)
            job_status = job['TranscriptionJob']['TranscriptionJobStatus']

            if job_status == "COMPLETED":
                # `TranscriptFileUri` を取得
                transcript_uri = job.get('TranscriptionJob', {}).get('Transcript', {}).get('TranscriptFileUri')

                if not transcript_uri:
                    return jsonify({"error": "TranscriptFileUri not found in Transcribe response"}), 500

                # S3 から JSON を取得
                response = requests.get(transcript_uri)

                if response.status_code == 200:
                    transcript_data = response.json()
                    transcript_text = transcript_data["results"]["transcripts"][0]["transcript"]
                    return jsonify({"status": "COMPLETED", "transcript": transcript_text, "raw_json": transcript_data}), 200
                elif response.status_code == 403:
                    return jsonify({"error": "Access to S3 transcript file is forbidden. Check S3 permissions."}), 403
                elif response.status_code == 404:
                    return jsonify({"error": "S3 transcript file not found. It may not be saved correctly."}), 404
                else:
                    return jsonify({"error": f"Failed to retrieve transcription file (HTTP {response.status_code})"}), 500

            elif job_status == "FAILED":
                return jsonify({"status": "FAILED"}), 500

            # タイムアウトチェック（最大5分待機）
            if time.time() - start_time > max_wait_time:
                return jsonify({"error": "Transcription job timeout"}), 500

            # 5秒待機して再チェック
            time.sleep(5)

    except Exception as e:
        return jsonify({"error": str(e)}), 500

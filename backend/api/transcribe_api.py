import boto3
import time
import json
from flask import Blueprint, request, jsonify
from config import AWS_REGION, AWSClient

transcribe_bp = Blueprint('transcribe_bp', __name__)
transcribe_client = AWSClient.init_transcribe_client()

@transcribe_bp.route('/start_transcription', methods=['POST'])
def start_transcription():
    data = request.json
    job_name = f"transcription-{int(time.time())}"
    media_uri = data.get("s3_uri")

    if not media_uri:
        return jsonify({"error": "Missing S3 URI"}), 400

    try:
        transcribe_client.start_transcription_job(
            TranscriptionJobName=job_name,
            Media={'MediaFileUri': media_uri},
            MediaFormat="mp4",  # 動画のフォーマットに応じて変更
            LanguageCode="ja-JP",  # 日本語の場合
            OutputBucketName=data.get("output_bucket")  # 結果を保存するS3バケット
        )
        return jsonify({"message": "Transcription started", "job_name": job_name}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@transcribe_bp.route('/get_transcription_result', methods=['GET'])
def get_transcription_result():
    job_name = request.args.get("job_name")

    if not job_name:
        return jsonify({"error": "Missing job_name parameter"}), 400

    try:
        job = transcribe_client.get_transcription_job(TranscriptionJobName=job_name)
        job_status = job['TranscriptionJob']['TranscriptionJobStatus']

        if job_status == "COMPLETED":
            transcript_uri = job['TranscriptionJob']['Transcript']['TranscriptFileUri']
            return jsonify({"status": "COMPLETED", "transcript_uri": transcript_uri}), 200
        elif job_status == "FAILED":
            return jsonify({"status": "FAILED"}), 500
        else:
            return jsonify({"status": "IN_PROGRESS"}), 202
    except Exception as e:
        return jsonify({"error": str(e)}), 500

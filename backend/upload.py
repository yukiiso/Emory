from flask import Blueprint, request, jsonify
import os
from google.cloud import storage
from config import google_credentials_path

# Create a single blueprint for uploads
upload_bp = Blueprint('upload_bp', __name__)

# Google Cloud Storage setup
if google_credentials_path:
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = google_credentials_path
else:
    print("GOOGLE_APPLICATION_CREDENTIALS is not set in config.env")

# Connect to GCS
client = storage.Client()
bucket_name = "hackathon-2025-bucket-git"
bucket = client.bucket(bucket_name)  # Updated method

# Function to upload files to Google Cloud Storage
def upload_to_gcs(file, filename):
    try:
        blob = bucket.blob(filename)
        blob.upload_from_file(file, content_type=file.content_type)  # Ensure correct MIME type
        return blob.public_url
    except Exception as e:
        print(f"Error uploading {filename} to GCS: {e}")
        return None

# Define file upload route (Handles both video & audio)
@upload_bp.route('/upload', methods=['POST'])
def upload_file():
    video_file = request.files.get('video')
    audio_file = request.files.get('audio')
    username = request.form.get('username')
    qid = request.form.get('qid')

    if not username or not qid:
        return jsonify({"error": "Username and QID are required"}), 400

    response_data = {}

    # Upload video if provided
    if video_file:
        video_filename = f"{username}_{qid}_v.webm"
        video_url = upload_to_gcs(video_file, video_filename)
        if not video_url:
            return jsonify({"error": "Video upload failed"}), 500
        response_data["video_url"] = video_url

    # Upload audio if provided
    if audio_file:
        audio_filename = f"{username}_{qid}_a.webm"
        audio_url = upload_to_gcs(audio_file, audio_filename)
        if not audio_url:
            return jsonify({"error": "Audio upload failed"}), 500
        response_data["audio_url"] = audio_url

    return jsonify({
        "message": "Files uploaded successfully",
        **response_data
    }), 200

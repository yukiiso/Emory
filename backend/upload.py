from flask import Blueprint, request, jsonify
import os
from google.cloud import storage
from config import google_credentials_path

# Create blueprints for video and audio upload
upload_video_bp = Blueprint('upload_video_bp', __name__)
upload_audio_bp = Blueprint('upload_audio_bp', __name__)

# Google Cloud Storage setup
if google_credentials_path:
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = google_credentials_path
else:
    print("GOOGLE_APPLICATION_CREDENTIALS is not set in config.env")

# Connect to GCS
client = storage.Client()
bucket_name = "hackathon-2025-bucket-git"
bucket = client.get_bucket(bucket_name)

# Function to upload files to Google Cloud Storage
def upload_to_gcs(file, filename):
    blob = bucket.blob(filename)
    blob.upload_from_file(file)
    return blob.public_url  # Return the public URL of the uploaded file

# Define video upload route
@upload_video_bp.route('/upload', methods=['POST'])
def upload_video():
    video_file = request.files.get('video')

    if not video_file:
        return jsonify({"error": "No video file provided"}), 400

    # Retrieve additional form data
    username = request.form.get('username')
    qid = request.form.get('qid')

    if not username or not qid:
        return jsonify({"error": "Username or QID missing"}), 400

    # Generate a unique filename for the video
    video_filename = f"{username}_{qid}_v.webm"

    # Upload video to GCS
    video_url = upload_to_gcs(video_file, video_filename)

    return jsonify({
        "message": "Video uploaded successfully",
        "video_url": video_url
    }), 200

# Define audio upload route
@upload_audio_bp.route('/upload', methods=['POST'])
def upload_audio():
    audio_file = request.files.get('audio')

    if not audio_file:
        return jsonify({"error": "No audio file provided"}), 400

    # Retrieve additional form data
    username = request.form.get('username')
    qid = request.form.get('qid')

    if not username or not qid:
        return jsonify({"error": "Username or QID missing"}), 400

    # Generate a unique filename for the audio
    audio_filename = f"{username}_{qid}_a.webm"

    # Upload audio to GCS
    audio_url = upload_to_gcs(audio_file, audio_filename)

    return jsonify({
        "message": "Audio uploaded successfully",
        "audio_url": audio_url
    }), 200

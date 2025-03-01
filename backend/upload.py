# Inside /emory/backend/upload.py

from flask import Blueprint

upload_video_bp = Blueprint('upload_video_bp', __name__)
upload_audio_bp = Blueprint('upload_audio_bp', __name__)

# Define your video upload routes
@upload_video_bp.route('/upload', methods=['POST'])
def upload_video():
    return "Video uploaded!"

# Define your audio upload routes
@upload_audio_bp.route('/upload', methods=['POST'])
def upload_audio():
    return "Audio uploaded!"


# load_dotenv('config.env')

# # Google Cloud Storageの設定
# google_credentials_path = os.getenv('GOOGLE_APPLICATION_CREDENTIALS')
# if google_credentials_path:
#     os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = google_credentials_path
# else:
#     print("GOOGLE_APPLICATION_CREDENTIALS is not set in config.env")

# # GCSに接続
# client = storage.Client()
# bucket_name = "hackathon-2025-bucket-git"
# bucket = client.get_bucket(bucket_name)

# # アップロードされるファイルの最大サイズ (例: 10MB)
# app.config['MAX_CONTENT_LENGTH'] = 10 * 1024 * 1024  

# # アップロードされたファイルをGCSに保存する関数
# def upload_to_gcs(file, filename):
#     blob = bucket.blob(filename)
#     blob.upload_from_file(file)
#     return blob.public_url  # 公開URLを返す

# @app.route('/')
# def index():
#     return 'ビデオと音声の録画とアップロードができます。'

# @app.route('/upload', methods=['POST'])
# def upload_file():
#     video_file = request.files.get('video')
#     audio_file = request.files.get('audio')

#     username = request.form.get('username')
#     qid = request.form.get('qid')

#     if not video_file or not audio_file:
#         return jsonify({"error": "No video/audio"}), 400

#     # Set File Name
#     video_filename = f"{username}_{qid}_v.webm"
#     audio_filename = f"{username}_{qid}_a.webm"

#     video_url = upload_to_gcs(video_file, video_filename)
#     audio_url = upload_to_gcs(audio_file, audio_filename)

#     return jsonify({
#         "message": "File Uploaded",
#         "video_url": video_url,
#         "audio_url": audio_url
#     }), 200
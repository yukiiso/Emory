import uuid
from flask import Blueprint, jsonify, request
from werkzeug.utils import secure_filename
from backend.config import S3_BUCKET, AWSClient


s3_bp = Blueprint('s3_bp', __name__)
s3_client = AWSClient.init_s3_client()


@s3_bp.route("/upload", methods=["POST"])
def upload_video():
    if "video" not in request.files:
        return jsonify({"error": "ファイルが選択されていません"}), 400

    video = request.files["video"]
    filename = secure_filename(video.filename)
    # TODO: ファイル名を合わせる
    unique_filename = f"{uuid.uuid4()}_{filename}"  # ユニークなファイル名にする

    try:
        s3_client.upload_fileobj(video, S3_BUCKET, unique_filename, ExtraArgs={"ContentType": video.content_type})
        video_url = f"https://{S3_BUCKET}.s3.amazonaws.com/{unique_filename}"
        # TODO: アップロードした動画の情報をRDSに入れる

        return jsonify({"message": "アップロード成功", "url": video_url}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
        

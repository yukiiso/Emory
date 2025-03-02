import uuid
import os
import subprocess
import traceback
from flask import Blueprint, jsonify, request
from werkzeug.utils import secure_filename
from config import S3_BUCKET, AWSClient

s3_bp = Blueprint('s3_bp', __name__)
s3_client = AWSClient.init_s3_client()

# 一時保存ディレクトリ
TMP_DIR = "/tmp"

@s3_bp.route("/upload", methods=["POST"])
def upload_video():
    if "video" not in request.files:
        return jsonify({"error": "ファイルが選択されていません"}), 400

    video = request.files["video"]
    filename = secure_filename(video.filename)
    unique_filename = f"{uuid.uuid4()}_{filename}"  # ユニークなファイル名
    webm_path = os.path.join(TMP_DIR, unique_filename)  # WebM の一時保存先
    mp4_filename = unique_filename.replace(".webm", ".mp4")  # MP4 ファイル名
    mp4_path = os.path.join(TMP_DIR, mp4_filename)  # MP4 の保存先

    try:
        print(f"📂 Saving WebM file to: {webm_path}")
        video.save(webm_path)

        # FFmpeg で WebM → MP4 変換
        command = ["ffmpeg", "-i", webm_path, "-c:v", "libx264", "-preset", "ultrafast", "-crf", "28", mp4_path]
        print(f"⚙️ Running FFmpeg command: {' '.join(command)}")

        result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

        # FFmpeg の出力を表示
        print(f"📜 FFmpeg stdout: {result.stdout}")
        print(f"⚠️ FFmpeg stderr: {result.stderr}")

        if result.returncode != 0:
            raise RuntimeError(f"FFmpeg failed with code {result.returncode}")

        print(f"✅ MP4 conversion complete: {mp4_path}")

        # MP4 を S3 にアップロード
        print(f"⬆️ Uploading {mp4_path} to S3 bucket: {S3_BUCKET} as {mp4_filename}")
        s3_client.upload_file(mp4_path, S3_BUCKET, mp4_filename, ExtraArgs={"ContentType": "video/mp4"})

        video_url = f"https://{S3_BUCKET}.s3.amazonaws.com/{mp4_filename}"
        print(f"✅ Upload successful! Video URL: {video_url}")

        # 一時ファイル削除
        os.remove(webm_path)
        os.remove(mp4_path)

        return jsonify({"message": "アップロード成功", "url": video_url}), 200

    except subprocess.CalledProcessError as e:
        print(f"❌ FFmpeg conversion failed: {e}")
        return jsonify({"error": f"動画変換に失敗しました: {str(e)}"}), 500
    except Exception as e:
        print(f"❌ Unexpected error: {traceback.format_exc()}")
        return jsonify({"error": str(e)}), 500

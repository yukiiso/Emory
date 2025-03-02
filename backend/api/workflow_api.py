# import requests
# from flask import Blueprint, request, jsonify
# from backend.models import User, Question, Record, FaceAnalysis, VoiceAnalysis
# from backend.app import db

# workflow_bp = Blueprint('workflow_bp', __name__)

# @workflow_bp.route('/run_transcription_workflow', methods=['POST'])
# def run_transcription_workflow():
#     """
#     ワークフロー: Transcribe を実行し、その結果を DB に保存
#     """
#     data = request.json
#     s3_uri = data.get("s3_uri")
#     user_id = data.get("user_id")
#     question_id = data.get("question_id")
#     output_bucket = data.get("output_bucket")

#     if not s3_uri or not user_id or not question_id:
#         return jsonify({"error": "Missing required parameters"}), 400

#     try:
#         # **Step 1: Transcribe を開始**
#         transcribe_url = "http://localhost:5001/api/transcribe/start_transcription"
#         transcribe_payload = {
#             "s3_uri": s3_uri,
#             "output_bucket": output_bucket,
#             "user_id": user_id,
#             "question_id": question_id
#         }
        
#         transcribe_response = requests.post(transcribe_url, json=transcribe_payload)
        
#         if transcribe_response.status_code != 200:
#             return jsonify({"error": "Failed to start transcription", "details": transcribe_response.json()}), 500
        
#         transcribe_data = transcribe_response.json()
#         print(f"✅ Transcription completed: {transcribe_data}")

#         # **Step 2: データを DB に保存**
#         transcript = transcribe_data.get("transcript")
#         sentiment = transcribe_data.get("sentiment")
#         sentiment_score = transcribe_data.get("sentiment_score", {})

#         if not transcript or not sentiment or not sentiment_score:
#             return jsonify({"error": "Missing required data from transcription response"}), 500

#         # 既存データを確認
#         existing_analysis = VoiceAnalysis.query.filter_by(user_id=user_id, question_id=question_id).first()

#         if existing_analysis:
#             # **更新**
#             existing_analysis.transcript = transcript
#             existing_analysis.mixed = sentiment_score.get("Mixed", 0.0)
#             existing_analysis.negative = sentiment_score.get("Negative", 0.0)
#             existing_analysis.neutral = sentiment_score.get("Neutral", 0.0)
#             existing_analysis.positive = sentiment_score.get("Positive", 0.0)
#         else:
#             # **新規作成**
#             new_analysis = VoiceAnalysis(
#                 user_id=user_id,
#                 question_id=question_id,
#                 transcript=transcript,
#                 mixed=sentiment_score.get("Mixed", 0.0),
#                 negative=sentiment_score.get("Negative", 0.0),
#                 neutral=sentiment_score.get("Neutral", 0.0),
#                 positive=sentiment_score.get("Positive", 0.0)
#             )
#             db.session.add(new_analysis)

#         db.session.commit()

#         return jsonify({
#             "status": "DB_UPDATED",
#             "transcript": transcript,
#             "sentiment": sentiment,
#             "sentiment_score": sentiment_score
#         }), 200

#     except Exception as e:
#         return jsonify({"error": str(e)}), 500

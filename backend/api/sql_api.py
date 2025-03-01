# This API is to display DB in browser. (Manual testing purposes)

from flask import Blueprint, jsonify
from backend.models import User, Question, Record, FaceAnalysis, VoiceAnalysis

# Blueprint for DB test
sql_bp = Blueprint('sql_bp', __name__)

# Health check route
@sql_bp.route('/health', methods=['GET'])
def health_check():
    return jsonify({"message": "SQL DB API is running!"})

# Get all users
@sql_bp.route('/User', methods=['GET'])
def get_users():
    try:
        # Query the users table using SQLAlchemy
        users = User.query.all()  # This fetches all records from the `users` table
        user_data = [
            {
                "id":       user.id, 
                "name":     user.name, 
                "age":      user.age,
                "gender":   user.gender,
                "username": user.username,
                "email":    user.email,
            }
            for user in users
        ]  # Adjust fields as necessary

        if user_data:
            return jsonify({'status': 'success', 'users': user_data})
        else:
            return jsonify({'status': 'success', 'users': []})
    except Exception as e:
        print("Database connection error:", e)
        return jsonify({'status': 'error', 'message': str(e)})

# Get all questions
@sql_bp.route('/Question', methods=['GET'])
def get_questions():
    try:
        questions = Question.query.all()
        question_data = [
            {
                "id":      question.id,
                "content": question.content
            }
            for question in questions
        ]

        if question_data:
            return jsonify({'status': 'success', 'questions': question_data})
        else:
            return jsonify({'status': 'success', 'questions': []})
    except Exception as e:
        print("Database connection error:", e)
        return jsonify({'status': 'error', 'message': str(e)})

# Get all records
@sql_bp.route('/Record', methods=['GET'])
def get_records():
    try:
        records = Record.query.all()
        record_data = [
            {
                "id":      record.id,
                "username": record.username,
                "v_name":   record.v_name,
                "a_name":   record.a_name,
                "date":     record.date
            }
            for record in records
        ]

        if record_data:
            return jsonify({'status': 'success', 'records': record_data})
        else:
            return jsonify({'status': 'success', 'records': []})
    except Exception as e:
        print("Database connection error:", e)
        return jsonify({'status': 'error', 'message': str(e)})

# Get all face analyses
@sql_bp.route('/FaceAnalysis', methods=['GET'])
def get_face_analyses():
    try:
        face_analyses = FaceAnalysis.query.all()
        face_analysis_data = [
            {
                "id":       analysis.id,
                "username": analysis.username,
                "question_id": analysis.question_id,
                "happy":    analysis.happy,
                "sad":      analysis.sad,
                "angry":    analysis.angry,
                "calm":     analysis.calm,
                "fear":     analysis.fear,
                "smile":    analysis.smile
            }
            for analysis in face_analyses
        ]

        if face_analysis_data:
            return jsonify({'status': 'success', 'face_analyses': face_analysis_data})
        else:
            return jsonify({'status': 'success', 'face_analyses': []})
    except Exception as e:
        print("Database connection error:", e)
        return jsonify({'status': 'error', 'message': str(e)})

# Get all voice analyses
@sql_bp.route('/VoiceAnalysis', methods=['GET'])
def get_voice_analyses():
    try:
        voice_analyses = VoiceAnalysis.query.all()
        voice_analysis_data = [
            {
                "id":        analysis.id,
                "username":  analysis.username,
                "question_id": analysis.question_id,
                "speed":     analysis.speed,
                "pulse":     analysis.pulse
            }
            for analysis in voice_analyses
        ]

        if voice_analysis_data:
            return jsonify({'status': 'success', 'voice_analyses': voice_analysis_data})
        else:
            return jsonify({'status': 'success', 'voice_analyses': []})
    except Exception as e:
        print("Database connection error:", e)
        return jsonify({'status': 'error', 'message': str(e)})


from flask import Blueprint, jsonify
from backend.config import OPENAI_API_KEY
import requests

# Blueprint for chatGPT AI
chatgpt_bp = Blueprint('chatgpt_bp', __name__)

@chatgpt_bp.route('/summary', methods=['GET'])
def summary_get():
    url = "https://api.openai.com/v1/chat/completions"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {OPENAI_API_KEY}"
    }
    data = {
        "model": "gpt-4o-mini",
        "messages": [{"role": "user", "content": "Say this is a test!"}],
        "temperature": 0.7
    }

    response = requests.post(url, json=data, headers=headers)
    
    if response.status_code == 402 and "insufficient_quota" in response.text:
        return jsonify({"message": "API quota exceeded. Please check your billing details.", "error": response.json()}), 402
    elif response.status_code == 200:
        return jsonify({"message": "Flask backend API is running!", "openai_response": response.json()})
    else:
        return jsonify({"message": "Flask backend API is running!", "error": response.text}), response.status_code
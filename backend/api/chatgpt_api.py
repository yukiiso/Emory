from flask import Blueprint, jsonify, request
from config import OPENAI_API_KEY
import requests
from backend.models import db
from models import Record

# Blueprint for chatGPT AI
chatgpt_bp = Blueprint('chatgpt_bp', __name__)

# Route to handle text summarization and store data to the Record table
@chatgpt_bp.route('/summary', methods=['POST'])
def summary_post():
    # Extract the text from the request
    input_text = request.json.get('text')

    if not input_text:
        return jsonify({"message": "No text provided"}), 400

    # Prepare the request to OpenAI API
    openai_url = "https://api.openai.com/v1/chat/completions"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {OPENAI_API_KEY}"
    }

    data = {
        "model": "gpt-4o-mini",
        "messages": [
            {"role": "user", "content": f"Please summarize this: {input_text}"}
        ],
        "temperature": 0.7
    }

    # Get the summary from OpenAI API
    response = requests.post(openai_url, json=data, headers=headers)

    if response.status_code == 402 and "insufficient_quota" in response.text:
        return jsonify({"message": "API quota exceeded. Please check your billing details.", "error": response.json()}), 402
    elif response.status_code == 200:
        summary = response.json()['choices'][0]['message']['content']
        
        # Store summary to database (if necessary)
        # new_record = Record(summary=summary)
        # db.session.add(new_record)
        # db.session.commit()

        return jsonify({"message": "Text summary generated successfully!", "summary": summary}), 200
    
    else:
        return jsonify({"message": "Error in summarizing text.", "error": response.text}), response.status_code
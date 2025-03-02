from flask import Blueprint, jsonify, request
from config import OPENAI_API_KEY
import requests
from app import db
from models import Record
import re

# Blueprint for chatGPT AI
chatgpt_bp = Blueprint('chatgpt_bp', __name__)

# Route to handle text summarization and store data to the Record table
@chatgpt_bp.route('/summary', methods=['POST'])
def summary_post():
    # Extract the text and audio filename from the request
    input_text = request.json.get('text')
    audiofilename = request.json.get('audiofilename')  
    
    if not input_text or not audiofilename:
        return jsonify({"message": "No text or audio filename provided"}), 400
    
    try:
        match = re.match(r"^([a-zA-Z0-9_]+)_(\d+)_a$", audiofilename)
        if not match:
            return jsonify({"message": "Invalid audio filename format."}), 400
        
        username = match.group(1)
        qid = int(match.group(2))

    except Exception as e:
        return jsonify({"message": f"Error extracting username and qid: {str(e)}"}), 400
    
    openai_url = "https://api.openai.com/v1/chat/completions"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {OPENAI_API_KEY}"
    }

    data = {
        "model": "gpt-4o-mini",
        "messages": [
            {"role": "user", "content": f"This is what the client of counseling talked. Please summarize it: {input_text}"}
        ],
        "temperature": 0.7
    }

    # Get the summary from OpenAI API
    response = requests.post(openai_url, json=data, headers=headers)
    
    if response.status_code == 402 and "insufficient_quota" in response.text:
        return jsonify({"message": "API quota exceeded. Please check your billing details.", "error": response.json()}), 402
    elif response.status_code == 200:
        summary = response.json()['choices'][0]['message']['content']
        
        new_record = Record(
            username=username, 
            qid=qid, 
            summary=summary,
        )
        db.session.add(new_record)
        db.session.commit()

        return jsonify({"message": "Text summary generated and stored successfully!", "summary": summary}), 200
    
    else:
        return jsonify({"message": "Error in summarizing text.", "error": response.text}), response.status_code

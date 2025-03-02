from flask import Blueprint, jsonify, request
from config import OPENAI_API_KEY
import requests

# Blueprint for chatGPT AI
chatgpt_bp = Blueprint('chatgpt_bp', __name__)

# Route to handle text summarization
@chatgpt_bp.route('/summary', methods=['POST'])
def summary_post():
    # Extract the text from the request
    input_text = request.json.get('text')  # Assuming the frontend sends a JSON payload with 'text' field
    
    if not input_text:
        return jsonify({"message": "No text provided"}), 400
    
    # Step 2: Send the text to OpenAI for summarization
    openai_url = "https://api.openai.com/v1/chat/completions"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {OPENAI_API_KEY}"
    }

   # Create a custom prompt, integrating the input text into the conversation
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
        return jsonify({"message": "Text summary generated successfully!", "summary": summary})
    else:
        return jsonify({"message": "Error in summarizing text.", "error": response.text}), response.status_code

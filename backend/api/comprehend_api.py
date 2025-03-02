import boto3
from flask import Blueprint, request, jsonify
from config import AWS_REGION, AWSClient

comprehend_bp = Blueprint('comprehend_bp', __name__)
comprehend_client = AWSClient.init_comprehend_client()

@comprehend_bp.route('/analyze_sentiment', methods=['POST'])
def analyze_sentiment():
    data = request.json
    text = data.get("text")
    language_code = data.get("language_code", "en")  # デフォルトは英語

    if not text:
        return jsonify({"error": "Missing text parameter"}), 400

    try:
        print(f"Analyzing sentiment for text: {text[:100]}...")  # デバッグ用ログ
        response = comprehend_client.detect_sentiment(
            Text=text,
            LanguageCode=language_code
        )
        print(f"Comprehend Response: {response}")  # デバッグ用ログ

        return jsonify({
            "sentiment": response.get("Sentiment"),
            "sentiment_score": response.get("SentimentScore")
        }), 200

    except comprehend_client.exceptions.InvalidRequestException as e:
        print(f"InvalidRequestException: {str(e)}")
        return jsonify({"error": "Invalid request to Comprehend", "details": str(e)}), 400

    except comprehend_client.exceptions.TextSizeLimitExceededException as e:
        print(f"TextSizeLimitExceededException: {str(e)}")
        return jsonify({"error": "Text size exceeds Comprehend limit", "details": str(e)}), 400

    except comprehend_client.exceptions.UnsupportedLanguageException as e:
        print(f"UnsupportedLanguageException: {str(e)}")
        return jsonify({"error": "Language not supported by Comprehend", "details": str(e)}), 400

    except Exception as e:
        print(f"Unexpected Error in Comprehend: {str(e)}")
        return jsonify({"error": "Comprehend processing failed", "details": str(e)}), 500

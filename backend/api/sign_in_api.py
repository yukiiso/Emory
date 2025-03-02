from flask import Flask, request, jsonify
from werkzeug.security import check_password_hash
from backend.models import db
from flask_cors import CORS
from models import User

app = Flask(__name__)
CORS(app, resources={
        r"/api/*": {"origins": "*"},    # Allow all origins for `/api` routes
    })   

@app.route('/', methods=['POST'])
def signin():
    data = request.get_json()

    # Extract data from the request
    username = data.get('username')
    password = data.get('password')

    # Check if required fields are missing
    if not all([username, password]):
        return jsonify({"error": "Missing required fields!"}), 400

    # Find the user by username
    user = User.query.filter_by(username=username).first()

    if user and check_password_hash(user.password, password):
        # Routing!!!! TO DO
        return jsonify({
            "message": "Login successful!",
            "user_id": user.id,
            "username": user.username,
            "category": user.category
        }), 200
    else:
        return jsonify({"error": "Invalid username or password!"}), 400
from flask import Flask, request, jsonify, Blueprint, current_app
from werkzeug.security import generate_password_hash
from backend.models import db, User
signup_bp = Blueprint('signup_bp', __name__)

@signup_bp.route('/test', methods=['GET'])
def test_signup_route():
    return jsonify({"message": "Signup route is working!"})


@signup_bp.route('/', methods=['POST'])
def signup():
    data = request.get_json()

    # Extract data from the request
    name = data.get('name')
    age = data.get('age')
    gender = data.get('gender')
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')
    category = data.get('category', 0)

    # Check if required fields are missing
    if not all([name, age, gender, username, email, password]):
        return jsonify({"error": "Missing required fields!"}), 400

    hashed_password = generate_password_hash(password)

    # Check if the username or email already exists
    with current_app.app_context():
        existing_user = User.query.filter((User.username == username) | (User.email == email)).first()
        if existing_user:
            return jsonify({"error": "Username or email already exists!"}), 400

        # Create a new User entry
        new_user = User(
            name=name,
            age=age,
            gender=gender,
            username=username,
            email=email,
            password=hashed_password,
            category=category
        )

        try:
            db.session.add(new_user)
            db.session.commit()
            return jsonify({"message": "User created successfully!", "redirectTo": "http://localhost:3000/sign-in"}), 201

        except Exception as e:
            db.session.rollback()
            return jsonify({"error": f"Error creating user: {str(e)}"}), 400

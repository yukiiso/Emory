from flask import Flask, request, jsonify
from werkzeug.security import generate_password_hash
from app import db
from models import User

app = Flask(__name__)

@app.route('/signup', methods=['POST'])
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

    hashed_password = generate_password_hash(password, method='sha256')

    # Check if the username or email already exists
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
        # Routing!!!! TO DO
        return jsonify({"message": "User created successfully!"}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"Error creating user: {str(e)}"}), 400

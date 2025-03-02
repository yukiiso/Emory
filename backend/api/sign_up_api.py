from flask import Flask, request, jsonify, Blueprint
from werkzeug.security import generate_password_hash
from backend.models import db
from flask_cors import CORS
from models import User

signup_bp = Blueprint('signup_bp', __name__)

app = Flask(__name__)
CORS(app, resources={
        r"/api/*": {"origins": "*"},    # Allow all origins for `/api` routes
    })   

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

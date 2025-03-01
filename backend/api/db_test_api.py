# This API is to display DB in browser. (Manual testing purposes)

from flask import Blueprint, jsonify

# Table import 
from backend.models import User

# Blueprint for DB test
db_test_bp = Blueprint('db_test_bp', __name__)

# TODO: あとで消すこの関数
@db_test_bp.route('/health', methods=['GET'])
def health_check():
    return jsonify({"message": "Flask backend API is runningSXtdrcyfghn"})
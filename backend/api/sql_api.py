# This API is to display DB in browser. (Manual testing purposes)

from flask import Blueprint, jsonify

# Table import 
from backend.models import User

# Blueprint for DB test
sql_bp = Blueprint('sql_bp', __name__)

# TODO: あとで消すこの関数
@sql_bp.route('/health', methods=['GET'])
def health_check():
    return jsonify({"message": "SQL DB API is running!"})
# This API is to display DB in browser. (Manual testing purposes)

from flask import Blueprint, jsonify

# Blueprint for DB test
dynamo_bp = Blueprint('dynamo_bp', __name__)

# TODO: あとで消すこの関数
@dynamo_bp.route('/health', methods=['GET'])
def health_check():
    return jsonify({"message": "DynamoDB API is running!"})
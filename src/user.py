from flask import Blueprint, request, jsonify
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
import uuid
import asyncio
from database import db

user_bp = Blueprint('user', __name__)

@user_bp.before_app_first_request
def initialize_database():
    asyncio.run(db.connect())

@user_bp.route('/user', methods=['POST'])
def create_user():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    if not username or not password:
        return jsonify({'error': 'Username and password are required'}), 400
    user_id = str(uuid.uuid4())
    asyncio.run(db.create_user(user_id, username, password))
    return jsonify({'user_id': user_id}), 201

@user_bp.route('/user/<user_id>', methods=['GET'])
@jwt_required()
def get_user(user_id):
    current_user = get_jwt_identity()
    user = asyncio.run(db.get_user(current_user))
    if not user:
        return jsonify({'error': 'User not found'}), 404
    return jsonify(user), 200

@user_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    user = asyncio.run(db.get_user(username))
    if user and user['password'] == password:
        access_token = create_access_token(identity=username)
        return jsonify({'token': access_token}), 200
    return jsonify({'error': 'Invalid credentials'}), 401
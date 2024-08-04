import logging
from quart import Quart, Blueprint, request, jsonify
from quart_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
import uuid
from database import insert_user_into_surreal, get_user_from_db

app = Quart(__name__)
jwt = JWTManager(app)

user_bp = Blueprint('user', __name__)
    
@user_bp.route('/user', methods=['POST'])
async def create_user():
    data = await request.get_json()
    username = data.get('username')
    password = data.get('password')
    if not username or not password:
        return jsonify({'error': 'Username and password are required'}), 400
    user_id = await insert_user_into_surreal(username, password)
    return jsonify({'user_id': user_id}), 201

@user_bp.route('/user/<user_id>', methods=['GET'])
async def get_user(user_id):
    user = await get_user_from_db(user_id)
    if not user:
        return jsonify({'error': 'User not found'}), 404
    return jsonify(user), 200

@user_bp.route('/login', methods=['POST'])
async def login():
    data = await request.get_json()
    username = data.get('username')
    # Add login logic here

app.register_blueprint(user_bp)

if __name__ == '__main__':
    app.run()
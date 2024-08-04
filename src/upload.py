from quart import Blueprint
from quart_jwt_extended import jwt_required

upload_bp = Blueprint('upload', __name__)

@upload_bp.route('/upload')
@jwt_required
async def video():
    return 'This is the video upload endpoint'
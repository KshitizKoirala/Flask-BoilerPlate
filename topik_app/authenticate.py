import jwt
from functools import wraps
from flask import request, jsonify, current_app

from .users.users import User


# TOKEN REQUIRED
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None

        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']

        if not token:
            return jsonify({"message": "Token is Missing!!"}), 401

        try:
            data = jwt.decode(token, current_app.config.get(
                'SECRET_KEY'), algorithms="HS256")
            current_user = User.query.filter_by(email=data["email"]).first()
        except:
            return jsonify({"message": "Token is invalid"}), 401

        return f(current_user, *args, **kwargs)
    return decorated

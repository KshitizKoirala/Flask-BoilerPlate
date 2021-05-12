import jwt
import traceback
from functools import wraps
from flask import request, jsonify, current_app

from ..api.users.users import User


class PermissionError(Exception):
    pass


# TOKEN REQUIRED DECORATOR
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
        except Exception:
            traceback.print_exc()  # This prints the traceback to the console
            err = traceback.format_exc()
            current_app.logger.error(err)
            return jsonify({"message": "Token is invalid"}), 401

        return f(current_user, *args, **kwargs)
    return decorated


# Authenticate All Routes
def all_routes_tokenized():
    if 'x-access-token' in request.headers:
        token = request.headers['x-access-token']
        try:
            data = jwt.decode(token, current_app.config.get(
                'SECRET_KEY'), algorithms="HS256")
            current_user = User.query.filter_by(email=data["email"]).first()
            if current_user.role != 'administrator':
                raise PermissionError
        except PermissionError:
            return jsonify({"message": "Invalid Permission"}), 401

        except Exception:
            traceback.print_exc()  # This prints the traceback to the console
            err = traceback.format_exc()
            current_app.logger.error(err)
            return jsonify({"message": "Token is invalid"}), 401
    else:
        return jsonify({"message": "Please Login in to continue..."}), 401


# # TOKEN REQUIRED DECORATOR
# def destroy_token(f):
#     @wraps(f)
#     def decorated(*args, **kwargs):
#         token = None

#         if 'x-access-token' in request.headers:
#             token = request.headers['x-access-token']

#         if not token:
#             return jsonify({"message": "Token is Missing!!"}), 401

#         try:
#             data = jwt.decode(token, current_app.config.get(
#                 'SECRET_KEY'), algorithms="HS256")
#             current_user = User.query.filter_by(email=data["email"]).first()
#             user.
#         except Exception:
#             traceback.print_exc()  # This prints the traceback to the console
#             err = traceback.format_exc()
#             current_app.logger.error(err)
#             return jsonify({"message": "Token is invalid"}), 401

#         return f(current_user, *args, **kwargs)
#     return decorated

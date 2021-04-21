import os
import jwt
import json
import datetime
from sqlalchemy import exc
from werkzeug.utils import secure_filename
from flask import Blueprint, jsonify, request, make_response, current_app
from werkzeug.security import generate_password_hash, check_password_hash

from .users import User
from ..Logger import logger
from topik_app.extensions import db
from topik_app.authenticate import token_required
from .serializer import user_schema, users_schema, post_schema


users = Blueprint('users', __name__, url_prefix='/users')

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}


# Chechk for file extensions
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# Get All Users
@users.route("/", methods=['GET'])
@token_required
def get_all_users(current_user):
    if current_user.role == 'administrator':
        users = User.query.all()
        if users:
            result = users_schema.dump(users)
            return jsonify(result)
        else:
            return jsonify({'message': "No Users Found"}), 404
    else:
        return jsonify({"message": "Invalid Permission"}), 401


# Get Single User
@users.route("/<id>", methods=['GET'])
@token_required
def get_user(current_user, id):
    if current_user.role == 'administrator':
        user = User.query.get(id)
        if user:
            return user_schema.jsonify(user)
        else:
            return jsonify({'message': "No User Found for this email"}), 404
    else:
        return jsonify({"message": "Invalid Permission"}), 401


# Add A User
@users.route("/add", methods=['POST'])
def add_user():
    password = request.form['password']
    password2 = request.form['password2']
    if password == password2:
        hashed_password = generate_password_hash(password, method='sha256')
    else:
        return jsonify({"message": "Passwords do not Match"}), 400
    full_name = request.form['full_name']
    email = request.form['email']
    password = hashed_password
    if request.files['profile_picture'] and allowed_file(request.files['profile_picture'].filename):
        profile_picture = request.files['profile_picture']
        profile_picture.save(secure_filename(profile_picture.filename))
    else:
        profile_picture = ""
    phone_number = request.form['phone_number']
    date_of_birth = request.form['date_of_birth']
    address = request.form['address']
    role = request.form['role']

    # Also Serializes the User to be entered into the database
    new_user = User(full_name, email, password,
                    phone_number, profile_picture, date_of_birth, role, address)

    try:
        db.session.add(new_user)
        db.session.commit()
        return user_schema.jsonify(new_user)

    except exc.IntegrityError:
        db.session.rollback()
        return jsonify({"message": "Please Check Your Email and PhoneNumber"}), 401

    except:
        db.session.rollback()
        current_app.logger.error('%s failed to create user')
        return jsonify({"message": "An Error Occured Please Try Again Later"}), 500


# Update A User
@users.route("/<id>", methods=['PUT'])
@token_required
def edit_user(current_user, id):
    password = request.form['password']
    password2 = request.form['password2']
    if password == password2:
        hashed_password = generate_password_hash(password, method='sha256')
    else:
        return jsonify({"message": "Passwords do not Match"}), 400
    user = User.query.get(id)

    if user is not None and current_user:
        if current_user.email == user.email or current_user.role == 'administrator':
            user.full_name = request.form['full_name']
            user.email = request.form['email']
            user.password = hashed_password
            if request.files['profile_picture'] and allowed_file(request.files['profile_picture'].filename):
                profile_picture = request.files['profile_picture']
                profile_picture.save(secure_filename(profile_picture.filename))
                user.profile_picture = profile_picture
            else:
                user.profile_picture = ""
            user.phone_number = request.form['phone_number']
            user.date_of_birth = request.form['date_of_birth']
            user.address = request.form['address']
            user.role = request.form['role']

            try:
                db.session.commit()
                return user_schema.jsonify(user), 200
            except exc.IntegrityError:
                db.session.rollback()
                return jsonify({"message": "Please Check Your Email and PhoneNumber"})
            except:
                db.session.rollback()
                current_app.logger.error('%s failed to edit user', user.email)
                return jsonify({"message": "An Error Occured Please Try Again Later"})

        else:
            return jsonify({"message": "Invalid Permission"}), 403
    else:
        return jsonify({"message": "No User Found! Please verify your permission and try again"}), 400


# DELETE A USER
@ users.route("/<id>", methods=['DELETE'])
@ token_required
def delete_user(current_user, id):
    user = User.query.get(id)

    if user is not None:
        if user.email == current_user.email:
            db.session.delete(user)
            db.session.commit()
            return user_schema.jsonify(user)
        else:
            return jsonify({"message": "Invalid Permissions"}), 403
    else:
        return jsonify({'message': "No User Found for this email"}), 404


# USER LOGIN
@ users.route('/login', methods=['POST'])
def user_login():
    auth = request.authorization
    if not auth or not auth.username or not auth.password:
        return make_response('Please enter a valid credentials', 401, {'WWW-Authenticate': 'Basic realm="Login required!"'})
    user = User.query.filter_by(email=auth.username).first()

    if not user:
        return make_response('No User Registered for this email', 401, {'WWW-Authenticate': 'Basic realm="Login required!"'})
    if check_password_hash(user.password, auth.password):
        token = jwt.encode({
            'id': user.id,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30),
            'email': user.email,
            'role': user.role
        },  current_app.config.get('SECRET_KEY'))
        return jsonify({'token': token}), 200
    return make_response('Invalid Email or Password', 401, {'WWW-Authenticate': 'Basic realm="Login required!"'})

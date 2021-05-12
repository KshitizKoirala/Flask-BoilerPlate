import os
import jwt
import json
import traceback
import datetime
from sqlalchemy import exc
from marshmallow import ValidationError
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash, check_password_hash
from flask import Blueprint, jsonify, request, current_app, url_for, session, render_template

from .users import User
from topik_app.extensions import db, oauth
from topik_app.services.filename_checker import allowed_file
from topik_app.authorization.authenticate import token_required
from topik_app.errors.errors import NoUserFoundError, InputError, BackendError
from topik_app.services.mail_service import send_mail
from .serializer import user_schema, users_schema, post_schema, oauth_schema, forgot_pwd, reset_pwd


users = Blueprint('users', __name__, url_prefix='/users')


# ANCHOR Get All Users
@users.route("/", methods=['GET'])
@token_required
def get_all_users(current_user):
    if current_user.role == 'administrator':
        users = User.query.all()
        result = users_schema.dump(users)
        return jsonify(result)

    else:
        return jsonify({"message": "Invalid Permission"}), 401


# ANCHOR Get Single User
@users.route("/<id>/", methods=['GET'])
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


# ANCHOR Add A User
@users.route("/add/", methods=['POST'])
def add_user():
    try:
        if request.method == 'POST':
            input_data = request.form
            data = json.dumps(input_data)
            schema = post_schema
            user_signup = schema.load(json.loads(data))
            password = user_signup['password']
            password2 = user_signup['password2']
            if password == password2:
                hashed_password = generate_password_hash(
                    password, method='sha256')
            else:
                return jsonify({"message": "Passwords do not Match"}), 400

            if not user_signup['role']:
                role = 'student'
            else:
                role = user_signup['role']

            full_name = user_signup['full_name']
            email = user_signup['email']
            password = hashed_password
            phone_number = user_signup['phone_number']
            date_of_birth = user_signup['date_of_birth']
            address = user_signup['address']

            if request.files and allowed_file(request.files['profile_picture'].filename):
                profile_picture = request.files['profile_picture']
                filename = secure_filename(
                    user_signup['email'] + '_' + profile_picture.filename)
                profile_picture.save(os.path.join(
                    current_app.config.get('PROFILE_UPLOAD_FOLDER'), filename))
            else:
                profile_picture = ""

             # Also Serializes the User to be entered into the database
            new_user = User(full_name, email, password,
                            phone_number, profile_picture, date_of_birth, role, address)
            db.session.add(new_user)
            db.session.commit()
            return user_schema.jsonify(new_user)

    except ValidationError as err:
        print(err.valid_data)  # => {"name": "John"}
        # => {"email": ['"foo" is not a valid email address.']}
        return jsonify({"error": err.messages}), 400

    except exc.IntegrityError:
        db.session.rollback()
        return jsonify({"message": "Duplicate Email or PhoneNumber. Please Verify!"}), 401

    except Exception:
        db.session.rollback()
        traceback.print_exc()  # This prints the traceback to the console
        err = traceback.format_exc()
        current_app.logger.error('Failed to create user' + err)
        return jsonify({"message": "An Error Occured Please Try Again Later"}), 500


# ANCHOR Update A User
@ users.route("/edit/<id>/", methods=['PUT'])
@ token_required
def edit_user(current_user, id):
    try:
        input_data = request.form
        data = json.dumps(input_data)
        schema = post_schema
        user_edit = schema.load(json.loads(data))

        password = user_edit['password']
        password2 = user_edit['password2']
        if password == password2:
            hashed_password = generate_password_hash(password, method='sha256')
        else:
            return jsonify({"message": "Passwords do not Match"}), 400
        user = User.query.get(id)

        if user is not None and current_user:
            if current_user.email == user.email or current_user.role == 'administrator':
                user.full_name = user_edit['full_name']
                user.email = user_edit['email']
                user.password = hashed_password
                if request.files and allowed_file(request.files['profile_picture'].filename):
                    profile_picture = request.files['profile_picture']
                    profile_picture.save(
                        secure_filename(profile_picture.filename))
                    user.profile_picture = profile_picture
                else:
                    user.profile_picture = user.profile_picture

                user.phone_number = user_edit['phone_number']
                user.date_of_birth = user_edit['date_of_birth']
                user.address = user_edit['address']
                if not user_edit['role']:
                    user.role
                else:
                    user.role = user_edit['role']
                db.session.commit()
                return user_schema.jsonify(user), 200
            else:
                return jsonify({"message": "Invalid Permission"}), 403
        else:
            return jsonify({"message": "No User Found! Please verify your permission and try again"}), 400

    except ValidationError as err:
        current_app.logger.error('%s failed to create user')
        print(err.valid_data)  # => {"name": "John"}
        # => {"email": ['"foo" is not a valid email address.']}
        return jsonify({"error": err.messages}), 400

    except exc.IntegrityError:
        db.session.rollback()
        return jsonify({"message": "Duplicate Email or PhoneNumber. Please Verify!"})
    except Exception:
        db.session.rollback()
        traceback.print_exc()  # This prints the traceback to the console
        err = traceback.format_exc()
        current_app.logger.error('%s failed to edit user' + err)
        return jsonify({"message": "An Error Occured Please Try Again Later"}), 500


# ANCHOR DELETE A USER
@ users.route("/delete/<id>/", methods=['DELETE'])
@ token_required
def delete_user(current_user, id):
    user = User.query.get(id)
    if user is not None:
        if user.email == current_user.email:
            db.session.delete(user)
            db.session.commit()
            return user_schema.jsonify(user)
        else:
            return jsonify({"message": "Invalid Permission"}), 403
    else:
        return jsonify({'message': "No User Found for this email"}), 404


# ANCHOR USER LOGIN
@ users.route('/login/', methods=['POST'])
def user_login():
    try:
        auth = request.authorization
        if not auth or not auth.username or not auth.password:
            raise InputError
        user = User.query.filter_by(email=auth.username).first()
        if not user:
            raise NoUserFoundError
        if check_password_hash(user.password, auth.password):
            token = create_token(user)
            return jsonify({"token": token}), 200
        return InputError.pwd_error()
        #  return make_response('Invalid Email or Password', 401, {'WWW-Authenticate': 'Basic realm="Login required!"'})

    except NoUserFoundError:
        return NoUserFoundError.email_not_found()
    except InputError:
        return InputError.login_error()
    except Exception:
        traceback.print_exc()  # This prints the traceback to the console
        err = traceback.format_exc()
        current_app.logger.error('Failed to create Token' + err)
        return BackendError.something_failed()


# # ANCHOR LOGOUT USER
# @users.route('/logout/', methods=['GET'])
# @destroy_token
# def logout_user(current_user):
#     user = current_user
#     print(user)
#     # user.authenticated = False
#     # db.session.add(user)
#     # db.session.commit()
#     destroy_token(user)
#     return jsonify({'message': "User Logged Out Successfully."}), 200


# OAuth Config
CONF_URL = 'https://accounts.google.com/.well-known/openid-configuration'

oauth.register(
    name='google',
    server_metadata_url=CONF_URL,
    client_kwargs={
        'scope': 'openid email profile'
    }
)


# ANCHOR USER OAUTH LOGIN
@users.route('/login-oauth/', methods=["GET"])
def login():
    redirect_uri = url_for('users.auth', _external=True)
    return oauth.google.authorize_redirect(redirect_uri)


# ANCHOR REDIRECTS LOGIN TO HERE
@users.route('/authorize/', methods=["GET"])
def auth():
    token = oauth.google.authorize_access_token()
    user = oauth.google.parse_id_token(token)
    session['user'] = user

    # Performing custom operations on the user i.e. signup or login
    db_user = User.query.filter_by(email=user['email']).first()
    if db_user is None:
        if user["picture"]:
            profile_picture = user["picture"]
        else:
            profile_picture = ""
        google_user = {
            "full_name": user['name'],
            "email": user['email'],
            "profile_picture": profile_picture,
            "role": "student"
        }
        try:
            json_user = json.dumps(google_user)
            schema = oauth_schema
            # Validation with schema.load()
            oauth_user_signup = schema.load(json.loads(json_user))
            # Also Serializes the User to be entered into the database
            new_user = User(oauth_user_signup['full_name'], oauth_user_signup['email'], None,
                            None, oauth_user_signup['profile_picture'], None, oauth_user_signup['role'], None)
            db.session.add(new_user)
            db.session.commit()
            return jsonify({"user": user})

        except ValidationError as err:
            db.session.rollback()
            # => {"email": ['"foo" is not a valid email address.']}
            print(err.messages)
            print(err.valid_data)  # => {"name": "John"}

        except exc.IntegrityError:
            db.session.rollback()
            return jsonify({"message": "Duplicate Email or PhoneNumber. Please Verify!"}), 401

        except Exception:
            db.session.rollback()
            traceback.print_exc()  # This prints the traceback to the console
            err = traceback.format_exc()
            current_app.logger.error(
                'Failed to create user from oauth' + err)
            return jsonify({"message": "An Error Occured Please Try Again Later"}), 500

    else:
        return jsonify({"user": user})


# ANCHOR FORGOT PASSWORD
@users.route("/forgot-pwd/", methods=['POST'])
def forgot_password():
    url = request.host_url + 'users/reset/'
    try:
        input_data = request.form
        data = json.dumps(input_data)
        schema = forgot_pwd
        user_signup = schema.load(json.loads(data))
        email = request.form['email']
        user_data = User.query.filter_by(email=email).first()
        if user_data is None:
            raise NoUserFoundError

        expires = datetime.datetime.utcnow() + datetime.timedelta(hours=3)
        reset_token = jwt.encode({
            'id': user_data.id,
            'exp': expires
        }, current_app.config.get('SECRET_KEY'))
        text_body = render_template(
            'reset_password.txt', url=url + reset_token)
        html_body = render_template(
            'reset_password.html', url=url + reset_token)
        send_mail('[CBT-KOREAN] Reset Your Password', sender='cbt@korean.ko',
                  recipients=[user_data.email], text_body=text_body, html_body=html_body)
        return jsonify({"message": "Mail Sent Successfully. Check your email to reset your password "}), 200

    except ValidationError as err:
        current_app.logger.error('%s failed to create user')
        print(err.valid_data)  # => {"name": "John"}
        # => {"email": ['"foo" is not a valid email address.']}
        return jsonify({"error": err.messages}), 400

    except NoUserFoundError:
        return NoUserFoundError.email_not_found()


# ANCHOR RESET PASSWORD
@users.route("/reset/<reset_token>", methods=["POST"])
def reset_password(reset_token):
    url = request.host_url + 'reset/'
    # data error handling
    token_data = jwt.decode(reset_token, current_app.config.get(
        'SECRET_KEY'), algorithms="HS256")
    try:
        input_data = request.form
        data = json.dumps(input_data)
        schema = reset_pwd
        reset_user_pwd = schema.load(json.loads(data))
        password = request.form['password']
        password2 = request.form['password2']
        if password == password2:
            hashed_password = generate_password_hash(password, method='sha256')
        else:
            return jsonify({"message": "Passwords do not Match."}), 400
        user = User.query.filter_by(id=token_data['id']).first_or_404(
            description='There is no such user registered.')
        user.password = hashed_password
        db.session.commit()
        send_mail('AWESOME APP Password reset successful',
                  sender='CBT-KOREAN',
                  recipients=[user.email],
                  text_body='Password reset was successful',
                  html_body='<p>Password reset was successful</p>')
        return jsonify({"message": "Mail Sent Successfully. An email confirmation was sent. "}), 200

    except ValidationError as err:
        return jsonify({"error": err.messages}), 400

    except Exception:
        db.session.rollback()
        traceback.print_exc()  # This prints the traceback to the console
        err = traceback.format_exc()
        current_app.logger.error('Failed to edit user' + err)
        return jsonify({"message": "An Error Occured Please Try Again Later"}), 500


# ANCHOR GENERATE ACCESS TOKEN
def create_token(user):
    token = jwt.encode({
        'id': user.id,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30),
        'email': user.email,
        'role': user.role
    },  current_app.config.get('SECRET_KEY'))
    return token


# ANCHOR GENERATE ACCESS TOKEN
def destroy_token(user):
    token = jwt.encode({
        'id': user.id,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30),
        'email': user.email,
        'role': user.role
    },  current_app.config.get('SECRET_KEY'))
    return token

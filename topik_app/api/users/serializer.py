from marshmallow import fields, validate

from topik_app.extensions import ma
from topik_app.api.users.users import User


# GET User Schema
class OAUTHUserSchema(ma.Schema):
    full_name = fields.Str(required=True, validate=[
        validate.Length(min=4, max=100)])
    email = fields.Email(required=True, validate=[
        validate.Length(min=4, max=100)])
    password = fields.Str(required=False)
    phone_number = fields.Integer(required=False)
    profile_picture = fields.Str(required=False)
    date_of_birth = fields.Date(required=False)
    role = fields.Str(required=True)
    address = fields.Str(required=False)

    class Meta:
        model = User
        fields = ('id', 'full_name', 'email', 'profile_picture', 'role')


# GET User Schema
class UserSchema(ma.Schema):
    class Meta:
        fields = ('id', 'full_name', 'email', 'profile_picture', 'phone_number',
                  'date_of_birth', 'role', 'address')


# POST A NEW USER User Schema
class PostUserSchema(ma.Schema):
    full_name = fields.Str(required=True, validate=[
                           validate.Length(min=4, max=100)])
    email = fields.Email(required=True, validate=[
                         validate.Length(min=4, max=100)])
    profile_picture = fields.Str(required=False)
    phone_number = fields.Integer(required=True)
    date_of_birth = fields.Date(required=True)
    address = fields.Str(required=True)
    password = fields.Str(required=True)
    password2 = fields.Str(required=True)
    role = fields.Str(required=True)

    class Meta:
        model = User
        fields = ('full_name', 'email', 'profile_picture', 'phone_number',
                  'date_of_birth', 'address', 'password', 'password2', 'role')


# FORGOT PASSWORD User Schema
class ForgotPwdUserSchema(ma.Schema):
    email = fields.Email(required=True, validate=[
                         validate.Length(min=4, max=100)])

    class Meta:
        fields = ('email', )


# RESET PASSWORD User Schema
class ResetPwdUserSchema(ma.Schema):
    password = fields.Str(required=True, validate=[
        validate.Length(min=4, max=100)])
    password2 = fields.Str(required=True, validate=[
        validate.Length(min=4, max=100)])

    class Meta:
        fields = ('password', 'password2')


# Initialize the Schema
oauth_schema = OAUTHUserSchema()
user_schema = UserSchema()
users_schema = UserSchema(many=True)
post_schema = PostUserSchema()
forgot_pwd = ForgotPwdUserSchema()
reset_pwd = ResetPwdUserSchema()

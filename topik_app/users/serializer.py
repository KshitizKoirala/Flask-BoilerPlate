from topik_app.extensions import ma


# GET User Schema
class UserSchema(ma.Schema):
    class Meta:
        fields = ('id', 'full_name', 'email', 'profile_picture', 'phone_number',
                  'date_of_birth', 'role', 'address')


# POST User Schema
class PostUserSchema(ma.Schema):
    class Meta:
        fields = ('full_name', 'email', 'password', 'password2', 'profile_picture', 'phone_number',
                  'date_of_birth', 'role', 'address')


# Initialize the Schema
user_schema = UserSchema()
users_schema = UserSchema(many=True)
post_schema = PostUserSchema()

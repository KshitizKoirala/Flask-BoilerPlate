from enum import Enum
from topik_app.extensions import db
from sqlalchemy.orm import validates


# Defining the Enum roles
class RoleEnum(str, Enum):
    Administrator: str = "administrator"
    Teacher: str = "teacher"
    Student: str = "student"


# Users Table
class User(db.Model):
    __tablename__ = 'user_table'

    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=True)
    phone_number = db.Column(db.BigInteger, nullable=True, unique=True)
    profile_picture = db.Column(db.String(500), nullable=True)
    date_of_birth = db.Column(db.DateTime, nullable=True)
    role = db.Column(db.Enum(RoleEnum), nullable=False)
    address = db.Column(db.String(300), nullable=True)
    created_on = db.Column(db.DateTime, server_default=db.func.now())
    updated_on = db.Column(
        db.DateTime, server_default=db.func.now(), server_onupdate=db.func.now())

    def __init__(self, full_name, email, password, phone_number, profile_picture, date_of_birth, role, address):
        self.full_name = full_name
        self.email = email
        self.password = password
        self.phone_number = phone_number
        self.profile_picture = profile_picture
        self.date_of_birth = date_of_birth
        self.role = role
        self.address = address

    @validates('email')
    def convert_lower(self, key, value):
        return value.lower()

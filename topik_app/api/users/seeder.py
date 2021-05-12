import click
import traceback
from flask import Blueprint
from werkzeug.security import generate_password_hash

# Custom routes
from topik_app.api.users.users import User
from topik_app.extensions import db


seeder_bp = Blueprint('seed', __name__)


# SEEDER to Create A New User
@seeder_bp.cli.command('user')
@click.command()
def seed():
    password = generate_password_hash("testing", method='sha256')
    user = User("ADMIN ADMIN", "testing@test.test", password,
                9800000000, "", "1996-05-21", "Administrator", "Test Road")
    try:
        db.session.add(user)
        db.session.commit()
        print("User Created Successfully.")
    except Exception:
        traceback.print_exc()  # This prints the traceback to the console
        print("Cannot Run Seeder.")

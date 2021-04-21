# Flask-BoilerPlate
Flask Application with CRUD API and Login

This is a basic template with user registration and Login functionality completed with logging and authentication middleware.

TO START THE APPLICATION FIRST TIME
a. Create a virtualenv
b. Install the dependencies
  pip install -r requirements.txt
c. Configure the .env file from .env.example
d. Open Python Shell and then
    i. from topik_app import db, create_app
    ii. db.create_all(app=create_app())
  Now you can exit the shell
e. flask run

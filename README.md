# Flask Application with CRUD API, JWT Login and OAuth 2.0 Login

_This is a basic template with User Registration, Automated O-Auth Registration and JWT Login functionality with logging and authentication middleware._

** TO START THE APPLICATION FIRST TIME **

1. Create a virtualenv
2. Install the dependencies
   > pip install -r requirements.txt (for WINDOWS)
   > pip3 install -r requirements.txt (for Mac Os and Ubuntu)
3. Configure the .env file from .env.example
4. Open Python Shell and then

```
  from topik_app import db, create_app
  db.create_all(app=create_app())
```

> Now you can exit the shell

5. Now we will run the seeder using the command

   > flask seed user

6. flask run

   Use the seeder credentials

   `email=testing@test.test`
   `password=testing`
   `role=administrator`

### List OF API's

Please Be Sure To Create a New User With `role="administrator"` first and then provide the access token in header as `x-access-token=YOUR_TOKEN` for other APIs.

** GET ALL USERS**
http://127.0.0.1:5000/users/

** CREATE A USER **
http://127.0.0.1:5000/users/add/

** GET Single User**
http://127.0.0.1:5000/users/1/

** UPDATE AN EXISTING USER**
http://127.0.0.1:5000/users/edit/1/

** DELETE A USER **
`User can only be deleted by the user themselves only.`
http://127.0.0.1:5000/users/delete/55/

** USER LOGIN **

> In Authorization set the type of header as `Basic Auth` and enter the credentials
> http://127.0.0.1:5000/users/login/

** USER OAUTH GOOGLE LOGIN **

> Currently forwards token as is. If user is not registered. They are registered and then redirected.
> http://127.0.0.1:5000/users/login-oauth/

** FORGOT PASSWORD **
`USE HTTP POST for both forgot and reset link`
http://127.0.0.1:5000/users/forgot-pwd/

### Running the Tests

_Add `Test_DB_CREDENTIALS` to the env file with its `DATABASE_URI` in the topik_app/config/config.py module_

In the powershell simply type `pytest` to run the tests.

# To see the coverage html report

1. `coverage run -m pytest`
2. `coverage html --omit=*/venv/*`

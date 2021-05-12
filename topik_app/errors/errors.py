
class NoUserFoundError(Exception):
    def email_not_found():
        EmailDoesnotExistsError = {
            "message": "Couldn't find the user with given email address.",
        }
        return EmailDoesnotExistsError, 404


class InputError(Exception):

    def login_error():
        valid_credentials = {
            "message": "Please enter valid credentials.",
        }
        return valid_credentials, 400

    def pwd_error():
        wrong_pwd = {
            "message": "Invalid Email or Password",
        }
        return wrong_pwd, 401


class BackendError(Exception):
    def something_failed():
        failed_error = {
            "message": "Something failed. Please Try Again Later."
        }
        return failed_error, 500

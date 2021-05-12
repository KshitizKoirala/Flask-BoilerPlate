import pytest


# Core Library modules
import ast
from base64 import b64encode

# Import our application
from tests.client import client
from topik_app.api.users.routes import create_token


class TestUser:
    data = {
        "full_name": "Test Subject",
        "email": "testing@gmail.com",
        "password": "testing",
        "password2": "testing",
        "phone_number": 9860000011,
        "date_of_birth": "1995-03-02",
        "address": "testng Street",
        "role": "administrator"
    }

    def test_SignUp(self, client, session):
        route = "/users/add/"
        data = self.data
        accept_header = 'multipart/form-data;'
        headers = {
            'Content-Type': accept_header,
        }
        rv = client.post(route, data=data, headers=headers)
        result = ast.literal_eval(rv.data.decode('utf-8'))
        assert result["email"] == "testing@gmail.com"

    def test_get_all_users(self, client, session, mock_user_object):
        route = "/users/"
        user = mock_user_object
        setattr(user, 'id', 2)
        token = create_token(user)
        headers = {
            'x-access-token': '{}'.format(token)
        }
        rv = client.get(route, headers=headers)
        result = ast.literal_eval(rv.data.decode('utf-8'))
        assert rv.status_code == 200
        assert result[0]["email"] == "testing@gmail.com"


class TestLogin:
    route = "/users/login/"

    def test_invalid_input(self, client, session):
        route = self.route
        credentials = b64encode(
            b"testing@gmail.com:").decode("utf-8")
        rv = client.post(
            route, headers={"Authorization": "Basic " + credentials})
        assert rv.status_code == 400

    def test_user_error(self, client, session):
        route = self.route
        credentials = b64encode(
            b"testingg@gmail.com@gmail.com:testing").decode("utf-8")
        rv = client.post(
            route, headers={"Authorization": "Basic " + credentials})
        result = ast.literal_eval(rv.data.decode('utf-8'))
        assert rv.status_code == 404
        assert result["message"] == "Couldn\'t find the user with given email address."

    def test_incorrect_pwd(self, client, session):
        route = self.route
        credentials = b64encode(
            b"testing@gmail.com:testiing").decode("utf-8")
        rv = client.post(
            route, headers={"Authorization": "Basic " + credentials})
        assert rv.status_code == 401

    def test_login_token(self, client, session):
        route = self.route
        credentials = b64encode(
            b"testing@gmail.com:testing").decode("utf-8")
        rv = client.post(
            route, headers={"Authorization": "Basic " + credentials})
        result = ast.literal_eval(rv.data.decode('utf-8'))
        assert rv.status_code == 200

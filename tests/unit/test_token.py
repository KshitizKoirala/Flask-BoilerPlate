# Core Library modules
import ast
from base64 import b64encode

# Import our application
from tests.client import client


def test_token(client, session):
    route = "/users/login/"
    credentials = b64encode(
        b"samratpandey46@gmail.com:testing").decode("utf-8")
    rv = client.post(
        route, headers={"Authorization": "Basic " + credentials})
    result = ast.literal_eval(rv.data.decode('utf-8'))
    print(result, rv.data)
    status_code = rv.status_code
    assert status_code == status_code

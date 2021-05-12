import pytest

from topik_app.api.users.users import User


@pytest.fixture
def mock_user_object():
    user = User(
        full_name="Mock User",
        email="testing@gmail.com",
        password="testing",
        phone_number=9800000000,
        profile_picture="",
        date_of_birth="1996-05-21",
        role="administrator",
        address="testng Street"
    )
    return user

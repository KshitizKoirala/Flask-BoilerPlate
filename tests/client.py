import pytest

# PyTest Configuration
from tests.conftest import app
from tests.conftest import _db


@pytest.fixture(scope='session')
def client(app):
    with app.test_client() as client:
        with app.app_context():
            _db.init_app(app)
        yield client

import pytest

from topik_app import create_app
from topik_app.config.config import TestingConfig
from topik_app.extensions import db as _db

from topik_app.api.users.users import User


@pytest.fixture(scope="session")
def app(request):
    """Test session-wide test `Flask` application."""
    app = create_app(TestingConfig)
    app.testing = True
    app.config['TESTING'] = True
    return app


@pytest.fixture(autouse=True)
def _setup_app_context_for_test(request, app):
    """
    Given app is session-wide, sets up a app context per test to ensure that
    app and request stack is not shared between tests.
    """
    ctx = app.app_context()
    ctx.push()
    yield  # tests will run here
    ctx.pop()


@pytest.fixture(scope="session")
def db(app, request):
    """Returns session-wide initialized database"""
    with app.app_context():
        _db.create_all()
        yield _db
        _db.drop_all()


@pytest.fixture(scope='function')
def session(db, request):
    """Creates a new database session for a test."""
    # connect to the database
    connection = db.engine.connect()

    # # begin a non-ORM transaction
    # transaction = connection.begin()

    # bind an individual session to the connection
    options = dict(bind=connection, binds={})
    session = db.create_scoped_session(options=options)

    # overload the default session with the session above
    db.session = session

    # yield session

    def teardown():
        session.close()
        # rollback - everything that happened with the
        # session above (including calls to commit())
        # is rolled back.
        # transaction.rollback()
        # return connection to the Engine
        connection.close()
        session.remove()

    request.addfinalizer(teardown)
    return session


@pytest.fixture
def mock_user():
    user = User(
        id="my_mock_id",
        full_name="Test Subject",
        email="testing@gmail.com",
        password="testing",
        phone_number=9860000011,
        date_of_birth="1995-03-02",
        address="lokanthalii",
        role="administrator"
    )
    return user

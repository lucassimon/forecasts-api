import pytest

# Third


# Apps
from apps import create_app
from apps.db import db


@pytest.fixture(scope='session')
def test_client():
    flask_app = create_app(testing=True)

    # Flask provides a way to test your application by exposing the Werkzeug test Client
    # and handling the context locals for you.
    testing_client = flask_app.test_client()

    # Establish an application context before running the tests.
    ctx = flask_app.app_context()
    ctx.push()

    yield testing_client  # this is where the testing happens!

    ctx.pop()


@pytest.fixture(scope='function')
def mongo(request):
    db.connection.drop_database('forecasts_test')

    def fin():
        db.connection.close()

        print('\n[teardown] db finalizer, disconnect from db')

    request.addfinalizer(fin)

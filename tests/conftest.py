import flask.testing
import pytest

import notes


@pytest.fixture(scope='session')
def app() -> flask.Flask:
    """Creates a Flask app object instance.

    :return: the app instance.
    """
    return notes.app


@pytest.fixture()
def client(app: flask.Flask) -> flask.testing.FlaskClient:
    """Creates a Flask testing client.

    :param app: Flask application object instance.
    :return: the testing client.
    """
    return app.test_client()

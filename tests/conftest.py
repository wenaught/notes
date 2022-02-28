import datetime
import os

import flask.testing
import pytest
import _pytest.fixtures
import yaml

import notes
from notes import Note

data_file_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "data/notes.yaml")
test_data = yaml.safe_load(open(data_file_path, 'r'))
endpoint = '/notes'


@pytest.fixture()
def app() -> flask.Flask:
    """Create a Flask app object instance. Drops the MongoDB database used for testing.

    :return: the app instance.
    """
    yield notes.create_app('test.yaml')
    notes.mongo.cx.drop_database(os.environ["MONGO_URI"].split('/')[-1])

@pytest.fixture()
def fill_notes(request: _pytest.fixtures.SubRequest, app: flask.Flask) -> list[dict]:
    """Fill database with Note documents.

    :param request: pytest Request object instance.
    :param app: Flask application object instance.
    :return: list of
    """
    contents = request.param['contents']
    for note in contents:
        Note(**note).commit()
    return contents

@pytest.fixture()
def client(app: flask.Flask) -> flask.testing.FlaskClient:
    """Create a Flask testing client.

    :param app: Flask application object instance.
    :return: the testing client.
    """
    return app.test_client()

import os

import flask.testing
import pytest
import _pytest.fixtures, _pytest.monkeypatch
import yaml
from mongomock.mongo_client import MongoClient

import notes
from notes.note.models import Note

data_file_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "data/notes.yaml")
test_data = yaml.safe_load(open(data_file_path, 'r'))
endpoint = '/note'


class PyMongoMock(MongoClient):
    def init_app(self, app):
        return super().__init__()


@pytest.fixture()
def app(monkeypatch: _pytest.monkeypatch) -> flask.Flask:
    """Create a Flask app object instance. Drops the MongoDB database used for testing.

    :param monkeypatch: a pytest monkeypatch fixture.
    :return: the app instance.
    """
    if os.getenv('MOCK_MONGO'):
        monkeypatch.setattr(notes, 'mongo', PyMongoMock())
    yield notes.create_app('test.yaml')
    if not os.getenv('MOCK_MONGO'):
        notes.mongo.cx.drop_database(os.environ["MONGO_URI"].split('/')[-1])

@pytest.fixture()
def fill_notes(request: _pytest.fixtures.SubRequest, app: flask.Flask) -> list[dict]:
    """Fill database with Note documents.

    :param request: pytest Request object instance.
    :param app: Flask application object instance.
    :return: list of dicts corresponding to created Note documents.
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

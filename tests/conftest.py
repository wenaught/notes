import os

import flask.testing
import pytest
import yaml

import notes

data_file_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "data/notes.yaml")
test_data = yaml.safe_load(open(data_file_path, 'r'))


@pytest.fixture()
def app() -> flask.Flask:
    """Create a Flask app object instance. Drops the MongoDB database used for testing.

    :return: the app instance.
    """
    yield notes.create_app()
    notes.mongo.cx.drop_database(os.environ["MONGO_URI"].split('/')[-1])


@pytest.fixture()
def client(app: flask.Flask) -> flask.testing.FlaskClient:
    """Create a Flask testing client.

    :param app: Flask application object instance.
    :return: the testing client.
    """
    return app.test_client()

import datetime
import logging
import os

import pytest
import yaml
from apiflask.schemas import EmptySchema
from marshmallow import Schema
from marshmallow.fields import String, Dict, List
from mongomock.mongo_client import MongoClient

import notes
from notes.note.model import OutNoteSchema, Note
from notes.user.model import OutUserSchema, User, InUserSchema

logger = logging.getLogger(__name__)

schemas = {
    'user_out': OutUserSchema(),
    'note_out': OutNoteSchema(),
    'many_note_out': OutNoteSchema(many=True),
    'empty': EmptySchema(),
    'verification_failed': Schema.from_dict({"message": String(),
                                             "detail": Dict(keys=String,
                                                            values=Dict(keys=String,
                                                                        values=List(String)))})(),
    'http_error': Schema.from_dict({"message": String(),
                                    "detail": Dict()})()
}

data_file_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "test_data.yml")
test_data = yaml.safe_load(open(data_file_path, "r"))


class PyMongoMock(MongoClient):
    def init_app(self, app):
        return super().__init__()


@pytest.fixture()
def app(monkeypatch):
    if os.getenv("MOCK_MONGO"):
        monkeypatch.setattr(notes, "mongo", PyMongoMock())
    yield notes.create_app("test.yaml")
    if not os.getenv("MOCK_MONGO"):
        notes.mongo.cx.drop_database(os.environ["MONGO_URI"].split("/")[-1])


@pytest.fixture()
def client(app):
    return app.test_client()


@pytest.fixture()
def default_user(app, request):
    if not request.param:
        return
    user_data = test_data["users"]["user_valid_all"]
    with app.app_context():
        logger.info("creating default user in database")
        user = User(**InUserSchema().load(user_data))
        user.commit()
        return OutUserSchema().dump(user)


@pytest.fixture()
def default_note(app, request, default_user):
    if not request.param:
        return
    note_data = test_data["notes"]["note_valid_all"]
    with app.app_context():
        logger.info("creating default note in database")
        note = Note(**note_data)
        note.added_timestamp = note.modified_timestamp = datetime.datetime.now()
        note.username = default_user["username"]
        note.commit()
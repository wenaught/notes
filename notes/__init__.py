"""Notes is a note-taking API."""
import os

from apiflask import APIFlask
from flask_pymongo import PyMongo

from notes.models import Note, instance

mongo: PyMongo = PyMongo()


def create_app() -> APIFlask:
    """Create an application instance.
    Requires an environment variable MONGO_URI to be set.

    :return: a Flask app.
    """
    app = APIFlask(__name__, instance_relative_config=True, title='Notes API')
    app.config['DESCRIPTION'] = __doc__
    mongo_uri = os.getenv("MONGO_URI")
    assert mongo_uri, "MONGO_URI was not set!"
    app.config['MONGO_URI'] = mongo_uri
    mongo.init_app(app)
    instance.set_db(mongo.db)
    Note.ensure_indexes()

    from notes.api import blueprint
    app.register_blueprint(blueprint)

    return app

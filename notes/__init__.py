"""Notes is a note-taking API."""
import os

import yaml
from apiflask import APIFlask
from flask import redirect
from flask_cors import CORS
from flask_pymongo import PyMongo

mongo: PyMongo = PyMongo()


def create_app(config_file_name: str, version: str = "development") -> APIFlask:
    """Create an application instance.
    Requires an environment variable MONGO_URI to be set.

    :param config_file_name: name of the configuration file in Flask's instance folder.
    :param version: app version to display in OpenAPI docs.
    :return: a Flask app.
    """
    app = APIFlask(__name__, instance_relative_config=True, title="Notes API", version=version)

    @app.route("/")
    @app.doc(hide=True)
    def docs():
        """Automatically redirect from index page to Swagger UI."""
        return redirect("docs", code=302)

    app.config.from_file(config_file_name, yaml.safe_load)
    CORS(app)

    mongo_uri = os.getenv("MONGO_URI")
    assert mongo_uri, "MONGO_URI was not set!"
    app.config["MONGO_URI"] = mongo_uri
    mongo.init_app(app)

    from notes.user.blueprint import user_blueprint
    from notes.user.model import user_umongo_instance, User
    user_umongo_instance.set_db(mongo.db)
    User.ensure_indexes()
    app.register_blueprint(user_blueprint)

    from notes.note.blueprint import note_blueprint
    from notes.note.model import note_umongo_instance, Note
    note_umongo_instance.set_db(mongo.db)
    Note.ensure_indexes()
    app.register_blueprint(note_blueprint)

    return app

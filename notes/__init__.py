from flask import Flask

app = Flask(__name__)


@app.route("/")
def hello_world() -> dict[str]:
    """Placeholder "Hello World" route.

    :return: a "Hello World" JSON document.
    """
    return {"hello": "world"}

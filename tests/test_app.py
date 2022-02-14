import flask.testing


def test_root(app: flask.Flask, client: flask.testing.FlaskClient) -> None:
    """Tests the '/' route of the app.

    :param app: Flask application object instance.
    :param client: Flask testing client.
    """
    with app.test_request_context('/'):
        assert flask.request.path == '/'
        assert flask.request.method == 'GET'
    response = client.get('/')
    assert response.json == {'hello': 'world'}

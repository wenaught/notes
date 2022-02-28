import pytest

from .conftest import test_data, endpoint


def test_get_docs(client):
    response = client.get('/docs')
    assert response.status_code == 200, f"/docs endpoint responded with unexpected code: {response.status_code}."
    assert "text/html" in response.content_type,\
        f"/docs endpoint responded with invalid content type: {response.content_type}."


@pytest.mark.parametrize("fill_notes", test_data['get'], indirect=True, ids=[data['id'] for data in test_data['get']])
def test_get_notes(fill_notes, client):
    for note in fill_notes:
        response = client.get(f"{endpoint}/{note['title']}")
        assert response.status_code == 200
        assert isinstance(response.json, dict)
        assert note == response.json


@pytest.mark.parametrize("fill_notes", test_data['get_all'], indirect=True, ids=[data['id'] for data in test_data['get_all']])
def test_get_all_notes(fill_notes, client):
    response = client.get(endpoint)
    assert response.status_code == 200
    assert isinstance(response.json, list)
    assert fill_notes == response.json


@pytest.mark.parametrize("post_test_data", test_data['post'], ids=[data['id'] for data in test_data['post']])
def test_post_note(client, post_test_data) -> None:
    for content in post_test_data['contents']:
        response = client.post(endpoint, json=content)
        assert response.json.get("title") == content["title"], \
            f"POST response didn't contain expected 'title' value: {response.json}"
        assert response.json.get("text") == content["text"], \
            f"POST response didn't contain expected 'text' value: {response.json}"
        assert all([
            "added_timestamp" in response.json,
            "modified_timestamp" in response.json,
            response.json.get("added_timestamp") == response.json.get("modified_timestamp")
        ]), f"POST response didn't contain expected timestamps: {response.json}"


@pytest.mark.parametrize("get_test_data", test_data['get_posted'], ids=[data['id'] for data in test_data['get_posted']])
def test_get_posted_notes(client, get_test_data) -> None:
    for content in get_test_data['contents']:
        post_response = client.post(endpoint, json=content)
        get_response = client.get(f'{endpoint}/{content["title"]}')
        assert get_response.json == post_response.json, \
            f"GET response didn't match POST response: {get_response.json}, {post_response.json}"


@pytest.mark.parametrize("get_all_test_data", test_data['get_all_posted'], ids=[data['id'] for data in test_data['get_all_posted']])
def test_get_all_posted_notes(client, get_all_test_data):
    expected_list = []
    for content in get_all_test_data['contents']:
        response = client.post(endpoint, json=content)
        assert response.status_code == 201, f"POST request to '/notes' with body {content} was unsuccessful."
        expected_list.append(response.json)
    actual_list = client.get(endpoint).json
    assert sorted(expected_list, key=lambda item: item['title']) == \
           sorted(actual_list, key=lambda item: item['title']), \
        f"GET response to get all notes didn't match expected response: {expected_list}, {actual_list}"
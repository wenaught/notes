import pytest

from .conftest import test_data


@pytest.mark.parametrize("post_test_data", test_data['post'], ids=[data['id'] for data in test_data['post']])
def test_post_note(client, post_test_data) -> None:
    for content in post_test_data['contents']:
        response = client.post('/notes', json=content)
        assert response.json.get("name") == content["name"], \
            f"POST response didn't contain expected 'name' value: {response.json}"
        assert response.json.get("text") == content["text"], \
            f"POST response didn't contain expected 'text' value: {response.json}"
        assert all([
            "added_timestamp" in response.json,
            "modified_timestamp" in response.json,
            response.json.get("added_timestamp") == response.json.get("modified_timestamp")
        ]), f"POST response didn't contain expected timestamps: {response.json}"


@pytest.mark.parametrize("get_test_data", test_data['get'], ids=[data['id'] for data in test_data['get']])
def test_get_note(client, get_test_data) -> None:
    for content in get_test_data['contents']:
        post_response = client.post('/notes', json=content)
        get_response = client.get(f'/notes/{content["name"]}')
        assert get_response.json == post_response.json, \
            f"GET response didn't match POST response: {get_response.json}, {post_response.json}"


@pytest.mark.parametrize("get_all_test_data", test_data['get_all'], ids=[data['id'] for data in test_data['get_all']])
def test_get_all_notes(client, get_all_test_data):
    expected_list = []
    for content in get_all_test_data['contents']:
        expected_list.append(client.post('/notes', json=content).json)
    actual_list = client.get('/notes').json
    assert sorted(expected_list, key=lambda item: item['name']) == \
           sorted(actual_list, key=lambda item: item['name']), \
        f"GET response to get all notes didn't match expected response: {expected_list}, {actual_list}"

import logging

import pytest
from marshmallow import ValidationError

from .conftest import test_data, schemas

logger = logging.getLogger(__name__)

@pytest.mark.parametrize("test_case,default_user,default_note",
                         zip(test_data["test_cases"],
                             [case.get('default_user') for case in test_data["test_cases"]],
                             [case.get('default_note') for case in test_data["test_cases"]]),
                         ids=[case["id"] for case in test_data["test_cases"]],
                         indirect=["default_user", "default_note"])
def test_app(client, test_case, default_user, default_note):
    headers = {}
    if default_user and not test_case.get("no_default_token"):
        headers["Authorization"] = f"Bearer {default_user['token']}"
    for request in test_case['requests']:
        logger.info(request['method'] + ' request to ' + request['endpoint'])
        response = getattr(client, request['method'])(request['endpoint'],
                                                      json=request.get('data'),
                                                      query_string=request.get('query'),
                                                      headers=headers)
        assert response.status_code == request['code'], "Unexpected status code"
        if request.get('response_schema'):
            try:
                schemas[request['response_schema']].load(response.json)
            except ValidationError:
                raise AssertionError(f"Response didn't conform to expected schema. Response: {response.data}")
        if request.get('keep_token'):
            logger.info('saved token for further requests')
            headers["Authorization"] = f"Bearer {response.json['token']}"
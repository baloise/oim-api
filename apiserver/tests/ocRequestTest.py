import flask_unittest
from app import create_flask_app
from unittest import mock

# This method will be used by the mock to replace requests.get
def mocked_requests_get(*args, **kwargs):
    class MockResponse:
        def __init__(self, json_data, status_code):
            self.json_data = json_data
            self.status_code = status_code

        def json(self):
            return self.json_data

    if args[0] == 'https://unittests.oc.mock/api/token':
        return_obj = {
            'token_type': 'bearer',
            'access_token': 'MOCK123roflcopter',
            'expires_in': 3600
        }
        return MockResponse(json_data=return_obj, status_code=200)
    elif args[0] == 'http://someotherurl.com/anothertest.json':
        return MockResponse({"key2": "value2"}, 200)

    print('Uncaught URL sent to mock get: {}'.format(str(args[0])))
    return MockResponse(None, 404)


class oimApiTests(flask_unittest.ClientTestCase):
    url_base = '/auth/v1.0'
    app = create_flask_app(config_name='unittests')  # Required by the parent class

    @mock.patch('requests.get', side_effect=mocked_requests_get)
    def test_1_get_token(self, client, blubb):
        response = client.get(self.url_base + '/test/gettoken')
        self.assertEqual(response.status_code, 200)
        self.assertIn('text/plain', response.content_type)
        self.assertGreater(len(response.data), 0, 'Response too small')
        self.assertInResponse(b'MOCK123roflcopter', response)
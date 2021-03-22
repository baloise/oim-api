import unittest
import flask_unittest
from app import create_flask_app
import re
from unittest import mock
from dotenv import load_dotenv
from tests.model_orders import TestModelOrder  # noqa: F401
from tests.model_statuspayload import TestModelStatuspayload


# Force overwrite envvars with mock values from .env.unittests
load_dotenv(dotenv_path='.env.unittests', override=True)


class DemoTests(flask_unittest.ClientTestCase):
    url_base = '/v1.0'
    app = create_flask_app(config_name='unittests')  # Required by the parent class

    def test_1_hello(self, client):
        response = client.get(self.url_base + '/hello')
        self.assertEqual(response.status_code, 200)
        self.assertIn('text/plain', response.content_type)
        self.assertInResponse(b'Hello World', response)

    def test_2_greet(self, client):
        response = client.get(self.url_base + '/greeting/Peter')
        self.assertStatus(response, 200)
        self.assertInResponse(b'Hello Peter!', response)

    def test_3_increment(self, client):
        url = self.url_base + '/persistance'
        regex = re.compile(b'^[0-9]+$')

        res1 = client.get(url)
        self.assertStatus(res1, 200)
        # Theoretically we could use str.isnumeric() but since regex are more interesting for a demo...
        self.assertRegex(res1.data, regex, 'First response is not a number')
        num1 = int(res1.data)

        res2 = client.get(url)
        self.assertStatus(res2, 200)
        self.assertRegex(res2.data, regex, 'Second response is not a number')
        num2 = int(res2.data)

        self.assertGreater(num2, num1)


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


class oimTests(flask_unittest.ClientTestCase):
    url_base = '/oim/v0.2'
    app = create_flask_app(config_name='unittests')  # Required by the parent class

    @mock.patch('requests.get', side_effect=mocked_requests_get)
    def test_1_get_token(self, client, blubb):
        response = client.get(self.url_base + '/test/gettoken')
        self.assertEqual(response.status_code, 200)
        self.assertIn('text/plain', response.content_type)
        self.assertGreater(len(response.data), 0, 'Response too small')
        self.assertInResponse(b'MOCK123roflcopter', response)


test_model_order = TestModelOrder()

test_model_status_payload = TestModelStatuspayload()

if __name__ == '__main__':
    unittest.main()

import flask_unittest
from app import app
import re


class DemoTests(flask_unittest.ClientTestCase):
    url_base = '/v1.0'
    app = app.app  # The flask webapp is a sub-object to the app object. We save a reference to it for quicker access

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


if __name__ == '__main__':
    flask_unittest.main()

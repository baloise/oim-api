import flask_unittest
from app import app


class DemoTests(flask_unittest.ClientTestCase):
    url_base = '/v1.0'
    app = app.app  # The flask webapp is a sub-object to the app object. We save a reference to it for quicker access

    def test_1_hello(self, client):
        response = client.get(self.url_base + '/hello')
        self.assertEqual(response.status_code, 200)
        self.assertIn('text/plain', response.content_type)
        self.assertInResponse(b'Hello World', response)


if __name__ == '__main__':
    flask_unittest.main()

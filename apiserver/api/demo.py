# This file only contains random hello-world-grade functions so
# that the demo api endpoints actually do something.
from connexion.exceptions import OAuthProblem, OAuthScopeProblem
from connexion.decorators.security import validate_scope


def hello_world():
    return 'Hello World'


def post_greeting(name: str) -> str:
    return 'Hello {name}!'.format(name=name)


def post_teamgreeting(name):
    return 'Team member: {name}'.format(name=name)


def add_order(body):
    return 'Order has be received: {}'.format(body), 201


class PersistanceDemo(object):
    count = 0

    def increase(self):
        self.count += 1

    def showcount(self):
        return self.count


# Create an instance of this class that lives within the memory of the app
persistance_demo = PersistanceDemo()


def persistance_get():
    # Method called by the api endpoint. See the .yaml files in
    # the openapi/ folder
    persistance_demo.increase()
    return persistance_demo.showcount()


########
# Below are the functions that show the auth possibilities

TOKEN_DB = {
    'asdf1234567890': {
        'uid': 100
    }
}


def apikey_auth(token, required_scopes):
    # This function is called to validate api_keys, see openapi/demoapi.yaml
    info = TOKEN_DB.get(token, None)

    if not info:
        raise OAuthProblem('Invalid token')

    return info


def basic_auth(username, password, required_scopes=None):
    if username == 'admin' and password == 'secret':
        info = {'sub': 'admin', 'scope': 'secrets'}
    elif username == 'foo' and password == 'bar':
        info = {'sub': 'user1', 'scope': ''}
    else:
        # optional: raise exception for custom error response
        return None

    # optional
    if required_scopes is not None and not validate_scope(required_scopes, info['scope']):
        raise OAuthScopeProblem(
                description='Provided user doesn\'t have the required access rights',
                required_scopes=required_scopes,
                token_scopes=info['scope']
            )

    return info


def get_secret(user) -> str:
    return "You are {user} and the secret is 'wbevuec'".format(user=user)


def get_secret_basicauth(user) -> str:
    return "You are {user} and the secret is 'wbevuec'".format(user=user)

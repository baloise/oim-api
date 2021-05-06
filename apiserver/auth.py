import os
import secrets
import time
import connexion
from connexion.exceptions import Unauthorized, BadRequestProblem
# from connexion.decorators.security import validate_scope
# from connexion.exceptions import OAuthScopeProblem, OAuthProblem
from werkzeug.exceptions import InternalServerError
from oim_logging import get_oim_logger


DEFAULT_TOKEN_LIFETIME = 3600

# This is an absolutely minimal token storage.
# TODO: Replace with DB (and cache)
TOKEN_STORE = {}


def util_get_token_info(query_token):
    global TOKEN_STORE
    return TOKEN_STORE.get(query_token, None)


def util_validate_token(query_token):
    log = get_oim_logger()
    global TOKEN_STORE

    query_token = str(query_token)
    log.debug('Validating token "{token}"'.format(token=query_token))

    check_result = TOKEN_STORE.get(query_token, None)
    if check_result:
        expiry = check_result.get('expiry', 0)
        if expiry > int(time.time()):
            log.debug('Valid token found.')
            return True
        else:
            log.info('Expired token used. Rejecting')
            return False

    log.info('Unknown token. Rejecting')
    return False


def util_create_token(scope='', owner=''):
    global TOKEN_STORE  # Ensure that we're working with the global namespace instance

    token_lifetime = int(os.getenv('TOKEN_LIFETIME', DEFAULT_TOKEN_LIFETIME))

    while True:
        proposed_token = secrets.token_urlsafe()

        if not util_validate_token(proposed_token):
            break  # unused token found

    create_timestamp = int(time.time())

    token_info = {
        'scope': scope,
        'created': create_timestamp,
        'expiry': create_timestamp + token_lifetime,
        'owner': owner,
    }

    TOKEN_STORE[proposed_token] = token_info

    return proposed_token


# This function is used by x-bearerInfoProc to validate tokens
def bearer_auth(token):
    log = get_oim_logger()
    log.debug('Validating token: {tok}'.format(tok=str(token)))
    validation_result = util_validate_token(query_token=token)
    if not validation_result:
        raise Unauthorized
    else:
        return util_get_token_info(token)


def check_ldap_creds(username, password):
    return True  # TODO: Implement LDAP


# This function is used to verity username and password
def basic_auth(username, password, required_scopes=None):
    # In debug and Test scenarios, allow auth skip with known params
    if os.getenv('DEBUG_SKIP_AUTH', '').lower() == 'true':
        if username == 'skip' and password == 'auth':
            return {'sub': 'skip', 'scope': ''}

    ldap_creds = check_ldap_creds(username, password)
    if ldap_creds:
        return {
            'sub': username,
            'scope': '',  # Dummy, TODO: Implement scope mapping from LDAP
            }

    return None  # Auth failed


# This function is triggered by the /token POST from the API
def token_post():
    log = get_oim_logger()

    form_body = connexion.request.form
    grant_type = form_body.get('grant_type', None)
    username = form_body.get('username', None)
    password = form_body.get('password', None)
    scope = form_body.get('scope', '')

    if not grant_type or not username or not password:
        # return 'Bad request', 400
        raise BadRequestProblem(detail='Missing one or more required inputs.')

    if not grant_type.lower() == 'password':
        log.error("Unsupported grant_type requested: {gt}".format(gt=grant_type))
        raise BadRequestProblem(detail='The only supported grant_type is currently "password".')

    # Validate credentials
    validation_results = basic_auth(username=username, password=password, required_scopes=scope)
    if not validation_results:
        raise Unauthorized

    created_token = util_create_token(owner=username)
    token_info = util_get_token_info(created_token)

    expires_in = int(token_info['expiry'] - time.time())

    if not created_token:
        log.error('Error creating a token for user {user}'.format(user=str(username)))
        raise InternalServerError

    return {
        'access_token': created_token,
        'token_type': 'bearer',  # only this type is supported at this time
        'expires_in':  expires_in,
    }

import os
import secrets
import time
import connexion
import sys
from distutils.util import strtobool
from connexion.exceptions import BadRequestProblem, OAuthProblem
# from connexion.decorators.security import validate_scope
# from connexion.exceptions import OAuthScopeProblem, OAuthProblem
from werkzeug.exceptions import InternalServerError
from oim_logging import get_oim_logger
import ldap3
from ldap3.core.exceptions import LDAPException
from ldap3.utils.dn import escape_rdn
from string import Template


DEFAULT_TOKEN_LIFETIME = 3600

SCOPE_MAP = {
    'subtree': ldap3.SUBTREE,
    'base': ldap3.BASE,
    'level': ldap3.LEVEL,
}

# This is an absolutely minimal token storage.
# TODO: Replace with DB (and cache)
TOKEN_STORE = {}


def map_scope(text, default=ldap3.SUBTREE):
    return SCOPE_MAP.get(str(text).lower(), default)


def need_missing_var(varname):
    log = get_oim_logger()
    log.critical('Envvar {varname} not set. Aborting execution!'.format(varname=str(varname)))
    sys.exit(3)


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
        raise OAuthProblem('Invalid token')
    else:
        return util_get_token_info(token)


def util_count_ldap_response_entries(response):
    if not response:
        return 0

    count = 0
    for entry in response:
        try:
            if entry.get('type', '') == 'searchResRef':
                count += 1
        except Exception:
            continue

    return count


def check_ldap_creds(username, password):
    log = get_oim_logger()

    untrusted_username = username
    username = escape_rdn(untrusted_username)  # as per ldap3 docs, usernames from untrusted sources must be escaped
    log.debug('Escaped username "{before}" to "{after}"'.format(before=untrusted_username, after=username))

    if username == '':  # Empty usernames are a no-go
        return False

    ldap_host = os.getenv('LDAP_HOST') or need_missing_var('LDAP_HOST')
    ldap_port = int(os.getenv('LDAP_PORT', '389'))
    ldap_usessl = os.getenv('LDAP_USESSL', 'false')
    ldap_usessl = bool(strtobool(ldap_usessl))
    ldap_base = os.getenv('LDAP_BASE') or need_missing_var('LDAP_BASE')
    ldap_login = escape_rdn(os.getenv('LDAP_LOGIN'))
    ldap_password = os.getenv('LDAP_PASSWORD', '')
    ldap_permitted_group = os.getenv('LDAP_PERMITTED_GROUP') or need_missing_var('LDAP_PERMITTED_GROUP')
    ldap_scope_user = os.getenv('LDAP_SCOPE_USER', 'SUBTREE')
    def_tpl = '(&(objectclass=user)(|(cn=$user)(samaccountname=$user)(mail=$user))(memberOf=$group))'
    ldap_filter_user_tpl = os.getenv('LDAP_FILTER_USER', def_tpl)
    ldap_username_attribs = os.getenv('LDAP_USERNAME_ATTRIBS', 'cn,samaccountname,mail')
    username_attribs = ldap_username_attribs.lower().split(',')
    # Fill in the templates
    try:
        ldap_filter_user_tpl = Template(ldap_filter_user_tpl)
        ldap_filter_user = ldap_filter_user_tpl.safe_substitute(user=username, group=ldap_permitted_group)
    except ValueError as exc:
        log.critical('Error parsing the ldap filter templates. Make sure to escape properly!', exc_info=exc)
        return False

    try:
        server = ldap3.Server(
            host=ldap_host,
            port=ldap_port,
            use_ssl=ldap_usessl,
            get_info=ldap3.ALL
        )
        conn = ldap3.Connection(
            server=server,
            user=ldap_login,
            password=ldap_password,
            client_strategy=ldap3.SAFE_SYNC,  # default is not threadsafe
            auto_bind=True,
            auto_range=True,
            read_only=True
        )
    except LDAPException as exc:
        log.error('Error connecting to LDAP.', exc_info=exc)
        return False

    log.debug('LDAP connection successful')

    ######
    # STEP: Search for requesting login user, including group membership
    status, result, response, _ = conn.search(
        search_base=ldap_base,
        search_filter=ldap_filter_user,
        search_scope=map_scope(ldap_scope_user),
        attributes=ldap3.ALL_ATTRIBUTES,  # TODO: Reduce this to the needed attribs only
    )

    if util_count_ldap_response_entries(response=response) < 1:
        log.info('LDAP search did not yield any satisfying results')
        if conn:
            conn.unbind()
        return False

    # Verify that the correct user was found by the ldap query
    user_found = False
    for entry in response:
        attribs = entry.get('attributes', {})
        for current_attrib in username_attribs:
            if attribs.get(current_attrib, '') == username:
                user_found = True
                break  # Stop looping thru attribs
        if user_found:
            break  # Stop looping thru entries

    if not user_found:
        log.debug('Could not locate use in full LDAP response... Did the LDAP search lie to us?!')
        if conn:
            conn.unbind()
        return False

    #####
    # STEP Verify credentials by trying a re-bind
    try:
        if not conn.rebind(user=username, password=password):
            log.info('Invalid credentials supplied.')
            if conn:
                conn.unbind()
            return False
    except LDAPException:
        log.exception('LDAP Exception, cannot verify login.')
        if conn:
            conn.unbind()
        return False
    #####
    # END
    # If we reached this point, we checked the user existance, group membership and password.
    if conn:
        conn.unbind()

    return True


# This function is used to verify username and password
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
        log.debug('Call to basic_auth returned false, outputting invalid_grant')
        # raise Unauthorized
        return {'error': 'invalid_grant'}, 400
    log.debug('Call to basic_auth returned positive, creating token....')

    created_token = util_create_token(owner=username)
    token_info = util_get_token_info(created_token)

    expires_in = int(token_info['expiry'] - time.time())

    if not created_token:
        log.error('Error creating a token for user {user}'.format(user=str(username)))
        raise InternalServerError

    log.debug('Token created, outputting.')
    return {
        'access_token': created_token,
        'token_type': 'bearer',  # only this type is supported at this time
        'expires_in':  expires_in,
    }

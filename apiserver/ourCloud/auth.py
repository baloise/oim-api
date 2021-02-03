import requests
from time import time
from urllib.parse import quote
from diskcache import Cache


class TokenAuthHandler(object):
    def __init__(self, parent, expiration_safety=60, url_suffix='/token'):
        if not parent:
            raise ValueError("No parent object given")
        parent.auth = self  # We add ourselves into the parent object
        self.parent = parent  # For future use we add a reference to our parent object
        self._cache = Cache()  # Create a cache instance for ourselves
        # Initialize internal variables
        self._token = ''
        self._expirytime = 0
        self._url_suffix_token = url_suffix
        self._base_url = parent.get_base_url()
        # Safety timespan in seconds to reduce expiry time by
        self._expiration_safety = expiration_safety

    def tokenIsExpired(self):
        if not self._expirytime:
            return True
        if self._expirytime > int(time()):
            return False
        else:
            return True

    def getExpirytime(self):
        return self._expirytime

    def flush(self):
        self._token = None
        self._expirytime = None
        self._cache.delete('OC.token')
        self._cache.delete('OC.expiry')

    def _getFromCache(self):
        self._token = self._cache.get('OC.token')
        self._expirytime = self._cache.get('OC.expiry')

    def _setToCache(self, token=None, token_expiry=None, expires_in=3600):
        if not token:
            token = self._token
        if not token_expiry:
            token_expiry = self._expirytime
        self._cache.set('OC.token', token, expire=expires_in)
        self._cache.set('OC.expiry', token_expiry, expire=expires_in)

    def _retrieveToken(self):
        # First we try to retrieve from cache if it exists
        self._getFromCache()

        # Now we start building the request to the backend
        url = self.parent.get_base_url() + self._url_suffix_token
        payload = 'grant_type=password&username={usern}&password={passw}'.format(
            usern=quote(self.parent.get_auth_user()),
            passw=quote(self.parent.get_auth_pass())
        )
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        # Send the request to the backend
        # response = requests.request("GET", url, headers=headers, data=payload)
        response = requests.get(url, headers=headers, data=payload)

        # Ensure response looks valid
        if not response.status_code == 200:
            return False
        json_response = response.json()
        assert json_response['token_type'] == 'bearer'
        assert isinstance(json_response['access_token'], str)

        # Parse response and set info
        self._token = json_response['access_token']
        countdown = int(json_response['expires_in']) - int(self._expiration_safety)
        expirytime = int(time()) + countdown
        self._expirytime = expirytime

        # Add the token info to the cache
        self._setToCache(token=self._token, token_expiry=self._expirytime, expires_in=countdown)
        return True

    def getToken(self, flush_existing=False):
        if flush_existing:
            self.flush()  # Explicit flush requested. Useful for debugging
        if not self._token or self.tokenIsExpired():
            if not self._retrieveToken():
                return False

        return self._token

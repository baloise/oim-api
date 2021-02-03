import os
import logging
from .auth import TokenAuthHandler


def required_envvar(envvar):
    # This function ensures that a requested envvar is exists and
    # hard terminates if it isn't
    if not os.getenv(envvar):
        logging.critical('Envvar {varname} not set. Aborting execution!'.format(varname=str(envvar)))
        raise ValueError('Error loading envvar {}'.format(str(envvar)))
    return os.getenv(envvar)


class ourCloud(object):
    def __init__(self):
        self.auth = TokenAuthHandler(self)

    def get_base_url(self):
        return os.getenv('OC_BASEURL')

    def get_auth_user(self):
        return os.getenv('OC_AUTH_USER')

    def get_auth_pass(self):
        return os.getenv('OC_AUTH_PASS')

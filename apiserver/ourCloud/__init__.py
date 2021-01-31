import os
import sys
import logging
from .auth import TokenAuthHandler


def required_envvar(envvar):
    # This function ensures that a requested envvar is exists and
    # hard terminates if it isn't
    if not os.getenv(envvar):
        logging.critical('Envvar {varname} not set. Aborting execution!'.format(varname=str(envvar)))
        sys.exit(50)
    return os.getenv(envvar)


class ourCloud(object):
    def __init__(self):
        self.base_url = required_envvar('OC_BASEURL')
        self.auth_user = required_envvar('OC_AUTH_USER')
        self.auth_pass = required_envvar('OC_AUTH_PASS')
        self.auth = TokenAuthHandler(self)

# config.py
# load all config from .env and display
# follow a hiracy of configs:
# real env, .env but stronges is the real env
import os
from dotenv import dotenv_values
global oim_config

def loadConfig():

    oim_config = {
        **dotenv_values(".env.oim"),     # load project oim shared variables
                                         #  like URL's or other fix interfaces
        **dotenv_values(".env"),         # load local development variables
                                         #  (excluded via gitignore)
        **dotenv_values(".env.secret"),  # load local sensitive variables
                                         #  (excluded via gitignore)
        **os.environ,                    # override loaded values with
                                         #  environment variables
    }
    # place the validation for required parameters
    # pissible set defaults if not set
    # return oim_config
    return


if __name__ == '__main__':
    loadConfig()

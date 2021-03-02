# config.py
# load all config from .env and display
# follow a hierarchy of configs:
# real env, .env but strongest is the real env
import os
from dotenv import dotenv_values


def load_config(main_config=".env") -> dict:

    oim_config = {
        **dotenv_values(".env.oim"),     # load project oim shared variables
                                         #  like URL's or other fix interfaces
        **dotenv_values(main_config),    # load local development variables
                                         #  (excluded via gitignore)
        **dotenv_values(".env.secret"),  # load local sensitive variables
                                         #  (excluded via gitignore)
        **os.environ,                    # override loaded values with
                                         #  environment variables
    }
    # place the validation for required parameters
    # possible set defaults if not set

    return oim_config

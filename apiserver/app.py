import connexion
from flask_sqlalchemy import SQLAlchemy
import os
from dotenv import load_dotenv
# from components.db import db

db = SQLAlchemy()


def create_connexion_app(config_name=None, dotenv_path=None, dotenv_override=False):
    if (config_name is not None) and (dotenv_path is None):
        dotenv_path = '.env.{}'.format(str(config_name))
    if (config_name is None) and (dotenv_path is None):
        dotenv_path = '.env'
    load_dotenv(dotenv_path=dotenv_path, override=dotenv_override)
    server_port = os.getenv('SERVER_PORT') or 9090

    connexion_app = connexion.FlaskApp(__name__, port=server_port, specification_dir='openapi/')

    connexion_app.app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('SQLALCHEMY_DATABASE_URI') or 'sqlite://:memory:'
    connexion_app.app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # This reduces warnings

    db.init_app(connexion_app.app)

    from blueprints.index import index as index_blueprint
    connexion_app.app.register_blueprint(index_blueprint)

    return connexion_app


def create_flask_app(**kwargs):
    capp = create_connexion_app(**kwargs)
    return capp.app


def load_openapis(connexion_app):
    # We tell it to load our API specs
    connexion_app.add_api('demoapi.yaml')

    # add_api() pipes the yaml spec thru the Jinja2 template engine before loading,
    # you can specify variables to be filled as shown with the arguments parameter below
    connexion_app.add_api('olddemo.yaml', arguments={'title': 'OpenAPI Demo of an older API version'})

    # Add the oim test api spec
    connexion_app.add_api('oimtest.yaml')

    # Add the Baloise OIM API specs
    # app.add_api('oimapi-v0.1.yaml')

    # API spec used for testing the order and cmdb classes
    connexion_app.add_api('oimtest_manu.yaml')


# Load non-yet-set envvars from .env file if it exists
# load_dotenv()


# Next we create an object called application that points to our webapp
# This is only needed when the webapp is loaded by a production-ready application server
# application is the default name that these servers look by WSGI specification
# application = connexion_app.app
# TODO: Fix the uwsgi production scenario now that we have an app factory function

# When this file is directly executed on the command line (to get a development server)
# the following if-block runs. It does not run when the file is included by a WSGI application-server
if __name__ == '__main__':
    connexion_app = create_connexion_app()
    load_openapis(connexion_app)
    connexion_app.run()

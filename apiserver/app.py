import connexion
from flask_sqlalchemy import SQLAlchemy
import os
# from dotenv import load_dotenv
from oim_logging import init_logging
from oim_logging import get_oim_logger
from load_config import load_config

db = SQLAlchemy()


def load_openapis(connexion_app):
    # We tell it to load our API specs
    connexion_app.add_api('demoapi-v1.yaml')

    # add_api() pipes the yaml spec thru the Jinja2 template engine before loading,
    # you can specify variables to be filled as shown with the arguments parameter below
    # connexion_app.add_api('olddemo.yaml', arguments={'title': 'OpenAPI Demo of an older API version'})

    # Authentication api
    connexion_app.add_api('auth-v1.yaml')

    # API spec used for oc calls
    connexion_app.add_api('oc-v0.1.yaml')

    # API parts not intended for customer use
    connexion_app.add_api('private-v0.1.yaml')

    # Add the oim itsm api spec
    connexion_app.add_api('itsm-v0.1.yaml')

    # Customer-facing API
    connexion_app.add_api('v0.8.yaml')


def create_connexion_app(config_name=None, dotenv_path=None,
                         dotenv_override=False):
    # if (config_name is not None) and (dotenv_path is None):
    #    dotenv_path = '.env.{}'.format(str(config_name))
    # if (config_name is None) and (dotenv_path is None):
    #    dotenv_path = '.env'

    # load_dotenv(dotenv_path=dotenv_path, override=dotenv_override)
    config = load_config()
    server_port = config.get('SERVER_PORT', '9090')

    init_logging(config)

    log = get_oim_logger()

    specdir = config.get('SPECDIR', 'openapi/')
    log.debug('Creating connexion_app')
    connexion_app = connexion.FlaskApp(__name__, port=server_port,
                                       specification_dir=specdir)

    connexion_app.app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('SQLALCHEMY_DATABASE_URI') or 'sqlite:///:memory:'
    connexion_app.app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # This reduces warnings

    log.debug('Initializing DB to Flaskapp')
    db.init_app(connexion_app.app)

    from blueprints.index import index as index_blueprint
    connexion_app.app.register_blueprint(index_blueprint)

    log.debug("Loading API's")
    load_openapis(connexion_app)

    return connexion_app


def create_flask_app(**kwargs):
    capp = create_connexion_app(**kwargs)
    return capp.app


# When this file is directly executed on the command line (to get a development server)
# the following if-block runs. It does not run when the file is included by a WSGI application-server
if __name__ == '__main__':
    connexion_app = create_connexion_app()
    connexion_app.run()

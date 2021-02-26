import connexion
from flask_sqlalchemy import SQLAlchemy
import os
from dotenv import load_dotenv
from oim_logging import init_logging

db = SQLAlchemy()


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


def create_connexion_app(config_name=None, dotenv_path=None, dotenv_override=False):
    if (config_name is not None) and (dotenv_path is None):
        dotenv_path = '.env.{}'.format(str(config_name))
    if (config_name is None) and (dotenv_path is None):
        dotenv_path = '.env'
    load_dotenv(dotenv_path=dotenv_path, override=dotenv_override)
    server_port = os.getenv('SERVER_PORT') or 9090

    init_logging()

    connexion_app = connexion.FlaskApp(__name__, port=server_port, specification_dir='openapi/')

    connexion_app.app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('SQLALCHEMY_DATABASE_URI') or 'sqlite:///:memory:'
    connexion_app.app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # This reduces warnings

    db.init_app(connexion_app.app)

    from blueprints.index import index as index_blueprint
    connexion_app.app.register_blueprint(index_blueprint)

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

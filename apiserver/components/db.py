from app import application as app
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import SQLAlchemyError
import logging
import os


def setup_db(db_to_setup):
    if not db_to_setup or not db_to_setup.engine:
        logging.error('setup_db called but no valid db object given. Connection issue?')

    if not db.engine.table_names():
        logging.info('Detected empty database, proceeding to create structure..')
        try:
            db.create_all()
        except SQLAlchemyError as e:
            logging.exception('Error creating database structure. Msg: {msg}'.format(msg=str(e)))


app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('SQLALCHEMY_DATABASE_URI') or 'sqlite:///:memory:'
db = SQLAlchemy(app)


# Setup basic structure if it isn't there already in the db.
setup_db(db)

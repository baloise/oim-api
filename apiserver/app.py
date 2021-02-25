import connexion
from flask import render_template
import os
import re
from dotenv import load_dotenv
import logging
import logging.config


# Load non-yet-set envvars from .env file if it exists
load_dotenv()

# start logging, get parameters from config file and load oim logging spec
logger_config_file = os.environ.get("LOGGING_CONFIGFILE")
logger_log_file = os.environ.get("LOGGING_LOGFILE")
logger_mailhost = os.environ.get("LOGGING_MAILHOST")
logging.config.fileConfig(logger_config_file,
                          defaults={'logfilename': logger_log_file,
                                    'mailhost': logger_mailhost,
                                    'toaddrs': 'foo@foo.ch'})
logger = logging.getLogger('oimLogger')

# start using our logger
logger.info('OIM logger startet')
# test different levels
logger.debug('This is an debug message')
logger.info('This is a info message')
logger.warning('This is a warning message')
logger.error('This is a error message')
logger.critical('This is a critical message')

# Now we create the webapp object
# server_port and spec_dir are now from .env file
server_port = os.environ.get("SERVER_PORT")
spec_dir = os.environ.get("SPECDIR")
app = connexion.FlaskApp(__name__, port=server_port, specification_dir=spec_dir)

# Next we tell it to load our API specs
app.add_api('demoapi.yaml')

# add_api() pipes the yaml spec thru the Jinja2 template engine before loading,
# you can specify variables to be filled as shown with the arguments parameter below
app.add_api('olddemo.yaml', arguments={'title': 'OpenAPI Demo of an older API version'})

# Add the oim test api spec
app.add_api('oimtest.yaml')

# Add the Baloise OIM API specs
# app.add_api('oimapi-v0.1.yaml')

# API spec used for testing the order and cmdb classes
# app.add_api('oimtest_manu.yaml')

# Next we create an object called application that points to our webapp
# This is only needed when the webapp is loaded by a production-ready application server
# application is the default name that these servers look by WSGI specification
application = app.app


# Define an index page to avoid confusion
# This looks thru all registered urls and hands the ui ones to the template
@app.route('/')
def show_index():
    ui_urls = []
    uire = re.compile(r'/ui/$')  # Define the regex pattern that matches UI's
    title = 'Index'
    all_urls = app.app.url_map  # This iterable object knows all registered urls
    for current_url in all_urls.iter_rules():
        if uire.findall(current_url.rule):  # Check against the pattern
            ui_urls.append(current_url.rule)  # On match, we add this url to our ui url list
    return render_template('index.j2.html', title=title, ui_urls=ui_urls)


# When this file is directly executed on the command line (to get a development server)
# the following if-block runs. It does not run when the file is included by a WSGI application-server
if __name__ == '__main__':
    app.run()

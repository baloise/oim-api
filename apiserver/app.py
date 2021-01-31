import connexion
import os
from dotenv import load_dotenv

# Load non-yet-set envvars from .env file if it exists
load_dotenv()

# Now we create the webapp object
server_port = os.getenv('SERVER_PORT') or 9090
app = connexion.FlaskApp(__name__, port=server_port, specification_dir='openapi/')

# Next we tell it to load our API specs
app.add_api('olddemo.yaml')
app.add_api('demoapi.yaml')
# add_api() pipes the yaml spec thru the Jinja2 template engine before loading,
# you can specify variables to be filled as shown with the arguments parameter below
app.add_api('oimtest.yaml', arguments={'title': 'OIM API!'})

# Next we create an object called application that points to our webapp
# This is only needed when the webapp is loaded by a production-ready application server
# application is the default name that these servers look by WSGI specification
application = app.app

# When this file is directly executed on the command line (to get a development server)
# the following if-block runs. It does not run when the file is included by a WSGI application-server
if __name__ == '__main__':
    app.run()

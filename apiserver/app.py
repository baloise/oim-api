import connexion

if __name__ == '__main__':
    app = connexion.FlaskApp(__name__, port=9090, specification_dir='openapi/')
    app.add_api('olddemo.yaml', arguments={'title': 'Old Demo API!'})
    app.add_api('demoapi.yaml', arguments={'title': 'Demo API!'})
    app.run()
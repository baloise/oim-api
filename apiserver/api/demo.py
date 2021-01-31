# This file only contains random hello-world-grade functions so
# that the demo api endpoints actually do something.

def hello_world():
    return 'Hello World'

def post_greeting(name: str) -> str:
    return 'Hello {name}'.format(name=name)

class PeristanceDemo(object):
    count = 0

    def increase(self):
        self.count += 1

    def showcount(self):
        return self.count

# Create an instance of this class that lives within the memory of the app
persistance_demo = PeristanceDemo()

def persistance_get():
    # Method called by the api endpoint. See the .yaml files in the openapi/ folder
    persistance_demo.increase()
    return persistance_demo.showcount()
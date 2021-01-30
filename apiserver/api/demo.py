
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

persistance_demo = PeristanceDemo()

def persistance_get():
    persistance_demo.increase()
    return persistance_demo.showcount()
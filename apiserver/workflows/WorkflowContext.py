from models.orders import Person


class WorkflowContext:
    def __init__(self, requester: Person):
        self.requester = requester

    def get_requester(self):
        return self.requester

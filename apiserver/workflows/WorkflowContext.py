from models.orders import Person


class WorkflowContext:
    def __init__(self, requester: Person, changeno: str):
        self.requester = requester
        self.changeno = changeno

    def get_requester(self):
        return self.requester

    def get_changeno(self):
        return self.changeno

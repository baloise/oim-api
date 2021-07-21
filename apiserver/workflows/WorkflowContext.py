from models.orders import Person


class WorkflowContext:
    def __init__(self, requester: Person):
        self.requester = requester
        self.changeno = None

    def get_requester(self):
        return self.requester

    def set_changeno(self, changeno: str):
        self.changeno = changeno

    def get_changeno(self):
        return self.changeno

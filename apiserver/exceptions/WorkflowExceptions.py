class StepException(Exception):
    def __init__(self, msg, order_id):
        self.msg = msg
        self.order_id = order_id


class RequestHandlerException(Exception):
    def __init__(self, msg):
        self.msg = msg


class TransmitException(Exception):
    def __init__(self, msg):
        self.msg = msg


class WorkflowIncompleteException(Exception):
    def __init__(self, msg):
        self.msg = msg

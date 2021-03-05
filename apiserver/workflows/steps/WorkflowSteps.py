from abc import ABC, abstractmethod
from models.my_orders import OrderItem


class AbstractWorkflowStep(ABC):

    def __init__(self, action):
        self.action = action

    def get_action(self):
        return self.action

    @abstractmethod
    def execute(self):
        print(" execute action: {}".format(self.action))


class DummyStep(AbstractWorkflowStep):
    def execute(self):
        print(" execute action: {}".format(self.action))


class DeployItemStep(AbstractWorkflowStep):
    def __init__(self, item: OrderItem):
        self.item = item
        self.action = "deploy"

    def execute(self):
        # extract details from order item
        # build request path
        # send request
        # handle response
        print(" {} item: {}".format(self.action, self.item.get_name()))


class VerifyItemStep(AbstractWorkflowStep):
    def __init__(self, item: OrderItem):
        self.item = item
        self.action = "verify"

    def execute(self):
        # check
        print(" {} item: {}".format(self.action, self.item.get_name()))

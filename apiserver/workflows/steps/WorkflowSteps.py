from abc import ABC, abstractmethod
from models.orders import OrderItem
from ourCloud.OurCloudHandler import OurCloudRequestHandler
from workflows.WorkflowContext import WorkflowContext
from oim_logging import get_oim_logger


class AbstractWorkflowStep(ABC):

    def __init__(self, action):
        self.action = action

    def get_action(self):
        return self.action

    @abstractmethod
    def execute(self, context: WorkflowContext):
        info = " execute action: {} for user {}".format(self.action, context.get_requester().email)
        print(info)
        logger = get_oim_logger()
        logger.info(info)


class DummyStep(AbstractWorkflowStep):
    def execute(self, context: WorkflowContext):
        info = " Execute step: {} for user {}".format(self.action, context.get_requester().email)
        print(info)
        logger = get_oim_logger()
        logger.info(info)


class DeployItemStep(AbstractWorkflowStep):
    def __init__(self, item: OrderItem):
        self.item = item
        self.action = "deploy"

    def execute(self, context: WorkflowContext):
        # extract details from order item
        # build request path
        # send request
        # handle response
        info = " Execute step: {} item {} size '{}' for user {}".format(self.action, self.item.get_cataloguename(),
                                                                        self.item.get_size(),
                                                                        context.get_requester().email)
        logger = get_oim_logger()
        logger.info(info)
        try:
            handler = OurCloudRequestHandler.getInstance()
            try:
                res = handler.create_vm(item=self.item, requester=context.get_requester())
            except Exception as e:
                error = "Failed to create vm: {} with parameters item='{} requester='{}' ".format(e, self.item, context.get_requester())  # noqa 501
                logger.error(error)
                raise Exception(error)
            else:
                info = " Step result: {} ({})".format(res, self)
                logger.info(info)
        except Exception as e:
            error = "Failed to instantiate request handler: {}".format(e)
            logger.error(error)
            raise Exception(error)
        else:
            logger.debug("Step completed ({})".format(self))


class VerifyItemStep(AbstractWorkflowStep):
    def __init__(self, item: OrderItem):
        self.item = item
        self.action = "verify"

    def execute(self, context: WorkflowContext):
        # check
        info = " Execute step: {} item {} size '{}' for user {}".format(self.action, self.item.get_cataloguename(),
                                                                        self.item.get_size().cataloguesize,
                                                                        context.get_requester().email)
        print(info)
        logger = get_oim_logger()
        logger.info(info)

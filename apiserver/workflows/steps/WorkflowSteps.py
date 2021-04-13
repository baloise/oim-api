from abc import ABC, abstractmethod
from models.orders import OrderItem
from ourCloud.OurCloudHandler import OurCloudRequestHandler
from workflows.WorkflowContext import WorkflowContext
from oim_logging import get_oim_logger
from exceptions.WorkflowExceptions import StepException, RequestHandlerException, TransmitException
import traceback
from app import db


class AbstractWorkflowStep(ABC):

    def __init__(self, action):
        self.action = action

    def get_action(self):
        return self.action

    @abstractmethod
    def execute(self, context: WorkflowContext):
        info = " execute action: {} for user {}".format(self.action, context.get_requester().email)
        logger = get_oim_logger()
        logger.info(info)


class DummyStep(AbstractWorkflowStep):
    def __init__(self):
        self.action = "dummy"

    def execute(self, context: WorkflowContext):
        info = "  Execute step: {} for user {}".format(self.action, context.get_requester().email)
        logger = get_oim_logger()
        logger.info(info)


class DeployVmStep(AbstractWorkflowStep):
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
                ocRequestId = handler.create_vm(item=self.item, requester=context.get_requester())
                self.persist_requestid(self.item, ocRequestId)
            except TransmitException as te:
                logger.error(te)
                raise StepException(te, self.item.order_id)  # use custom Exception here
            except Exception as e:
                track = traceback.extract_stack()
                logger.debug(track)
                error = "Failed to create vm: {} with parameters item='{} requester='{}' ".format(e, self.item, context.get_requester())  # noqa 501
                logger.error(error)
                raise  # StepException(error, self.item.order_id)  # use custom Exception here
            else:
                info = f" Step result: {ocRequestId} ({self})"
                logger.info(info)
        except RequestHandlerException as e:
            error = "Failed to instantiate request handler: {}".format(e)
            logger.error(error)
            raise Exception(error)
        else:
            logger.debug("Step completed ({})".format(self))

    def persist_requestid(self, item, reqid):
        anOrderItem = OrderItem.query.get(item.id)
        anOrderItem.set_backend_request_id(reqid)
        db.session.commit()


class VerifyItemStep(AbstractWorkflowStep):
    def __init__(self, item: OrderItem):
        self.item = item
        self.action = "verify"

    def execute(self, context: WorkflowContext):
        # check
        info = "  Execute step: {} item {} size '{}' for user {}".format(self.action, self.item.get_cataloguename(),
                                                                         self.item.get_size().cataloguesize,
                                                                         context.get_requester().email)
        logger = get_oim_logger()
        logger.info(info)
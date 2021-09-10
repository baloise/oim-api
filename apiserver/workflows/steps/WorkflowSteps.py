from abc import ABC, abstractmethod
from models.orders import OrderItem
from ourCloud.OurCloudHandler import OurCloudRequestHandler
from orchestra.OrchestraRequestHandler import OrchestraChangeHandler
from workflows.WorkflowContext import WorkflowContext
from oim_logging import get_oim_logger
from exceptions.WorkflowExceptions import StepException, RequestHandlerException, TransmitException
from random import sample
import traceback
from app import db
import time
from datetime import datetime
import os
from ourCloud.OcStaticVars import TRANSLATE_TARGETS
from adapter.OrchestraAdapters import environment_adapter
from itsm.handler import ValuemationHandler
from itsm.handler import CreateChangeDetails
from itsm.handler import CloseChangeDetails


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
    def __init__(self, message="no message"):
        self.action = "dummy"
        self.message = message

    def execute(self, context: WorkflowContext):
        info = "  Execute step {} for user {}: {ms}".format(self.action, context.get_requester().email, ms=self.message)
        logger = get_oim_logger()
        logger.info(info)


class AwaitDeployStep(AbstractWorkflowStep):
    def __init__(self, item: OrderItem):
        self.action = "awaitdeploy"
        self.logger = get_oim_logger()
        self.STATUS_CLOSED = "CH_CLD"
        self.item = item

    def execute(self, context: WorkflowContext):
        crnr = context.getItemChangeno(self.item)
        info = "  Execute step: {ac} for change {chg} for item {itm}".format(ac=self.action,
                                                                             chg=crnr,
                                                                             itm=self.item.get_cataloguename())
        self.logger.info(info)
        while True:
            if self.isDeploymentDone(context):
                break
            time.sleep(10)

    def isDeploymentDone(self, context: WorkflowContext):
        crnr = context.getItemChangeno(self.item)
        try:
            chstatus = self.getTicketStatus(context.get_changeno())
        except Exception as re:
            error = "Error while reading status of change nr {cnr}: {err}".format(cnr=crnr,
                                                                                  err=re)
            self.logger.error(error)
            return False
        self.logger.info("Poll status of change {nr}: {chs}".format(nr=crnr,
                                                                    chs=chstatus))
        if chstatus is None:
            self.logger.error("Error while trying to poll status of change nr {nr}: change unknown".format(nr=crnr))   # noqa E501
            return False
        if chstatus == self.STATUS_CLOSED:  # TODO: we only check the STATUS for now, more fields might be relevant later on # noqa E501
            # we're done, let's continue the workflow
            return True
        return False

    def getTicketStatus(self, changeno: str):
        if self.do_simulate():
            self.logger.info("Simulate orca ticket api")
            retStat = self.STATUS_CLOSED  # TODO: CH_CLD means "deployment done", adjust if more fields might be relevant later on # noqa E501
        else:
            handler = OrchestraChangeHandler()
            retStat = handler.select_change("TICKETNO", changeno)
        return retStat

    def do_simulate(self) -> bool:
        mystring = os.getenv('ORCA_SIMULATE', "True")
        doSimulate = True
        if mystring.lower() == 'false':
            doSimulate = False
        if doSimulate:
            self.logger.info("Simulation enabled, requests will NOT be sent do ORCA ({})".format(doSimulate))
            return True
        else:
            self.logger.info("Simulation disabled, requests will be sent do ORCA ({})".format(doSimulate))
            return False


class CreateCrStep(AbstractWorkflowStep):
    def __init__(self, item: OrderItem):
        self.action = "createcr"
        self.item = item

    def execute(self, context: WorkflowContext):
        info = "  Execute step: {ac} for item {itm}".format(ac=self.action, itm=self.item.get_cataloguename())
        logger = get_oim_logger()
        logger.info(info)
        myRequestor = context.get_requester().username
        myEnv = environment_adapter().translate(self.item.getEnvironment(), TRANSLATE_TARGETS.VAL)
        myDuedate = datetime.now().strftime("%Y-%m-%d")
        myValenv_id = myEnv
        myService_id = self.item.getBusinessServiceId()

        # ToDo: Not defined and not clear where we can get this, maybe not required
        myCategory = ""
        myChangeDetails = CreateChangeDetails()
        myChangeDetails.setShorttext("OIM Testing Standard Change (Georges)")
        myChangeDetails.setDescription("OIM Testing Standard Change (Georges)")
        myChangeDetails.setReqPerson(myRequestor)
        myChangeDetails.setCategory(myCategory)
        myChangeDetails.setServicesId(myService_id)
        myChangeDetails.setdueDate(myDuedate)
        myChangeDetails.setEnvironmentId(myValenv_id)

        myChange = ValuemationHandler(myChangeDetails)
        lRet = myChange.create_change()
        if lRet == "11":
            logger.error("create of CR is failed:{}".format(lRet))
        else:
            try:
                crnr = lRet['data']['ticketno']
            except KeyError:
                logger.error("create of CR is failed:{}".format(lRet))
                return None

        # crnr = self.getRandomChangeNr()
        context.add_item(self.item, crnr)
        logger.info("CR {nr} has been created".format(nr=crnr))

    def getRandomChangeNr(self) -> str:
        c = "{s}{i}".format(s="CH-", i=''.join(sample("123456789", 7)))
        return c


class CloseCrStep(AbstractWorkflowStep):
    def __init__(self, item: OrderItem):
        self.action = "closecr"
        self.item = item

    def execute(self, context: WorkflowContext):
        info = "  Execute step: {ac} for item {itm}".format(ac=self.action, itm=self.item.get_cataloguename())
        logger = get_oim_logger()
        logger.info(info)
        myChange = context.get_requester().crnr
        # mySystem = context.get_requester().system
        mySystem = "CHZ1-TS-01"

        myChangeDetails = CloseChangeDetails()
        myChangeDetails.setChangeNr(myChange)
        myChangeDetails.setSystem(mySystem)
        myChangeDetails.setStatus("CH_REVD")
        myChangeDetails.setShorttext("PreClose")
        myChangeDetails.setDescription("OIM Testing Standard Change (Georges)")

        myChange = ValuemationHandler(myChangeDetails)
        lRet = myChange.close_change()
        if lRet == "11":
            logger.error("close of CR is failed:{}".format(lRet))
        else:
            try:
                crnr = lRet['data']['ticketno']
            except KeyError:
                logger.error("close of CR is failed:{}".format(lRet))
                return None

        # crnr = self.getRandomChangeNr()
        context.add_item(self.item, crnr)
        logger.info("CR {nr} has been closed".format(nr=crnr))


class DeployVmStep(AbstractWorkflowStep):
    def __init__(self, item: OrderItem):
        self.item = item
        self.action = "deploy"

    def execute(self, context: WorkflowContext):
        # extract details from order item
        # build request path
        # send request
        # handle response
        info = " Execute step: {ac} item {it} size '{si}' for user {us}".format(ac=self.action, it=self.item.get_cataloguename(),   # noqa E501
                                                                                si=self.item.get_size().catalogueid,
                                                                                us=context.get_requester().email)
        logger = get_oim_logger()
        logger.info(info)

        try:
            handler = OurCloudRequestHandler.getInstance()
            try:
                crnr = context.getItemChangeno(self.item)
                ocRequestId = handler.create_vm(item=self.item, requester=context.get_requester(), changeno=crnr)   # noqa E501
                self.persist_requestid(self.item, ocRequestId)
            except TransmitException as te:
                logger.error(te)
                raise StepException(te, self.item.order_id)  # use custom Exception here
            except Exception as e:
                track = traceback.extract_stack()
                logger.debug(track)
                errorStr = "Failed to create vm: {err} with parameters item='{itm}' requester='{rster}' ".format(err=e, itm=self.item.get_cataloguename().cataloguename, rster=context.get_requester())  # noqa 501
                logger.error(errorStr)
                raise  # StepException(errorStr, self.item.order_id)  # use custom Exception here
            else:
                info = f" Step result: {ocRequestId} ({self.action})"
                logger.info(info)
        except RequestHandlerException as e:
            errorStr = "Failed to instantiate request handler: {}".format(e)
            logger.error(errorStr)
            raise Exception(errorStr)
        else:
            logger.debug("Step completed ({})".format(self.action))

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
        infoStr = "  Execute step: {} item {} size '{}' for user {}".format(self.action, self.item.get_cataloguename(),
                                                                            self.item.get_size().cataloguesize,
                                                                            context.get_requester().email)
        logger = get_oim_logger()
        logger.info(infoStr)

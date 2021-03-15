from ourCloud.OurCloudHandler import OurCloudRequestHandler
from oim_logging import get_oim_logger
from workflows.Factory import WorkflowFactory, OrderFactory
from workflows.Workflows import WorkflowTypes
from models.orders import OrderItem, Person, SbuType
from models.orders import OrderType
from workflows.WorkflowContext import WorkflowContext
from ourCloud.OcStaticVars import OC_CATALOGOFFERINGS, OC_CATALOGOFFERING_SIZES  # noqa F401

# type alias
Param = [str]


def feedback_request_details(body):
    logger = get_oim_logger()

    if len(body) > 0:
        info = "Request {reqno} has details: {det}".format(det=body["details"], reqno=body["requestno"])
        logger.info(info)
        return info
    else:
        return "Requestno {reqno} has no details".format(reqno=body["requestno"])


def deletevm(hostname: str):
    handler = OurCloudRequestHandler.getInstance()
    ocstatus = handler.delete_vm(hostname)
    logger = get_oim_logger()

    if len(ocstatus) > 0:
        info = "Delete request : {ocstatus}".format(ocstatus=ocstatus)
        logger.info(info)
        return info
    else:
        return 'Request failed'


def createvm(body):
    logger = get_oim_logger()
    workflowFactory = WorkflowFactory()
    orderFactory = OrderFactory()

    personPeter = Person(
            username='u12345',
            email=body.get("requester"),
            sbu=SbuType.SHARED
        )

    catName = body.get("cataloguename")
    offering = OC_CATALOGOFFERINGS.from_str(catName)
    catSize = body.get("size")
    logger.info(catSize)
    size = OC_CATALOGOFFERING_SIZES.from_str(catSize)
    rhel_item = OrderItem(offering, size)
    items = [rhel_item]
    new_order = orderFactory.get_order(OrderType.CREATE_ORDER, items, personPeter)

    wf = workflowFactory.get_workflow(WorkflowTypes.WF_CREATE_VM)
    context = WorkflowContext(personPeter)
    wf.set_context(context)
    wf.set_order(new_order)

    try:
        ocstatus = wf.execute()
    except Exception as e:
        logger.error(e)
        return "{}".format(e), 500

    if len(ocstatus) > 0:
        info = "New request : {ocstatus}".format(ocstatus=ocstatus)
        logger.debug(info)
        return info
    else:
        error = "Request failed"
        logger.error(error)
        return "{}".format(error), 500


def get_request_status(requestno: int) -> str:
    handler = OurCloudRequestHandler.getInstance()
    ocstatus = handler.get_request_status(requestno)
    logger = get_oim_logger()

    if len(ocstatus) > 0:
        info = "Request {reqno} has status: {ocstatus}".format(ocstatus=ocstatus, reqno=requestno)
        logger.info(info)
        return info
    else:
        return 'Requestno invalid'


def get_request_details(requestno: int, attributes: Param) -> str:
    handler = OurCloudRequestHandler.getInstance()
    extendedParams = attributes  # ["RequestDetailID", "InstanceSize", "hdnOSType"]
    ocKeyVal = handler.get_extended_request_parameters(requestno, extendedParams)
    logger = get_oim_logger()

    if len(ocKeyVal) > 0:
        info = "Request {reqno} extended parameters values: {ocstatus}".format(ocstatus=ocKeyVal, reqno=requestno)
        logger.info(info)
        return info
    else:
        return 'Requestno invalid'

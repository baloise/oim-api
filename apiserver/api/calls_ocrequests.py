from ourCloud.OurCloudHandler import OurCloudRequestHandler
from oim_logging import get_oim_logger
from workflows.Factory import WorkflowFactory, OrderFactory
from workflows.Workflows import WorkflowTypes
from models.orders import OrderItem
from models.orders import OrderType
from workflows.WorkflowContext import WorkflowContext
from ourCloud.OcStaticVars import OC_CATALOGOFFERINGS, OC_CATALOGOFFERING_SIZES  # noqa F401
from app import db
from api.calls_helpers import persist_person
from exceptions.WorkflowExceptions import WorkflowIncompleteException

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
    db.create_all()

    eml = body.get("requester")
    personPeter = persist_person(eml)

    catName = body.get("cataloguename")
    offering = OC_CATALOGOFFERINGS.from_str(catName)

    catSize = body.get("size")
    size = OC_CATALOGOFFERING_SIZES.from_str(catSize)

    rhel_item = OrderItem(offering, size)

    tag = body.get("tag")
    rhel_item.set_reference(tag)

    items = [rhel_item]
    new_order = orderFactory.get_order(OrderType.CREATE_ORDER, items, personPeter)

    wf = workflowFactory.get_workflow(WorkflowTypes.WF_CREATE_VM)
    context = WorkflowContext(personPeter)
    wf.set_context(context)
    wf.set_order(new_order)

    try:
        ocstatus = wf.execute()
    except WorkflowIncompleteException as wie:
        return "{}".format(wie), 500

    info = "New request : {ocstatus}".format(ocstatus=ocstatus)
    logger.info(info)
    show_items()
    oi = get_item_id(rhel_item)
    retStr = {"orderid": oi.id, "itemid": oi.id, "requestid": oi.backend_request_id}
    return retStr, 201


def get_item_id(item):
    anItem = OrderItem.query.get(item.id)
    return anItem


def show_items():
    allitems = OrderItem.query.all()
    logger = get_oim_logger()
    logger.debug(repr(allitems))


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

from ourCloud.OurCloudHandler import OurCloudRequestHandler
import logging
from oim_logging import get_oim_logger

# type alias
Param = [str]


def feedback_request_details(body):
    if len(body) > 0:
        info = "Request {reqno} has details: {det}".format(det=body["details"], reqno=body["requestno"])
        logging.getLogger(get_oim_logger()).info(info)
        return info
    else:
        return "Requestno {reqno} has no details".format(reqno=body["requestno"])


def deletevm(hostname: str):
    handler = OurCloudRequestHandler.getInstance()
    ocstatus = handler.delete_vm(hostname)

    if len(ocstatus) > 0:
        info = "Delete request : {ocstatus}".format(ocstatus=ocstatus)
        logging.getLogger(get_oim_logger()).info(info)
        return info
    else:
        return 'Request failed'


def createvm():
    handler = OurCloudRequestHandler.getInstance()
    ocstatus = handler.create_vm()

    if len(ocstatus) > 0:
        info = "New request : {ocstatus}".format(ocstatus=ocstatus)
        logging.getLogger(get_oim_logger()).info(info)
        return info
    else:
        return 'Request failed'


def get_request_status(requestno: int) -> str:
    handler = OurCloudRequestHandler.getInstance()
    ocstatus = handler.get_request_status(requestno)

    if len(ocstatus) > 0:
        info = "Request {reqno} has status: {ocstatus}".format(ocstatus=ocstatus, reqno=requestno)
        logging.getLogger(get_oim_logger()).info(info)
        return info
    else:
        return 'Requestno invalid'


def get_request_details(requestno: int, attributes: Param) -> str:
    handler = OurCloudRequestHandler.getInstance()
    extendedParams = attributes  # ["RequestDetailID", "InstanceSize", "hdnOSType"]
    ocKeyVal = handler.get_extended_request_parameters(requestno, extendedParams)

    if len(ocKeyVal) > 0:
        info = "Request {reqno} extended parameters values: {ocstatus}".format(ocstatus=ocKeyVal, reqno=requestno)
        logging.getLogger(get_oim_logger()).info(info)
        return info
    else:
        return 'Requestno invalid'

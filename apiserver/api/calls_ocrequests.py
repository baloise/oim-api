from ourCloud.OurCloudHandler import OurCloudRequestHandler
import logging
import datetime

# type alias
Param = [str]


def feedback_request_details(body):
    if len(body) > 0:
        info = "Request {reqno} has details: {det}".format(det=body["details"], reqno=body["requestno"])
        logging.info(info)
        writeLog(info)
        return info
    else:
        return "Requestno {reqno} has no details".format(reqno=body["requestno"])


def writeLog(msg: str):
    filename = 'oclogging.log'
    # Open the file in append mode and append the new content in file_object
    with open(filename, 'a') as file_object:
        now = datetime.datetime.now()
        file_object.write("{t}: {m}\n".format(m=msg, t=now.strftime('%Y-%m-%d %H:%M:%S')))


def deletevm(hostname: str):
    handler = OurCloudRequestHandler.getInstance()
    ocstatus = handler.delete_vm(hostname)

    if len(ocstatus) > 0:
        info = "Delete request : {ocstatus}".format(ocstatus=ocstatus)
        logging.info(info)
        return info
    else:
        return 'Request failed'


def createvm():
    handler = OurCloudRequestHandler.getInstance()
    ocstatus = handler.create_vm()

    if len(ocstatus) > 0:
        info = "New request : {ocstatus}".format(ocstatus=ocstatus)
        logging.info(info)
        return info
    else:
        return 'Request failed'


def get_request_status(requestno: int) -> str:
    handler = OurCloudRequestHandler.getInstance()
    ocstatus = handler.get_request_status(requestno)

    if len(ocstatus) > 0:
        info = "Request {reqno} has status: {ocstatus}".format(ocstatus=ocstatus, reqno=requestno)
        logging.info(info)
        return info
    else:
        return 'Requestno invalid'


def get_request_details(requestno: int, attributes: Param) -> str:
    handler = OurCloudRequestHandler.getInstance()
    extendedParams = attributes  # ["RequestDetailID", "InstanceSize", "hdnOSType"]
    ocKeyVal = handler.get_extended_request_parameters(requestno, extendedParams)

    if len(ocKeyVal) > 0:
        info = "Request {reqno} extended parameters values: {ocstatus}".format(ocstatus=ocKeyVal, reqno=requestno)
        logging.info(info)
        return info
    else:
        return 'Requestno invalid'

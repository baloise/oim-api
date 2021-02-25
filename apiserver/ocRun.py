from dotenv import load_dotenv
from ourCloud.OurCloudHandler import OurCloudRequestHandler
from ourCloud.OurCloudStatusProducer import OurCloudStatusProducer
import logging

load_dotenv()
logger = logging.getLogger()
logging.basicConfig(
    level=logging.INFO,
    style="{",
    datefmt="%d.%m.%Y %H:%M:%S",
    format="{asctime} {levelname}: {message}"
)
logger.setLevel(logging.INFO)


if False:
    handler = OurCloudRequestHandler.getInstance()
    reqno = 93
    ocstatus = handler.get_request_status(reqno)
    print("Request {reqno} has status: {ocstatus}".format(ocstatus=ocstatus, reqno=reqno))

    ocstatus = handler.list_extended_request_parameters(reqno)
    print("Request {reqno} has extended parameters: {ocstatus}".format(ocstatus=ocstatus, reqno=reqno))

    extendedParams = ["RequestDetailID", "InstanceSize", "hdnOSType"]
    ocstatus = handler.get_extended_request_parameters(reqno, extendedParams)
    print("Request {reqno} extended parameters values: {ocstatus}".format(ocstatus=ocstatus, reqno=reqno))

producer = OurCloudStatusProducer()
producer.pollStatus(93)

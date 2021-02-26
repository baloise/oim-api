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

logger.setLevel(logging.DEBUG)

reqno = 135
handler = OurCloudRequestHandler.getInstance()
if False:
    ocstatus = handler.get_request_status(reqno)
    logging.info("Request {reqno} has status: {ocstatus}".format(ocstatus=ocstatus, reqno=reqno))

    ocParamList = handler.list_extended_request_parameters(reqno)
    logging.info("Request {reqno} has extended parameters: {params}".format(params=ocParamList, reqno=reqno))

    extendedParams = ocParamList[1:]  # ["RequestDetailID", "InstanceSize", "hdnOSType"]
    ocKeyVal = handler.get_extended_request_parameters(reqno, extendedParams)
    logging.info("Request {reqno} extended parameters values: {ocstatus}".format(ocstatus=ocKeyVal, reqno=reqno))

producer = OurCloudStatusProducer(["RequestDetailID", "InstanceSize", "hdnOSType"], finalStatus="Fulfilment Completed")
producer.pollStatus(reqno)

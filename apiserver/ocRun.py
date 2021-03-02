from dotenv import load_dotenv
from ourCloud.OurCloudHandler import OurCloudRequestHandler
from ourCloud.OurCloudStatusProducer import OurCloudStatusProducer
import logging
from ourCloud.OcStaticVars import OC_REQUESTFIELD, OC_STATUS, OC_CATALOGOFFERINGS

load_dotenv()
logger = logging.getLogger()
logging.basicConfig(
    level=logging.INFO,
    style="{",
    datefmt="%d.%m.%Y %H:%M:%S",
    format="{asctime} {levelname}: {message}"
)

logger.setLevel(logging.INFO)

reqno = 136
handler = OurCloudRequestHandler.getInstance()
if True:
    ocstatus = handler.get_request_status(reqno)
    logging.info("Request {reqno} has status: {ocstatus}".format(ocstatus=ocstatus, reqno=reqno))

    ocParamList = handler.list_extended_request_parameters(reqno)
    logging.info("Request {reqno} has extended parameters: {params}".format(params=ocParamList, reqno=reqno))

    extendedParams = ocParamList[1:]
    ocKeyVal = handler.get_extended_request_parameters(reqno, extendedParams)
    logging.info("Request {reqno} extended parameters values: {ocstatus}".format(ocstatus=ocKeyVal, reqno=reqno))

producer = OurCloudStatusProducer([OC_REQUESTFIELD.REQUESTDETAILID.value, OC_REQUESTFIELD.INSTANCESIZE.value,
                                   OC_REQUESTFIELD.OSTYPE.value],
                                  finalStatus=OC_STATUS.FULFILLMENT_COMPLETED.value)
producer.pollStatus(reqno)

for member in OC_CATALOGOFFERINGS:
    logging.info('{}={}'.format(member.name, member.value))

logging.info(OC_CATALOGOFFERINGS.WINS2019.cataloguename)

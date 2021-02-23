from dotenv import load_dotenv
from ourCloud.OurCloudHandler import OurCloudRequestHandler

load_dotenv()

handler = OurCloudRequestHandler.getInstance()
reqno = 93
ocstatus = handler.get_request_status(reqno)
print("Request {reqno} has status: {ocstatus}".format(ocstatus=ocstatus, reqno=reqno))


ocstatus = handler.list_extended_request_parameters(reqno)
print("Request {reqno} has extended parameters: {ocstatus}".format(ocstatus=ocstatus, reqno=reqno))

extendedParams = ["RequestDetailID", "InstanceSize", "hdnOSType"]
ocstatus = handler.get_extended_request_parameters(reqno, extendedParams)
print("Request {reqno} extended parameters values: {ocstatus}".format(ocstatus=ocstatus, reqno=reqno))

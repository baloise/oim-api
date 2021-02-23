from dotenv import load_dotenv
from ourCloud.OurCloudHandler import OurCloudRequestHandler

load_dotenv()

handler = OurCloudRequestHandler.getInstance()
reqno = 93
ocstatus = handler.GetCustomTableRecordsByName(reqno)
print("Request {reqno} has status: {ocstatus}".format(ocstatus=ocstatus, reqno=reqno))

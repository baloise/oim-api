import logging
from itsm.handler import ValuemationHandler


logger = logging.getLogger()
logging.basicConfig(
    level=logging.DEBUG,
    style="{",
    datefmt="%d.%m.%Y %H:%M:%S",
    format="{asctime} {levelname}: {message}"
)

myChange = ValuemationHandler()

# Show ENV
# x = myChange.showEnv()
# print("Return:[", x, "]")

# Test Update Standard Change
params = {
        "status": "CH_IMPF",
        "description": "Free text can place hier, final version(Georges)",
        "ticketno": "CH-0000020",
        "changeOwnerGroup": "HCL-Linux"
    }

lRet = myChange.update_change(params)
print("Return:[", lRet, "]")
exit()

# Test Create Standard Change
params = {
        "ticketclass": "RFC/Change",
        "tickettype": "Standard Change",
        "status": "CH_REC",
        "tckShorttext": "Standard Change: Testing the workflow from OIM(Georges)",
        "description": "Standard Change: Testing the workflow from OIM(Georges)",
        "statementtype": "Information",
        "persnoReqBy": "B037158",
        "category": "Linux",
        "servicesid": "560",
        "system": "CHZ1-TS-01",
        "dueDate": "2021-07-26",
        "environmentId": "3",
        "changeOwnerPersonNo": "",
        "changeOwnerGroup": "HCL-DCOps"
    }

lRet = myChange.create_change(params)
print("Return:[", lRet, "]")

import logging
import json
from itsm.handler import ValuemationHandler


# Test Update Standard Change
def updateChange(myChange, ticketNr: str) -> json:
    params = {
            "status": "CH_IMPF",
            "description": "Clone | Update by GGR!",
            "ticketno": ticketNr,
            "changeOwnerGroup": "HCL-Linux"
        }

    lRet = myChange.update_change(params)
    # print("Return:[", lRet, "]")
    return lRet


# Test Create Standard Change
def createChange(myChange) -> json:
    params = {
            "ticketclass": "RFC/Change",
            "tickettype": "Standard Change",
            "status": "CH_REC",
            "tckShorttext": "Testing Standard Change from OIM(Georges)",
            "description": "Testing Standard Change from OIM(Georges)",
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
    # print("Return:[", lRet, "]")
    return lRet


if __name__ == '__main__':
    logger = logging.getLogger()
    logging.basicConfig(
        level=logging.DEBUG,
        style="{",
        datefmt="%d.%m.%Y %H:%M:%S",
        format="{asctime} {levelname}: {message}"
    )

    myChange = ValuemationHandler()

    # lRet = createChange(myChange)
    # retStr = {"ticketno": lRet['data']['ticketno'], "status": lRet['score']}
    lRet = updateChange(myChange, 'CH-0000022')
    retStr = {"ticketno": lRet['data']['ticketno'], "changestatus": lRet['score']}
    print(retStr)

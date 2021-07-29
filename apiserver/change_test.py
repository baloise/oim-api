import logging
import json
from itsm.handler import ValuemationHandler
from itsm.handler import CreateChangeDetails
from datetime import datetime


# Test Update Standard Change
def updateChange(myChange, ticketNr: str) -> json:
    params = {
            "status": "CH_IMPF",
            "description": "Clone | Update by GGR!",
            "ticketno": ticketNr,
            "system": "CHZ1-TS-01",
            "changeOwnerGroup": "HCL-Linux"
        }

    lRet = myChange.update_change(params)
    # print("Return:[", lRet, "]")
    return lRet


# Test Create Standard Change List
def createChangeList() -> json:
    params = {
            "tckShorttext": "OIM Testing Standard Change (Georges)",
            "description": "OIM Testing Standard Change (Georges)",
            "persnoReqBy": "B037158",
            "category": "Linux",
            "servicesid": "560",
            "dueDate": "2021-07-29",
            "environmentId": "3"
        }

    myChange = ValuemationHandler(params)
    lRet = myChange.create_change()
    return lRet


# Test Create Standard Change Object
def createChangeObj() -> json:
    myChangeDetails = CreateChangeDetails()
    myChangeDetails.setShorttext("OIM Testing Standard Change (Georges)")
    myChangeDetails.setDescription("OIM Testing Standard Change (Georges)")
    myChangeDetails.setReqPerson("B037158")
    myChangeDetails.setCategory("Linux")
    myChangeDetails.setServicesId("560")
    # myChangeDetails.setServicesId("1360")
    myChangeDetails.setdueDate(datetime.now().strftime("%Y-%m-%d"))
    myChangeDetails.setEnvironmentId("3")

    myChange = ValuemationHandler(myChangeDetails)
    lRet = myChange.create_change()
    return lRet


if __name__ == '__main__':
    logger = logging.getLogger()
    logging.basicConfig(
        level=logging.DEBUG,
        style="{",
        datefmt="%d.%m.%Y %H:%M:%S",
        format="{asctime} {levelname}: {message}"
    )

    lRet = createChangeObj()

    if lRet == "11":
        retStr = lRet
    else:
        retStr = {"ticketno": lRet['data']['ticketno'], "status": lRet['score']}

    # lRet = createChangeList()
    # lRet = updateChange(myChange, 'CH-0000025')
    # retStr = {"ticketno": lRet['data']['ticketno'], "changestatus": lRet['score']}
    print(retStr)

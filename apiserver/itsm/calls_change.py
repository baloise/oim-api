from oim_logging import get_oim_logger
from itsm.handler import ValuemationHandler


def update_change(body):
    logger = get_oim_logger()
    mystatus = body.get("status")
    myticketno = body.get("ticketno")
    mydescription = body.get("description")
    mytaskname = body.get("taskname")
    mysupportgroup = body.get("changeOwnerGroup")

    info = "Update change : {stat}, {tck}, {desc}, {tskn} {supg}".format(stat=mystatus, tck=myticketno,
                                                                         desc=mydescription, tskn=mytaskname,
                                                                         supg=mysupportgroup)
    logger.info(info)

    # Concatinate taskname + description
    sNewDescription = mytaskname + " | " + mydescription

    params = {
        "status": mystatus,
        "description": sNewDescription,
        "ticketno": myticketno,
        "changeOwnerGroup": mysupportgroup
    }

    MyChange = ValuemationHandler()
    lRet = MyChange.update_change(params)

    retStr = {"ticketno": lRet['data']['ticketno'], "changestatus": lRet['score']}
    return retStr, 200

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

    if lRet is None:
        return 'internal server error', 500
    elif lRet['score'] == 'success':
        retStr = {"ticketno": lRet['data']['ticketno'], "changestatus": lRet['score']}
        return retStr, 200
    elif lRet['score'] == 'danger' and lRet['message'] == 'ticket.not.found':
        retStr = {"ticketno": myticketno, "changestatus": lRet['message']}
        return retStr, 404
    else:
        retStr = {"ticketno": myticketno, "changestatus": "failed"}
        return retStr, 500

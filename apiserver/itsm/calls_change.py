from oim_logging import get_oim_logger


def update_change(body):
    logger = get_oim_logger()
    mystatus = body.get("status")
    myticketno = body.get("ticketno")
    mydescription = body.get("description")
    mysupportgroup = body.get("changeOwnerGroup")

    info = "Update change : {stat}, {tck}, {desc}, {supg}".format(stat=mystatus, tck=myticketno, desc=mydescription,
                                                                  supg=mysupportgroup)
    logger.info(info)

    retStr = {"ticketno": myticketno, "changestatus": mystatus}
    return retStr, 200

from api.CMDBHandler import CMDBHandler


def get_cmdb_items() -> str:
    cmdbh = CMDBHandler()
    infostatus = cmdbh.list_items()
    if len(infostatus) > 0:
        return infostatus
    else:
        return 'The CMDB is empty'


def get_cmdb_id(name) -> str:
    cmdbh = CMDBHandler()
    idlist = cmdbh.get_id(name)
    if len(idlist) > 1:
        return 'The following items contain {name} have the id: {idlist}'.format(name=name, idlist=idlist)  # noqa
    else:
        return 'There is no item with thie name'


def get_cmdb_item_info(id) -> str:
    cmdbh = CMDBHandler()
    info = cmdbh.get_item_info(id)
    if len(info) > 0:
        return 'Item {id} infos: {info}'.format(id=id, info=info)
    else:
        return 'The specified item id is invalid'

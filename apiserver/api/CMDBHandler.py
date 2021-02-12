from api.CMDBFactory import CMDBFactory


class CMDBHandler:
    def __init__(self):
        self.connector = CMDBFactory('api/cmdb_data.xml')

    def list_items(self):
        return self.connector.list_items()

    def add_item(self, name, itype, requester_id='b0123456', description=None):
        return self.connector.generate_item(name, requester_id, itype, description)     # noqa

    def get_item_info(self, itemid):
        return self.connector.get_info(itemid)

    def get_id(self, name):
        return self.connector.get_id(name)


if __name__ == '__main__':
    ch = CMDBHandler()
    print(ch.list_items())
#    ch.add_item()
#    ch.get_item_info('##')

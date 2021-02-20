from abc import ABC, abstractmethod
from zeep import Client
from datetime import datetime
# from zeep.transports import Transport
# from requests import Session
# from requests.auth import HTTPBasicAuth
# session = Session()
# session.auth = HTTPBasicAuth('b000', 'pass')


class OrchestraRequestHandler():        # This class knows SOAP
    def __init__(self, url):
        self.soap_client = Client(url)

    def list_operations(self):
        print('Namespace: ', self.soap_client.namespaces)
        print('Operations: ', self.soap_client.service._operations)

    def get_item_by_id(self, id):
        return self.soap_client.service.get_item_by_id(id)

    def get_item(self, filter):  # filter using one or dict of values
        return self.soap_client.service.get_item(**filter)

    def add_item(self, data):
        return self.soap_client.service.add_item(**data)

    def update_item(self, query):  # update one or dict of values
        return self.soap_client.service.update_item(**query)


class GenericCmdbHandler(ABC):
    @abstractmethod
    def get_item_by_id(self, id): pass

    @abstractmethod
    def get_item(self, filter): pass

    @abstractmethod
    def add_item(self, data): pass

    @abstractmethod
    def update_item(self, query): pass


class OrchestraCmdbHandler(GenericCmdbHandler):     # has no idea of SOAP
    def __init__(self):
        self.url = 'http://x10066984.balgroupit.com:8819/cmdb_request?wsdl'
        self.orchestra = OrchestraRequestHandler(self.url)

    def get_item_by_id(self, id):
        return self.orchestra.get_item_by_id(id)

    def get_item(self, field, pattern):  # Simplified version
        xml_filter = {'field': field, 'pattern': pattern}
        return self.orchestra.get_item(xml_filter)

    def add_item(self, field, data):  # data must be a dictionnary
        if data is None:  # create fake
            data = {'item': {'key': '77', '_value_1_': {
                    'id': 'svx-blibli',
                    'type': 'system',
                    'cidr': '1.2.3.4/18',
                    'active_from': '2021-01',
                    'active_until': '2023-12',
                    'provider': 'HCL',
                    'sla': 'gold',
                    'service_asset': 'Project 42',
                    'size': 'S3',
                    'order_id': '3298492',
                    'storage_type': 'NetApp+',
                    'patch_window': 'a',
                    'securty_zone': 'a',
                    'parent_id': '0',
                    'has_cid': 'true'}}}
        return self.orchestra.add_item(data)

    def update_item(self, query):  # query must be a dictionnary
        return self.orchestra.update_item(query)

    def inactivate_item(self):
        query = {'id': '1',
                 'field': 'active_until',
                 'value': datetime.ctime(datetime.utcnow())}
        print(query)
        return self.update_item(query)


if __name__ == '__main__':
    cmdb_h = OrchestraCmdbHandler()
    cmdb_h.orchestra.list_operations()
    for item in cmdb_h.get_item_by_id(
            'instance@svw-blablat001.balgroupit.com'):
        print(item)
    for item in cmdb_h.get_item('type', 'system'):
        print(item)

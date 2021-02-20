from abc import ABC, abstractmethod
from zeep import Client
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

    def get_item(self, filter):
        return self.soap_client.service.get_item(**filter)


class GenericCmdbHandler(ABC):
    @abstractmethod
    def get_item_by_id(self, id): pass

    def delete_item(self, id): pass     # Only update active_date

    def add_item(self): pass

    @abstractmethod
    def get_item(self, filter): pass


class OrchestraCmdbHandler(GenericCmdbHandler):     # This class has no idea of SOAP
    def __init__(self):
        self.url = 'http://x10066984.balgroupit.com:8819/cmdb_request?wsdl'
        self.orchestra = OrchestraRequestHandler(self.url)

    def get_item_by_id(self, id):
        return self.orchestra.get_item_by_id(id)

    def get_item(self, field, pattern):
        xml_filter = {'field': field, 'pattern': pattern}
        print(xml_filter['field'])
        return self.orchestra.get_item(xml_filter)


if __name__ == '__main__':
    cmdb_h = OrchestraCmdbHandler()
    cmdb_h.orchestra.list_operations()
    for item in cmdb_h.get_item_by_id('instance@svw-blablat001.balgroupit.com'):
        print(item)
    for item in cmdb_h.get_item('type', 'system'):
        print(item)

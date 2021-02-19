from abc import ABC, abstractmethod
from zeep import Client
# from zeep.transports import Transport
# from requests import Session
# from requests.auth import HTTPBasicAuth

orchestra_cmdb_webservice = 'http://x10066984.balgroupit.com:8819/get_cmdb_item?wsdl'

# session = Session()
# session.auth = HTTPBasicAuth('b000', 'pass')


class OrchestraRequestHandler():
    def __init__(self, url):
        self.soap_client = Client(url)

    def list_operations(self):
        print('Namespace: ', self.soap_client.namespaces)
        print('Operations: ', self.soap_client.service._operations)

    def get_item(self, id):
        return self.soap_client.service.get_item(id)


class GenericCmdbHandler(ABC):
    @abstractmethod
    def get_item(self, id): pass


class OrchestraCmdbHandler(GenericCmdbHandler):     # This class has no idea of SOAP
    def __init__(self):
        self.orchestra = OrchestraRequestHandler(orchestra_cmdb_webservice)

    def get_item(self, id):
        return self.orchestra.get_item(id)


if __name__ == '__main__':
    cmdb_h = OrchestraCmdbHandler()
    cmdb_h.orchestra.list_operations()
    for item in cmdb_h.get_item('instance@svw-blablat001.balgroupit.com'):
        print(item)

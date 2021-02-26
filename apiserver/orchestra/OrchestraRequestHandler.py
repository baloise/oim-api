# Version 0.16
from abc import ABC, abstractmethod
from zeep import Client
from random import random
# from datetime import datetime
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

    def get_asset(self, filter):
        return self.soap_client.service.get_asset(**filter)

    def deactivate_asset(self, id):
        return self.soap_client.service.deactivate_asset(id)

    def insert_asset(self, data):
        return self.soap_client.service.insert_asset(**data)

#    def update_item(self, query):  # update one or dict of values
#        return self.soap_client.service.update_item(**query)


class GenericCmdbHandler(ABC):

    @abstractmethod
    def get_asset(self, filter): pass

    @abstractmethod
    def deactivate_asset(self, query): pass

    @abstractmethod
    def insert_asset(self, data): pass


class OrchestraCmdbHandler(GenericCmdbHandler):     # has no idea of SOAP
    def __init__(self):
        self.url = 'http://127.0.0.1:8819/cmdb_request?wsdl'
        self.orchestra = OrchestraRequestHandler(self.url)

    def get_asset(self, field, pattern):
        xml_filter = {'field': field, 'pattern': pattern}
        return self.orchestra.get_asset(xml_filter)

    def deactivate_asset(self, id):
        return self.orchestra.deactivate_asset(id)

    def fake_ip(self):
        return '10.0.'+str(int(random()*256))+'.'+str(int(random()*256))+'/24'

    def fake_name(self):
        tmp = ''
        for i in range(0, 24):
            tmp += chr(48+int(random()*75))
        return tmp

    def insert_asset(self, data=None):  # data must be a dictionnary
        if data is None:  # create fake
            data = {'asset': {
                    'id': 0,
                    'name': self.fake_name(),
                    'type_id': int(1+random()*3),
                    'cidr': self.fake_ip(),
                    'active_since': '2020-11-01T07:15:00',
                    'active_until': '2030-12-31T17:40:00',
                    'provider_id': 1,
                    'sla_id': int(1+random()*3),
                    'service_id': int(1+random()*3),
                    'tshirt_size_id': int(1+random()*3),
                    'order_id': int(1+random()*999999),
                    'has_cid': 'true'}}
        return self.orchestra.insert_asset(data)

#    def update_asset(self, query):
#        query = {'id': '1',
#                 'field': 'active_until',
#                 'value': datetime.ctime(datetime.utcnow())}
#        print(query)
#        return self.update_asset(query)


if __name__ == '__main__':
    cmdb_h = OrchestraCmdbHandler()
    cmdb_h.orchestra.list_operations()
    print("List all assets")
    for asset in cmdb_h.get_asset('id', '%'):
        print(asset)
    print('_____________________')
    print("List all assets from type rhel")
    for asset in cmdb_h.get_asset('type', '%rhel%'):
        print(asset)
    print('_____________________')
    print('deactivate asset id=3')
    cmdb_h.deactivate_asset(3)
    print('insert a random asset')
    cmdb_h.insert_asset()

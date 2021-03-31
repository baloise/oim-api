from abc import ABC, abstractmethod
from zeep import Client
from adapter.OrchestraAdapters import cmdb_adapter, environment_adapter, cmdb_performance_adapter, provider_sla_adapter  # noqa E501
from ourCloud.OcStaticVars import ENVIRONMENT, TRANSLATE_TARGETS, METAL_CLASS, STORAGE_PERFORMANCE_LEVEL                 # noqa E501

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

    def select_system(self, filter):
        return self.soap_client.service.select_system(**filter)

#    def deactivate_asset(self, id):
#        return self.soap_client.service.deactivate_asset(id)

    def insert_system(self, data):
        return self.soap_client.service.insert_system(**data)

#    def update_item(self, query):  # update one or dict of values
#        return self.soap_client.service.update_item(**query)


class GenericCmdbHandler(ABC):

    #    @abstractmethod
    #    def get_asset(self, filter): pass

    #    @abstractmethod
    #    def deactivate_asset(self, query): pass

    @abstractmethod
    def insert_system(self, data): pass

    @abstractmethod
    def select_system(self, data): pass


class OrchestraCmdbHandler(GenericCmdbHandler):     # has no idea of SOAP
    def __init__(self):
        self.url = 'http://127.0.0.1:8819/sp_cmdb_soap?wsdl'
        self.orchestra = OrchestraRequestHandler(self.url)
        self.cmdb_perf = cmdb_performance_adapter().translate(STORAGE_PERFORMANCE_LEVEL.HIGH, TRANSLATE_TARGETS.CMDB)  # noqa E501
        self.cmdb_env_id = environment_adapter().translate(ENVIRONMENT.TEST, TRANSLATE_TARGETS.CMDB)    # noqa E501
        self.cmdb_sla_brz = provider_sla_adapter().translate(METAL_CLASS.GOLD)

    def select_system(self, field, pattern):
        xml_filter = {'field': field, 'pattern': pattern}
        return self.orchestra.select_system(xml_filter)

#    def deactivate_asset(self, id):
#        return self.orchestra.deactivate_asset(id)

#    def fake_ip(self):
#        return '10.0.'+str(int(random()*256))+'.'+str(int(random()*256))+'/24'

#    def fake_name(self):
#        tmp = ''
#        for i in range(0, 24):
#            tmp += chr(48+int(random()*75))
#        return tmp

    def insert_system(self, payload=None):  # payload must be a dictionnary
        payload.update(self.cmdb_env_id)
        payload.update(self.cmdb_sla_brz)
        payload.update(self.cmdb_perf)
        payload = {'AMA_SYSTEM':payload}
        print("[DBG] payload: {}".format(payload))
        if payload is not None:  # exits
            return self.orchestra.insert_system(payload)
        else:
            return None

#    def update_asset(self, query):
#        query = {'id': '1',
#                 'field': 'active_until',
#                 'value': datetime.ctime(datetime.utcnow())}
#        print(query)
#        return self.update_asset(query)


if __name__ == '__main__':
    cmdb_h = OrchestraCmdbHandler()
    cmdb_h.orchestra.list_operations()
#    print("List all assets")
#    for asset in cmdb_h.get_asset('id', '%'):
#        print(asset)
#    print('_____________________')
#    print("List all assets from type rhel")
#    for asset in cmdb_h.get_asset('type', '%rhel%'):
#        print(asset)
#    print('_____________________')
#    print('deactivate asset id=3')
#    cmdb_h.deactivate_asset(3)

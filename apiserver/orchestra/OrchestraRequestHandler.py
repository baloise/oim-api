from abc import ABC, abstractmethod
from zeep import Client
from adapter.OrchestraAdapters import cmdb_adapter, environment_adapter, cmdb_performance_adapter, provider_sla_adapter  # noqa E501
from ourCloud.OcStaticVars import ENVIRONMENT, TRANSLATE_TARGETS, METAL_CLASS, STORAGE_PERFORMANCE_LEVEL                 # noqa E501

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

    def select_like_system(self, filter):
        return self.soap_client.service.select_like_system(**filter)

    def select_system(self, filter):
        return self.soap_client.service.select_system(**filter)

    def deactivate_system(self, filter):
        return self.soap_client.service.deactivate_system(**filter)

    def delete_system(self, filter):
        return self.soap_client.service.delete_system(**filter)

    def insert_system(self, data):
        return self.soap_client.service.insert_system(**data)

    def update_system(self, data):
        return self.soap_client.service.update_system(**data)


class GenericCmdbHandler(ABC):

    @abstractmethod
    def update_system(self, data): pass

    @abstractmethod
    def deactivate_system(self, filter): pass

    @abstractmethod
    def delete_system(self, filter): pass

    @abstractmethod
    def insert_system(self, data): pass

    @abstractmethod
    def select_like_system(self, filter): pass

    @abstractmethod
    def select_system(self, filter): pass


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

    def select_like_system(self, field, pattern):
        xml_filter = {'field': field, 'pattern': pattern}
        return self.orchestra.select_like_system(xml_filter)

    def deactivate_system(self, field, pattern):
        xml_filter = {'field': field, 'pattern': pattern}
        return self.orchestra.deactivate_system(xml_filter)

    def delete_system(self, field, pattern):
        xml_filter = {'field': field, 'pattern': pattern}
        return self.orchestra.delete_system(xml_filter)

    def update_system(self, payload):
        payload.update(self.cmdb_env_id)
        payload.update(self.cmdb_sla_brz)
        payload.update(self.cmdb_perf)
        payload = {'AMA_SYSTEM': payload}
        print("[DBG] payload: {}".format(payload))
        return self.orchestra.update_system(payload)

    def insert_system(self, payload=None):  # payload must be a dictionnary
        payload.update(self.cmdb_env_id)
        payload.update(self.cmdb_sla_brz)
        payload.update(self.cmdb_perf)
        payload = {'AMA_SYSTEM': payload}
        print("[DBG] payload: {}".format(payload))
        if payload is not None:  # exits
            return self.orchestra.insert_system(payload)
        else:
            return None

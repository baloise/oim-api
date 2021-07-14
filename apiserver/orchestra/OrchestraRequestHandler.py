# Orca Request Handler - Version 21
#
from abc import ABC, abstractmethod
from zeep import Client
from adapter.OrchestraAdapters import cmdb_adapter, environment_adapter, cmdb_performance_adapter, provider_sla_adapter  # noqa E501
from ourCloud.OcStaticVars import ENVIRONMENT, TRANSLATE_TARGETS, METAL_CLASS, STORAGE_PERFORMANCE_LEVEL                 # noqa E501

from zeep.transports import Transport
from requests import Session
# from requests.auth import HTTPBasicAuth
session = Session()
session.verify = False
transport = Transport(session=session)
# session.auth = HTTPBasicAuth('b000', 'pass')


class OrchestraRequestHandler():        # This class knows SOAP
    def __init__(self, url):
        self.soap_client = Client(url, transport=transport)


    def list_operations(self):
        print('Namespace: ', self.soap_client.namespaces)
        print('Operations: ', self.soap_client.service._operations)

    def select_like_system(self, filter):
        return self.soap_client.service.select_like_system(**filter)

    def select_system(self, filter):
        return self.soap_client.service.select_system(**filter)

    def select_like_component(self, filter):
        return self.soap_client.service.select_like_component(**filter)

    def select_component(self, filter):
        return self.soap_client.service.select_component(**filter)

    def deactivate_system(self, filter):
        return self.soap_client.service.deactivate_system(**filter)

    def delete_component(self, filter):
        return self.soap_client.service.delete_component(**filter)

    def insert_component(self, data):
        return self.soap_client.service.insert_component(**data)

    def insert_system_full(self, data):
        return self.soap_client.service.insert_system_full(**data)

    def update_system(self, data):
        return self.soap_client.service.update_system(**data)

    def update_component(self, data):
        return self.soap_client.service.update_component(**data)

    def delete_system_full(self, filter):
        return self.soap_client.service.delete_system_full(**filter)


class GenericCmdbHandler(ABC):

    @abstractmethod
    def update_system(self, data): pass

    @abstractmethod
    def update_component(self, data): pass

    @abstractmethod
    def deactivate_system(self, filter): pass

    @abstractmethod
    def delete_system_full(self, filter): pass

    @abstractmethod
    def insert_system_full(self, data): pass

    @abstractmethod
    def select_like_system(self, filter): pass

    @abstractmethod
    def select_system(self, filter): pass

    @abstractmethod
    def select_like_component(self, filter): pass

    @abstractmethod
    def select_component(self, filter): pass

    @abstractmethod
    def delete_component(self, filter): pass

    @abstractmethod
    def insert_component(self, data): pass

class OrchestraCmdbHandler(GenericCmdbHandler):     # has no idea of SOAP
    def __init__(self):
        #self.url = 'https://127.0.0.1:8843/oim_cmdb_soap?wsdl'  
        self.url = 'https://sandbox-orchestra.balgroupit.com:8843/oim_cmdb_soap?wsdl'
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

    def select_component(self, field, pattern):
        xml_filter = {'field': field, 'pattern': pattern}
        return self.orchestra.select_component(xml_filter)

    def select_like_component(self, field, pattern):
        xml_filter = {'field': field, 'pattern': pattern}
        return self.orchestra.select_like_component(xml_filter)

    def deactivate_system(self, field, pattern):
        xml_filter = {'field': field, 'pattern': pattern}
        return self.orchestra.deactivate_system(xml_filter)

    def delete_system_full(self, field, pattern):
        xml_filter = {'field': field, 'pattern': pattern}
        return self.orchestra.delete_system_full(xml_filter)
        
    def delete_component(self, field, pattern):
        xml_filter = {'field': field, 'pattern': pattern}
        return self.orchestra.delete_component(xml_filter)

    def update_system(self, payload):
        payload.update(self.cmdb_env_id)
        payload.update(self.cmdb_sla_brz)
        payload.update(self.cmdb_perf)
        payload = {'AMA_SYSTEM': payload}
        print("[DBG] payload: {}".format(payload))
        return self.orchestra.update_system(payload)

    def update_component(self, payload):
        payload = {'AMA_COMPONENT': payload}
        print("[DBG] payload: {}".format(payload))
        return self.orchestra.update_component(payload)

    def insert_component(self, payload=None):
        payload = {'AMA_COMPONENT': payload}
        print("[DBG] payload: {}".format(payload))
        if payload is not None:  # exits
            return self.orchestra.insert_component(payload)
        else:
            return None

    def insert_system_full(self, payload=None):  # payload must be a dictionnary
        payload.update(self.cmdb_env_id)
        payload.update(self.cmdb_sla_brz)
        payload.update(self.cmdb_perf)
        payload = {'AMA_SYSTEM': payload}
        print("[DBG] payload: {}".format(payload))
        if payload is not None:  # exits
            return self.orchestra.insert_system_full(payload)
        else:
            return None

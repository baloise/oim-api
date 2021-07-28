# _________________________________
# Orca Request Handler - Version 21
# _________________________________
#
# from typing import ForwardRef
from abc import ABC, abstractmethod
from zeep import Client
from adapter.OrchestraAdapters import cmdb_adapter, environment_adapter, cmdb_performance_adapter, provider_sla_adapter  # noqa E501
from ourCloud.OcStaticVars import ENVIRONMENT, TRANSLATE_TARGETS, METAL_CLASS, STORAGE_PERFORMANCE_LEVEL , SERVICE_LEVEL                # noqa E501

from zeep.transports import Transport
from requests import Session
# from requests.auth import HTTPBasicAuth
session = Session()
session.verify = False
transport = Transport(session=session)
# session.auth = HTTPBasicAuth('user', 'pass')


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

    def select_like_ticket(self, filter):
        return self.soap_client.service.select_like_ticket(**filter)

    def select_ticket(self, filter):
        return self.soap_client.service.select_ticket(**filter)

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
    def select_ticket(self, filter): pass

    @abstractmethod
    def select_like_ticket(self, filter): pass

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
        self.url = 'https://localhost:8843/oim_cmdb_soap?wsdl' # noqa E501
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

    def select_ticket(self, field, pattern):
        xml_filter = {'field': field, 'pattern': pattern}
        return self.orchestra.select_ticket(xml_filter)

    def select_like_ticket(self, field, pattern):
        xml_filter = {'field': field, 'pattern': pattern}
        return self.orchestra.select_like_ticket(xml_filter)

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

    def insert_system_full(self, payload=None):  # payload must be a dictionnary # noqa E501
        payload.update(self.cmdb_env_id)
        payload.update(self.cmdb_sla_brz)
        payload.update(self.cmdb_perf)
        payload = {'AMA_SYSTEM': payload}
        print("[DBG] payload: {}".format(payload))
        if payload is not None:  # exits
            return self.orchestra.insert_system_full(payload)
        else:
            return None


class GenericChangeHandler(ABC):

    @abstractmethod
    def update_change(self, data): pass

    @abstractmethod
    def deactivate_change(self, filter): pass

    @abstractmethod
    def delete_change(self, filter): pass

    @abstractmethod
    def insert_system(self, data): pass

    @abstractmethod
    def select_like_change(self, filter): pass

    @abstractmethod
    def select_change(self, filter): pass


class OrchestraChangeHandler(GenericChangeHandler):     # has no idea of SOAP
    def __init__(self):
        self.url = 'http://127.0.0.1:8819/sp_cmdb_soap?wsdl'
        self.orchestra = OrchestraRequestHandler(self.url)
        self.cmdb_perf = cmdb_performance_adapter().translate(STORAGE_PERFORMANCE_LEVEL.HIGH, TRANSLATE_TARGETS.CMDB)  # noqa E501
        self.cmdb_env_id = environment_adapter().translate(ENVIRONMENT.TEST, TRANSLATE_TARGETS.CMDB)    # noqa E501
        self.cmdb_sla_brz = {"OIM_PROVIDER_SLA": provider_sla_adapter().translate(SERVICE_LEVEL.ELITE, TRANSLATE_TARGETS.CMDB) }    # noqa E501

    def select_change(self, field, pattern):
        xml_filter = {'field': field, 'pattern': pattern}
        return self.orchestra.select_system(xml_filter)

    # Maybe not needed for the change
    def select_like_change(self, field, pattern):
        xml_filter = {'field': field, 'pattern': pattern}
        return self.orchestra.select_like_system(xml_filter)

    # Maybe not needed for the change
    def deactivate_change(self, field, pattern):
        xml_filter = {'field': field, 'pattern': pattern}
        return self.orchestra.deactivate_system(xml_filter)

    # Maybe not needed for the change, not sure if we need to delete a change or a task # noqa E501
    def delete_change(self, field, pattern):
        xml_filter = {'field': field, 'pattern': pattern}
        return self.orchestra.delete_system(xml_filter)

    def update_change(self, payload):
        payload.update(self.cmdb_env_id)
        payload.update(self.cmdb_sla_brz)
        payload.update(self.cmdb_perf)
        payload = {'AMS_TICKET': payload}
        print("[DBG] payload: {}".format(payload))
        return self.orchestra.update_system(payload)

    def insert_change(self, payload=None):  # payload must be a dictionnary
        payload.update(self.cmdb_env_id)
        payload.update(self.cmdb_sla_brz)
        payload.update(self.cmdb_perf)
        payload = {'AMA_SYSTEM': payload}
        print("[DBG] payload: {}".format(payload))
        if payload is not None:  # exits
            return self.orchestra.insert_system(payload)
        else:
            return None

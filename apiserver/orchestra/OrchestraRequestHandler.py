# _________________________________
# Orca Request Handler - Version 21
# _________________________________
#
# from typing import ForwardRef
import logging
import os
from abc import ABC, abstractmethod
import sqlite3
from requests import Session
from requests.auth import HTTPBasicAuth
from zeep import Client, Settings, helpers
from zeep.cache import InMemoryCache, SqliteCache
from zeep.transports import Transport
from adapter.OrchestraAdapters import cmdb_performance_adapter, provider_sla_adapter  # noqa E501
from adapter.GenericAdapters import environment_adapter
from ourCloud.OcStaticVars import ENVIRONMENT, TRANSLATE_TARGETS, SERVICE_LEVEL, STORAGE_PERFORMANCE_LEVEL  # noqa E501
from oim_logging import get_oim_logger
# from pprint import pformat


class OrchestraRequestHandler():        # This class knows SOAP
    def __init__(
        self,
        url,
        username=None,
        password=None,
        timeout=10,
        zeep_cache_ttl=300,
        strict=True,
        xml_huge_tree=False,
    ):
        self.log = get_oim_logger()
        self.log.debug('Creating Orchestra RequestHandler...')

        # Detect debug mode and force zeep into it aswell
        if os.getenv('DEBUG', '').lower() == 'true':
            zeep_logger = logging.getLogger('zeep.transports')
            if zeep_logger:
                zeep_logger.setLevel(logging.DEBUG)

        self._session = Session()

        if os.getenv('TLS_NO_VERIFY', '').lower() == 'true':
            self._session.verify = False

        if username and password:
            # Authentication params given, setting it up
            self._session.auth = HTTPBasicAuth(username=username, password=password)

        self._cache = None
        zeep_cache_file = os.getenv('SOAP_CACHEDB', None)
        if zeep_cache_file:  # This fails on None (never set) and on empty (unset) alike
            try:
                self._cache = SqliteCache(path=zeep_cache_file, timeout=zeep_cache_ttl)
            except sqlite3.OperationalError as exc:
                self.log.warn(f'Error creating cache db file {zeep_cache_file}: {exc}')
                self.log.warn('Falling back to in-memory cache.')
                self._cache = InMemoryCache(timeout=zeep_cache_ttl)
            except RuntimeError:
                self.log.warn('The required sqlite dependency was not found.')
            except ValueError:
                self.log.warn('In-memory sqlite not supported for cache, ignoring')
        if not self._cache:  # If we reach this point without a valid _cache we fall back to in-memory
            self.log.debug('Creating in-memory cache for SOAP requests.')
            self._cache = InMemoryCache(timeout=zeep_cache_ttl)

        self._transport = Transport(
            session=self._session,
            timeout=timeout,  # Session timeout in seconds
            cache=self._cache,  # Reduce the remote calls to the WSDL
        )

        zeep_settings = Settings(
            strict=strict,
            xml_huge_tree=xml_huge_tree,
        )
        self.soap_client = Client(url, transport=self._transport, settings=zeep_settings)
        self.log.debug('Creating Orchestra RequestHandler...done.')

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
        self.url = 'https://svw-orcht003.balgroupit.com:8443/oim_cmdb_soap?wsdl' # noqa E501
        self.orchestra = OrchestraRequestHandler(self.url)
        self.cmdb_perf = cmdb_performance_adapter().translate(STORAGE_PERFORMANCE_LEVEL.HIGH, TRANSLATE_TARGETS.CMDB)  # noqa E501
        self.cmdb_env_id = environment_adapter().translate(ENVIRONMENT.TEST, TRANSLATE_TARGETS.CMDB)    # noqa E501
        self.cmdb_sla_brz = provider_sla_adapter().translate(SERVICE_LEVEL.PREMIUM, TRANSLATE_TARGETS.CMDB)

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
    def select_like_change(self, filter): pass

    @abstractmethod
    def select_change(self, filter): pass


class OrchestraChangeHandler(GenericChangeHandler):     # has no idea of SOAP
    def __init__(self):
        self.url = 'https://127.0.0.1:8843/oim_cmdb_soap?wsdl'
        self.orchestra = OrchestraRequestHandler(self.url)
        self.cmdb_perf = cmdb_performance_adapter().translate(STORAGE_PERFORMANCE_LEVEL.HIGH, TRANSLATE_TARGETS.CMDB)  # noqa E501
        self.cmdb_env_id = environment_adapter().translate(ENVIRONMENT.TEST, TRANSLATE_TARGETS.CMDB)    # noqa E501
        self.cmdb_sla_brz = {"OIM_PROVIDER_SLA": provider_sla_adapter().translate(SERVICE_LEVEL.ELITE, TRANSLATE_TARGETS.CMDB) }    # noqa E501
        self.logger = get_oim_logger()

    def select_change(self, field, pattern):
        xml_filter = {'field': field, 'pattern': pattern}
        ticketList = self.orchestra.select_ticket(xml_filter)
        amsTicketObj = ticketList[0]
        st = amsTicketObj.STATUS
        return st

    # Maybe not needed for the change
    def select_like_change(self, field, pattern):
        xml_filter = {'field': field, 'pattern': pattern}
        return self.orchestra.select_like_ticket(xml_filter)

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


class OrchestraServiceInfoHandler():
    def __init__(self, url=None):
        self.log = logging.getLogger()
        self.log.debug('Creating OSIH...')
        if not url:
            url = os.getenv('ORCHESTRA_SERVICEINFO_URL', None)
            if not url:
                self.log.error('Unable to locate ORCHESTRA_SERVICEINFO_URL. Failing...')
                return None
        self.url = url
        self.orchestra = OrchestraRequestHandler(
            self.url,
            username=os.getenv('ORCHESTRA_SERVICEINFO_USER', None),
            password=os.getenv('ORCHESTRA_SERVICEINFO_PASS', None),
            strict=False,
            xml_huge_tree=True,
        )
        if not self.orchestra.soap_client:
            self.log.error('Something went wrong creating the SOAP client. Failing...')
            return None

    def retrieveServicesByName(self, pattern):
        results = {'error': None}
        try:
            results = self.orchestra.soap_client.service.getServicesByName(pattern)
        except AttributeError:
            errMsg = 'Called method before successful constructor?!'
            self.log.error(errMsg)
            return {'error': errMsg}
        if results:
            results = helpers.serialize_object(results, dict)  # We serialize to a more portable data structure
        # self.log.debug(f'SOAP Results: {pformat(results)}')
        return results

    def retrievePersonById(self, id):
        if not self.orchestra:
            self.log.error('Called method before successful constructor?!')
            return False

        results = self.orchestra.soap_client.service.getPersonById(id)
        if results:
            results = helpers.serialize_object(results, dict)

        # self.log.debug(f'SOAP Results: {pformat(results)}')
        return results

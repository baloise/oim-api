from abc import ABC, abstractmethod
from zeep import Client
#from adapter.OrchestraAdapters import environment_adapter, cmdb_performance_adapter, provider_sla_adapter
#from ourCloud.OcStaticVars import ENVIRONMENT, TRANSLATE_TARGETS, METAL_CLASS, STORAGE_PERFORMANCE_LEVEL   # noqa E501

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

#    def get_asset(self, filter):
#        return self.soap_client.service.get_asset(**filter)

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


class OrchestraCmdbHandler(GenericCmdbHandler):     # has no idea of SOAP
    def __init__(self):
        self.url = 'http://127.0.0.1:8819/sp_cmdb_soap?wsdl'
        self.orchestra = OrchestraRequestHandler(self.url)
        # self.cmadapter = cmdb_performance_adapter()
        # self.cmdb_perf = cmdb_adapter.translate(STORAGE_PERFORMANCE_LEVEL.HIGH, TRANSLATE_TARGETS.CMDB)  # noqa E501
        # self.environment_adapter = environment_adapter()
        # self.cmdb_env_id = environment_adapter.translate(ENVIRONMENT.TEST, TRANSLATE_TARGETS.CMDB)    # noqa E501
        # self.prosla_adapter = provider_sla_adapter()
        # self.cmdb_sla_brz = provider_sla_adapter.translate(METAL_CLASS.GOLD)
        # print("[DBG] Performance: {}".format(self.cmdb_perf))
        # print("[DBG] Environment: {}".format(self.cmdb_env_id))
        # print("[DBG] SLA: {}".format(self.cmdb_sla_brz))

#    def get_asset(self, field, pattern):
#        xml_filter = {'field': field, 'pattern': pattern}
#        return self.orchestra.get_asset(xml_filter)

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
        # payload.update(self.cmdb_env_id)
        # payload.update(self.cmdb_sla_brz)
        # payload.update(self.cmdb_perf)
        print("[DBG] payload: {}".format(payload))
        if payload is None:  # exits
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

    print('insert a system')
    payload = {
      "STATUS": "ACT",
      "NAME": "manu_210330_1057",
      "DOMAIN_ID": 8,
      "VALIDFROM": "2021-03-17T00:00:00",
      "VALIDTO": "2100-01-01T00:00:00",
      "OIM_TSHIRT_SIZE": "S1",
      "SYSTEMTYPE_ID": 100162,
      "OIM_CID": "NO CID",
      "OIM_INTERNAL_AUDIT": "",
      "OIM_MIRRORING": "Not Mirrored",
      "SHORTTEXT": "Added by OIM API",
      "SERVICE_INSTANCE": "Medium",
      "BUSINESSPART_ID": 100233,
      "OIM_PATCH_WINDOW": "H-SERVER-SCCM-BCH-LV33-03-MI-2100",
      "OIM_PROVIDER_SERVICELINE": "Server"
    }

    print("payload: {}".format(payload))
    sp_result = cmdb_h.insert_system(payload)
    print("[SP Result] ", sp_result)

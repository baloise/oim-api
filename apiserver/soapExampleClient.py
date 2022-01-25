from adapter.OrchestraAdapters import cmdb_performance_adapter, provider_sla_adapter
from adapter.GenericAdapters import environment_adapter
import zeep
from ourCloud.OcStaticVars import ENVIRONMENT, TRANSLATE_TARGETS, METAL_CLASS, STORAGE_PERFORMANCE_LEVEL


cmadapter = cmdb_performance_adapter()
cmdb_perf = cmadapter.translate(STORAGE_PERFORMANCE_LEVEL.HIGH, TRANSLATE_TARGETS.CMDB)
print("Performance: {}".format(cmdb_perf))

environment_adapter = environment_adapter()
cmdb_env_id = environment_adapter.translate(ENVIRONMENT.TEST, TRANSLATE_TARGETS.CMDB)
print("Environment: {}".format(cmdb_env_id))

prosla_adapter = provider_sla_adapter()
cmdb_sla_brz = prosla_adapter.translate(METAL_CLASS.GOLD)
print("SLA: {}".format(cmdb_sla_brz))
print("XXXX")

wsdl = 'http://read.the.code:8819/and/correct/me?wsdl'  # noqa E501
client = zeep.Client(wsdl=wsdl)
# service = client.bind('sp_cmdb_mini', 'PortSoapBinding_0')
service = client.bind('sp_cmdb_soap', 'PortSoapBinding_0')


print("Namespaces: {}".format(client.namespaces))
payload = {
  "STATUS": "ACT",
  "NAME": "dummy1",
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

payload.update(cmdb_env_id)
payload.update(cmdb_sla_brz)
payload.update(cmdb_perf)
print("payload: {}".format(payload))
fff = service.insert_system(AMA_SYSTEM=payload)
print(fff)

from adapter.OrchestraAdapters import environment_adapter, cmdb_performance_adapter, provider_sla_adapter
import zeep
from ourCloud.OcStaticVars import ENVIRONMENT


adapter = environment_adapter()
adapter.read_file()

# adapter.get_apinames()
# adapter.get_orcaids()
# adapter.get_ocids()


cmadapter = cmdb_performance_adapter()
cmadapter.read_file()
cmadapter.get_apiperformance()
res = cmadapter.translate("high")
print(res)

environment_adapter = environment_adapter()
environment_adapter.read_file()
cmdb_env_id = environment_adapter.translate(ENVIRONMENT.TEST)
print(cmdb_env_id)

prosla_adapter = provider_sla_adapter()
prosla_adapter.read_file()
cmdb_sla_brz = prosla_adapter.translate("goldi")

print("XXXX")
# wsdl = 'http://x10037275.balgroupit.com:8819/mini_action?wsdl'
wsdl = 'http://x10037275.balgroupit.com:8819/Orchestra/48dbe175-f1fa-4e60-ad8c-4db85ffc036f/83/PortSoapBinding_0/sp_cmdb_soap?wsdl'  # noqa E501
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
  "OIM_PERFORMANCE": "Medium",
  "SHORTTEXT": "Added by OIM API",
  "SERVICE_INSTANCE": "Medium",
  "BUSINESSPART_ID": 100233,
  "OIM_PATCH_WINDOW": "H-SERVER-SCCM-BCH-LV33-03-MI-2100",
  "OIM_PROVIDER_SERVICELINE": "Server"
}

payload.update(cmdb_env_id)
payload.update(cmdb_sla_brz)
print("payload: {}".format(payload))
fff = service.insert_system(AMA_SYSTEM=payload)
print(fff)

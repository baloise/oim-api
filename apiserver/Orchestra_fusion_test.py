from orchestra.OrchestraRequestHandler import OrchestraCmdbHandler


cmdb_h = OrchestraCmdbHandler()
cmdb_h.orchestra.list_operations()

for system in cmdb_h.select_system('NAME', '%manu_%'):
    print(system.NAME, system.SYSTEM_ID, system.STATUS)

print('insert a system')
payload = {
      "STATUS": "ACT",
      "NAME": "manu_5",
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

sp_result = cmdb_h.insert_system(payload)
print("[SP Result] ", sp_result)

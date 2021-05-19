from orchestra.OrchestraRequestHandler import OrchestraCmdbHandler


cmdb_h = OrchestraCmdbHandler()
cmdb_h.orchestra.list_operations()

print('create a change(insert)')
# need input from ITSM Team about which fields
payload = {
      "SYSTEM_ID": 0,
      "STATUS": "ACT",
      "NAME": "manu_9",
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

print('select a change')
# Get a change incl. the linked task
sp_result = cmdb_h.deactivate_system('SYSTEM_ID', '101460')
sp_result = cmdb_h.deactivate_system('NAME', 'manu_23')

# Delete a change incl. tasks
print('delete a change')
sp_result = cmdb_h.delete_system('NAME', 'manu_8')

# Update, but need input from ITSM Team
print('update a change')
payload = {
      "SYSTEM_ID": 101441,
      "NAME": "manu_6",
      "VALIDFROM": "2345-01-10T00:00:00",
      "OIM_TSHIRT_SIZE": "S3"
    }
cmdb_h.update_system(payload)

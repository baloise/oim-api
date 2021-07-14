from orchestra.OrchestraRequestHandler import OrchestraCmdbHandler


cmdb_h = OrchestraCmdbHandler()

print('\nList all services:\n')
cmdb_h.orchestra.list_operations()

print('\n\nList all systems with where like\n')
for system in cmdb_h.select_like_system('NAME', '%manu%'):
    print(system.NAME, system.SYSTEM_ID, system.STATUS)

print('\n\nList all systems with where =\n')
for system in cmdb_h.select_system('NAME', 'manu_6'):
    print(system.NAME, system.SYSTEM_ID, system.STATUS)

print('\n\ninsert a system full\n')
payload = {
      "SYSTEM_ID": 0,
      "STATUS": "ACT",
      "NAME": "manu_sysfull_80",
      "DOMAIN_ID": 8,
      "VALIDFROM": "2021-03-17T00:00:00",
      "VALIDTO": "2100-01-01T00:00:00",
      "OIM_TSHIRT_SIZE": "S1",
      "SYSTEMTYPE_ID": 100162,
      "OIM_CID": "NO CID",
      "OIM_INTERNAL_AUDIT": "",
      "OIM_MIRRORING": "Not Mirrored",
      "SHORTTEXT": "Added by OIM API 1",
      "BUSINESSPART_ID": 100233,
      "OIM_PATCH_WINDOW": "H-SERVER-SCCM-BCH-LV33-03-MI-2100",
      "OIM_PROVIDER_SERVICELINE": "Server",
      "AMA_COMPONENT": {
            "TYPE_ID": 100436,
            "STATUS": "ACT",
            "OIM_STORAGE_CLASS": "HIGH M",
            "OIM_TSHIRT_SIZE": "M1",
            "AMA_COMPSYSTEM": {
                "VALIDFROM": "2021-04-07T00:00:00",
                "VALIDTO": "2100-01-01T00:00:00",
                "IS_MAINC": "N"
            }
        }
    }


sp_result = cmdb_h.insert_system_full(payload)
print("[SP Result] ", sp_result)


sp_result = cmdb_h.deactivate_system('SYSTEM_ID', '101460')
sp_result = cmdb_h.deactivate_system('NAME', 'manu_23')

sp_result = cmdb_h.delete_system_full('NAME', 'manu_sysfull_79')

print('\n\nupdate a system\n')
payload = {
      "SYSTEM_ID": 101441,
      "NAME": "manu_6",
      "VALIDFROM": "2345-01-10T00:00:00",
      "OIM_TSHIRT_SIZE": "S3"
    }
cmdb_h.update_system(payload)

# -----
print('\n\nList all components with where like\n')
cmdb_h.select_like_component('STATUS', '%ACT')

payload = {
            "TYPE_ID": 100436,
            "STATUS": "ACT",
            "OIM_STORAGE_CLASS": "HIGH M",
            "OIM_TSHIRT_SIZE": "M1"
        }

sp_result = cmdb_h.insert_component(payload)
print("[SP Result] ", sp_result)

print('\n\nupdate a system\n')
payload = {
      "STATUS" : "INACT",
      "OIM_TSHIRT_SIZE": "S3"
    }
cmdb_h.update_system(payload)

cmdb_h.delete_component('STATUS','INACT')

print('\n\nList all components with where like\n')
cmdb_h.select_like_component('STATUS', '%ACT')


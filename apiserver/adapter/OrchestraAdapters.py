import os
import json
import jmespath
from ourCloud.OcStaticVars import ENVIRONMENT, TRANSLATE_TARGETS, METAL_CLASS, STORAGE_PERFORMANCE_LEVEL


class AbstractAdapter:
    
    def __init__(self):
        self.json = None
        self.field = None
        self.file = None

    def read_file(self):
#        print('[DBG] ', os.listdir())
        with open(self.file, 'r') as myfile:
            data = myfile.read()
            self.json = json.loads(data)


class provider_sla_adapter(AbstractAdapter):

    def __init__(self):
        self.json = None
        self.field = "provider_sla"
        self.file = 'apiserver/mappings/sla_mappings.json'
        self.read_file()

    def translate(self, sla_level: METAL_CLASS) -> dict:
        json_query = "{field}[?level=='{apiname}'].{translation}".format(field=self.field, apiname=sla_level.value,
                                                                         translation="orcaid")
        res = jmespath.search(json_query, self.json)
        return {"OIM_PROVIDER_SLA": res[0]}


class environment_adapter(AbstractAdapter):

    def __init__(self):
        self.json = None
        self.field = "environment"
        self.file = 'apiserver/mappings/environment_mappings.json'
        self.read_file()

    # def get_apinames(self):
    #     for env in self.json[self.field]:
    #         print(env['name'])

    # def get_orcaids(self):
    #     for env in self.json[self.field]:
    #         print(env['orcaid'])

    # def get_ocids(self):
    #     for env in self.json[self.field]:
    #         print(env['ocid'])

    def translate(self, envir: ENVIRONMENT, target: TRANSLATE_TARGETS) -> dict:
        if TRANSLATE_TARGETS.CMDB == target:
            json_query = "{field}[?name=='{apiname}'].{translation}".format(field=self.field, apiname=envir.apiname,
                                                                            translation="orcaid")
            res = jmespath.search(json_query, self.json)
            return {"ENVIRONMENT_ID": res[0]}   # dict required by orca
        elif TRANSLATE_TARGETS.OURCLOUD == target:
            json_query = "{field}[?name=='{apiname}'].{translation}".format(field=self.field, apiname=envir.apiname,
                                                                            translation="ocid")
            res = jmespath.search(json_query, self.json)
            return {"ENVIRONMENT_ID": res[0]}   # TODO: format required by ourcloud tbd
        return None


class cmdb_adapter(AbstractAdapter):

    def __init__(self):
        self.json = None
        self.file = 'apiserver/mappings/cmdb_mappings.json'


class cmdb_status_adapter(cmdb_adapter):

    def __init__(self):
        super().__init__()
        self.field = "systemstatus"

    def get_apistatuses(self):
        for env in self.json[self.field]:
            print(env['active'])

    def get_orcastatuses(self):
        for env in self.json[self.field]:
            print(env['orcastatus'])


class cmdb_types_adapter(cmdb_adapter):

    def __init__(self):
        super().__init__()
        self.field = "systemtypes"

    def get_apitypes(self):
        for env in self.json[self.field]:
            print(env['type'])

    def get_orcanames(self):
        for env in self.json[self.field]:
            print(env['orcaname'])

    def get_orcaids(self):
        for env in self.json[self.field]:
            print(env['ocid'])


class cmdb_mirror_adapter(cmdb_adapter):

    def __init__(self):
        super().__init__()
        self.field = "storagemirror"

    def get_apimirrors(self):
        for env in self.json[self.field]:
            print(env['mirrored'])

    def get_orcanames(self):
        for env in self.json[self.field]:
            print(env['orcaname'])

    def get_ocids(self):
        for env in self.json[self.field]:
            print(env['ocid'])


class cmdb_performance_adapter(cmdb_adapter):

    def __init__(self):
        super().__init__()
        self.field = "storageperformance"
        self.read_file()

    # def get_apiperformance(self):
    #     for env in self.json[self.field]:
    #         print(env['name'])

    # def get_orcanames(self):
    #     for env in self.json[self.field]:
    #         print(env['orcaname'])

    # def get_ocids(self):
    #     for env in self.json[self.field]:
    #         print(env['ocid'])

    def translate(self, name: STORAGE_PERFORMANCE_LEVEL, target: TRANSLATE_TARGETS):
        if TRANSLATE_TARGETS.CMDB == target:
            json_query = "{field}[?name=='{apiname}'].{translation}".format(field=self.field, apiname=name.value,
                                                                            translation="orcaname")
            res = jmespath.search(json_query, self.json)
            return {"OIM_PERFORMANCE": res[0]}  # dict required by orca
        elif TRANSLATE_TARGETS.OURCLOUD == target:
            json_query = "{field}[?name=='{apiname}'].{translation}".format(field=self.field, apiname=name.value,
                                                                            translation="ocid")
            res = jmespath.search(json_query, self.json)
            return {"OIM_PERFORMANCE": res[0]}   # TODO: format required by ourcloud tbd

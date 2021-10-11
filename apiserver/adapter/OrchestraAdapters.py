import jmespath
from ourCloud.OcStaticVars import TRANSLATE_TARGETS, SERVICE_LEVEL, STORAGE_PERFORMANCE_LEVEL
from adapter.GenericAdapters import AbstractAdapter


class provider_sla_adapter(AbstractAdapter):

    def __init__(self):
        self.json = None
        self.field = "provider_sla"
        self.file = 'mappings/sla_mappings.json'
        self.read_file()

    def translate(self, sla_level: SERVICE_LEVEL, target: TRANSLATE_TARGETS) -> dict:
        if TRANSLATE_TARGETS.CMDB == target:
            json_query = "{field}[?level=='{apiname}'].{translation}".format(field=self.field, apiname=sla_level.value,
                                                                             translation="orcaid")
            res = jmespath.search(json_query, self.json)
            return {"OIM_PROVIDER_SLA": res[0]}
        elif TRANSLATE_TARGETS.OURCLOUD == target:
            json_query = "{field}[?level=='{apiname}'].{translation}".format(field=self.field, apiname=sla_level.value,
                                                                             translation="ocid")
            res = jmespath.search(json_query, self.json)
            return res[0]   # TODO: format required by ourcloud tbd
        return None


class cmdb_adapter(AbstractAdapter):

    def __init__(self):
        self.json = None
        self.file = 'mappings/cmdb_mappings.json'


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

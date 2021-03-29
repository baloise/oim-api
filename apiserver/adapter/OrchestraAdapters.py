import json
import jmespath
from ourCloud.OcStaticVars import ENVIRONMENT


class AbstractAdapter:

    def read_file(self):
        with open(self.file, 'r') as myfile:
            data = myfile.read()
            self.json = json.loads(data)


class provider_sla_adapter(AbstractAdapter):

    def __init__(self):
        self.json = None
        self.field = "provider_sla"
        self.file = 'mappings/sla_mappings.json'

    def translate(self, sla_level: str) -> dict:
        json_query = "{field}[?level=='{apiname}'].{translation}".format(field=self.field, apiname=sla_level,
                                                                         translation="orcaid")
        res = jmespath.search(json_query, self.json)
        return {"OIM_PROVIDER_SLA": res[0]}


class environment_adapter(AbstractAdapter):

    def __init__(self):
        self.json = None
        self.field = "environment"
        self.file = 'mappings/environment_mappings.json'

    def get_apinames(self):
        for env in self.json[self.field]:
            print(env['name'])

    def get_orcaids(self):
        for env in self.json[self.field]:
            print(env['orcaid'])

    def get_ocids(self):
        for env in self.json[self.field]:
            print(env['ocid'])

    def translate(self, envir: ENVIRONMENT) -> dict:
        json_query = "{field}[?name=='{apiname}'].{translation}".format(field=self.field, apiname=envir.apiname,
                                                                        translation="orcaid")
        res = jmespath.search(json_query, self.json)
        return {"ENVIRONMENT_ID": res[0]}


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

    def get_apiperformance(self):
        for env in self.json[self.field]:
            print(env['name'])

    def get_orcanames(self):
        for env in self.json[self.field]:
            print(env['orcaname'])

    def translate(self, name):
        json_query = "{field}[?name=='{apiname}'].{translation}".format(field=self.field, apiname=name,
                                                                        translation="orcaname")
        res = jmespath.search(json_query, self.json)
        return res[0]

    def get_ocids(self):
        for env in self.json[self.field]:
            print(env['ocid'])

import json
import jmespath
from ourCloud.OcStaticVars import ENVIRONMENT, TRANSLATE_TARGETS


class AbstractAdapter:

    def __init__(self):
        self.json = None
        self.field = None
        self.file = None

    def read_file(self):
        with open(self.file, 'r') as myfile:
            data = myfile.read()
            self.json = json.loads(data)


class environment_adapter(AbstractAdapter):

    def __init__(self):
        self.json = None
        self.field = "environment"
        self.file = 'mappings/environment_mappings.json'
        self.read_file()

    def translate(self, envir: ENVIRONMENT, target: TRANSLATE_TARGETS) -> dict:
        if TRANSLATE_TARGETS.CMDB == target:
            json_query = "{field}[?name=='{oimname}'].{translation}".format(field=self.field, oimname=envir.oimname,
                                                                            translation="orcaid")
            res = jmespath.search(json_query, self.json)
            return {"ENVIRONMENT_ID": res[0]}   # dict required by orca
        elif TRANSLATE_TARGETS.OURCLOUD == target:
            json_query = "{field}[?name=='{oimname}'].{translation}".format(field=self.field, oimname=envir.oimname,
                                                                            translation="ocid")
            res = jmespath.search(json_query, self.json)
            return {"ENVIRONMENT_ID": res[0]}   # TODO: format required by ourcloud tbd
        elif TRANSLATE_TARGETS.VAL == target:
            json_query = "{field}[?name=='{oimname}'].{translation}".format(field=self.field, oimname=envir.oimname,
                                                                            translation="orcaid")
            res = jmespath.search(json_query, self.json)
            return res[0]
        return None

import json
import jmespath
from ourCloud.OcStaticVars import ENVIRONMENT, TRANSLATE_TARGETS


class AbstractConverter:

    def __init__(self):
        self.json = None
        self.field = None
        self.file = None

    def read_file(self):
        with open(self.file, 'r') as myfile:
            data = myfile.read()
            self.json = json.loads(data)


class EnvironmentConverter(AbstractConverter):

    def __init__(self):
        self.json = None
        self.field = "environment"
        self.file = 'mappings/environment_mappings.json'
        self.read_file()

    def translate(self, envirStr: str, source: TRANSLATE_TARGETS) -> ENVIRONMENT:
        if TRANSLATE_TARGETS.OURCLOUD == source:
            json_query = "{field}[?ocid=='{ocname}'].{attr}".format(field=self.field, ocname=envirStr.upper(),
                                                                    attr="name")
            res = jmespath.search(json_query, self.json)
            return ENVIRONMENT.from_str(res[0])
        return None

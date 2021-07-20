import json
import jmespath
from ourCloud.OcStaticVars import SBU, OC_CATALOGOFFERINGS


class AbstractAdapter:

    def __init__(self):
        self.json = None
        self.field = None
        self.file = None

    def read_file(self):
        with open(self.file, 'r') as myfile:
            data = myfile.read()
            self.json = json.loads(data)


class SbuAdapter(AbstractAdapter):

    def __init__(self):
        self.json = None
        self.field = "sbu"
        self.file = 'apiserver/mappings/sbu_mappings.json'
        self.read_file()

    def translate(self, sbu: SBU) -> dict:
        json_query = "{field}[?name=='{apiname}'].{translation}".format(field=self.field, apiname=sbu.value,
                                                                        translation="ocid")
        res = jmespath.search(json_query, self.json)
        return res[0]


class OfferingAdapter(AbstractAdapter):

    def __init__(self):
        self.json = None
        self.field = "offering"
        self.file = 'apiserver/mappings/offerings_mappings.json'
        self.read_file()

    def translate(self, offering: OC_CATALOGOFFERINGS, attribute: str) -> dict:
        if attribute not in ['ocid', 'occatalogid']:
            return None
        json_query = "{field}[?name=='{apiname}'].{translation}".format(field=self.field, apiname=offering.value,
                                                                        translation=attribute)
        res = jmespath.search(json_query, self.json)
        return res[0]

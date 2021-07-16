import json
import jmespath
from ourCloud.OcStaticVars import ENVIRONMENT, TRANSLATE_TARGETS, SBU


class AbstractAdapter:

    def __init__(self):
        self.json = None
        self.field = None
        self.file = None

    def read_file(self):
        with open(self.file, 'r') as myfile:
            data = myfile.read()
            self.json = json.loads(data)

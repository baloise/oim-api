import unittest
import yaml
from api.calls_automagic import validateYML


class TestValidateYML(unittest.TestCase):
    def obj_to_yaml(self, the_object):
        return yaml.dump(the_object)

    def yaml_to_obj(self, payload):
        return yaml.load(payload, Loader=yaml.FullLoader)

    def test_100_valid_ampgdb(self):
        with open('schemas/yamlvalidation/references/postgres-db-yaml.yaml') as f:
            body = f.read()
        return_message, return_code = validateYML(body)
        # print(return_message)
        assert return_code == 200

    def test_200_nokind(self):
        # kind attrib missing
        with open('schemas/yamlvalidation/references/postgres-db-yaml.yaml') as f:
            body = f.read()
            obj = self.yaml_to_obj(body)
        del obj['kind']
        body = self.obj_to_yaml(obj)
        # print("Corrupt no-kind yaml: \n" + body)
        _, return_code = validateYML(body)
        assert return_code == 422

    def test_201_unknown_kind(self):
        # kind points to something we have no schemahints for
        with open('schemas/yamlvalidation/references/postgres-db-yaml.yaml') as f:
            body = f.read()
            obj = self.yaml_to_obj(body)
        obj['kind'] = 'FakeKindUnitTests'
        body = self.obj_to_yaml(obj)
        _, return_code = validateYML(body)
        assert return_code == 422

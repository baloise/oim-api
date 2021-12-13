import unittest
import yaml
import os
from pathlib import Path
from api.calls_automagic import validateYML


class TestValidateYML(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(TestValidateYML, self).__init__(*args, **kwargs)
        self.base_dir = Path(Path(os.path.dirname(os.path.abspath(__file__))), Path('..'))
        self.reference_dir = self.base_dir / 'schemas' / 'yamlvalidation' / 'references'

    def obj_to_yaml(self, the_object):
        return yaml.dump(the_object)

    def yaml_to_obj(self, payload):
        return yaml.load(payload, Loader=yaml.FullLoader)

    def test_100_valid_ampgdb(self):
        with open(self.reference_dir / 'postgres-db-yaml.yaml', 'r') as f:
            body = f.read()
        return_message, return_code = validateYML(body)
        # print(return_message)
        assert return_code == 200

    def test_200_nokind(self):
        # kind attrib missing
        with open(self.reference_dir / 'postgres-db-yaml.yaml', 'r') as f:
            body = f.read()
            obj = self.yaml_to_obj(body)
        del obj['kind']
        body = self.obj_to_yaml(obj)
        # print("Corrupt no-kind yaml: \n" + body)
        _, return_code = validateYML(body)
        assert return_code == 422

    def test_201_unknown_kind(self):
        # kind points to something we have no schemahints for
        with open(self.reference_dir / 'postgres-db-yaml.yaml', 'r') as f:
            body = f.read()
            obj = self.yaml_to_obj(body)
        obj['kind'] = 'FakeKindUnitTests'
        body = self.obj_to_yaml(obj)
        _, return_code = validateYML(body)
        assert return_code == 422


if __name__ == '__main__':
    unittest.main(verbosity=2)

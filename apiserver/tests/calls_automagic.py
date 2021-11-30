import unittest
import yaml
from api.calls_automagic import validateYML


class TestValidateYML(unittest.TestCase):
    valid_yaml_vm = """
apiVersion: v1alpha1
kind: VirtualMachine
metadata:
  name: corellia
  serviceOwner: b012345
  labels:
    environment: test
spec:
  status: active # one of active / decommissioned / deleted
  id: 28f5a2fb-ecce-4dd6-9b89-bc2319da9634
  adminRole: F-AAD-APP-XYZ-SH-T-BizDevOps-Engineer
  ServerSizeCode: S1
  DriveSize : 5
  operatingSystem:
    kind: RHEL
    version: 8
    """

    def toYaml(self, the_object):
        return yaml.dump(the_object)

    def setUp(self):
        self.body = self.valid_yaml_vm
        self.obj = yaml.load(self.valid_yaml_vm, Loader=yaml.FullLoader)

    def tearDown(self):
        self.body = ''
        self.obj = None

    def test_1_validvm(self):
        _, return_code = validateYML(self.body)
        assert return_code == 200

    def test_2_nokind(self):
        del self.obj['kind']
        body = self.toYaml(self.obj)
        _, return_code = validateYML(body)
        assert return_code == 422

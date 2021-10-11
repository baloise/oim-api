
import urllib3
from ourCloud.auth import TokenAuthHandler
import json
from .ocPaths.CreateVmPath import CreateVmPath
from .ocPaths.DeleteVmPath import DeleteVmPath
from .ocPaths.GetExtendedParametersPath import GetExtendedParametersPath
from .ocPaths.GetRequestStatusPath import GetRequestStatusPath
from .ocPaths.GetAllCiDetailsPath import GetAllCiDetailsPath
from .ocPaths.GetCiMasterDataPath import GetCiMasterDataPath
from .ocPaths.AbstractOcPath import AbstractOcPath
from models.orders import VmOrderItem, Person
from oim_logging import get_oim_logger


class doubleQuoteDict(dict):

    def __str__(self):
        return json.dumps(self)

    def __repr__(self):
        return json.dumps(self)


class OurCloudRequestHandler:
    __instance = None

    @staticmethod
    def getInstance():
        """ Static access method. """
        logger = get_oim_logger()
        logger.debug("Initializing request handler")
        if OurCloudRequestHandler.__instance is None:
            OurCloudRequestHandler()
        return OurCloudRequestHandler.__instance

    def __init__(self):
        if OurCloudRequestHandler.__instance is not None:
            raise Exception("This is a singleton class.")
        else:
            OurCloudRequestHandler.__instance = self
            abstractPath = AbstractOcPath()     # required to provide default url
            self.auth = TokenAuthHandler(abstractPath)
            urllib3.disable_warnings()

    def create_vm(self, item: VmOrderItem, requester: Person, changeno: str):
        path = CreateVmPath(item)
        path.set_requester(requester)
        path.set_changeno(changeno)
        path.set_auth_token_handler(self.auth)
        res = path.send_request()
        return res

    def delete_vm(self, hostname: str):
        path = DeleteVmPath(hostname)
        path.set_auth_token_handler(self.auth)
        res = path.send_request()
        return res

    def get_extended_request_parameters(self, requestno, parameters: list) -> dict:
        path = GetExtendedParametersPath(requestno=requestno, parameters=parameters, listall=False)
        path.set_auth_token_handler(self.auth)
        res = path.send_request()
        return res

    def list_extended_request_parameters(self, requestno):
        path = GetExtendedParametersPath(requestno=requestno, parameters=None, listall=True)
        path.set_auth_token_handler(self.auth)
        res = path.send_request()
        return res

    def get_request_status(self, requestno) -> str:
        path = GetRequestStatusPath(requestno)
        path.set_auth_token_handler(self.auth)
        res = path.send_request()
        return res

    def get_all_ci_details(self, data_filter=''):
        path = GetAllCiDetailsPath(data_filter=data_filter)
        path.set_auth_token_handler(self.auth)
        res = path.send_request()
        return res

    def get_specific_ci_object_data(self, object_name, object_type='VM'):
        path = GetCiMasterDataPath(object_name=object_name, object_type=object_type)
        path.set_auth_token_handler(self.auth)
        res = path.send_request()
        return res

import os
from abc import ABC  # abstractmethod
import json
import jmespath
from oim_logging import get_oim_logger
from ourCloud.OcStaticVars import OC_RESPONSEFIELD, OC_REQUESTFIELD, OC_OBJECTTYPE, OC_ACTIONMAME, OC_LANGUAGE, OC_CATALOGOFFERINGS  # noqa F401


class AbstractOcPath(ABC):
    OC_RESPONSEFIELD, OC_REQUESTFIELD, OC_OBJECTTYPE, OC_ACTIONMAME, OC_LANGUAGE, OC_CATALOGOFFERINGS

    def __init__(self):
        self.log = get_oim_logger()

    # @abstractmethod
    def get_url(self) -> str:
        pass

    # @abstractmethod
    def get_body(self):
        return {}

    # @abstractmethod
    def send_request(self):
        pass

    def get_header(self) -> str:
        headers = {
            "Content-Type": "application/json",
            'Authorization': 'Bearer ' + self.getCurrentToken()
        }
        return headers

    def no_simulate(self) -> bool:
        sim = bool(os.getenv('NOSIM'))
        if sim:
            self.log.info("Simulation disabled, requests will be sent do OC: {}".format(sim))
            return sim
        else:
            self.log.info("Simulation enabled, requests will NOT be sent do OC: {}".format(sim))
            return True

    def set_auth_token_handler(self, handler):
        self.auth = handler

    def get_base_url(self):
        return os.getenv('OC_BASEURL')

    def get_auth_user(self):
        return os.getenv('OC_AUTH_USER')

    def get_auth_pass(self):
        return os.getenv('OC_AUTH_PASS')

    def getCustomTableName(self):
        return "MyCloudCIMaster"

    def getOrgEntityId(self):
        return "ORG-26DCF7FF-D05B-4932-AB94-543FA32888BB"

    def getEnvironmentEntityId(self):
        return "VMWAR-15CFFB35-7FC6-449C-9F7F-1CF83A8A6237"

    def getCatalogueEntityId(self):
        return "CAT-B0290737-0DFD-4D71-8139-F4CDBC6CE2AD"

    def getPlatformCode(self):
        return "VMWAR"

    def getSubscriptionId(self):
        return "VMWAR"

    def getCatalogueId(self):
        return "3"

    def getPageNo(self):
        return "-1"

    def getPageSize(self):
        return "-1"

    def getCurrentToken(self):
        return self.auth.getToken()

    def getPlatformEntityId(self):
        return "VMWAR-15CFFB35-7FC6-449C-9F7F-1CF83A8A6237"

    def getResultJson(self, responseRaw, json_query):
        try:
            jsonString = responseRaw.json()['Result']
            jsonObj = json.loads(jsonString)
        except json.decoder.JSONDecodeError as e:
            print("JSON parse error: ", e.args[0])
            return None
        else:
            requestStatus = jmespath.search(json_query, jsonObj)
            return requestStatus


class doubleQuoteDict(dict):

    def __str__(self):
        return json.dumps(self)

    def __repr__(self):
        return json.dumps(self)

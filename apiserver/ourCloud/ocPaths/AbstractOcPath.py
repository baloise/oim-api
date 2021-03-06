from json.decoder import JSONDecodeError
import os
from abc import ABC  # abstractmethod
import json
import jmespath
from ourCloud.OcStaticVars import OC_RESPONSEFIELD, OC_REQUESTFIELD, OC_OBJECTTYPE, OC_ACTIONMAME, OC_LANGUAGE, OC_CATALOGOFFERINGS  # noqa F401
from oim_logging import get_oim_logger


def traversing_decoder(obj, key=None):
    """This helper function traverses a given dict (can have nested docts or lists)
    and when it encounters a string value, it attempts to load it as json.
    If it succeeds, it replaces the string value with the decoded json object.

    Arguments:
    obj - Required. dict or list. Object to traverse.
    key - Optional. Used internally for traversing. Do not fill this.
    """
    if isinstance(obj, list):
        for item in obj:
            traversing_decoder(item)
    elif isinstance(obj, dict) and not key:
        for curkey in obj.keys():
            traversing_decoder(obj, key=curkey)
    elif isinstance(obj, dict) and key:
        if type(obj[key]) is str:  # we only get active for string values
            try:
                obj[key] = json.loads(obj[key])
                return
            except ValueError:
                return
            except JSONDecodeError:
                return
    return


class AbstractOcPath(ABC):
    OC_RESPONSEFIELD = OC_RESPONSEFIELD
    OC_REQUESTFIELD = OC_REQUESTFIELD
    OC_OBJECTTYPE = OC_OBJECTTYPE
    OC_ACTIONMAME = OC_ACTIONMAME
    OC_LANGUAGE = OC_LANGUAGE
    OC_CATALOGOFFERINGS = OC_CATALOGOFFERINGS

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

    def do_simulate(self) -> bool:
        mystring = os.getenv('OC_SIMULATE', "True")
        doSimulate = True
        if mystring.lower() == 'false':
            doSimulate = False
        if doSimulate:
            self.log.info("Simulation enabled, requests will NOT be sent do OC ({})".format(doSimulate))
            return True
        else:
            self.log.info("Simulation disabled, requests will be sent do OC ({})".format(doSimulate))
            return False

    def set_auth_token_handler(self, handler):
        self.auth = handler

    def get_base_url(self):
        return os.getenv('OC_BASEURL')

    def get_auth_user(self):
        return os.getenv('OC_AUTH_USER')

    def get_auth_pass(self):
        return os.getenv('OC_AUTH_PASS')

    def get_verify(self):
        if os.getenv('TLS_NO_VERIFY', 'FALSE').lower() == 'true':
            return False
        return True

    def getCustomTableName(self):
        return "MyCloudCIMaster"

    def getOrgEntityId(self):
        # return "ORG-26DCF7FF-D05B-4932-AB94-543FA32888BB"
        org_entity_id = os.getenv(
            'OC_ORG_ENTITY_ID',
            'ORG-F4960B51-21C2-4CAC-997C-974B15111EB6'  # default
        )
        return org_entity_id

    def getEnvironmentEntityId(self):
        return "VMWAR-15CFFB35-7FC6-449C-9F7F-1CF83A8A6237"

    def getCatalogueEntityId(self):
        return "CAT-B0290737-0DFD-4D71-8139-F4CDBC6CE2AD"

    def getPlatformCode(self):
        return "VMWAR"

    def getSubscriptionId(self):
        return "VMWAR"

    def getPageNo(self):
        return "-1"

    def getPageSize(self):
        return "-1"

    def getCurrentToken(self):
        return self.auth.getToken()

    def getPlatformEntityId(self):
        return "VMWAR-15CFFB35-7FC6-449C-9F7F-1CF83A8A6237"

    def getResultJson(self, responseRaw, json_query=None):
        try:
            jsonResponse = responseRaw.json()
            # self.log.debug(f'getResultJson processing: {jsonResponse}')
            jsonResult = jsonResponse.get('Result', '')
            if type(jsonResult) is str:
                jsonObj = json.loads(jsonResult)
            else:
                jsonObj = jsonResult
        except json.decoder.JSONDecodeError as e:
            self.log.error(f'JSON parse error: {e.args[0]}')
            return None
        except TypeError as e:
            self.log.error(f'Type error in getResultJson: {e.args[0]}')
            return None

        traversing_decoder(jsonObj)  # This goes thru the object and tries to decode remaining jsonstrings

        if json_query:
            return jmespath.search(json_query, jsonObj)
        else:
            return jsonObj


class doubleQuoteDict(dict):

    def __str__(self):
        return json.dumps(self)

    def __repr__(self):
        return json.dumps(self)

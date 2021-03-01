import os
import json
import datetime
import jmespath
from ourCloud.OcStaticVars import OC_RESPONSEFIELD, OC_REQUESTFIELD, OC_OBJECTTYPE, OC_ACTIONMAME, OC_LANGUAGE  # noqa F401


class AbstractOcPath:
    OC_RESPONSEFIELD, OC_REQUESTFIELD

    def get_url(self) -> str:
        pass

    def get_body(self):
        return {}

    def get_header(self) -> str:
        headers = {
            "Content-Type": "application/json",
            'Authorization': 'Bearer ' + self.getCurrentToken()
        }
        return headers

    def send_request(self):
        pass

    def do_simulate(self) -> bool:
        sim = bool(os.getenv('DOSIM'))
        self.writeLog("Simulation enabled, requests will not be sent do OC: {}".format(sim))
        if sim:
            return sim
        else:
            return False

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

    def writeLog(self, msg: str):
        filename = 'oclogging.log'
        # Open the file in append mode and append the new content in file_object
        with open(filename, 'a') as file_object:
            now = datetime.datetime.now()
            file_object.write("{t}: {m}\n".format(m=msg, t=now.strftime('%Y-%m-%d %H:%M:%S')))

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

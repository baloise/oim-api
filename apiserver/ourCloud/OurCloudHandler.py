import requests
import os
from ourCloud.auth import TokenAuthHandler
import json
import jmespath


class OurCloudRequestHandler:
    __instance = None

    @staticmethod
    def getInstance():
        """ Static access method. """
        if OurCloudRequestHandler.__instance is None:
            OurCloudRequestHandler()
        return OurCloudRequestHandler.__instance

    def __init__(self):
        if OurCloudRequestHandler.__instance is not None:
            raise Exception("This is a singleton class.")
        else:
            OurCloudRequestHandler.__instance = self
            self.auth = TokenAuthHandler(self)

    def get_all_request_details(self, requestno):
        # 3.4.5
        pass

    def get_request_status(self, requestno):
        # 3.4.4
        if not requestno:
            raise ValueError("No request number provided")
        self.requestno = requestno

        method_url = '{baseUrl}/Requests/Request'.format(
            baseUrl=self.get_base_url()
        )

        payload = {}
        headers = {
            'Authorization': 'Bearer ' + self.getCurrentToken()
        }

        responseRaw = requests.request("GET", method_url, headers=headers, data=payload, verify=False)
        return self.parseJson(responseRaw, 'Status')

    def getProxy(self):
        proxies = {
            'http': os.getenv('HTTP_PROXY'),
            'https': os.getenv('HTTPS_PROXY')
        }
        return proxies

    def get_base_url(self):
        return os.getenv('OC_BASEURL')

    def get_auth_user(self):
        return os.getenv('OC_AUTH_USER')

    def get_auth_pass(self):
        return os.getenv('OC_AUTH_PASS')

    def getCustomTableName(self):
        return "/MyCloudCIMaster"

    def getOrgEntityId(self):
        return "/ORG-26DCF7FF-D05B-4932-AB94-543FA32888BB"

    def getPageNo(self):
        return "/-1"

    def getPageSize(self):
        return "/-1"

    def getCurrentToken(self):
        return self.auth.getToken()

    def parseJson(self, responseRaw, attribute="*"):
        try:
            jsonString = responseRaw.json()['Result']
            jsonObj = json.loads(jsonString)
        except json.decoder.JSONDecodeError as e:
            print("JSON parse error: ", e.args[0])
            return None
        else:
            requestStatus = jmespath.search("[?RequestNo == `{no}`].{attribute}|[0]".format(no=self.requestno,
                                            attribute=attribute), jsonObj)
            return requestStatus

import requests
import urllib3
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
            urllib3.disable_warnings()

    def get_extended_request_parameters(self, requestno, parameters: list):
        # 3.4.5
        if not requestno:
            raise ValueError("No request number provided")

        method_url = '{baseUrl}/Requests/RequestDetails/OrgEntityID{orgEntityId}/PlatformEntityID{platformEntityId}/RequestNo/{requestNo}/RequestDetailId{requestDetailId}'.format(  # noqa: E501
            baseUrl=self.get_base_url(),
            orgEntityId=self.getOrgEntityId(),
            platformEntityId=self.getPlatformEntityId(),
            requestNo=requestno,
            requestDetailId="/-1"
        )

        payload = {}
        headers = {
            'Authorization': 'Bearer ' + self.getCurrentToken()
        }

        responseRaw = requests.request("GET", method_url, headers=headers, data=payload, verify=False)
        jsonString = responseRaw.json()['Result']
        jsonObj = json.loads(jsonString)

        # 1. outer filter all request details
        method_json_query = "Table[].AllRequestDetails[]|[0]"
        outer = self.getResultJson(responseRaw, method_json_query)

        # 2. inner filter requestno and attributes
        # method_json_query_inner = "[?RequestNo == `{no}`].{attribute}|[0]".format(no=requestno,
        #  attribute='[LocationName, RequestedStatusText, RequestDetailID]')
        jsonObj = json.loads(outer)
        # requestStatus = jmespath.search(method_json_query_inner, jsonObj)

        # 3. inner filter requestno and extended parameters
        method_json_query_extended = "\
            [?RequestNo == `{no}`].{attribute}|[0]".format(no=requestno,
                                                           attribute='[RequestDetailsExtendedParameter]')
        extendedParameters = jmespath.search(method_json_query_extended, jsonObj)

        # 5. filter extended parameters by given keys
        extendedKeys = {}
        for key in parameters:
            method_json_query_extended_keys = "[?KeyName=='{key}'].KeyValue|[0]".format(key=key)
            extendedValue = jmespath.search(method_json_query_extended_keys, extendedParameters[0])
            extendedKeys[key] = extendedValue

        return extendedKeys

    def list_extended_request_parameters(self, requestno):
        # 3.4.5
        if not requestno:
            raise ValueError("No request number provided")

        method_url = '{baseUrl}/Requests/RequestDetails/OrgEntityID{orgEntityId}/PlatformEntityID{platformEntityId}/RequestNo/{requestNo}/RequestDetailId{requestDetailId}'.format(  # noqa: E501
            baseUrl=self.get_base_url(),
            orgEntityId=self.getOrgEntityId(),
            platformEntityId=self.getPlatformEntityId(),
            requestNo=requestno,
            requestDetailId="/-1"
        )

        payload = {}
        headers = {
            'Authorization': 'Bearer ' + self.getCurrentToken()
        }

        responseRaw = requests.request("GET", method_url, headers=headers, data=payload, verify=False)
        jsonString = responseRaw.json()['Result']
        jsonObj = json.loads(jsonString)

        # 1. outer filter all request details
        method_json_query = "Table[].AllRequestDetails[]|[0]"
        outer = self.getResultJson(responseRaw, method_json_query)

        # 2. inner filter requestno and attributes
        # method_json_query_inner = "[?RequestNo == `{no}`].{attribute}|[0]".format(no=requestno,
        #  attribute='[LocationName, RequestedStatusText, RequestDetailID]')
        jsonObj = json.loads(outer)
        # requestStatus = jmespath.search(method_json_query_inner, jsonObj)

        # 3. inner filter requestno and extended parameters
        method_json_query_extended = "\
            [?RequestNo == `{no}`].{attribute}|[0]".format(no=requestno,
                                                           attribute='[RequestDetailsExtendedParameter]')
        extendedParameters = jmespath.search(method_json_query_extended, jsonObj)

        # 4. filter key names of extended parameters
        method_json_query_extended_keys = "[*].{attribute}".format(attribute='KeyName')
        extendedKeys = jmespath.search(method_json_query_extended_keys, extendedParameters[0])

        return extendedKeys

    def get_request_status(self, requestno):
        # 3.4.4
        if not requestno:
            raise ValueError("No request number provided")

        method_url = '{baseUrl}/Requests/Request'.format(
            baseUrl=self.get_base_url()
        )

        payload = {}
        headers = {
            'Authorization': 'Bearer ' + self.getCurrentToken()
        }

        responseRaw = requests.request("GET", method_url, headers=headers, data=payload, verify=False)

        method_json_query = "[?RequestNo == `{no}`].{attribute}|[0]".format(no=requestno, attribute='Status')
        return self.getResultJson(responseRaw, method_json_query)

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

    def getPlatformEntityId(self):
        return "/VMWAR-15CFFB35-7FC6-449C-9F7F-1CF83A8A6237"

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

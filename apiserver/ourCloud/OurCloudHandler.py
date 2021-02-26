import requests
import urllib3
import os
from ourCloud.auth import TokenAuthHandler
import json
import jmespath
import logging
import datetime


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

    def create_vm(self):
        method_url = '{baseUrl}/Requests/Create'.format(baseUrl=self.get_base_url())

        bodyJson = {}
        bodyJson["items"] = []
        bodyJson["items"].append(
                {
                    "hdnRegionName": {
                        "key": "hdnRegionName",
                        "value": "UK"
                    },
                    "hdnOrgName": {
                        "key": "hdnOrgName",
                        "value": "Baloise"
                    },
                    "InstanceSize": {
                        "key": "InstanceSize",
                        "value": "Small (S2) - Cores: 1, Memory: 4"
                    },
                    "itemno": 1
                })

        bodyJson["orderno"] = "0"
        bodyJson["uitemplateid"] = "1"
        bodyJson["servicecatalogid"] = self.getCatalogueId()
        bodyJson["catalogueentityid"] = self.getCatalogueEntityId()
        bodyJson["envrionmententityid"] = self.getEnvironmentEntityId()
        bodyJson["cataloguename"] = "RHEL7.X"
        bodyJson["selectedlocationid"] = "0"
        bodyJson["subscriptionid"] = self.getSubscriptionId()
        bodyJson["platformcode"] = self.getPlatformCode()
        bodyJson["isdraft"] = "N"
        bodyJson["orgentityid"] = self.getOrgEntityId()
        bodyJson["language"] = "en-US"
        bodyJson["offset"] = "-330"
        bodyJson["changenumber"] = ""
        bodyJson["requestforEMail"] = ""

        payload = doubleQuoteDict(bodyJson)
        payloadStr = json.dumps(payload)
        payload = payloadStr
        self.writeLog(payload)

        headers = {
            "Content-Type": "application/json",
            'Authorization': 'Bearer ' + self.getCurrentToken()
        }

        response = requests.post(method_url, headers=headers, data=payload, verify=False)

        # Ensure response looks valid
        if not response.status_code == 200:
            logging.error("An error occured while transmitting request ({code}): {txt}".format(
                code=response.status_code,
                txt=response.text))
            return ""
        if response["StatusCode"] == 200:
            logging.info("New request has been created successfully: {code}".format(
                code=response["RequestId"]))
            return response.text
        else:
            logging.info("Failed to create request: {code}".format(
                code=response["ErrorMessage"]))
            return ""

    def writeLog(self, msg: str):
        filename = 'oclogging.log'
        # Open the file in append mode and append the new content in file_object
        with open(filename, 'a') as file_object:
            now = datetime.datetime.now()
            file_object.write("{t}: {m}\n".format(m=msg, t=now.strftime('%Y-%m-%d %H:%M:%S')))

    def delete_vm(self, hostname: str):
        method_url = "{baseUrl}/Resources/ActionRequest".format(
            baseUrl=self.get_base_url())

        bodyJson = {}
        bodyJson["items"] = []
        bodyJson["items"].append(
                {
                    "VMName": {
                        "key": "VMName",
                        "value": hostname
                    },
                    "itemno": 1
                })

        bodyJson["actionName"] = "Delete VM"
        bodyJson["actionrequestno"] = "0"
        bodyJson["orgEntityId"] = self.getOrgEntityId()
        bodyJson["language"] = "en-US"
        bodyJson["offSet"] = "-330"
        bodyJson["actionprocesstemplateid"] = "8"
        bodyJson["changenumber"] = ""
        bodyJson["instancecount"] = 1
        bodyJson["objectid"] = hostname
        bodyJson["uitemplateid"] = "6"
        bodyJson["environmentEntityId"] = self.getEnvironmentEntityId()
        bodyJson["platformCode"] = self.getPlatformEntityId()
        bodyJson["objectType"] = "VM"

        headers = {
            "Content-Type": "application/json",
            'Authorization': 'Bearer ' + self.getCurrentToken()
        }

        payloadStr = json.dumps(doubleQuoteDict(bodyJson))
        payload = payloadStr
        self.writeLog(payload)

        response = requests.post(method_url, headers=headers, data=payload, verify=False)
        self.writeLog(response.text)

        # Ensure response looks valid
        if not response.status_code == 200:
            logging.error("An error occured while transmitting request ({code}): {txt}".format(
                code=response.status_code,
                txt=response.text))
            return ""

        responseJson = json.loads(response.text)
        # if delete request has been sent repeatedly, there is no StatusCode but Status=Fail
        if responseJson["Status"] == "Fail":
            info = "Failed to create request: {code}".format(
                code=responseJson["Message"])
            logging.info(info)
            self.writeLog(info)
            return ""

        if responseJson["StatusCode"] == 200:
            logging.info("New request has been created successfully: {code}".format(
                code=responseJson["RequestId"]))
            return response.text
        else:
            logging.info("Failed to create request: {code}".format(
                code=responseJson["ErrorMessage"]))
            return ""

    def get_extended_request_parameters(self, requestno, parameters: list) -> dict:
        # 3.4.5
        if not requestno:
            raise ValueError("No request number provided")

        method_url = '{baseUrl}/Requests/RequestDetails/OrgEntityID/{orgEntityId}/PlatformEntityID{platformEntityId}/RequestNo/{requestNo}/RequestDetailId{requestDetailId}'.format(  # noqa: E501
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

        method_url = '{baseUrl}/Requests/RequestDetails/OrgEntityID/{orgEntityId}/PlatformEntityID{platformEntityId}/RequestNo/{requestNo}/RequestDetailId{requestDetailId}'.format(  # noqa: E501
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

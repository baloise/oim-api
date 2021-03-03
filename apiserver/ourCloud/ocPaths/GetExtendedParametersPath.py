from . import AbstractOcPath
import requests
import json
import jmespath


class GetExtendedParametersPath(AbstractOcPath.AbstractOcPath):
    # 3.4.5

    def __init__(self, requestno, parameters: list, listall=False):
        if not requestno:
            raise ValueError("No requestno provided")
        if not listall and not parameters:
            raise ValueError("No parameters provided")
        self.listall = listall
        self.requestno = requestno
        self.parameters = parameters
        super().__init__()

    def get_url(self) -> str:
        method_url = '{baseUrl}/Requests/RequestDetails/OrgEntityID/{orgEntityId}/PlatformEntityID/{platformEntityId}/RequestNo/{requestNo}/RequestDetailId/{requestDetailId}'.format(  # noqa: E501
            baseUrl=self.get_base_url(),
            orgEntityId=self.getOrgEntityId(),
            platformEntityId=self.getPlatformEntityId(),
            requestNo=self.requestno,
            requestDetailId="/-1"
        )
        return method_url

    def send_request(self) -> str:
        responseRaw = requests.request("GET", self.get_url(), headers=self.get_header(), data=self.get_body(),
                                       verify=False)
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
            [?RequestNo == `{no}`].{attribute}|[0]".format(no=self.requestno,
                                                           attribute='[RequestDetailsExtendedParameter]')
        extendedParameters = jmespath.search(method_json_query_extended, jsonObj)

        # 4. filter extended parameters by given keys
        if self.listall:
            method_json_query_extended_keys = "[*].{attribute}".format(attribute='KeyName')
            extendedKeys = jmespath.search(method_json_query_extended_keys, extendedParameters[0])
        else:
            extendedKeys = {}
            for key in self.parameters:
                method_json_query_extended_keys = "[?KeyName=='{key}'].KeyValue|[0]".format(key=key)
                extendedValue = jmespath.search(method_json_query_extended_keys, extendedParameters[0])
                extendedKeys[key] = extendedValue

        return extendedKeys

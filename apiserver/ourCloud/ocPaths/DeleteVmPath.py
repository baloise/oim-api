from .AbstractOcPath import doubleQuoteDict, AbstractOcPath
import requests
import json


class DeleteVmPath(AbstractOcPath):
    # 3.4.81

    def __init__(self, hostname: str):
        if not hostname:
            raise ValueError("No hostname provided")
        super.__init__(self)
        self.hostname = hostname

    def get_url(self) -> str:
        return "{baseUrl}/Resources/ActionRequest".format(
            baseUrl=self.get_base_url())

    def get_body(self) -> str:
        bodyJson = {}
        bodyJson["items"] = []
        bodyJson["items"].append(
                {
                    self.OC_REQUESTFIELD.VMNAME.value: {
                        "key": self.OC_REQUESTFIELD.VMNAME.value,
                        "value": self.hostname
                    },
                    "itemno": 1
                })

        bodyJson[self.OC_REQUESTFIELD.ACTIONMAME.value] = self.OC_ACTIONMAME.DELETEVM.value
        bodyJson[self.OC_REQUESTFIELD.ACTIONREQUESTNO.value] = "0"
        bodyJson[self.OC_REQUESTFIELD.ORGENTITYID.value] = self.getOrgEntityId()
        bodyJson[self.OC_REQUESTFIELD.LANGUAGE.value] = self.OC_LANGUAGE.EN_US.value
        bodyJson[self.OC_REQUESTFIELD.OFFSET.value] = "-330"
        bodyJson[self.OC_REQUESTFIELD.ACTIONPROCESSTEMPLATEID.value] = "8"
        bodyJson[self.OC_REQUESTFIELD.CHANGENUMBER.value] = ""
        bodyJson[self.OC_REQUESTFIELD.INSTANCECOUNT.value] = 1
        bodyJson[self.OC_REQUESTFIELD.OBJECTID.value] = self.hostname
        bodyJson[self.OC_REQUESTFIELD.UITEMPLATEID.value] = "6"
        bodyJson[self.OC_REQUESTFIELD.ENVRIONMENTENTITYID.value] = self.getEnvironmentEntityId()
        bodyJson[self.OC_REQUESTFIELD.PLATFORMCODE.value] = self.getPlatformEntityId()
        bodyJson[self.OC_REQUESTFIELD.OBJECTTYPE.value] = self.OC_OBJECTTYPE.VM.value

        payloadStr = json.dumps(doubleQuoteDict(bodyJson))
        payload = payloadStr
        self.log.info(payload)

        return payload

    def send_request(self) -> str:
        if self.do_simulate():
            return "Simulate deletion of VM {}".format(self.hostname)
        response = requests.post(self.get_url(), headers=self.get_header(), data=self.get_body(), verify=False)
        self.log.info(response.text)

        # Ensure response looks valid
        if not response.status_code == 200:
            self.log.error("An error occured while transmitting request ({code}): {txt}".format(
                code=response.status_code,
                txt=response.text))
            return ""

        responseJson = json.loads(response.text)
        # if delete request has been sent repeatedly, there is no StatusCode but Status=Fail
        if responseJson["Status"] == "Fail":
            info = "Failed to create request: {code}".format(
                code=responseJson["Message"])
            self.log.info(info)
            return ""

        if responseJson["StatusCode"] == 200:
            self.log.info("New request has been created successfully: {code}".format(
                code=responseJson["RequestId"]))
            return response.text
        else:
            self.log.info("Failed to create request: {code}".format(
                code=responseJson["ErrorMessage"]))
            return ""

from ourCloud.ocPaths.AbstractOcPath import doubleQuoteDict, AbstractOcPath
import requests
import json
from models.orders import OrderItem, Person
from unittest.mock import Mock
from requests.models import Response


class CreateVmPath(AbstractOcPath):
    # 3.4.80

    def __init__(self, item: OrderItem):
        super().__init__()
        self.item = item
        self.requester = None
        self.log.debug("Initialize path: create VM")

    def set_requester(self, requester: Person):
        self.requester = requester

    def get_requester(self):
        return self.requester

    def get_url(self) -> str:
        return '{baseUrl}/Requests/Create'.format(baseUrl=self.get_base_url())

    def get_body(self) -> str:
        bodyJson = {}
        bodyJson["items"] = []
        bodyJson["items"].append(
                {
                    self.OC_REQUESTFIELD.REGIONNAME.value: {
                        "key": self.OC_REQUESTFIELD.REGIONNAME.value,
                        "value": "UK"
                    },
                    self.OC_REQUESTFIELD.ORGNAME.value: {
                        "key": self.OC_REQUESTFIELD.ORGNAME.value,
                        "value": "Baloise"
                    },
                    self.OC_REQUESTFIELD.INSTANCESIZE.value: {
                        "key": self.OC_REQUESTFIELD.INSTANCESIZE.value,
                        "value": self.item.get_size().cataloguesize   # "Small (S2) - Cores: 1, Memory: 4"     # input from user # noqa: E501
                    },
                    "itemno": 1
                })

        bodyJson[self.OC_REQUESTFIELD.ORDERNO.value] = "0"
        bodyJson[self.OC_REQUESTFIELD.UITEMPLATEID.value] = "1"
        bodyJson[self.OC_REQUESTFIELD.SERVICECATALOGID.value] = self.getCatalogueId()
        bodyJson[self.OC_REQUESTFIELD.CATALOGUEENTITYID.value] = self.getCatalogueEntityId()
        bodyJson[self.OC_REQUESTFIELD.ENVRIONMENTENTITYID.value] = self.getEnvironmentEntityId()
        bodyJson[self.OC_REQUESTFIELD.CATALOGUENAME.value] = self.item.get_cataloguename()  # OC_CATALOGOFFERINGS.RHEL7.cataloguename        # input fom user # noqa: E501
        bodyJson[self.OC_REQUESTFIELD.SERVICECATALOGID.value] = "0"
        bodyJson[self.OC_REQUESTFIELD.SUBSCRIPTIONID.value] = self.getSubscriptionId()
        bodyJson[self.OC_REQUESTFIELD.PLATFORMCODE.value] = self.getPlatformCode()
        bodyJson[self.OC_REQUESTFIELD.ISDRAFT.value] = "N"
        bodyJson[self.OC_REQUESTFIELD.ORGENTITYID.value] = self.getOrgEntityId()
        bodyJson[self.OC_REQUESTFIELD.LANGUAGE.value] = self.OC_LANGUAGE.EN_US.value
        bodyJson[self.OC_REQUESTFIELD.OFFSET.value] = "-330"
        bodyJson[self.OC_REQUESTFIELD.CHANGENUMBER.value] = ""
        bodyJson[self.OC_REQUESTFIELD.REQUESTFOREMAIL.value] = self.get_requester().email   # input fom user

        payload = doubleQuoteDict(bodyJson)
        payloadStr = json.dumps(payload)
        payload = payloadStr
        self.log.info(payload)

        return payload

    def send_request(self) -> str:
        response = {}
        if self.no_simulate():
            self.log.info("Simulate creation of VM")
            # return "simulate create VM"
            response = Mock(spec=Response)
            response.json.return_value = {}
            response.text = "Simulate creation of VM"
            response.status_code = 400
        else:
            response = requests.post(self.get_url(), headers=self.get_header(), data=self.get_body(), verify=False)

        # Ensure response looks valid
        if not response.status_code == 200:
            error = "An error occured while transmitting request ({code}): {txt}".format(
                    code=response.status_code,
                    txt=response.text)
            self.log.error(error)
            raise Exception(error)
        responseJson = json.loads(response.text)
        if responseJson[self.OC_RESPONSEFIELD.STATUSCODE.value.value] == 200:
            self.log.info("New request has been created successfully: {code}".format(
                code=responseJson[self.OC_RESPONSEFIELD.REQUESTID.value]))
            return responseJson[self.OC_RESPONSEFIELD.MESSAGE.value]
        else:
            error = "Failed to create request: {code}".format(
                    code=response[self.OC_RESPONSEFIELD.ERRORMESSAGE.value])
            self.log.error(error)
            raise Exception(error)

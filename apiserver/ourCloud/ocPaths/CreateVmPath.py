from ourCloud.ocPaths.AbstractOcPath import doubleQuoteDict, AbstractOcPath
import requests
import json
from models.orders import OrderItem, Person
from unittest.mock import Mock
from exceptions.WorkflowExceptions import TransmitException
from datetime import datetime
from adapter.OurCloudAdapters import SbuAdapter, OfferingAdapter
from adapter.OrchestraAdapters import provider_sla_adapter  # noqa E501
from ourCloud.OcStaticVars import TRANSLATE_TARGETS


class CreateVmPath(AbstractOcPath):
    # 3.4.80

    def __init__(self, item: OrderItem):
        super().__init__()
        self.item = item
        self.requester = None
        self.changeno = None
        self.log.debug("Initialize path: create VM")

    def set_requester(self, requester: Person):
        self.requester = requester

    def get_requester(self) -> Person:
        return self.requester

    def set_changeno(self, changeno: str):
        self.changeno = changeno

    def get_changeno(self):
        return self.changeno

    def get_url(self) -> str:
        # return '{baseUrl}/Requests/Create'.format(baseUrl=self.get_base_url())
        return '{baseUrl}/GenericScripts/Execute/OrgEntityId/{orgEntityId}/Scripts/16'.format(baseUrl=self.get_base_url(), orgEntityId=self.getOrgEntityId())   # noqa E501

    """def get_body_lab(self) -> str:
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

        return payload"""

    def get_body(self) -> str:
        bodyJson = {}
        bodyJson["items"] = []
        now = datetime.now()
        now_string = now.strftime("%d/%m/%Y %H:%M:%S")
        sbu = self.get_requester().get_sbu()
        offering = self.item.get_cataloguename()
        self.log.info("Append items {sb}".format(sb=sbu))
        bodyJson["items"].append(
                {
                    self.OC_REQUESTFIELD.SBUCODE.value: {
                        "key": self.OC_REQUESTFIELD.SBUCODE.value,
                        "value": SbuAdapter().translate(sbu)
                    },  # ok
                    self.OC_REQUESTFIELD.SERVICELEVEL.value: {
                        "key": self.OC_REQUESTFIELD.SERVICELEVEL.value,
                        "value": provider_sla_adapter().translate(self.item.get_servicelevel(), TRANSLATE_TARGETS.OURCLOUD)  # TODO: replace with item detail and translate  # noqa E501
                    },  # ok
                    self.OC_REQUESTFIELD.SERVERTYPE.value: {
                        "key": self.OC_REQUESTFIELD.SERVERTYPE.value,
                        "value": self.item.get_servertype()
                    },  # ok
                    self.OC_REQUESTFIELD.APPCODE.value: {
                        "key": self.OC_REQUESTFIELD.APPCODE.value,
                        "value": self.item.get_appcode().appcode
                    },  # ok
                    self.OC_REQUESTFIELD.SERVERROLE.value: {
                        "key": self.OC_REQUESTFIELD.SERVERROLE.value,
                        "value": "WEB"  # TODO: derived from item detail (APP/DB/WEB)
                    },
                    self.OC_REQUESTFIELD.CATALOGUENAME.value: {
                        "key": self.OC_REQUESTFIELD.CATALOGUENAME.value,
                        "value": OfferingAdapter().translate(offering, "ocid")  # TODO replace attribute usage
                    },
                    self.OC_REQUESTFIELD.CHANGENUMBER.value: {
                        "key": self.OC_REQUESTFIELD.CHANGENUMBER.value,
                        "value": self.get_changeno()
                    },
                    self.OC_REQUESTFIELD.ENVIRONMENT.value: {
                        "key": self.OC_REQUESTFIELD.ENVIRONMENT.value,
                        "value": "TEST"  # TODO: replace with item detail and translate
                    },
                    # AD Group
                    self.OC_REQUESTFIELD.WINPATCHWINDOW.value: {
                        "key": self.OC_REQUESTFIELD.WINPATCHWINDOW.value,
                        "value": "H-SERVER-SCCM-BCH-LV50-02-DO-2000"  # TODO: replace with item detail and translate
                    },
                    self.OC_REQUESTFIELD.STORAGETYPE.value: {
                        "key": self.OC_REQUESTFIELD.STORAGETYPE.value,
                        "value": "HPM"  # TODO: replace with item detail and translate
                    },
                    self.OC_REQUESTFIELD.SERVERSIZE.value: {
                        "key": self.OC_REQUESTFIELD.SERVERSIZE.value,
                        "value": self.item.get_size().catalogueid   # TODO: translate
                    },
                    self.OC_REQUESTFIELD.DATADISK.value: {
                        "key": self.OC_REQUESTFIELD.DATADISK.value,
                        "value": {
                            "I": "30"  # TODO: replace with item detail
                        }
                    },
                    self.OC_REQUESTFIELD.TAG.value: {
                        "key": self.OC_REQUESTFIELD.TAG.value,
                        "value": {
                            "OimRequestTime": now_string,
                            "OimComment": "oim test"
                        }
                    },
                    self.OC_REQUESTFIELD.ITEMNO.value: 1  # always 1
                })

        bodyJson[self.OC_REQUESTFIELD.SERVICECATALOGUEID.value] = OfferingAdapter().translate(offering, "occatalogueid")  # TODO replace attribute usage  # noqa E501
        # bodyJson[self.OC_REQUESTFIELD.CATALOGUEENTITYID.value] = self.getCatalogueEntityId()
        # bodyJson[self.OC_REQUESTFIELD.ENVRIONMENTENTITYID.value] = self.getEnvironmentEntityId()
        # bodyJson[self.OC_REQUESTFIELD.SUBSCRIPTIONID.value] = self.getSubscriptionId()
        # bodyJson[self.OC_REQUESTFIELD.ISDRAFT.value] = "N"
        bodyJson[self.OC_REQUESTFIELD.ORGENTITYID.value] = self.getOrgEntityId()
        bodyJson[self.OC_REQUESTFIELD.CHANGENUMBER.value] = self.get_changeno()
        bodyJson[self.OC_REQUESTFIELD.PLATFORMCODE.value] = self.getPlatformCode()
        # bodyJson[self.OC_REQUESTFIELD.LANGUAGE.value] = self.OC_LANGUAGE.EN_US.value
        # bodyJson[self.OC_REQUESTFIELD.OFFSET.value] = "-330"
        # bodyJson[self.OC_REQUESTFIELD.REQUESTFOREMAIL.value] = self.get_requester().email   # input fom user

        payload = doubleQuoteDict(bodyJson)
        payloadStr = json.dumps(payload)
        payload = payloadStr
        self.log.info(payload)

        return payload

    def send_request(self) -> str:
        response = {}
        if self.do_simulate():
            self.log.info("Simulate creation of VM")
            self.log.info("url: {url}, body: {body}".format(url=self.get_url(), body=self.get_body()))

            response_mock = Mock()
            response_mock.status_code = 200     # simulate error by changing to != 200
            response_mock.text = "{\"StatusCode\": 200, \"RequestId\": \"99\", \"ErrorMessage\": \"something went wrong\", \"Message\": \"mess\"}"   # noqa 501
            response = response_mock
        else:
            response = requests.post(self.get_url(), headers=self.get_header(), data=self.get_body(), verify=False)

        # Ensure response looks valid
        if not response.status_code == 200:
            error = "An error occured while transmitting request ({code}): {txt}".format(
                    code=response.status_code,
                    txt=response.text)
            raise TransmitException(error)

        responseJson = json.loads(response.text)
        if responseJson[self.OC_RESPONSEFIELD.STATUSCODE.value] == 200:
            self.log.info("New request has been created successfully. OC request ID={code}".format(
                code=responseJson[self.OC_RESPONSEFIELD.REQUESTID.value]))
            return responseJson[self.OC_RESPONSEFIELD.REQUESTID.value]
        else:
            error = "Failed to create request: {code}".format(
                    code=responseJson[self.OC_RESPONSEFIELD.ERRORMESSAGE.value])
            self.log.error(error)
            raise Exception(error)

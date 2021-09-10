from oim_logging import get_oim_logger
import os
from dotenv import load_dotenv
import requests
import json


class CreateChangeDetails():
    def __init__(self):

        self.tckShorttext = ''
        self.description = ''
        self.persnoReqBy = ''
        self.category = ''
        self.servicesid = ''
        self.dueDate = ''
        self.environmentId = ''

    def setShorttext(self, param: str):
        self.tckShorttext = param

    def setDescription(self, param: str):
        self.description = param

    def setReqPerson(self, param: str):
        self.persnoReqBy = param

    def setCategory(self, param: str):
        self.category = param

    def setServicesId(self, param: str):
        self.servicesid = param

    def setdueDate(self, param: str):
        self.dueDate = param

    def setEnvironmentId(self, param: str):
        self.environmentId = param


@property
class CloseChangeDetails():
    def __init__(self):

        self.changeNr = None
        self.tckShorttext = None
        self.description = None
        self.system = None
        self.status = None
        self.changeOwnerGroup = None


class ValuemationHandler():
    def __init__(self, cParams=None):

        if isinstance(cParams, dict):
            # print("Params is: dict")
            self.params = cParams
        elif isinstance(cParams, CreateChangeDetails):
            # print("Params is: class")
            self.MyCreateChangeDetails = cParams
        elif isinstance(cParams, CloseChangeDetails):
            self.MyCloseChangeDetails = cParams
        elif cParams is None:
            pass

        load_dotenv()
        self.logger = get_oim_logger()
        self.logger.debug("ValuemationHandler initialized")

        self.valuemation_baseurl = os.getenv('VALUEMATION_BASEURL')
        if not self.valuemation_baseurl:
            self.logger.error("No VALUEMATION_BASEURL defined")

        self.valuemation_access_token = os.getenv('VALUEMATION_ACCESS_TOKEN')
        if not self.valuemation_access_token:
            self.logger.error("No VALUEMATION_ACCESS_TOKEN defined")

        self.valuemation_auth_user = os.getenv('VALUEMATION_AUTH_USER')
        if not self.valuemation_auth_user:
            self.logger.error("No VALUEMATION_AUTH_USER defined")

        self.valuemation_auth_password = os.getenv('VALUEMATION_AUTH_PASSWORD')
        if not self.valuemation_auth_password:
            self.logger.error("No VALUEMATION_AUTH_PASSWORD defined")

        if cParams is None:
            self.logger.debug("Call ValuemationHandler without parameters")

    def showEnv(self):
        print("URL:[", self.valuemation_baseurl, "]")
        print("AccessToken:[", self.valuemation_access_token, "]")
        print("AuthUser:[", self.valuemation_auth_user, "]")
        print("AuthPW:[", self.valuemation_auth_password, "]")

    def create_change(self) -> json:
        body_base = {
            "accessToken": self.valuemation_access_token,
            "username": self.valuemation_auth_user,
            "password": self.valuemation_auth_password,
            "encrypted": "N",
            "service": "CreateBAStandardChange",
            "params": {
                "persnoAffected": self.valuemation_auth_user,
                "actualUser": self.valuemation_auth_user,
                "ticketclass": "RFC/Change",
                "tickettype": "Standard Change",
                "status": "CH_REC",
                "changeOwnerGroup": "MVP.shopDemo.Purchase",
                "changeOwnerPersonNo": "",
                "statementtype": "Information"
            }
        }

        if hasattr(self, 'MyCreateChangeDetails'):
            params = {
                "tckShorttext": self.MyCreateChangeDetails.tckShorttext,
                "description": self.MyCreateChangeDetails.description,
                "persnoReqBy": self.MyCreateChangeDetails.persnoReqBy,
                "category": self.MyCreateChangeDetails.category,
                "servicesid": self.MyCreateChangeDetails.servicesid,
                "dueDate": self.MyCreateChangeDetails.dueDate,
                "environmentId": self.MyCreateChangeDetails.environmentId
            }
            body_final = json.loads(json.dumps(body_base))
            body_final["params"].update(params)
        else:
            body_final = json.loads(json.dumps(body_base))
            body_final["params"].update(self.params)

        try:
            self.logger.debug("Valuemation Api DEBUG(full request):[{0}]".
                              format(json.dumps(body_final)))
            response = requests.post(self.valuemation_baseurl, json=body_final)
            response.raise_for_status()

        except requests.exceptions.HTTPError as errh:
            self.logger.error("Valuemation REST Api error(HTTP):[" + str(errh) + "]")
            return None
        except requests.exceptions.ConnectionError as errc:
            self.logger.error("Valuemation REST Api error(Connection):[" + str(errc) + "]")
            return None
        except requests.exceptions.Timeout as errt:
            self.logger.error("Valuemation REST Api error(Timeout):[" + str(errt) + "]")
            return None
        except requests.exceptions.RequestException as err:
            self.logger.error("Valuemation REST Api error(RequestException):[" + str(err) + "]")
            return None
        else:
            if response.json()['returnCode'] != '00':
                self.logger.error("Valuemation Api error:[{0}]".
                                  format(response.json()))
                self.logger.error("Valuemation Api error:[{0}] detail:[{1}] (parameter failure)".
                                  format(response.json()['returnCode'], response.json()['message']))
                lRet = response.json()['returnCode']
            else:
                self.logger.info("StandardChange {0} created".format(response.json()['result']))
                lRet = response.json()['result']

        return lRet

    def close_change(self):
        # Final close a change is CH_REVD -> CH_CLD
        body_base = {
            "accessToken": self.valuemation_access_token,
            "username": self.valuemation_auth_user,
            "password": self.valuemation_auth_password,
            "encrypted": "N",
            "service": "UpdateBAStandardChange",
            "params": {
                }
            }

        if hasattr(self, 'CloseChangeDetails'):
            params = {
                "changeNr": self.CloseChangeDetails.changeNr,
                "tckShorttext": self.CloseChangeDetails.tckShorttext,
                "description": self.CloseChangeDetails.description,
                "system": self.CloseChangeDetails.system,
                "status": self.CloseChangeDetails.status,
                "changeOwnerGroup": self.CloseChangeDetails.changeOwnerGroup
            }

            body_final = json.loads(json.dumps(body_base))
            body_final["params"].update(params)
        else:
            body_final = json.loads(json.dumps(body_base))
            body_final["params"].update(self.params)

        try:
            response = requests.post(self.valuemation_baseurl, json=body_final)
            response.raise_for_status()

        except requests.exceptions.HTTPError as errh:
            self.logger.error("Valuemation REST Api error(HTTP):[" + str(errh) + "]")
            return None
        except requests.exceptions.ConnectionError as errc:
            self.logger.error("Valuemation REST Api error(Connection):[" + str(errc) + "]")
            return None
        except requests.exceptions.Timeout as errt:
            self.logger.error("Valuemation REST Api error(Timeout):[" + str(errt) + "]")
            return None
        except requests.exceptions.RequestException as err:
            self.logger.error("Valuemation REST Api error(RequestException):[" + str(err) + "]")
            return None
        else:
            self.logger.info("StandardChange {0} closed".format(response.json()['result']))

        return response.json()['result']

    def update_change(self, params: dict):

        body_base = {
            "accessToken": self.valuemation_access_token,
            "username": self.valuemation_auth_user,
            "password": self.valuemation_auth_password,
            "encrypted": "N",
            "service": "UpdateBAStandardChange",
            "params": {}
            }

        body_final = json.loads(json.dumps(body_base))
        body_final["params"].update(params)

        try:
            response = requests.post(self.valuemation_baseurl, json=body_final)
            response.raise_for_status()

        except requests.exceptions.HTTPError as errh:
            self.logger.error("Valuemation REST Api error(HTTP):[" + str(errh) + "]")
            return None
        except requests.exceptions.ConnectionError as errc:
            self.logger.error("Valuemation REST Api error(Connection):[" + str(errc) + "]")
            return None
        except requests.exceptions.Timeout as errt:
            self.logger.error("Valuemation REST Api error(Timeout):[" + str(errt) + "]")
            return None
        except requests.exceptions.RequestException as err:
            self.logger.error("Valuemation REST Api error(RequestException):[" + str(err) + "]")
            return None
        else:
            self.logger.info("StandardChange {0} updated".format(response.json()['result']))

        return response.json()['result']

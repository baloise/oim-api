from oim_logging import get_oim_logger
import os
from dotenv import load_dotenv
import requests
import json


class ValuemationHandler:

    def __init__(self):
        load_dotenv()
        logger = get_oim_logger()
        logger.debug("ValuemationHandler initialized")

        self.valuemation_baseurl = os.getenv('VALUEMATION_BASEURL')
        if not self.valuemation_baseurl:
            logger.error("No VALUEMATION_BASEURL defined")

        self.valuemation_access_token = os.getenv('VALUEMATION_ACCESS_TOKEN')
        if not self.valuemation_access_token:
            logger.error("No VALUEMATION_ACCESS_TOKEN defined")

        self.valuemation_auth_user = os.getenv('VALUEMATION_AUTH_USER')
        if not self.valuemation_auth_user:
            logger.error("No VALUEMATION_AUTH_USER defined")

        self.valuemation_auth_password = os.getenv('VALUEMATION_AUTH_PASSWORD')
        if not self.valuemation_auth_password:
            logger.error("No VALUEMATION_AUTH_PASSWORD defined")

    def showEnv(self):
        print("URL:[", self.valuemation_baseurl, "]")
        print("AccessToken:[", self.valuemation_access_token, "]")
        print("AuthUser:[", self.valuemation_auth_user, "]")
        print("AuthPW:[", self.valuemation_auth_password, "]")

    def create_change(self, params: dict):
        self.logger = get_oim_logger()

        body_base = {
            "accessToken": self.valuemation_access_token,
            "username": self.valuemation_auth_user,
            "password": self.valuemation_auth_password,
            "encrypted": "N",
            "service": "CreateBAStandardChange",
            "params": {
                "persnoAffected": self.valuemation_auth_user,
                "actualUser": self.valuemation_auth_user
            }
        }

        body_final = json.loads(json.dumps(body_base))
        body_final["params"].update(params)

        try:
            response = requests.post(self.valuemation_baseurl, json=body_final)
            response.raise_for_status()

        except requests.exceptions.HTTPError as errh:
            self.logger.error("Valuemation REST Api error(HTTP):[" + errh + "]")
        except requests.exceptions.ConnectionError as errc:
            self.logger.error("Valuemation REST Api error(Connection):[" + errc + "]")
        except requests.exceptions.Timeout as errt:
            self.logger.error("Valuemation REST Api error(Timeout):[" + errt + "]")
        except requests.exceptions.RequestException as err:
            self.logger.error("Valuemation REST Api error(RequestException):[" + err + "]")

        self.logger.info("StandardChange {0} created".format(response.json()))
        return response.json()

    def update_change(self, params: dict):
        self.logger = get_oim_logger()

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
            self.logger.error("Valuemation REST Api error(HTTP):[" + errh + "]")
        except requests.exceptions.ConnectionError as errc:
            self.logger.error("Valuemation REST Api error(Connection):[" + errc + "]")
        except requests.exceptions.Timeout as errt:
            self.logger.error("Valuemation REST Api error(Timeout):[" + errt + "]")
        except requests.exceptions.RequestException as err:
            self.logger.error("Valuemation REST Api error(RequestException):[" + err + "]")

        self.logger.info("StandardChange {0} updated".format(response.json()))
        return response.json()

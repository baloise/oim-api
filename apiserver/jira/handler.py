from oim_logging import get_oim_logger
import os
import requests
from requests.auth import HTTPBasicAuth


class JiraHandler:

    def __init__(self):

        logger = get_oim_logger()
        logger.debug("JiraHandler initialized")

        self.jira_baseurl = os.getenv('JIRA_BASEURL')
        if not self.jira_baseurl:
            logger.error("No JIRA_BASEURL defined")

        self.jira_auth_user = os.getenv('JIRA_AUTH_USER')
        if not self.jira_auth_user:
            logger.error("No JIRA_AUTH_USER defined")

        self.jira_auth_pass = os.getenv('JIRA_AUTH_PASS')
        if not self.jira_auth_pass:
            logger.error("No JIRA_AUTH_PASS defined")

    def get_issue_json(self, jira_key):
        logger = get_oim_logger()
        logger.debug("Searching for {0}".format(jira_key))

        response = requests.get(
            "{0}/issue/{1}".format(self.jira_baseurl, jira_key),
            auth=HTTPBasicAuth(self.jira_auth_user, self.jira_auth_pass)
        )

        return response.json()

    def create_issue_siamsid(self, summary, description):
        logger = get_oim_logger()

        body = {
            "fields": {
                "project":
                    {
                        "key": "SIAM"
                    },
                "summary": summary,
                    "description": description,
                    "issuetype": {
                        "name": "Task"
                    },
                "customfield_24250": {
                        "value": "SIAM SID"
                    }
            }
        }

        response = self.create_issue(body)

        logger.info("Jira {0} created".format(response.json()['key']))

        return response.json()

    def create_issue(self, body):
        response = requests.post(
            "{0}/issue".format(self.jira_baseurl),
            json=body,
            auth=HTTPBasicAuth(self.jira_auth_user,
                               self.jira_auth_pass)
        )
        return response

    def create_comment(self, jira_key, comment):

        body = {
            "body": comment
        }
        response = requests.post(
            "{0}/issue/{1}/comment".format(self.jira_baseurl, jira_key),
            json=body,
            auth=HTTPBasicAuth(self.jira_auth_user,
                               self.jira_auth_pass)
        )
        return response

    def upload_attachment(self, jira_key, path_to_file):
        logger = get_oim_logger()

        logger.debug("Reading file '{0}'".format(path_to_file))
        uploadfile = open(path_to_file, "rb")

        logger.debug("Uploading '{0}' for {1}".format(path_to_file, jira_key))
        response = requests.post(
            "{0}/issue/{1}/attachments".format(self.jira_baseurl, jira_key),
            files={"file": uploadfile},
            headers={"X-Atlassian-Token": "no-check"},
            auth=HTTPBasicAuth(self.jira_auth_user, self.jira_auth_pass)
        )

        return response.json()

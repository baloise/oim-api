from oim_logging import get_oim_logger
import os
import requests
from requests.auth import HTTPBasicAuth
import enum


class JIRABOARD(enum.Enum):
    # kv from oc docu
    SIAMSID = "SIAM SID"
    HCLDIS = "DIS Overview"


class JiraHandler:

    def __init__(self):
        self.logger = get_oim_logger()
        self.logger.debug("JiraHandler initialized")

        self.jira_baseurl = os.getenv('JIRA_BASEURL')
        if not self.jira_baseurl:
            self.logger.error("No JIRA_BASEURL defined")

        self.jira_auth_user = os.getenv('JIRA_AUTH_USER')
        if not self.jira_auth_user:
            self.logger.error("No JIRA_AUTH_USER defined")

        self.jira_auth_pass = os.getenv('JIRA_AUTH_PASS')
        if not self.jira_auth_pass:
            self.logger.error("No JIRA_AUTH_PASS defined")

    def get_issue_json(self, jira_key):
        self.logger.debug("Searching for {0}".format(jira_key))

        response = requests.get(
            "{0}/issue/{1}".format(self.jira_baseurl, jira_key),
            auth=HTTPBasicAuth(self.jira_auth_user, self.jira_auth_pass)
        )

        return response.json()

    def create_issue_withlabel(self, summary, description):
        label = "hcl"

        issuenr = self.create_issue_generic(summary, description, label, JIRABOARD.SIAMSID)
        ky = issuenr['key']
        if issuenr:
            self.set_reporter(ky, "B041091")


    def create_issue_siamsid(self, summary, description):
        self.create_issue_generic(summary, description, "",
                                  JIRABOARD.SIAMSID)

    def create_issue_generic(self, summary, description, label,
                             board: JIRABOARD, reporter=None):
        logger = get_oim_logger()

        body = {
            "fields": {
                "project": {"key": "SIAM"},
                "summary": summary,
                "description": description,
                "issuetype": {"name": "Task"},
                "labels": [label],
                "customfield_24250": {"value": board.value}
            }
        }

        # Jira will use the JIRA_AUTH_USER as reporter,
        # but it will be overwritten if parameter 'reporter' is set
        if reporter is not None:
            body["fields"]["reporter"] = {
                "name": reporter
            }

        try:
            response = self.create_issue(body)
            if response.status_code in [404, 400]:
                raise Exception(response.text)
        except Exception as e:
            self.logger.error("Creating jira failed with error {err}".format(err=getattr(e, 'message', repr(e))))
            self.logger.debug(body)
        else:
            self.logger.info("Jira {0} created".format(response.json()['key']))

        return response.json()

    def set_reporter(self, jira_key: str, name: str):
        body = {
            "fields": {
             "reporter": {"name": name}
            }
        }

        try:
            response = self.update_issue(jira_key, body)
            if response.status_code in [404, 400]:
                raise Exception(response.text)
        except Exception as e:
            self.logger.error("Updating jira failed with error {err}".format(err=getattr(e, 'message', repr(e))))
            self.logger.debug(body)
        else:
            self.logger.info("Jira {0} updated".format(jira_key))

        return response.json()

    def update_issue(self, jira_key, body):
        response = requests.put(
            "{baseurl}/issue/{jira_key}".format(baseurl=self.jira_baseurl, jira_key=jira_key),
            json=body,
            auth=HTTPBasicAuth(self.jira_auth_user,
                               self.jira_auth_pass)
        )
        return response

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
        self.logger.debug("Reading file '{0}'".format(path_to_file))
        uploadfile = open(path_to_file, "rb")

        self.logger.debug("Uploading '{0}' for {1}".format(path_to_file, jira_key))
        response = requests.post(
            "{0}/issue/{1}/attachments".format(self.jira_baseurl, jira_key),
            files={"file": uploadfile},
            headers={"X-Atlassian-Token": "no-check"},
            auth=HTTPBasicAuth(self.jira_auth_user, self.jira_auth_pass)
        )

        return response.json()

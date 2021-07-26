import json
import logging
from jira.handler import JiraHandler, JIRABOARD
from dotenv import load_dotenv


class IssueReader:

    def __init__(self):
        self.json = None
        self.file = "issues.json"

    def read_file(self):
        with open(self.file, 'r') as myfile:
            data = myfile.read()
            self.json = json.loads(data)

    def get_json(self):
        return self.json


load_dotenv()
logger = logging.getLogger()
logging.basicConfig(
    level=logging.DEBUG,
    style="{",
    datefmt="%d.%m.%Y %H:%M:%S",
    format="{asctime} {levelname}: {message}"
)

app = IssueReader()
app.read_file()
myJira = JiraHandler()

jsonStr = app.get_json()
for issue in jsonStr['issues']:
    desc = issue['description']
    syst = issue['system']
    service = issue['service']
    team = issue['orderteam']
    status = issue['status']
    label = "hcl"
    reporter = None

    intro = "Issue: {iss}\nAffected system: {sys}\nIn order to remedy this issue, please take the following measure(s):\n".format(iss=desc, sys=syst)  # noqa F501
    li = []
    for mes in issue['measures']:
        li.append('  * '+mes+'\n')
    measures = intro+(''.join(li))

    desc = 'PostgreSQL Service Review Finding: '+desc
    print(desc)
    print(measures)
    if status == '':
        logger.info(myJira.create_issue_generic(desc, measures, label, JIRABOARD.HCLDIS, reporter, team, service))
    else:
        print(status)

# logger.info(myJira.get_issue_json("DIS-15322"))

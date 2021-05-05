from dotenv import load_dotenv
import logging
from jira.handler import JiraHandler


load_dotenv()
logger = logging.getLogger()
logging.basicConfig(
    level=logging.DEBUG,
    style="{",
    datefmt="%d.%m.%Y %H:%M:%S",
    format="{asctime} {levelname}: {message}"
)

myJira = JiraHandler()

# myJira.upload_attachment("SIAM-318", "requirements.txt")
myJira.create_comment("SIAM-318", "hello World")

# SIAM SID Checker
logger.info(myJira.create_issue_siamsid("testjira", "b041435"))

# Jira reading checker
# myfeedback = myJira.get_issue_json('SIAM-318')
# logger.info(myfeedback['fields']['status']['name'])

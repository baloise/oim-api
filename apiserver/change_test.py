import logging
from itsm.handler import ValuemationHandler


logger = logging.getLogger()
logging.basicConfig(
    level=logging.DEBUG,
    style="{",
    datefmt="%d.%m.%Y %H:%M:%S",
    format="{asctime} {levelname}: {message}"
)

myChange = ValuemationHandler()

# Show ENV
# x = myChange.showEnv()
# print("Return:[", x, "]")
# Test Update
update_string = '{"status":"", "description":"Free text can place hier", "ticketno":"", "changeOwnerGroup":""}'
lRet = myChange.update_change()
print("Return:[", lRet, "]")

create_string = '{"":"", "":"", "":"", "":""}'
lRet = myChange.create_change()
print("Return:[", lRet, "]")

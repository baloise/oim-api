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
# params = {
#     "params": {
#         "status":"CH_IMPF",
#         "description":"Free text can place hier",
#         "ticketno":"CH-0000016",
#         "changeOwnerGroup":"HCL-Windows"
#     }
# }
params = {
        "status": "CH_IMPF",
        "description": "Free text can place hier, final version(Georges)",
        "ticketno": "CH-0000016",
        "changeOwnerGroup": "HCL-Linux"
    }

lRet = myChange.update_change(params)
print("Return:[", lRet, "]")

# Test Create
# create_string = '{"":"", "":"", "":"", "":""}'
# lRet = myChange.create_change()
# print("Return:[", lRet, "]")

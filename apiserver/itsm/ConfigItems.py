from oim_logging import get_oim_logger
from abc import ABC
from datetime import datetime
from typing import List
from ourCloud.OcStaticVars import OC_CATALOGOFFERING_SIZES, ENVIRONMENT, TRANSLATE_TARGETS
from adapter.GenericConverters import EnvironmentConverter
import ipaddress


class AbstractConfigItem(ABC):
    itemName = None
    itemId = 0
    validFrom = None
    validTo = None
    status = None
    typeId = None

    def __init__(self, name: str):
        self.itemName = name

    def getItemName(self) -> str:
        return self.itemName

    def setItemName(self, name):
        self.itemName = name

    def getItemId(self) -> int:
        return self.itemId

    def getStatus(self) -> str:
        return self.status

    # @abstractmethod
    def getComponents(self):
        return {}

    # @abstractmethod
    def setTypeId(self, id: int):
        self.typeId = id

    def getValidFrom(self) -> datetime:
        return self.validFrom

    def getValidTo(self) -> datetime:
        return self.validTo

    # @abstractmethod
    def fromJson(self, jsonStr: str):
        pass


class ConfigItem(AbstractConfigItem):
    def __init__(self):
        self.log = get_oim_logger()


class AbstractConfigItemComponent(ABC):
    def __init__(self):
        return

    # def setTypeId(self, typeid: int):
    #     self.typeId = typeid

    # def getTypeId(self) -> str:
    #     return self.typeId

    def isServerComponent(self) -> bool:
        return False


class ServerComponent(AbstractConfigItemComponent):
    environment = None  # Acceptance etc
    tshirt = None  # S1 etc
    storageClass = None  # HPM etc.

    def __init__(self, environment: ENVIRONMENT, shirtsize: OC_CATALOGOFFERING_SIZES, storagecl: str):
        super().__init__()
        self.environment = environment
        self.tshirt = shirtsize
        self.storageClass = storagecl

    def getEnvironment(self) -> ENVIRONMENT:
        return self.environment

    def setEnvironment(self, env: ENVIRONMENT):
        self.environment = env

    def isServerComponent(self) -> bool:
        return True

    def getSize(self) -> OC_CATALOGOFFERING_SIZES:
        return self.tshirt

    def setSize(self, siz: OC_CATALOGOFFERING_SIZES):
        self.tshirt = siz


class SystemConfigItem(ConfigItem):
    components = None
    mainIpAddress = None
    serviceLine = None
    shortText = None
    size = None
    requestId = None
    systemKeys = ['ComputerName',   # hostname used by customer
                  'IpAddress',      # ip used by customer
                  'ObjectType',     # VM
                  'RequestNo',      #
                  'NoOfCPCU',       # cores
                  'MemoryInMB',     #
                  'OS',             # "Windows"/"Linux"
                  'Size',           # catalogue size
                  'Tags',           # custom tags
                  'CustomField3',   # "IISW01", "JBSL03"
                  'CustomField9',   # "Dev", "TEST", "Acc"
                  'DecommisionDate'
                  ]

    def __init__(self, requestId: int):
        super().__init__()
        self.requestId = requestId
        self.setTypeId = 100162  # System type ID for VM INT
        self.components = []

    def getIpAddress(self) -> ipaddress:
        return self.mainIpAddress

    def setIpAddress(self, adr: ipaddress):
        self.mainIpAddress = adr

    def getComponents(self) -> List[AbstractConfigItemComponent]:
        return self.components

    def getServerComponent(self) -> ServerComponent:
        for comp in self.components:
            if comp.isServerComponent():  # TODO: replace with comp type enum
                return comp
        return None

    def hasServerComponent(self) -> bool:
        for comp in self.components:
            if comp.isServerComponent():
                return True
        return False

    def addComponent(self, component: AbstractConfigItemComponent):
        self.components.append(component)

    def setServiceLine(self, line: str):
        self.serviceLine = line

    def setShortText(self, text: str):
        self.shortText = text

    def getServiceLine(self) -> str:
        return self.serviceLine

    def getShortText(self) -> str:
        return self.shortText

    def getSize(self) -> str:
        return self.size

    def setSize(self, size):
        self.size = size  # TODO: use size obj

    def updateAttributeValue(self, key, val):
        if key == 'ComputerName':
            self.setItemName(val)
        elif key == 'IpAddress':
            # TODO: translate to ipaddress
            self.setIpAddress(val)
        elif key == 'Size':
            if self.hasServerComponent():
                scomp = self.getServerComponent()
                sizObj = OC_CATALOGOFFERING_SIZES.from_id(val)
                scomp.setSize(sizObj)
            else:  # need to create server component with size attribute
                sizObj = OC_CATALOGOFFERING_SIZES.from_id(val)
                scomp = ServerComponent(environment=None, shirtsize=sizObj, storagecl=None)
                self.addComponent(scomp)
        elif key == 'CustomField9':  # environment
            if self.hasServerComponent():
                scomp = self.getServerComponent()
                envObj = EnvironmentConverter().translate(val, TRANSLATE_TARGETS.OURCLOUD)
                scomp.setEnvironment(envObj)
            else:  # need to create server component with environment attribute
                envObj = EnvironmentConverter().translate(val, TRANSLATE_TARGETS.OURCLOUD)
                scomp = ServerComponent(environment=envObj, shirtsize=None, storagecl=None)
                self.addComponent(scomp)

    def fromJson(self, jsonStr: str):
        # loop through list of predefined keys and read value from json
        for key in self.systemKeys:
            if key in jsonStr:
                val = jsonStr[key]
                # add to CfgItm object
                self.updateAttributeValue(key, val)
                self.log.info(f"Updated system with relevant key from json:  {key}={val}")
            else:
                errMsg = f"System parameter is missing in oc details of request {self.requestId}"
                self.log.error(errMsg)
                raise BaseException(errMsg)

        # all relevant system keys are included in the json and ci object is filled

        # mount0 = jsonStr['ActualDiskJSON'][0]['DriveOrMountPoint']

    def __str__(self):
        head = self.getItemName()
        ccount = len(self.getComponents())
        cenv = self.getServerComponent().getEnvironment().oimname
        csize = self.getServerComponent().getSize().cataloguesize
        return f"name is '{head}', {ccount} components, env is '{cenv}', size is '{csize}'"


class DiskComponent(AbstractConfigItemComponent):
    name = None
    sizeGb = 0

    def __init__(self, name: str, sizeGb: int):
        super.__init()
        self.name = name
        self.sizeGb = sizeGb

    def getName(self) -> str:
        return self.name

    # @abstractmethod
    def getLabel(self) -> str:
        pass

    def getSize(self) -> int:
        return self.sizeGb


class LinuxMountpointComponent(DiskComponent):
    group = None
    owner = None
    permissions = 0o777

    def setGroup(self, group: str):
        self.group = group

    def getGroup(self) -> str:
        return self.group

    def getLabel(self) -> str:
        return self.name

    def setOwner(self, owner: str):
        self.owner = owner

    def getOwner(self) -> str:
        return self.owner

    def setPermissions(self, rwx: int):
        self.permissions = rwx

    def getPermissions(self) -> int:
        return int(self.permissions, 8)


class WindowsDiskComponent(DiskComponent):
    label = None

    def __init__(self, driveName: str, driveLabel: str):
        super.__init__()
        self.name = driveName
        self.label = driveLabel

    def getLabel(self) -> str:
        return self.label

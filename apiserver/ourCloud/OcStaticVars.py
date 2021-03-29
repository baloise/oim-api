import enum


class OC_STATUS(enum.Enum):
    FULFILLMENT_COMPLETED = "Fulfilment Completed"
    AUTO_APPROVED = "Auto Approved"


class OC_RESPONSEFIELD(enum.Enum):
    MESSAGE = "Message"
    ERRORMESSAGE = "ErrorMessage"
    STATUSCODE = "StatusCode"
    REQUESTID = "RequestId"


class OC_REQUESTFIELD(enum.Enum):
    ACTIONMAME = "actionName"
    ACTIONPROCESSTEMPLATEID = "actionprocesstemplateid"
    ACTIONREQUESTNO = "actionrequestno"
    CATALOGUEENTITYID = "catalogueentityid"
    CATALOGUENAME = "cataloguename"
    CHANGENUMBER = "changenumber"
    ENVRIONMENTENTITYID = "envrionmententityid"
    INSTANCECOUNT = "instancecount"
    INSTANCESIZE = "InstanceSize"
    ISDRAFT = "isdraft"
    LANGUAGE = "language"
    OBJECTID = "objectid"
    OBJECTTYPE = "objectType"
    OFFSET = "offset"
    ORDERNO = "orderno"
    ORGENTITYID = "orgentityid"
    ORGNAME = "hdnOrgName"
    OSTYPE = "hdnOSType"
    PLATFORMCODE = "platformcode"
    REGIONNAME = "hdnRegionName"
    REQUESTDETAILID = "RequestDetailID"
    REQUESTFOREMAIL = "requestforEMail"
    SELECTEDLOCATIONID = "selectedlocationid"
    SERVICECATALOGID = "servicecatalogid"
    SUBSCRIPTIONID = "subscriptionid"
    UITEMPLATEID = "uitemplateid"
    VMNAME = "VMName"


class OC_OBJECTTYPE(enum.Enum):
    VM = "VM"


class OC_ACTIONMAME(enum.Enum):
    DELETEVM = "Delete VM"


class OC_LANGUAGE(enum.Enum):
    EN_US = "en-US"


class OC_CATALOGOFFERING_SIZES(bytes, enum.Enum):
    def __new__(cls, value, cataloguesize, catalogueid):
        obj = bytes.__new__(cls)
        obj._value_ = value
        obj.cataloguesize = cataloguesize
        obj.catalogueid = catalogueid
        return obj
    S1 = (1, "Small (S1) - Cores: 2, Memory: 4", "S1")
    S2 = (2, "Small (S2) - Cores: 1, Memory: 4", "S2")     # Lab only
    M1 = (3, "Medium (M1) - Cores: 4, Memory: 8", "M1")
    M2 = (4, "Medium (M2) - Cores: 4, Memory: 16", "M2")
    L1 = (5, "Large (L1) - Cores: 8, Memory: 32", "L1")
    L2 = (6, "Large (L2) - Cores: 8, Memory: 64", "L2")
    X1 = (7, "ExtraLarge (X1) - Cores: 16, Memory: 64", "X1")

    @classmethod
    def from_str(cls, cataloguename):
        if cataloguename == 'Small (S1) - Cores: 2, Memory: 4':
            return cls.S1
        elif cataloguename == 'Small (S2) - Cores: 1, Memory: 4':
            return cls.S2
        elif cataloguename == 'Medium (M1) - Cores: 4, Memory: 8':
            return cls.M1
        elif cataloguename == 'Medium (M2) - Cores: 4, Memory: 16':
            return cls.M2
        elif cataloguename == 'Large (L1) - Cores: 8, Memory: 32':
            return cls.L1
        elif cataloguename == 'Large (L2) - Cores: 8, Memory: 64':
            return cls.L2
        elif cataloguename == 'ExtraLarge (X1) - Cores: 16, Memory: 64':
            return cls.X1
        else:
            raise NotImplementedError


class OC_CATALOGOFFERINGS(bytes, enum.Enum):

    def __new__(cls, value, cataloguename, catalogueid):
        obj = bytes.__new__(cls)
        obj._value_ = value
        obj.cataloguename = cataloguename
        obj.catalogueid = catalogueid
        return obj
    WINS2019 = (1, 'Windows 2019', 1)
    RHEL7 = (2, 'RHEL7.X', 2)
    PGRHEL7 = (3, 'RHEL7.X PostgreSQL', 6)

    @classmethod
    def from_str(cls, cataloguename):
        if cataloguename == 'Windows 2019':
            return cls.WINS2019
        elif cataloguename == 'RHEL7.X':
            return cls.RHEL7
        elif cataloguename == 'RHEL7.X':
            return cls.PGRHEL7
        else:
            raise NotImplementedError


class ENVIRONMENT(bytes, enum.Enum):

    def __new__(cls, value, apiname, orcaid, ocid):
        obj = bytes.__new__(cls)
        obj._value_ = value
        obj.apiname = apiname
        obj.orcaid = orcaid
        obj.ocid = ocid
        return obj
    DEVELOPMENT = (1, 'development', 1, 'DEV')
    TEST = (2, 'test', 2, 'TEST')
    INTEGRATION = (3, 'intgegration', 3, 'INT')
    ACCEPTANCE = (4, 'acceptance', 4, 'ACC')
    PRODUCTION = (5, 'production', 5, 'PROD')

    @classmethod
    def get_id(cls, val):
        if val == cls.DEVELOPMENT:
            return cls.DEVELOPMENT.orcaid
        elif val == cls.TEST:
            return cls.TEST.orcaid
        elif val == cls.INTEGRATION:
            return cls.INTEGRATION.orcaid
        elif val == cls.ACCEPTANCE:
            return cls.ACCEPTANCE.orcaid
        elif val == cls.PRODUCTION:
            return cls.PRODUCTION.orcaid
        else:
            raise NotImplementedError

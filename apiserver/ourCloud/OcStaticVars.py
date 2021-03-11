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
        obj = bytes.__new__(cls, [value])
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


class OC_CATALOGOFFERINGS(bytes, enum.Enum):

    def __new__(cls, value, cataloguename, catalogueid):
        obj = bytes.__new__(cls, [value])
        obj._value_ = value
        obj.cataloguename = cataloguename
        obj.catalogueid = catalogueid
        return obj
    WINS2019 = (1, 'Windows 2019', 1)
    RHEL7 = (2, 'RHEL7.X', 2)
    PGRHEL7 = (3, 'RHEL7.X PostgreSQL', 6)

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

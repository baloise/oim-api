# from marshmallow import Schema, fields, validate
from app import db
import enum
from datetime import datetime
from ourCloud.OcStaticVars import ENVIRONMENT, OC_CATALOGOFFERINGS, OC_CATALOGOFFERING_SIZES, SERVICE_LEVEL
from models.statuspayload import StatusPayload  # noqa: F401
from ourCloud.OcStaticVars import APPLICATIONS


class OrderType(enum.Enum):
    CREATE_ORDER = 0
    DELETE_ORDER = 100
    MODIFY_ORDER = 200


class SbuType(enum.Enum):
    BE = 'BE'
    CHB_CH = 'CH-BCH'  # Enum elements can't contain minus in the key
    CH_SOB = 'CH-SOB'
    DE = 'DE'
    LI = 'LI'
    LURED = 'LU-RED'
    LU_YELLOW = 'LU-YELLOW'
    BITS = 'BITS'


# This is a proposition of possible order states. TODO: Verify with team.
class OrderStateType(enum.Enum):
    def __new__(cls, value, state):
        obj = object.__new__(cls)
        obj._value_ = value
        obj.state = state
        return obj

    NEW = (0, 'NEW')  # Order just created
    VERIFIED = (100, 'VERIFIED')  # Order has completed verification
    CR_CREATED = (150, 'CR_CREATED')  # Change Request has been created per item
    BE_PROCESSING = (200, 'BE_PROCESSING')  # Accepted by backends, implementation in progress
    BE_FAILED = (300, 'BE_FAILED')  # Backends reported failure
    BE_DONE = (400, 'BE_DONE')  # Backend done, tests can start
    TESTING = (500, 'TESTING')  # Backends reported success, testing
    TEST_FAILED = (600, 'TEST_FAILED')  # Testing unsuccessful
    TEST_SUCCEEDED = (700, 'TEST_SUCCEEDED')  # Testing successful
    CMDB_DONE = (800, 'CMDB_DONE')
    CR_CLOSED = (850, 'CR_CLOSED')  # Change Request has been closed per item
    HANDOVER_DONE = (900, 'HANDOVER_DONE')
    DONE = (1000, 'DONE')  # Order fully completed

    @classmethod
    def from_state(cls, state):
        if state == 'NEW':
            return cls.NEW.value
        elif state == 'VERIFIED':
            return cls.VERIFIED.value
        elif state == 'CR_CREATED':
            return cls.CR_CREATED.value
        elif state == 'BE_PROCESSING':
            return cls.BE_PROCESSING.value
        elif state == 'BE_FAILED':
            return cls.BE_FAILED.value
        elif state == 'BE_DONE':
            return cls.BE_DONE.value
        elif state == 'TESTING':
            return cls.TESTING.value
        elif state == 'TEST_FAILED':
            return cls.TEST_FAILED.value
        elif state == 'TEST_SUCCEEDED':
            return cls.TEST_SUCCEEDED.value
        elif state == 'CMDB_DONE':
            return cls.CMDB_DONE.value
        elif state == 'CR_CLOSED':
            return cls.CR_CLOSED.value
        elif state == 'HANDOVER_DONE':
            return cls.HANDOVER_DONE.value
        elif state == 'DONE':
            return cls.DONE.value
        else:
            raise NotImplementedError


class BackendType(enum.Enum):
    ORCHESTRA = 'ORCHESTRA'
    OURCLOUD = 'OURCLOUD'


class Person(db.Model):
    __tablename__ = 'persons'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    email = db.Column(db.String(100), nullable=False)
    sbu = db.Column(db.String(100), nullable=True)
    orders = db.relationship('Order', backref='person', lazy=True)

    def __init__(self, username: str, email: str, sbu: SbuType):
        self.username = username
        self.email = email
        self.sbu = sbu.value

    def get_id(self):
        return self.id

    def get_sbu(self):
        return self.sbu

# class PersonSchema(Schema):
#     id = fields.Email()
#     email = fields.Email()
#     sbu = fields.Str(validate=validate.OneOf([
#         'BE',
#         'CH-BCH',
#         'CH-SOB',
#         'DE',
#         'LI',
#         'LU-RED',
#         'LU-YELLOW',
#         'SHARED'
#         ]))


class OrderItem(db.Model):
    __tablename__ = 'orderitems'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    type = db.Column(db.String(50))
    reference = db.Column(db.String(80), nullable=False)
    cataloguename = db.Column(db.String(500), nullable=False)
    size = db.Column(db.String(50), nullable=False)
    environment = db.Column(db.String(50), nullable=False)
    businessService = db.Column(db.String(50), nullable=True)
    backend_request_id = db.Column(db.Integer, nullable=True)
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id'))
    order = db.relationship("Order", back_populates="items")

    __mapper_args__ = {
        'polymorphic_identity': 'orderitem',
        'with_polymorphic': '*',
        "polymorphic_on": type
    }

    def __init__(self, name: OC_CATALOGOFFERINGS, size: OC_CATALOGOFFERING_SIZES, environment: ENVIRONMENT):
        self.cataloguename = name.cataloguename
        self.size = size.cataloguesize
        self.environment = environment.oimname

    def set_reference(self, reference):
        self.reference = reference

    def set_backend_request_id(self, reqid):
        self.backend_request_id = reqid

    def setBusinessService(self, serviceName):
        self.businessService = serviceName

    def get_reference(self):
        return self.reference

    def get_cataloguename(self) -> OC_CATALOGOFFERINGS:
        cn = OC_CATALOGOFFERINGS.from_str(self.cataloguename)
        return cn

    def is_Vm(self) -> bool:
        return self.cataloguename in (OC_CATALOGOFFERINGS.WINS2019.cataloguename,
                                      OC_CATALOGOFFERINGS.RHEL7.cataloguename)

    def get_size(self) -> OC_CATALOGOFFERING_SIZES:
        sz = OC_CATALOGOFFERING_SIZES.from_str(self.size)
        return sz

    def getEnvironment(self) -> ENVIRONMENT:
        env = ENVIRONMENT.from_str(self.environment)
        return env

    def getBusinessService(self) -> str:
        if self.businessService is None:
            return "SIAM-SID (Test) prod - SA"  # servicesid = 1360
        return self.businessService

    def __repr__(self):
        return f"<OrderItem {self.id!r} for Order {self.order.id!r} has Request ID: {self.backend_request_id}>"


# class OrderItemSchema(Schema):
#     id = fields.Integer()
#     reference = fields.Str()
#     item_type = fields.Str()  # TODO: Add validation for the known types


class VmOrderItem(OrderItem):

    servicelevel = None
    appcode = None

    __mapper_args__ = {
        'polymorphic_identity': 'vmorderitem',
        'with_polymorphic': '*'
    }

    def __init__(self, name: OC_CATALOGOFFERINGS, size: OC_CATALOGOFFERING_SIZES, environment: ENVIRONMENT):
        super().__init__(name, size, environment)

    def set_appcode(self, appcode: APPLICATIONS):
        self.appcode = appcode

    def get_appcode(self) -> APPLICATIONS:
        return self.appcode

    def set_servicelevel(self, servicelevel: SERVICE_LEVEL):
        self.servicelevel = servicelevel

    def get_servicelevel(self) -> SERVICE_LEVEL:
        return self.servicelevel

    def get_servertype(self) -> str:
        for item in APPLICATIONS:
            if item == self.appcode:
                return item.ocservertype
        return None


class OrderStatus(db.Model):
    __tablename__ = 'orderstatuses'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    state = db.Column(db.Enum(OrderStateType), nullable=False)
    since = db.Column(db.DateTime, index=True, default=datetime.now)
    system = db.Column(db.Enum(BackendType))
    # This attribute might actually be a dupe of the dbrel parent_order
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id'))
    order = db.relationship("Order", back_populates="history")
    payload = db.relationship("StatusPayload", uselist=False, backref="status")

    def __repr__(self):
        return f"<OrderStatus {self.id!r} for Order {self.order.id!r}>"

# class OrderStatusSchema(Schema):
#     id = fields.Integer()
#     state = fields.Str()  # TODO: Add ENUM here
#     since = fields.DateTime()
#     system = fields.Str()  # TODO: Add ENUM for existing backend systems, Is this actually needed.


class Order(db.Model):
    __tablename__ = 'orders'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    create_date = db.Column(db.DateTime, default=db.func.current_timestamp())
    requester = db.Column(db.Integer, db.ForeignKey('persons.id'), nullable=False)
    type = db.Column(db.String(20))
    history = db.relationship('OrderStatus', back_populates='order', lazy=True)
    items = db.relationship('OrderItem', back_populates='order', lazy=True)

    __mapper_args__ = {
        'polymorphic_on': type,
        'polymorphic_identity': 'order'
    }

    def __init__(self, order_type: OrderType, items, requester: Person):
        self.order_type = order_type.value
        self.items: list = items
        self.requester = requester.get_id()

    def __repr__(self):
        return f"<Order {self.id!r}>"

    def add_item(self, item):
        self.items.append(item)

    def get_items(self) -> list:
        return self.items

    def set_requester(self, requester: Person):
        self.requester = requester.get_id()

    def set_create_date(self, createdate: datetime):
        self.create_date = createdate

    def get_requester(self):
        return self.requester

    def get_type(self) -> OrderType:
        return OrderType(self.order_type)

    def set_type(self, order_type: OrderType):
        self.order_type = order_type.value


class CreateOrder(Order):

    __mapper_args__ = {
        'polymorphic_identity': 'createorder'
    }


class DeleteOrder(Order):

    __mapper_args__ = {
        'polymorphic_identity': 'deleteorder'
    }


class ModifyOrder(Order):

    __mapper_args__ = {
        'polymorphic_identity': 'modifyorder'
    }

# class OrderSchema(Schema):
#     id = fields.Integer()
#     create_date = fields.DateTime()
#     history = fields.Nested(OrderStatusSchema())  # All status updates
#     requestor = PersonSchema()
#     items = fields.Nested(OrderItemSchema()

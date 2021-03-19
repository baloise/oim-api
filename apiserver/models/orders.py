# from marshmallow import Schema, fields, validate
from app import db
import enum
from datetime import datetime
from ourCloud.OcStaticVars import OC_CATALOGOFFERINGS, OC_CATALOGOFFERING_SIZES


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
    SHARED = 'SHARED'


# This is a proposition of possible order states. TODO: Verify with team.
class OrderStateType(enum.Enum):
    def __new__(cls, value, state):
        obj = object.__new__(cls)
        obj._value_ = value
        obj.state = state
        return obj

    NEW = (0, 'NEW')  # Order just created
    VERIFIED = (100, 'VERIFIED')  # Order has completed verification
    BE_PROCESSING = (200, 'BE_PROCESSING')  # Accepted by backends, implementation in progress
    BE_FAILED = (300, 'BE_FAILED')  # Backends reported failure
    BE_DONE = (400, 'BE_DONE')  # Backend done, tests can start
    TESTING = (500, 'TESTING')  # Backends reported success, testing
    TEST_FAILED = (600, 'TEST_FAILED')  # Testing unsuccessful
    TEST_SUCCEEDED = (700, 'TEST_SUCCEEDED')  # Testing successful
    CMDB_DONE = (800, 'CMDB_DONE')
    HANDOVER_DONE = (900, 'HANDOVER_DONE')
    DONE = (1000, 'DONE')  # Order fully completed

    @classmethod
    def from_state(cls, state):
        if state == 'NEW':
            return cls.NEW.value
        elif state == 'VERIFIED':
            return cls.VERIFIED.value
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
    reference = db.Column(db.String(80), nullable=False)
    cataloguename = db.Column(db.String(500), nullable=False)
    size = db.Column(db.String(50), nullable=False)
    backend_request_id = db.Column(db.Integer, nullable=True)
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id'))
    order = db.relationship("Order", back_populates="items")

    def __init__(self, name: OC_CATALOGOFFERINGS, size: OC_CATALOGOFFERING_SIZES):
        self.cataloguename = name.cataloguename
        self.size = size.cataloguesize

    def set_reference(self, reference):
        self.reference = reference

    def set_backend_request_id(self, reqid):
        self.backend_request_id = reqid

    def get_reference(self):
        return self.reference

    def get_cataloguename(self) -> OC_CATALOGOFFERINGS:
        return self.cataloguename

    def is_Vm(self) -> bool:
        return self.cataloguename in (OC_CATALOGOFFERINGS.WINS2019.cataloguename,
                                      OC_CATALOGOFFERINGS.RHEL7.cataloguename)

    def get_size(self) -> OC_CATALOGOFFERING_SIZES:
        return self.size

    def __repr__(self):
        return f"<OrderItem {self.id!r} for Order {self.order.id!r} has Request ID: {self.backend_request_id}>"


# class OrderItemSchema(Schema):
#     id = fields.Integer()
#     reference = fields.Str()
#     item_type = fields.Str()  # TODO: Add validation for the known types


class OrderStatus(db.Model):
    __tablename__ = 'orderstati'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    state = db.Column(db.Enum(OrderStateType), nullable=False)
    since = db.Column(db.DateTime, index=True, default=datetime.now)
    system = db.Column(db.Enum(BackendType))
    # This attribute might actually be a dupe of the dbrel parent_order
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id'))
    order = db.relationship("Order", back_populates="history")

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

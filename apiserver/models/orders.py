# from marshmallow import Schema, fields, validate
from components.db import db
import enum


class SbuType(enum.Enum):
    BE = 'BE'
    CHBCH = 'CH-BCH'
    CHSOB = 'CH-SOB'
    DE = 'DE'
    LI = 'LI'
    LURED = 'LU-RED'
    LUYELLOW = 'LU-YELLOW'
    SHARED = 'SHARED'


class OrderItemType(enum.Enum):
    DMY = 'DMY'  # Dummy order type not found in any catalogue


# This is a proposition of possible order states. TODO: Verify with team.
class OrderStateType(enum.Enum):
    NEW = 'NEW'  # Order just created
    VERIFIED = 'VERIFIED'  # Order has completed verification
    IN_PROGRESS = 'IN_PROGRESS'  # Accepted by backends, implementation in progress
    BE_DONE = 'BE_DONE'  # Backend done, tests can start
    BE_FAIL = 'BE_FAIL'  # Backends reported failure
    TESTING = 'TESTING'  # Backends reported success, testing
    TEST_FAIL = 'TEST_FAIL'  # Testing unsuccessful
    TEST_SUCCESS = 'TEST_SUCCESS'  # Testing successful
    CMDB_DONE = 'CMDB_DONE'
    DONE = 'DONE'  # Order fully completed


class BackendType(enum.Enum):
    ORCHESTRA = 'ORCHESTRA'
    OURCLOUD = 'OURCLOUD'


class Person(db.Model):
    id = db.Column(db.BigInteger, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    email = db.Column(db.String(100), nullable=False)
    sbu = db.Column(db.Enum(SbuType), nullable=False)
    orders = db.relationship('Order', backref='person', lazy=True)


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
    id = db.Column(db.BigInteger, primary_key=True)
    reference = db.Column(db.String(80), nullable=False)
    item_type = db.Column(db.Enum(OrderItemType), nullable=False)
    order = db.Column(db.BigInteger, db.ForeignKey('order.id'))


# class OrderItemSchema(Schema):
#     id = fields.Integer()
#     reference = fields.Str()
#     item_type = fields.Str()  # TODO: Add validation for the known types


class OrderStatus(db.Model):
    id = db.Column(db.BigInteger, primary_key=True)
    state = db.Column(db.Enum(OrderStateType), nullable=False)
    since = db.Column(db.DateTime)
    system = db.Column(db.Enum(BackendType))
    order = db.Column(db.BigInteger, db.ForeignKey('order.id'))

    def __repr__(self):
        return f"<OrderStatus {self.id!r} for Order {self.order.id!r}>"

# class OrderStatusSchema(Schema):
#     id = fields.Integer()
#     state = fields.Str()  # TODO: Add ENUM here
#     since = fields.DateTime()
#     system = fields.Str()  # TODO: Add ENUM for existing backend systems, Is this actually needed.


class Order(db.Model):
    id = db.Column(db.BigInteger, primary_key=True)
    create_date = db.Column(db.DateTime)
    history = db.relationship('OrderStatus', backref='order', lazy=True)
    requestor = db.Column(db.BigInteger, db.ForeignKey('person.id'), nullable=False)
    items = db.relationship('OrderItem', backref='order', lazy=True)

    def __repr__(self):
        return f"<Order {self.id!r}>"


# class OrderSchema(Schema):
#     id = fields.Integer()
#     create_date = fields.DateTime()
#     history = fields.Nested(OrderStatusSchema())  # All status updates
#     requestor = PersonSchema()
#     items = fields.Nested(OrderItemSchema()

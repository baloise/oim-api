# from marshmallow import Schema, fields, validate
from app import db
import enum
from datetime import datetime


class SbuType(enum.Enum):
    BE = 'BE'
    CHB_CH = 'CH-BCH'  # Enum elements can't contain minus in the key
    CH_SOB = 'CH-SOB'
    DE = 'DE'
    LI = 'LI'
    LURED = 'LU-RED'
    LU_YELLOW = 'LU-YELLOW'
    SHARED = 'SHARED'


class OrderItemType(enum.Enum):
    DMY = 'DMY'  # Dummy order type not found in any catalogue


# This is a proposition of possible order states. TODO: Verify with team.
class OrderStateType(enum.Enum):
    NEW = 'NEW'  # Order just created
    VERIFIED = 'VERIFIED'  # Order has completed verification
    BE_PROCESSING = 'BE_PROCESSING'  # Accepted by backends, implementation in progress
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
    __tablename__ = 'persons'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    email = db.Column(db.String(100), nullable=False)
    sbu = db.Column(db.Enum(SbuType), nullable=True)
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
    __tablename__ = 'orderitems'

    id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    reference = db.Column(db.String(80), nullable=False)
    item_type = db.Column(db.Enum(OrderItemType), nullable=False)
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id'))


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
    # order exists as backref from Order class

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
    create_date = db.Column(db.DateTime)
    history = db.relationship('OrderStatus', backref='order', lazy=True)
    requestor = db.Column(db.Integer, db.ForeignKey('persons.id'), nullable=False)
    items = db.relationship('OrderItem', backref='order', lazy=True)

    def __repr__(self):
        return f"<Order {self.id!r}>"


# class OrderSchema(Schema):
#     id = fields.Integer()
#     create_date = fields.DateTime()
#     history = fields.Nested(OrderStatusSchema())  # All status updates
#     requestor = PersonSchema()
#     items = fields.Nested(OrderItemSchema()

from marshmallow import Schema, fields, validate


class PersonSchema(Schema):
    id = fields.Email()
    email = fields.Email()
    sbu = fields.Str(validate=validate.OneOf([
        'BE',
        'CH-BCH',
        'CH-SOB',
        'DE',
        'LI',
        'LU-RED',
        'LU-YELLOW',
        'SHARED'
        ]))


class OrderItemSchema(Schema):
    id = fields.Integer()
    reference = fields.Str()
    item_type = fields.Str()  # TODO: Add validation for the known types


class OrderStatusSchema(Schema):
    id = fields.Integer()
    state = fields.Str()  # TODO: Add ENUM here
    since = fields.DateTime()
    system = fields.Str()  # TODO: Add ENUM for existing backend systems, Is this actually needed.


class OrderSchema(Schema):
    id = fields.Integer()
    create_date = fields.DateTime()
    history = fields.Nested(OrderStatusSchema())  # All status updates
    requestor = PersonSchema()
    items = fields.Nested(OrderItemSchema())

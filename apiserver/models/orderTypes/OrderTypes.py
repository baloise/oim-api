import enum
from models.orders import Order


class OrderType(enum.Enum):
    CREATE_ORDER = 0
    DELETE_ORDER = 100
    MODIFY_ORDER = 200


class GenericOrder(Order):
    type: OrderType = None

    def __init__(self, items, requester):
        super().__init__(items, requester)

    def get_type(self) -> OrderType:
        return self.type

    def set_type(self, type: OrderType):
        self.type = type

    type = property(get_type, set_type)


class CreateOrder(GenericOrder):
    type: OrderType = OrderType.CREATE_ORDER


class DeleteOrder(GenericOrder):
    type: OrderType = OrderType.DELETE_ORDER


class ModifyOrder(GenericOrder):
    type: OrderType = OrderType.MODIFY_ORDER

from api.OrderFactory import OrderFactory


class OrderHandler:

    def __init__(self):
        self.connector = OrderFactory('api/orders_data.xml')

    def list_orders(self):
        self.connector.list_orders()

    def add_order(self, requester_id='b0123456', bu='BU 401', order_type='VM', description=None):   # noqa
        return self.connector.generate_order(requester_id, bu, order_type, description)             # noqa

    def get_order_status(self, orderid):
        return self.connector.get_status(orderid)

    def get_order_details(self, orderid):
        return self.connector.get_details(orderid)

    # def update_status(self,attribute,value):
        # self.connector....


if __name__ == '__main__':
    ohandler = OrderHandler()
    ohandler.list_orders()
    ohandler.get_order_status('1613028463047852')
    ohandler.get_order_details('1613028463047852')
    print("New Order ID=", ohandler.add_order(requester_id='b039214', description='This is my order'))  # noqa
    ohandler.list_orders()

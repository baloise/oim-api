from api.OrderHandlerTester import OrderHandler


def add_order(requester_id, bu, order_type, description):
    order = OrderHandler()
    orderno = order.add_order(requester_id, bu, order_type, description)
    return 'Order ' + orderno + ' has been added'


def get_order_status(id) -> str:
    order = OrderHandler()
    status = order.get_order_status(id)
    if len(status) > 0:
        return 'Order {id} has the status: {status}'.format(id=id, status=status)   # noqa
    else:
        return 'The specified order id is invalid'


def get_order_details(id) -> str:
    order = OrderHandler()
    info = order.get_order_details(id)
    if len(info) > 0:
        return 'Order {id} infos: {info}'.format(id=id, info=info)
    else:
        return 'The specified order id is invalid'

from datetime import datetime
from oim_logging import get_oim_logger
from models.orders import OrderStateType, BackendType, Order, OrderStatus
from app import db


def create_status(status):
    log = get_oim_logger()
    osStateValues = set(item.state for item in OrderStateType)
    stateName = status.get('state', OrderStateType.NEW.state)
    if stateName not in osStateValues:
        log.warn('Illegal state given: {name}'.format(name=stateName))
        return 'Illegal state given', 400

    btStateValues = set(item.value for item in BackendType)
    if status.get('system') not in btStateValues:
        log.warn('Illegal system given: {}'.format(str(status.get('system'))))
        return 'Illegal system given', 400

    order_id = status.get('orderid', None)
    if not order_id:
        log.warn('create_status called without orderid!')
        return 'Order not found', 404
    order = db.session.query(Order).filter(Order.id == order_id).one_or_none()
    if not order:
        log.info('create_status() called with non-existent order id: {oid}'.format(
            oid=str(order_id)
        ))
        return 'Order not found', 404
    else:
        log.debug('Successfully retreived order item for id: {oid}'.format(
            oid=str(order_id)
        ))
    log.debug('Constructing new orderstatus item')

    new_status = OrderStatus(
        state=stateName,
        since=status.get('since', datetime.now()),
        system=status.get('system')
    )

    log.debug("Adding new status {stat} to order object {oid}".format(
        stat=stateName,
        oid=str(order_id)))
    order.history.append(new_status)
    db.session.commit()
    log.debug('All done, new status created with id: {sid}'.format(
        sid=new_status.id
    ))
    return {'statusid': new_status.id}, 201

from datetime import datetime
from app import db
from models.orders import OrderType, Person, Order, OrderStateType, BackendType, OrderStatus
from workflows.Factory import OrderFactory
from oim_logging import get_oim_logger


def retrieve_user(id=None, username=None, email=None, create_if_missing=False):
    log = get_oim_logger()
    if not id and not username and not email:
        log.error('retrieve_user called without any parameters?!')
        return None

    user = None

    if id:
        user = db.session.query(Person).filter(Person.id == id).one_or_none()
    elif username:
        user = db.session.query(Person).filter(Person.username == username).one_or_none()
    elif email:
        user = db.session.query(Person).filter(Person.email == email).one_or_none()

    if not user:
        log.warn('Requested user not found. (Params: username={un}, email={em}, id={id})'.format(un=username, em=email, id=id))  # noqa: E501

    if not user and create_if_missing:
        log.warn('Creating non-existing user as requested...')
        user = Person(
            username=username,
            email=email
        )
        db.session.add(user)

    return user


# This method is actually in the wrong file and should
# be moved to an own one for order calls. However at the time
# of writing this the existing calls_order.py is using a previous/different
# set of classes.
def create_minimal_order(orderinfo):
    log = get_oim_logger()

    requester_username = orderinfo.get('requester_username', 'b000000')
    requester = retrieve_user(username=requester_username, create_if_missing=True)
    if not requester:
        log.critical('Error retrieving person object for requester')
        return 'Error retrieving user', 500
    order_factory = OrderFactory()
    items = []
    new_order = order_factory.get_order(
        OrderType.CREATE_ORDER,
        items,
        requester
    )
    db.session.add(new_order)
    db.session.commit()
    return {'order_id': new_order.id}, 201


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


def list_statuses(orderid):
    pass

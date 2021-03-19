import unittest
import os
from datetime import datetime
from oim_logging import get_oim_logger
from models.orders import Person, SbuType, OrderStateType, OrderItem, OrderStatus, Order, BackendType  # noqa: F401,E501
from app import create_flask_app, db


class TestDbData(unittest.TestCase):
    def setUp(self):
        os.environ['SQLACHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.app = create_flask_app(config_name='unittests')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

        # add Person
        self.personPeter = Person(
            username='u12345',
            email='peter.parker@test.fake',
            sbu=SbuType.SHARED
        )
        # add orderStatus
        self.orderStatusFoo = OrderStatus(
            # add the fileds
            state=OrderStateType.NEW,
            system=BackendType.ORCHESTRA,
            order_id=1
        )

        current_datetime = datetime.utcnow()
        running_logger = get_oim_logger()
        running_logger.info('DateTime:[{}]'.format(current_datetime))

        # add Order
        self.orderFoo = Order(
            create_date=current_datetime,
            # history=1,
            requestor=1,
            # items=1
        )
        db.session.add(self.orderFoo)
        db.session.commit()
        # add OrderItems
        self.orderItemFoo = OrderItem(
            reference='foo',
            item_type=OrderItemType.DMY,
            # order_id=self.orderFoo.id
        )
        self.orderFoo.items.append(self.orderItemFoo)
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_1_order_exists(self):
        db.session.add(self.orderItemFoo)
        db.session.commit()
        reference = OrderItem.query.filter_by(reference='foo')
        assert reference is not None

#    def test_2_order_doesnt_exist(self):
#        db.session.add(self.orderItemFoo)
#        db.session.commit()
#        reference = OrderItem.query.filter_by(reference='notFoo')
#        assert reference.count() == 0

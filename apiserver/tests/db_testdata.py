import unittest
import os
from datetime import datetime
from oim_logging import get_oim_logger
from models.orders import Person, SbuType, OrderStateType, OrderItem, OrderStatus, Order, OrderType, BackendType, OC_CATALOGOFFERING_SIZES, OC_CATALOGOFFERINGS  # noqa: F401,E501
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
        db.session.add(self.personPeter)
        db.session.commit()

        # add orderStatus
        self.orderStatusFoo = OrderStatus(
            state=OrderStateType.NEW,
            system=BackendType.ORCHESTRA,
            order_id=1
        )
        db.session.add(self.orderStatusFoo)
        db.session.commit()

        # add OrderItems
        self.orderItemFoo = OrderItem(
            name=OC_CATALOGOFFERINGS.RHEL7,
            size=OC_CATALOGOFFERING_SIZES.S1
        )
        self.orderItemFoo.set_reference('foo')
        # db.session.add(self.orderItemFoo)
        # db.session.commit()

        # define current datetime utc
        current_datetime = datetime.utcnow()
        running_logger = get_oim_logger()
        running_logger.info('CREATE_ORDER DateTime:[{}]'.format(current_datetime))

        # add Order
        self.orderFoo = Order(
            requester=self.personPeter,
            order_type=OrderType.CREATE_ORDER,
            items=[self.orderItemFoo]
        )
        self.orderFoo.set_create_date(current_datetime)
        db.session.add(self.orderFoo)
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_1_orderItem_exists(self):
        db.session.add(self.orderItemFoo)
        db.session.commit()
        query = OrderItem.query.filter_by(reference='foo')

        assert query.count() > 0

    def test_2_order_date(self):
        pass

#    def test_2_order_doesnt_exist(self):
#        db.session.add(self.orderItemFoo)
#        db.session.commit()
#        reference = OrderItem.query.filter_by(reference='notFoo')
#        assert reference.count() == 0

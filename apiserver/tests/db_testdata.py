import unittest
import os
from datetime import datetime
# from oim_logging import get_oim_logger
from models.orders import Person, SbuType, OrderStateType, OrderItem, OrderStatus, Order, OrderType, BackendType, OC_CATALOGOFFERING_SIZES, OC_CATALOGOFFERINGS  # noqa: F401,E501
from app import create_flask_app, db
from ourCloud.OcStaticVars import SERVICE_LEVEL, APPLICATIONS


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
            sbu=SbuType.BITS
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

        # add OrderItem1
        self.orderItemTest1 = OrderItem(
            name=OC_CATALOGOFFERINGS.RHEL7,
            size=OC_CATALOGOFFERING_SIZES.S1
        )
        self.orderItemTest1.set_reference('TestItem1 reference')
        # add OrderItem2
        self.orderItemTest2 = OrderItem(
            name=OC_CATALOGOFFERINGS.WINS2019,
            size=OC_CATALOGOFFERING_SIZES.L1
        )
        self.orderItemTest2.set_reference('TestItem2 reference')
        # add Order
        self.orderTest = Order(
            requester=self.personPeter,
            order_type=OrderType.CREATE_ORDER,
            items=[self.orderItemTest1, self.orderItemTest2]
        )
        self.orderTest.set_create_date(datetime.utcnow())

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_1_order_exists(self):
        db.session.add(self.orderTest)
        db.session.add(self.orderItemTest1)
        db.session.commit()
        query = db.session.query(Order).filter(Order.id == 1)
        # query = Order.query.  # wip not finished
        # running_logger = get_oim_logger()
        # running_logger.info('test_1 query:[{}]'.format(query))
        # running_logger.info('test_1 count:[{}]'.format(query.count()))
        assert query.count() == 1

    def test_2_orderItem_exists(self):
        db.session.add(self.orderTest)
        db.session.add(self.orderItemTest1)
        db.session.commit()
        query = OrderItem.query.filter_by(reference='TestItem1 reference')
        assert query.count() == 1

    def test_3_order_doesnt_exists(self):
        db.session.add(self.orderTest)
        db.session.add(self.orderItemTest1)
        db.session.commit()
        query = db.session.query(Order).filter(Order.id == 10)
        assert query.count() == 0

    def test_4_orderItem_doesnt_exist(self):
        db.session.add(self.orderTest)
        db.session.add(self.orderItemTest1)
        db.session.commit()
        query = OrderItem.query.filter_by(reference='TestItem1 no reference')
        assert query.count() == 0

    def test_5_both_orderItems_exist(self):
        db.session.add(self.orderTest)
        db.session.add(self.orderItemTest1)
        db.session.add(self.orderItemTest2)
        db.session.commit()
        query1 = OrderItem.query.filter_by(reference='TestItem1 reference')
        query2 = OrderItem.query.filter_by(reference='TestItem2 reference')
        assert query1.count() == 1
        assert query2.count() == 1

    def test_6_count_orderItems_exist(self):
        db.session.add(self.orderTest)
        db.session.add(self.orderItemTest1)
        db.session.add(self.orderItemTest2)
        db.session.commit()
        query = db.session.query(Order.items)
        assert query.count() == 2

    def test_7_order_createdate_exist(self):
        db.session.add(self.orderTest)
        db.session.add(self.orderItemTest1)
        db.session.add(self.orderItemTest2)
        current_datetime = datetime.utcnow()
        self.orderTest.set_create_date(current_datetime)
        db.session.commit()
        query = db.session.query(Order.create_date)
        for row in query.all():
            cur_create_date = row.create_date

        assert cur_create_date == current_datetime

    def test_8_change_orderType_exist(self):
        db.session.add(self.orderTest)
        db.session.add(self.orderItemTest1)
        db.session.add(self.orderItemTest2)
        # change OrderType from CREATE_ORDER to MODIFY_ORDER
        self.orderTest.set_type(OrderType.MODIFY_ORDER)
        db.session.commit()
        query = db.session.query(Order).filter(Order.id == 1)
        for row in query.all():
            cur_orderType = row.get_type()

        assert cur_orderType == OrderType.MODIFY_ORDER

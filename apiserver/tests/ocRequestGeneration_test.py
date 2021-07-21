import unittest
import os
from datetime import datetime
# from oim_logging import get_oim_logger
from models.orders import Person, SbuType, OrderStateType, VmOrderItem, OrderItem, OrderStatus, Order, OrderType, BackendType, OC_CATALOGOFFERING_SIZES, OC_CATALOGOFFERINGS  # noqa: F401,E501
from app import create_flask_app, db
from ourCloud.OcStaticVars import SERVICE_LEVEL, APPLICATIONS
from workflows.Factory import WorkflowFactory, OrderFactory
from workflows.WorkflowContext import WorkflowContext
from workflows.Workflows import WorkflowTypes


class TestOcRequestJson(unittest.TestCase):
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
        self.orderItemTest1 = VmOrderItem(
            name=OC_CATALOGOFFERINGS.RHEL7,
            size=OC_CATALOGOFFERING_SIZES.S1
        )
        self.orderItemTest1.set_reference('VmTestItem1 reference')
        self.orderItemTest1.set_servicelevel(SERVICE_LEVEL.BASIC)
        self.orderItemTest1.set_appcode(APPLICATIONS.VALUEMATION)
        # add OrderItem2
        self.orderItemTest2 = VmOrderItem(
            name=OC_CATALOGOFFERINGS.WINS2019,
            size=OC_CATALOGOFFERING_SIZES.L1
        )
        self.orderItemTest2.set_reference('VmTestItem2 reference')
        self.orderItemTest2.set_servicelevel(SERVICE_LEVEL.BASIC)
        self.orderItemTest2.set_appcode(APPLICATIONS.VALUEMATION)
        # add Order
        self.testOrder = Order(
            requester=self.personPeter,
            order_type=OrderType.CREATE_ORDER,
            items=[self.orderItemTest1, self.orderItemTest2]
        )
        self.testOrder.set_create_date(datetime.utcnow())

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_1_both_orderItems_exist(self):
        db.session.add(self.testOrder)
        db.session.add(self.orderItemTest1)
        db.session.add(self.orderItemTest2)
        db.session.commit()
        query1 = OrderItem.query.filter_by(reference='VmTestItem1 reference')
        query2 = OrderItem.query.filter_by(reference='VmTestItem2 reference')
        assert query1.count() == 1
        assert query2.count() == 1

    def test_2_order_json_ok(self):
        new_order = OrderFactory().get_order(OrderType.CREATE_ORDER,
                                             [self.orderItemTest1, self.orderItemTest2],
                                             self.personPeter)
        new_order.set_requester(self.personPeter)

        db.session.add(new_order)
        db.session.add(self.orderItemTest1)
        db.session.add(self.orderItemTest2)
        db.session.commit()

        wf = WorkflowFactory().get_workflow(WorkflowTypes.WF_CREATE_VM)
        context = WorkflowContext(self.personPeter)
        wf.set_context(context)
        wf.set_order(new_order)
        wf.execute()

        assert True

    if __name__ == '__main__':
        unittest.main()

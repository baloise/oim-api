import unittest
import flask_unittest
import json
import os
from datetime import datetime
from models.orders import BackendType, Person, SbuType, OrderStateType, OrderItem, OrderStatus, OrderType  # noqa: F401,E501
from models.statuspayload import StatusPayload
from workflows.Factory import OrderFactory
from app import create_flask_app, db


class TestModelStatuspayload(unittest.TestCase):
    def __init__(self, methodName='runTest') -> None:
        super().__init__(methodName=methodName)
        self.order_factory = OrderFactory()

    def prepare_relatives(self):
        db.session.add(self.personPeter)
        db.session.commit()
        items = []
        self.order = self.order_factory.get_order(OrderType.CREATE_ORDER, items, self.personPeter)
        assert self.order is not None
        db.session.add(self.order)

    def setUp(self):
        os.environ['SQLACHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.app = create_flask_app(config_name='unittests')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.drop_all()
        db.create_all()

        self.personPeter = Person(
            username='u12345',
            email='peter.parker@test.fake',
            sbu=SbuType.SHARED
        )

        self.sample_payload_1 = json.dumps(
            {
                'attrib1': 'TheValue1',
                'attrib2': {
                    'key': 'TheKeyName2',
                    'value': 'TheValue2'
                },
                'attrib3': [
                    {'key': 'TheKeyName3a', 'value': 'TheValue3a'},
                    {'key': 'TheKeyName3b', 'value': 'TheValue3b'},
                    {'key': 'TheKeyName3c', 'value': 'TheValue3c'},
                ]
            },
            indent=4
        )

    def tearDown(self):
        db.session.remove()
        self.app_context.pop()

    def test_1_create_new_status(self):
        # Prepare relations first
        self.prepare_relatives()

        status_1_a = OrderStatus(
            state=OrderStateType.NEW,
            since=datetime.now,
            system=BackendType.ORCHESTRA,
            order_id=self.order.id
        )

        db.session.add(status_1_a)
        assert status_1_a is not None

    def test_10_create_new_statuspayload(self):
        # Prepare relations first
        self.prepare_relatives()

        status_10_a = OrderStatus(
            state=OrderStateType.NEW,
            since=datetime.now,
            system=BackendType.ORCHESTRA,
            order_id=self.order.id
        )

        db.session.add(status_10_a)
        assert status_10_a is not None

        payload_10_a = StatusPayload(
            status_id=status_10_a.id,
            payload=self.sample_payload_1
        )
        db.session.add(payload_10_a)
        assert payload_10_a is not None

        db.session.commit()

        found_payloads = StatusPayload.query.filter_by(status_id=status_10_a.id)
        assert found_payloads is not None
        assert found_payloads.count() == 1


class TestApiStatusPayload(flask_unittest.ClientTestCase):
    pass   # Not yet implemented

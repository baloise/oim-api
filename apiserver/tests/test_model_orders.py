import unittest
from inspect import getsourcefile
import os
import sys
# These lines work around importing troubles. __file__ is too unreliable
current_dir = os.path.dirname(os.path.abspath(getsourcefile(lambda: 0)))
sys.path.insert(0, current_dir[:current_dir.rfind(os.path.sep)])
from models.orders import Person, SbuType, OrderItemType, OrderStateType, OrderItem, OrderStatus, Order  # noqa: E402
from components.db import db  # noqa: E402


class TestModelOrder(unittest.TestCase):
    def __init__(self, methodName):
        self.db = db
        super().__init__(methodName)

    def setUp(self):
        #db.init_app('sqlite://:memory:')
        #db.create_all()
        self.personPeter = Person(
            username='u12345',
            email='peter.parker@test.fake',
            sbu=SbuType.SHARED
        )
        db.session.add(self.personPeter)
        return super().setUp()

    def tearDown(self):
        # No specific cleanup yet
        return super().tearDown()

    def test_1_user_exists(self):
        user = Person.query.filter_by(username='b12345')
        assert user is not None


if __name__ == '__main__':
    unittest.main()

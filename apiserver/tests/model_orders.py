import unittest
import os
from models.orders import Person, SbuType, OrderStateType, OrderItem, OrderStatus, Order  # noqa: F401,E501
from app import create_flask_app, db
from sqlalchemy import select, create_engine


class TestModelOrder(unittest.TestCase):
    def setUp(self):
        os.environ['SQLACHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.app = create_flask_app(config_name='unittests')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

        self.personPeter = Person(
            username='u12345',
            email='peter.parker@test.fake',
            sbu=SbuType.SHARED
        )

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_1_user_exists(self):
        db.session.add(self.personPeter)
        db.session.commit()
        # user = Person.query.filter_by(username='u12345g')
        user = db.session.query(Person).filter(Person.username == 'u12345')
        print('User:[{}]'.format(user))

        conn = db.session
        select_st = select([Person.username])
        res = conn.execute(select_st)
        for _row in res:
            print(_row)

        assert user is not None

    def test_2_user_doesnt_exist(self):
        db.session.add(self.personPeter)
        db.session.commit()
        user = Person.query.filter_by(username='b059485')
        assert user.count() == 0


if __name__ == '__main__':
    TD = TestModelOrder()
    TD.setUp()
    TD.test_1_user_exists()

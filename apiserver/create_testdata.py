# create_testdata.py
import os
import enum
import connexion
from load_config import load_config
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from ourCloud.OcStaticVars import OC_CATALOGOFFERINGS, OC_CATALOGOFFERING_SIZES
from oim_logging import get_oim_logger
from models.orders import Person, SbuType, OrderStateType, OrderItem, OrderStatus, Order, BackendType  # noqa: F401,E501
from app import db, create_flask_app
from sqlalchemy import *
from sqlalchemy.orm import sessionmaker

# db = SQLAlchemy()


class TestData():
    def __init__(self):
        # config = load_config()
        os.environ['SQLACHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.app = create_flask_app(config_name='unittests')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def createTestData(self):
        # add Person
        self.personPeter = Person(
            username='u12345',
            email='peter.parker@test.fake',
            sbu=SbuType.SHARED
        )
        db.session.add(self.personPeter)
        db.session.commit()
        # add Order
        self.orderTest = Order(
            requester='',
            type=''
        )
        db.session.add(self.orderTest)
        db.session.commit()
        # add OrderItem
        self.orderItem = OrderItem(
            reference='test123',
            cataloguename='FED123',
            size='100',
            backend_request_id=1,
            order_id=1
        )

    def showTestData(self):
        print("Show Testdata")
        print("Person: Peter")
        # query the person
        # Session = sessionmaker()
        # Session.configure(bind=db)
        # session = Session()
        user = Person.query.filter_by(username='b12345')
        # query = session.query(Person).filter(Person.username == 'u12345')
        for _row in user.all():
            print(_row.id, _row.username, _row.email, _row.sbu, _row.orders)
        print('Resultat -> [{}]'.format(user))
        # result = db.session.query(func.count(Person.id)).group_by(Person.username)
        # print('Resultat 2:[{}]'.format(result))
        # query the order
        # query the order item


if __name__ == '__main__':
    TD = TestData()
    TD.showTestData()

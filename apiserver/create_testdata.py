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
        query = session.query()
        s = db.session.query(func.count(Person.id))
        rs = s.execute()
        print('Resultat 1:[{}]'.format(rs))
        result = db.session.query(func.count(Person.id)).group_by(Person.username)
        print('Resultat 2:[{}]'.format(result))


if __name__ == '__main__':
    TD = TestData()
    TD.showTestData()

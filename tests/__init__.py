import sqlalchemy
import unittest

from sqltree import db, model

def setUpModule():
    global engine, Session, connection, transaction
    engine = sqlalchemy.create_engine(
        'postgresql://merkle:merkle123@localhost/merkle_test',
        echo=False)
    db.bind_engine(engine)
    connection = engine.connect()

    db.create_tables()

    transaction = connection.begin()
    
def tearDownModule():
    transaction.rollback()
    connection.close()
    engine.dispose()

class DatabaseTest(unittest.TestCase):
    def setUp(self):
        self.session = db.Session()
        self.session.begin_nested()

    def tearDown(self):
        self.session.close()


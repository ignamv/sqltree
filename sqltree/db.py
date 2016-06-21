import sqlalchemy.ext.declarative
import sqlalchemy.orm

Base = sqlalchemy.ext.declarative.declarative_base()
Session = sqlalchemy.orm.sessionmaker()
session = None

from . import model

def create_tables():
    Base.metadata.create_all()

def bind_engine(engine):
    Session.configure(bind=engine)
    Base.metadata.bind = engine
    session = Session()


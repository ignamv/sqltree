import sqlalchemy
import enum
from sqlalchemy import types, Column
from sqlalchemy.orm.session import Session

from .db import Base

iccapTypes = dict(
    MODEL = 'Model',
    SETUP = 'Setup',
    DUT = 'Dut',
    PLOT = 'Plot',
)

class IccapTreeNode(Base):
    __tablename__ = 'IccapTreeNode'
    id = Column(types.Integer, primary_key=True)
    parent_id = Column(types.Integer, 
                         sqlalchemy.ForeignKey('IccapTreeNode.id'),
                         index=True)
    children = sqlalchemy.orm.relationship(
        'IccapTreeNode',
        remote_side='IccapTreeNode.parent_id',
        cascade="all, delete-orphan",
        backref=sqlalchemy.orm.backref("parent",
                                       remote_side='IccapTreeNode.id'))
    type = Column(types.Enum(*iccapTypes.keys(), name='IccapType'))
    name = Column(types.String)
    value = Column(types.String)
    
    __table_args__ = (sqlalchemy.schema.UniqueConstraint(
        'parent_id', 'type', 'name'),)

    def __repr__(self):
        return "IccapTreeNode(type='{}', name='{}', value='{}'".format(
            self.type, self.name, self.value)

    def child(self, name):
        session = Session.object_session(self)
        return session.query(IccapTreeNode).filter(
            IccapTreeNode.parent_id == self.id).filter(
                IccapTreeNode.name == name).one()



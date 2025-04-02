"""
('AD-KOTAKB', 'Sent Rs.700.00 from Kotak Bank AC X7054 to q433211742@ybl on 22-11-23.UPI Ref 369269550727. Not you, kotak.com/fraud', '2023-11-22 11:45:58', 'SMS', '919987709059', 0)
"""
from sqlalchemy import Boolean
from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import TIMESTAMP
from sqlalchemy import JSON
from sqlalchemy.orm import relationship

from db.base_class import Base


class iPMessage(Base):
    id = Column(String, primary_key=True, index=True)
    sender = Column(String, nullable=False, index=True)
    text = Column(String, nullable=False)
    timestamp = Column(TIMESTAMP, nullable=False)
    type = Column(String, default=True)
    receiver = Column(String, nullable=False)
    _number_ = Column(String, nullable=False)
    amount = Column(JSON)
    accounts_info = Column(JSON)
    to_id = Column(JSON, nullable=True, default=None)
    usr_acted = Column(Boolean)


class txnMessage(Base):
    id = Column(String, primary_key=True, index=True)
    sender = Column(String, nullable=False, index=True)
    text = Column(String, nullable=False)
    timestamp = Column(String, default=False)
    type = Column(String, default=True)
    receiver = Column(String, nullable=False)
    _number_ = Column(String, nullable=False)
    amount = Column(Integer)
    accounts_info = Column(String)
    to_id = Column(String, nullable=True, default=None)
    usr_acted = Column(Integer, default=0)

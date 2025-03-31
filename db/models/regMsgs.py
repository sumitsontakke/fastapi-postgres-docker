"""
To mark break point for processed messages
"""
from datetime import datetime
from unittest.main import MODULE_EXAMPLES

from sqlalchemy import Boolean
from sqlalchemy import Column
from sqlalchemy import DateTime
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy.orm import relationship

from db.base_class import Base

# Stores raw messages from the iMessages database
class regMsgs(Base):
    id = Column(Integer, primary_key=True)
    sender = Column(String, index=True)
    text = Column(String, index=True)
    timestamp = Column(DateTime, index=True)
    type = Column(String, index=True)
    receiver = Column(String, index=True)
    _number_ = Column(String, index=True)
    is_txn_message = Column(Boolean, default=False)

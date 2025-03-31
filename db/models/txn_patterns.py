from sqlalchemy import Column, Integer, String, Text
from db.base_class import Base


class txnPatterns(Base):
    """
    Schema for the txnPatterns table.
    Stores regex patterns for identifying transaction-related messages.
    """
    id = Column(Integer, primary_key=True, index=True)
    pattern = Column(Text, nullable=False)  # Regex pattern
    description = Column(String, nullable=True)  # Optional description of the pattern
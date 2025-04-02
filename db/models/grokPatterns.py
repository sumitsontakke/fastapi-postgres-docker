from sqlalchemy import Column, Integer, String, Text
from db.base_class import Base


class GrokPattern(Base):
    """
    Schema for the GrokPattern table.
    Stores patterns for extracting specific fields from text messages.
    """
    id = Column(Integer, primary_key=True, index=True)
    field = Column(String, nullable=False)  # Field to extract (e.g., 'amount', 'account')
    pattern = Column(Text, nullable=False)  # Grok pattern for extracting the field
    description = Column(String, nullable=True)  # Optional description of the pattern
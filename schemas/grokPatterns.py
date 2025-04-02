from pydantic import BaseModel
from typing import Optional


class GrokRequest(BaseModel):
    """
    Pydantic model for adding or updating a Grok pattern.
    """
    field: str
    pattern: str
    description: Optional[str] = None


class GrokResponse(BaseModel):
    """
    Pydantic model for returning Grok pattern details.
    """
    id: int
    field: str
    pattern: str
    description: Optional[str] = None

    class Config:
        orm_mode = True
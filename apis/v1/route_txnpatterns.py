from pydantic import BaseModel
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from db.repository.txn_patterns import add_pattern, get_all_patterns, update_pattern
from core.config import log
from db.session import get_db

router = APIRouter()

# Define a Pydantic model for the request body
class PatternRequest(BaseModel):
    pattern: str
    description: str = None


@router.post("/patterns")
def create_pattern(request: PatternRequest, db: Session = Depends(get_db)):
    """
    Add a new transaction pattern to the database.

    Args:
        request (PatternRequest): The request body containing the pattern and description.
        db (Session): The database session.

    Returns:
        dict: The newly created pattern record.
    """
    return add_pattern(db, request.pattern, request.description)

@router.get("/patterns", response_model=list)
def fetch_patterns(db: Session = Depends(get_db)):
    """
    Fetch all transaction patterns from the database.
    """
    return get_all_patterns(db)


@router.put("/patterns/{pattern_id}")
def modify_pattern(pattern_id: int, new_pattern: str, description: str = None, db: Session = Depends(get_db)):
    """
    Update an existing transaction pattern in the database.
    """
    return update_pattern(db, pattern_id, new_pattern, description)
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from db.repository.grokPatterns import (
    add_grok_pattern,
    get_all_grok_patterns,
    update_grok_pattern,
    delete_grok_pattern,
    get_grok_pattern_by_id
)
from db.session import get_db
from core.config import log
from schemas.grokPatterns import GrokRequest, GrokResponse

router = APIRouter()


@router.post("/", response_model=GrokResponse)
def create_grok_pattern(request: GrokRequest, db: Session = Depends(get_db)):
    """
    Add a new Grok pattern to the database.

    Args:
        request (GrokRequest): The request body containing the Grok pattern details.
        db (Session): The database session.

    Returns:
        GrokResponse: The newly created Grok pattern.
    """
    new_pattern = add_grok_pattern(
        db, 
        field=request.field, 
        pattern=request.pattern, 
        description=request.description
    )
    if not new_pattern:
        raise HTTPException(status_code=500, 
                            detail="Failed to add Grok pattern.")
    return new_pattern


@router.get("/", response_model=List[GrokResponse])
def list_grok_patterns(db: Session = Depends(get_db)):
    """
    List all Grok patterns in the database.

    Args:
        db (Session): The database session.

    Returns:
        List[GrokResponse]: A list of all Grok patterns.
    """
    patterns = get_all_grok_patterns(db)
    if not patterns:
        log.warning("No Grok patterns found in the database.")
        raise HTTPException(status_code=404, detail="No Grok patterns found.")
    else:
        log.debug("printing last pattern fetched from database")
        log.info(patterns[-1])
    return patterns


@router.put("/{pattern_id}", response_model=GrokResponse)
def update_grok_pattern_byId(
    pattern_id: int, request: GrokRequest, db: Session = Depends(get_db)
):
    """
    Update an existing Grok pattern in the database.

    Args:
        pattern_id (int): The ID of the Grok pattern to update.
        request (GrokRequest): The request body containing the updated Grok pattern details.
        db (Session): The database session.

    Returns:
        GrokResponse: The updated Grok pattern.
    """
    updated_pattern = update_grok_pattern(
        db,
        pattern_id=pattern_id,
        field=request.field,
        pattern=request.pattern,
        description=request.description,
    )
    if not updated_pattern:
        raise HTTPException(status_code=404, detail="Grok pattern not found.")
    return updated_pattern



@router.get("/{pattern_id}", response_model=GrokResponse)
def get_grok_pattern(pattern_id: int, db: Session = Depends(get_db)):
    """
    Retrieve a single Grok pattern by its ID.

    Args:
        pattern_id (int): The ID of the Grok pattern to retrieve.
        db (Session): The database session.

    Returns:
        GrokResponse: The Grok pattern details.
    """
    pattern = get_grok_pattern_by_id(db=db, pattern_id=pattern_id)

    # If the pattern is not found, raise an HTTPException
    if not pattern:
        log.warning(f"Grok pattern with ID {pattern_id} not found.")
        raise HTTPException(status_code=404, detail="Grok pattern not found.")

    # Log the retrieved pattern for debugging purposes
    log.info(f"Retrieved Grok pattern: {pattern}")

    # Return the pattern as a response
    return pattern


@router.delete("/{pattern_id}", response_model=dict)
def delete_grok_pattern_endpoint(pattern_id: int, db: Session = Depends(get_db)):
    """
    Delete a Grok pattern from the database.
    """
    success = delete_grok_pattern(db, pattern_id)
    if not success:
        raise HTTPException(status_code=404, detail="Grok pattern not found.")
    return {"message": f"Grok pattern with ID {pattern_id} deleted successfully."}


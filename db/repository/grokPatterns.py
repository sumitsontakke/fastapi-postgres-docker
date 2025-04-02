from sqlalchemy.orm import Session
from db.models.grokPatterns import GrokPattern
from core.config import log


def get_all_grok_patterns(db: Session):
    """
    Fetch all Grok patterns from the database.

    Args:
        db (Session): The database session.

    Returns:
        dict: A dictionary where keys are fields (e.g., 'amount') and values are patterns.
    """
    try:
        patterns = db.query(GrokPattern).all()
        log.info(f"db.repository: Loaded {len(patterns)} Grok patterns from the database.")
        # return {pattern.field: pattern.pattern for pattern in patterns}
        return patterns
    except Exception as e:
        log.error(f"Error fetching Grok patterns from the database: {e}")
        return {}


def add_grok_pattern(db: Session, field: str, pattern: str, description: str = None):
    """
    Add a new Grok pattern to the database.

    Args:
        db (Session): The database session.
        field (str): The field to extract (e.g., 'amount').
        pattern (str): The Grok pattern for extracting the field.
        description (str): Optional description of the pattern.

    Returns:
        GrokPattern: The newly created Grok pattern record.
    """
    try:
        new_pattern = GrokPattern(field=field, pattern=pattern, description=description)
        db.add(new_pattern)
        db.commit()
        db.refresh(new_pattern)
        log.info(f"Added new Grok pattern for field '{field}': {pattern}")
        return new_pattern
    except Exception as e:
        log.error(f"Error adding Grok pattern to the database: {e}")
        return None
    
def get_grok_pattern_by_id(db: Session, pattern_id: int):
    try:
        # Query the database for the Grok pattern with the given ID
        pattern = db.query(GrokPattern).filter(GrokPattern.id == pattern_id).first()
        return pattern
    except Exception as e:
        log.warning(f"matching pattern for id:{pattern_id} not found")
    return None


def update_grok_pattern(db: Session, pattern_id: int, field: str, pattern: str, description: str = None):
    """
    Update an existing Grok pattern in the database.

    Args:
        db (Session): The database session.
        pattern_id (int): The ID of the pattern to update.
        field (str): The updated field to extract.
        pattern (str): The updated Grok pattern.
        description (str): Optional updated description of the pattern.

    Returns:
        GrokPattern: The updated Grok pattern record.
    """
    log.info("db.repository: Updating GrokPattern with id", str(pattern_id))
    try:
        existing_pattern = db.query(GrokPattern).filter(GrokPattern.id == pattern_id).first()
        if existing_pattern:
            existing_pattern.field = field
            existing_pattern.pattern = pattern
            existing_pattern.description = description
            db.commit()
            db.refresh(existing_pattern)
            log.info(f"Updated Grok pattern ID {pattern_id} for field '{field}': {pattern}")
            return existing_pattern
        else:
            log.warning(f"Grok pattern ID {pattern_id} not found.")
            return None
    except Exception as e:
        log.error(f"Error updating Grok pattern in the database: {e}")
        return None


def delete_grok_pattern(db: Session, pattern_id: int):
    """
    Delete a Grok pattern from the database.

    Args:
        db (Session): The database session.
        pattern_id (int): The ID of the pattern to delete.

    Returns:
        bool: True if the pattern was deleted, False otherwise.
    """
    try:
        existing_pattern = db.query(GrokPattern).filter(GrokPattern.id == pattern_id).first()
        if existing_pattern:
            db.delete(existing_pattern)
            db.commit()
            log.info(f"Deleted Grok pattern ID {pattern_id}.")
            return True
        else:
            log.warning(f"Grok pattern ID {pattern_id} not found.")
            return False
    except Exception as e:
        log.error(f"Error deleting Grok pattern from the database: {e}")
        return False
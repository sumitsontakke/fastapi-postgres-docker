from sqlalchemy.orm import Session
from db.models.txn_patterns import txnPatterns
from core.config import log


def get_all_patterns(db: Session):
    """
    Fetch all patterns from the txnPatterns table.

    Args:
        db (Session): The database session.

    Returns:
        list: A list of regex patterns.
    """
    try:
        patterns = db.query(txnPatterns).all()
        log.info(f"db.repository: Loaded {len(patterns)} transaction patterns from the database.")
        return [pattern.pattern for pattern in patterns]
    except Exception as e:
        log.error(f"db.repository: Error fetching transaction patterns from the database: {e}")
        return []


def add_pattern(db: Session, pattern: str, description: str = None):
    """
    Add a new pattern to the txnPatterns table.

    Args:
        db (Session): The database session.
        pattern (str): The regex pattern to add.
        description (str): Optional description of the pattern.

    Returns:
        txnPatterns: The newly created pattern record.
    """
    try:
        new_pattern = txnPatterns(pattern=pattern, description=description)
        db.add(new_pattern)
        db.commit()
        db.refresh(new_pattern)
        log.info(f"db.repository: Added new pattern: {pattern}")
        return new_pattern
    except Exception as e:
        log.error(f"db.repository: Error adding pattern to the database: {e}")
        return None


def update_pattern(db: Session, pattern_id: int, new_pattern: str, description: str = None):
    """
    Update an existing pattern in the txnPatterns table.

    Args:
        db (Session): The database session.
        pattern_id (int): The ID of the pattern to update.
        new_pattern (str): The new regex pattern.
        description (str): Optional new description of the pattern.

    Returns:
        txnPatterns: The updated pattern record.
    """
    try:
        pattern = db.query(txnPatterns).filter(txnPatterns.id == pattern_id).first()
        if pattern:
            pattern.pattern = new_pattern
            pattern.description = description
            db.commit()
            db.refresh(pattern)
            log.info(f"db.repository: Updated pattern ID {pattern_id} to: {new_pattern}")
            return pattern
        else:
            log.warning(f"db.repository: Pattern ID {pattern_id} not found.")
            return None
    except Exception as e:
        log.error(f"db.repository: Error updating pattern in the database: {e}")
        return None
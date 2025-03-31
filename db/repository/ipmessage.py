import datetime as dt
import uuid
import json

from sqlalchemy.orm import Session

from core.config import log
from db.models.ipmessage import iPMessage
from db.models.ipmessage import txnMessage
from schemas.ipmessage import createIPMessage
from schemas.txn_msg_schema import txnMsgNewCreate



def create_new_ipmessage(imessage: createIPMessage, db: Session):
    """
    Creates a new iPMessage record in the database.

    Args:
        imessage (createIPMessage): The validated iMessage data from the API request.
        db (Session): The database session.

    Returns:
        iPMessage: The newly created iPMessage record.
    """
    # Convert accounts_info to JSON string if it's a complex structure
    # log.info(f"accounts_info: {imessage.get('accounts_info',None)}")
    # if "accounts_info" in imessage.keys() and isinstance(imessage.get("accounts_info",None), (list, dict)):
    #     imessage.accounts_info = json.dumps(imessage.get("accounts_info",[]))

    # Create a new iPMessage object from the schema
    this_doc = iPMessage(**imessage.dict())

    # Generate a unique ID for the message
    this_doc.id = str(uuid.uuid4())

    # Set default values for additional fields
    this_doc._number_ = "0"
    this_doc.usr_acted = False

    # Add the new record to the database
    db.add(this_doc)
    db.commit()
    db.refresh(this_doc)

    return this_doc


def create_new_txnMsg():
    pass


def find_ipmessage(db, **ipmsg):
    """
    Check if the iMessage already exists in the Application database, iPMessage table.
    If it exists, return True; otherwise, return False.
    :param db: Database session
    :param ipmsg: Dict containing the iMessage details (sender, text, timestamp, type, receiver)
    :return: True if iMessage exists, False if not, None if an error occurs
    """
    try:
        ipmsg = db.query(iPMessage).filter(
            iPMessage.sender == ipmsg["sender"],
            iPMessage.text == ipmsg["text"],
            iPMessage.timestamp == ipmsg["timestamp"],
            iPMessage.type == ipmsg["type"],
            iPMessage.receiver == ipmsg["receiver"],
        ).first()
        # if ipmsg exact match found in iPMessage table, return True
        if ipmsg:
            log.info(f"iMessage already exists in the database: {ipmsg}")
            return True
        else:
            log.info("iMessage not found in the database.")
            return False
    except Exception as e:
        log.error(f"Error in finding iMessage: {e}")
        return None
    
from fastapi import Depends
from sqlalchemy.orm import Session

from business.definitions.iMessages import iMessages
from core.config import log
from db.repository.ipmessage import create_new_ipmessage
from db.repository.ipmessage import find_ipmessage
from db.session import get_db


from datetime import datetime
from sqlalchemy.orm import Session
from core.config import log
from db.repository.ipmessage import create_new_ipmessage, find_ipmessage

from schemas.ipmessage import createIPMessage

def sync_imessages_db(db: Session, imsg: dict):
    """
    Synchronizes a single iMessage with the database.

    Args:
        db (Session): The database session.
        imsg (dict): The iMessage data to synchronize.

    Returns:
        None
    """
    try:
        # log.info(f"Syncing iMessage with the database: {imsg}")
        # log.debug(f"iMessage details: {imsg}")
        # log.info(f"Argument received is of type: {type(imsg)}")

        # Ensure the timestamp is a datetime object
        if isinstance(imsg['timestamp'], str):
            try:
                imsg['timestamp'] = datetime.strptime(imsg['timestamp'], '%Y-%m-%d %H:%M:%S')
            except ValueError as e:
                log.error(f"Invalid timestamp format: {imsg['timestamp']}. Error: {e}")
                raise ValueError("Invalid timestamp format. Expected '%Y-%m-%d %H:%M:%S'.")


        # Extract only the relevant keys for the database query
        imsg_query = {
            'sender': imsg['sender'],
            'text': imsg['text'],
            'timestamp': datetime.strptime(imsg['timestamp'], '%Y-%m-%d %H:%M:%S')
            if isinstance(imsg['timestamp'], str)
            else imsg['timestamp'],
            'type': imsg['type'],
            'receiver': imsg['receiver']
        }

        # Check if the message already exists in the database
        if not find_ipmessage(db, **imsg_query):
            log.info("Message not found in the database. Creating a new record.")
            
            # Validate and clean the imsg dictionary before creating a new record
            cleaned_imsg = {
                "sender": imsg["sender"],
                "text": imsg["text"],
                "timestamp": imsg_query["timestamp"],
                "type": imsg["type"],
                "receiver": imsg["receiver"],
                "_number_": imsg.get("_number_", "0"),
                "amount": imsg.get("amount", [0]),
                "accounts_info": imsg.get("accounts_info", ""),
                "to_id": imsg.get("to_id", "")
            }

            # Convert cleaned_imsg to a Pydantic model
            imessage_model = createIPMessage(**cleaned_imsg)

            # Pass the Pydantic model to create_new_ipmessage
            ip_message = create_new_ipmessage(imessage_model, db=db)
            if ip_message:
                log.info(f'Message synced with database, id: {getattr(ip_message, "id", None)}')
        else:
            log.info("Message already exists in the database. Skipping creation.")

    except Exception as e:
        log.error(f"Error syncing iMessage with the database: {e}")
        raise

def txnmsg_main(db):
    """Process imessages into application database"""
    # Get all imessages from iMessages database (file)
    txn_messages = iMessages.get_messages(iMessages(db=db))
    log.info(f"txn_messages: {txn_messages}")
    # check if txn_msg already in db and add if not available
    log.info(f"Passing messages to sync with \n{len(txn_messages)}")
    # [sync_imessages_db(db, imsg=imsg) for imsg in txn_messages]
    imsg_count = 0
    for imsg in txn_messages:
        log.info(f"Processing message: #{imsg_count}")
        imsg_count += 1
        sync_imessages_db(db, imsg=imsg)
    # post unprocessed imessages
    return {"status": "Success"}


if __name__ == "__main__":
    db: Session = Depends(get_db)
    txnmsg_main(db=db)

import uuid
from business.definitions.iMessages import iMessages
from core.config import log
from db.repository.ipmessage import create_new_ipmessage
from db.repository.ipmessage import find_ipmessage
from db.models.regMsgs import regMsgs


def txnmsgs_refresh_getapi(db):
    """
    returns all imessages with parsed fields
    """
    txn_messages = iMessages.get_messages(iMessages(db=db))
    return txn_messages


def feed_all_msg_into_regMsgs(db):
    """
    Feed all messages into the regMsgs table.
    """
    txn_messages = iMessages.get_all_raw_messages(iMessages(db=db))
    if not txn_messages:
        log.info("No messages to process.")
        return
    log.info(f"Number of messages to process: {len(txn_messages)}")
    log.info(f"Messages: {txn_messages[-1]}")
    # Iterate over the messages and add them to the regMsgs table
    for msg in txn_messages:
        msg_obj = regMsgs(
            sender = msg[0],
            text = msg[1],
            timestamp = msg[2],
            type = msg[3],
            receiver = msg[4],
            _number_ = msg[5],
            is_txn_message = True if "_fi" in msg[0] else False
        )
        db.add(msg_obj)
        db.commit()
        db.refresh(msg_obj)
    log.info(f"Processed {len(txn_messages)} messages and added them to regMsgs.")
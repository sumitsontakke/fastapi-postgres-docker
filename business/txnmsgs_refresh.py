from business.definitions.iMessages import iMessages
from core.config import log
from db.repository.ipmessage import create_new_ipmessage
from db.repository.ipmessage import find_ipmessage


def txnmsgs_refresh_getapi(db):
    """
    returns all imessages with parsed fields
    """
    txn_messages = iMessages.get_messages(iMessages(db=db))
    return txn_messages

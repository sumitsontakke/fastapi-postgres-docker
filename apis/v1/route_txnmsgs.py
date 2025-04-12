"""
### **Summary of API Endpoints**
1. **`GET /test_new_msgs/`**:
   - Fetches the latest transaction messages from the database.
   - Calls a business logic function (`txnmsgs_refresh_getapi`) to process and retrieve the messages.

2. **`POST /syncdb`**:
   - Synchronizes the iMessage database by processing and storing transaction messages.
   - Calls a business logic function (`txnmsg_main`) to handle the synchronization.

3. **`POST /post_new_msgs`**:
   - Creates a new transaction message in the database.
   - Accepts a payload of type `createIPMessage` and inserts it into the database.

"""

from fastapi import APIRouter
from fastapi import Depends
from fastapi import status
from sqlalchemy.orm import Session

from business.txnmsg_main import txnmsg_main, debug_msg_parse
from business.txnmsgs_refresh import txnmsgs_refresh_getapi, feed_all_msg_into_regMsgs
from core.config import log
from db.repository.ipmessage import create_new_ipmessage
from db.session import get_db
from schemas.ipmessage import createIPMessage, txnMsg

# Initialize the API router for transaction message-related endpoints
router = APIRouter()

#  API Endpoint to call feed_all_msg_into_regMsgs from business.txnmsgs_refresh
@router.get("/feed_all_msg_into_regMsgs", status_code=status.HTTP_200_OK)
def feed_regMsgs(db: Session = Depends(get_db)):
    """
    Endpoint: POST /feed_all_msg_into_regMsgs
    Purpose:
        - Feeds all messages into the regMsgs table.
        - Calls the `feed_all_msg_into_regMsgs` function to process and store messages.
    Data Interaction:
        - Uses the database session to insert messages into the regMsgs table.
    Returns:
        - A status message indicating the operation was successful.
    """
    # Call the business logic function to feed messages into regMsgs
    feed_all_msg_into_regMsgs(db=db)
    return {"status": "Ok"}

# @router.get("/test_new_msgs/", status_code=status.HTTP_200_OK)
# async def get_txnmsgs(db: Session = Depends(get_db)):
#     """
#     Endpoint: GET /test_new_msgs/
#     Purpose:
#         - Fetches the latest transaction messages from the database.
#         - Calls the `txnmsgs_refresh_getapi` function to retrieve and process transaction messages.
#     Data Interaction:
#         - Interacts with the database session to fetch transaction messages.
#     Returns:
#         - A dictionary containing the list of transaction messages under the key "m_transactions".
#     """
#     # Log the request for debugging purposes
#     log.info("Fetching transaction messages from the database.")

#     # Call the business logic function to fetch transaction messages
#     data = txnmsgs_refresh_getapi(db)

#     # Log the result of the fetch operation
#     log.info("Fetched transaction messages: %s", data)

#     # Return the fetched transaction messages
#     return {"m_transactions": data}

@router.get("/test_new_msgs/")
def get_txnmsgs(db: Session = Depends(get_db)):
    """
    Endpoint: GET /test_new_msgs/
    Purpose:
        - Fetches the latest transaction messages from the database.
        - Calls the `txnmsgs_refresh_getapi` function to retrieve and process transaction messages.
    Data Interaction:
        - Interacts with the database session to fetch transaction messages.
    Returns:
        - A dictionary containing the list of transaction messages under the key "m_transactions".
    """
    data = txnmsgs_refresh_getapi(db)
    return {"m_transactions": data}

@router.post("/debug-parse", status_code=status.HTTP_200_OK, response_model=dict)
def debbug_txnmsg_parse(request: txnMsg, db: Session = Depends(get_db)):
    parsed_msg = debug_msg_parse(request.message, db)
    return parsed_msg

@router.post("/syncdb", status_code=status.HTTP_200_OK)
async def sync_imsgdb(db: Session = Depends(get_db)):
    """
    Endpoint: POST /syncdb
    Purpose:
        - Synchronizes the iMessage database by processing and storing transaction messages.
        - Calls the `txnmsg_main` function to handle the synchronization logic.
    Data Interaction:
        - Uses the database session to update or insert transaction messages into the database.
    Returns:
        - A status message indicating the synchronization was successful.
    """
    txnmsg_main(db=db)
    return {"status": "Ok"}


@router.post("/post_new_msgs", status_code=status.HTTP_201_CREATED)
async def post_account(imessage: createIPMessage, db: Session = Depends(get_db)):
    """
    Endpoint: POST /post_new_msgs
    Purpose:
        - Creates a new transaction message record in the database.
        - Accepts a payload of type `createIPMessage` to define the new transaction message.
        - Calls the `create_new_ipmessage` function to insert the new record into the database.
    Data Interaction:
        - Inserts a new transaction message into the database using the provided payload.
    Returns:
        - A status message indicating the transaction message was successfully created.
    """
    # Log the incoming payload for debugging purposes
    log.info("Creating new iMessage transaction: %s", imessage)

    # Call the repository function to create a new transaction message
    imsg = create_new_ipmessage(imessage, db=db)

    # Log the result of the creation process
    log.info("New iMessage transaction created: %s", imsg)

    return {"imsg": "ok"}
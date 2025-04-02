from fastapi import APIRouter
from fastapi import Depends
from fastapi import status
from sqlalchemy.orm import Session

from business.txnmsgs_v1 import txnmsg_process, txnmsg_fetch
from core.config import log
from db.session import get_db

# Initialize the API router for transaction message-related endpoints
router = APIRouter()


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
    txnmsg_process(db=db)
    return {"status": "Ok"}

@router.get("/get_txnmsgs", status_code=status.HTTP_200_OK)
def get_txnmsgs(db: Session = Depends(get_db)):
    """
    Endpoint: GET /get_txnmsgs
    Purpose:
        - Fetches the latest transaction messages from the database.
        - Calls the `txnmsgs_refresh_getapi` function to retrieve and process transaction messages.
    Data Interaction:
        - Interacts with the database session to fetch transaction messages.
    Returns:
        - A dictionary containing the list of transaction messages under the key "m_transactions".
    """
    log.info("Fetching transaction messages from the database.")
    all_messages = txnmsg_fetch(db=db)
    return {"data": all_messages}
from typing import List

from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from fastapi import status
from sqlalchemy.orm import Session

from db.repository.bills import create_new_bill
from db.repository.bills import delete_bill_by_id
from db.repository.bills import get_all_bills
from db.repository.bills import get_bill_by_biller
from db.repository.bills import get_bill_by_due_date
from db.repository.bills import get_bill_by_id
from db.repository.bills import get_bill_by_type
from db.repository.bills import update_bill_by_id
from db.session import get_db
from schemas.bills import createBill, viewBill, statusBill, viewBillwithStatus

router = APIRouter()

@router.post("/bills", response_model=viewBill, status_code=status.HTTP_201_CREATED)
def create_bill(bill: createBill, db: Session = Depends(get_db)):
    bill = create_new_bill(bill=bill, db=db)
    # if bill and bill.get("status") == "error":
    #     raise HTTPException(
    #         status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
    #         detail
    #         =bill
    #     )
    return bill

@router.get("/bills", response_model=List[viewBill])
def get_bills(db: Session = Depends(get_db)):
    bills = get_all_bills(db=db)
    return bills

# get list of bills sorted by due date
@router.get("/bills/sorted", response_model=List[viewBillwithStatus])
def get_bills_sorted(db: Session = Depends(get_db)):
    bills = get_all_bills(db=db)
    bills.sort(key=lambda x: x.dueDate)
    for bill in bills:
        if bill.paidAmount >= bill.billAmount:
            bill.status = "Paid"
        elif bill.paidAmount < bill.billAmount and bill.paidAmount > 0:
            bill.status = "Partially Paid"
        else:
            bill.status = "Unpaid"
    return bills

@router.get("/bills/{id}", response_model=viewBill)
def get_bill(id: str, db: Session = Depends(get_db)):
    bill = get_bill_by_id(id=id, db=db)
    if not bill:
        raise HTTPException(
            detail=f"Bill with ID {id} does not exist.",
            status_code=status.HTTP_404_NOT_FOUND,
        )
    return bill

@router.put("/bills/{id}", response_model=viewBill)
def update_bill(id: str, bill: createBill, db: Session = Depends(get_db)):
    bill = update_bill_by_id(id=id, bill=bill, db=db)
    if not bill:
        raise HTTPException(detail=f"Bill with id {id} does not exist")
    return bill

@router.delete("/bills/{id}", response_model=statusBill)
def delete_bill(id: str, db: Session = Depends(get_db)):
    bill = delete_bill_by_id(id=id, db=db)
    if not bill:
        raise HTTPException(detail=f"Bill with id {id} does not exist")
    return {"status": "Deleted Successfully"}

# @router.get("/bills/biller/{biller}", response_model=List[viewBill])
# def get_bill_by_biller(biller: str, db: Session = Depends(get_db)):
#     bills = get_bill_by_biller(biller=biller, db=db)
#     if bills and bills.get("status") == "error":
#         raise HTTPException(
#             status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
#             detail=bills
#         )
#     return bills

# @router.get("/bills/due_date/{dueDate}", response_model=List[viewBill])
# def get_bill_by_due_date(dueDate: str, db: Session = Depends(get_db)):
#     bills = get_bill_by_due_date(dueDate=dueDate, db=db)
#     return bills

@router.get("/bills/type/{type}", response_model=List[viewBill])
def get_bill_by_type(type: str, db: Session = Depends(get_db)):
    bills = get_bill_by_type(type=type, db=db)
    return bills
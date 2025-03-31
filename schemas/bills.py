# scheme required for bills model and as used in repository/bills.py
from datetime import date
from db.models.bills import Bills
from pydantic import BaseModel


class createBill(BaseModel):
    biller: str
    dueDate: str
    type: str
    billAmount: int
    paidAmount: int
    paidStatus: bool

class viewBill(BaseModel):
    id: int
    biller: str
    type: str
    billAmount: int
    paidAmount: int
    dueDate: date
    paidStatus: bool

class viewBillwithStatus(BaseModel):
    id: int
    biller: str
    type: str
    billAmount: int
    paidAmount: int
    dueDate: date
    paidStatus: bool
    status: str

class statusBill(BaseModel):
    status: str
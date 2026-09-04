from pydantic import BaseModel
from typing import Optional
from datetime import date,datetime


# ─── Customer Schemas ────────────────────────────────────────────────────────

class CustomerCreate(BaseModel):
    customer_id:str
    customer_name:str
    email:str
    mobile:str
    city:str
    customer_type:str
    registration_date:Optional[date]=None
    status:Optional[str]="Active"

class CustomerUpdate(BaseModel):
    customer_name:Optional[str]=None
    email:Optional[str]=None
    mobile:Optional[str]=None
    city:Optional[str]=None
    customer_type:Optional[str]=None
    status:Optional[str]=None

class CustomerResponse(BaseModel):
    customer_id:str
    customer_name:str
    email:str
    mobile:str
    city:str
    customer_type:str
    registration_date:Optional[date]=None
    status:Optional[str]=None

    class Config:
        from_attributes=True


# ─── Account Schemas ─────────────────────────────────────────────────────────

class AccountCreate(BaseModel):
    account_id:str
    customer_id:str
    account_type:str
    branch_id:str
    balance:float
    opening_date:Optional[date]=None
    account_status:Optional[str]="Active"

class AccountUpdate(BaseModel):
    account_type:Optional[str]=None
    balance:Optional[float]=None
    account_status:Optional[str]=None

class AccountResponse(BaseModel):
    account_id:str
    customer_id:str
    account_type:str
    branch_id:str
    balance:float
    opening_date:Optional[date]=None
    account_status:Optional[str]=None

    class Config:
        from_attributes=True


# ─── Branch Schemas ──────────────────────────────────────────────────────────

class BranchResponse(BaseModel):
    branch_id:str
    branch_name:str
    city:str
    state:str
    manager_name:str
    ifsc_code:str
    status:Optional[str]=None

    class Config:
        from_attributes=True


# ─── Transaction Schemas ─────────────────────────────────────────────────────

class TransactionCreate(BaseModel):
    transaction_id:str
    account_id:str
    transaction_type:str
    transaction_amount:float
    transaction_date:date
    transaction_mode:str
    merchant_category:Optional[str]=None

class TransactionResponse(BaseModel):
    transaction_id:str
    account_id:str
    transaction_type:str
    transaction_amount:float
    transaction_date:date
    transaction_mode:str
    merchant_category:Optional[str]=None
    transaction_category:Optional[str]=None
    risk_status:Optional[str]=None

    class Config:
        from_attributes=True


# ─── Loan Schemas ────────────────────────────────────────────────────────────

class LoanResponse(BaseModel):
    loan_id:str
    customer_id:str
    loan_type:str
    loan_amount:float
    interest_rate:float
    loan_start_date:Optional[date]=None
    loan_status:Optional[str]=None

    class Config:
        from_attributes=True


# ─── Rejected Record Schema ─────────────────────────────────────────────────

class RejectedRecordResponse(BaseModel):
    id:int
    entity_type:str
    record_data:str
    rejection_reason:str
    rejected_at:datetime
    pipeline_run_id:str

    class Config:
        from_attributes=True


# ─── Pipeline Schema ────────────────────────────────────────────────────────

class PipelineExecutionResponse(BaseModel):
    id:int
    run_id:str
    started_at:datetime
    completed_at:Optional[datetime]=None
    status:str
    summary_json:Optional[str]=None

    class Config:
        from_attributes=True

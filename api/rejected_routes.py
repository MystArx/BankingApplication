from fastapi import APIRouter,HTTPException
from config.logger_config import logger
import pandas as pd
import numpy as np
import os
from config.settings import REJECTED_CUSTOMERS_FILE,REJECTED_ACCOUNTS_FILE,REJECTED_BRANCHES_FILE,REJECTED_TRANSACTIONS_FILE,REJECTED_LOANS_FILE

router=APIRouter(prefix="/api/rejected",tags=["Rejected Records"])


def _read_rejected_csv(filepath,entity_name):
    if not os.path.exists(filepath):
        return {"message":f"No rejected {entity_name} records found","records":[]}
    try:
        df=pd.read_csv(filepath)
        df=df.where(pd.notnull(df),None)
        records=df.to_dict(orient="records")
        return {"total_rejected":len(records),"records":records}
    except Exception as e:
        logger.error(f"Error reading rejected {entity_name}: {e}")
        raise HTTPException(status_code=500,detail=str(e))


@router.get("/customers")
def get_rejected_customers():
    return _read_rejected_csv(REJECTED_CUSTOMERS_FILE,"customers")


@router.get("/accounts")
def get_rejected_accounts():
    return _read_rejected_csv(REJECTED_ACCOUNTS_FILE,"accounts")


@router.get("/branches")
def get_rejected_branches():
    return _read_rejected_csv(REJECTED_BRANCHES_FILE,"branches")


@router.get("/transactions")
def get_rejected_transactions():
    return _read_rejected_csv(REJECTED_TRANSACTIONS_FILE,"transactions")


@router.get("/loans")
def get_rejected_loans():
    return _read_rejected_csv(REJECTED_LOANS_FILE,"loans")

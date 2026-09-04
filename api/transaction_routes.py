from fastapi import APIRouter,HTTPException
from database.database_connection import LocalSession
from models.models import Transaction,Account
from schemas.schemas import TransactionCreate,TransactionResponse
from config.logger_config import logger
from datetime import date

router=APIRouter(prefix="/api/transactions",tags=["Transactions"])


@router.get("/",response_model=list[TransactionResponse])
def get_all_transactions():
    session=LocalSession()
    try:
        transactions=session.query(Transaction).limit(1000).all()
        return transactions
    except Exception as e:
        logger.error(f"Error fetching transactions: {e}")
        raise HTTPException(status_code=500,detail=str(e))
    finally:
        session.close()


@router.get("/high-value",response_model=list[TransactionResponse])
def get_high_value_transactions():
    session=LocalSession()
    try:
        transactions=session.query(Transaction).filter(Transaction.transaction_category=="HIGH VALUE").all()
        return transactions
    except Exception as e:
        logger.error(f"Error fetching high-value transactions: {e}")
        raise HTTPException(status_code=500,detail=str(e))
    finally:
        session.close()


@router.get("/suspicious",response_model=list[TransactionResponse])
def get_suspicious_transactions():
    session=LocalSession()
    try:
        transactions=session.query(Transaction).filter(Transaction.risk_status.in_(["HIGH RISK","MEDIUM RISK"])).all()
        return transactions
    except Exception as e:
        logger.error(f"Error fetching suspicious transactions: {e}")
        raise HTTPException(status_code=500,detail=str(e))
    finally:
        session.close()


@router.get("/{transaction_id}",response_model=TransactionResponse)
def get_transaction_by_id(transaction_id:str):
    session=LocalSession()
    try:
        transaction=session.get(Transaction,transaction_id)
        if transaction is None:
            raise HTTPException(status_code=404,detail="Transaction not found")
        return transaction
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error fetching transaction: {e}")
        raise HTTPException(status_code=500,detail=str(e))
    finally:
        session.close()


@router.post("/",response_model=TransactionResponse)
def create_transaction(txn_data:TransactionCreate):
    session=LocalSession()
    try:
        existing=session.get(Transaction,txn_data.transaction_id)
        if existing:
            raise HTTPException(status_code=400,detail="Transaction already exists")

        account=session.get(Account,txn_data.account_id)
        if account is None:
            raise HTTPException(status_code=400,detail="Account does not exist")

        # Derive transaction_category and risk_status
        amount=txn_data.transaction_amount
        if amount>=100000:
            category="HIGH VALUE"
        elif amount>=50000:
            category="MEDIUM VALUE"
        else:
            category="NORMAL"

        if amount>=200000:
            risk="HIGH RISK"
        elif amount>=100000:
            risk="MEDIUM RISK"
        else:
            risk="NORMAL"

        transaction=Transaction(
            transaction_id=txn_data.transaction_id,
            account_id=txn_data.account_id,
            transaction_type=txn_data.transaction_type,
            transaction_amount=txn_data.transaction_amount,
            transaction_date=txn_data.transaction_date,
            transaction_mode=txn_data.transaction_mode,
            merchant_category=txn_data.merchant_category,
            transaction_category=category,
            risk_status=risk
        )
        session.add(transaction)
        session.commit()
        session.refresh(transaction)
        logger.info(f"Created transaction: {txn_data.transaction_id}")
        return transaction
    except HTTPException:
        raise
    except Exception as e:
        session.rollback()
        logger.error(f"Error creating transaction: {e}")
        raise HTTPException(status_code=500,detail=str(e))
    finally:
        session.close()


@router.get("/account/{account_id}",response_model=list[TransactionResponse])
def get_transactions_by_account(account_id:str):
    session=LocalSession()
    try:
        transactions=session.query(Transaction).filter(Transaction.account_id==account_id).all()
        return transactions
    except Exception as e:
        logger.error(f"Error fetching transactions by account: {e}")
        raise HTTPException(status_code=500,detail=str(e))
    finally:
        session.close()


@router.get("/date/{transaction_date}",response_model=list[TransactionResponse])
def get_transactions_by_date(transaction_date:date):
    session=LocalSession()
    try:
        transactions=session.query(Transaction).filter(Transaction.transaction_date==transaction_date).all()
        return transactions
    except Exception as e:
        logger.error(f"Error fetching transactions by date: {e}")
        raise HTTPException(status_code=500,detail=str(e))
    finally:
        session.close()

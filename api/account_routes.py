from fastapi import APIRouter,HTTPException
from database.database_connection import LocalSession
from models.models import Account,Customer
from schemas.schemas import AccountCreate,AccountUpdate,AccountResponse
from config.logger_config import logger

router=APIRouter(prefix="/api/accounts",tags=["Accounts"])


@router.get("/",response_model=list[AccountResponse])
def get_all_accounts():
    session=LocalSession()
    try:
        accounts=session.query(Account).all()
        return accounts
    except Exception as e:
        logger.error(f"Error fetching accounts: {e}")
        raise HTTPException(status_code=500,detail=str(e))
    finally:
        session.close()


@router.get("/{account_id}",response_model=AccountResponse)
def get_account_by_id(account_id:str):
    session=LocalSession()
    try:
        account=session.get(Account,account_id)
        if account is None:
            raise HTTPException(status_code=404,detail="Account not found")
        return account
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error fetching account: {e}")
        raise HTTPException(status_code=500,detail=str(e))
    finally:
        session.close()


@router.get("/customer/{customer_id}",response_model=list[AccountResponse])
def get_accounts_by_customer(customer_id:str):
    session=LocalSession()
    try:
        accounts=session.query(Account).filter(Account.customer_id==customer_id).all()
        return accounts
    except Exception as e:
        logger.error(f"Error fetching accounts by customer: {e}")
        raise HTTPException(status_code=500,detail=str(e))
    finally:
        session.close()


@router.post("/",response_model=AccountResponse)
def create_account(account_data:AccountCreate):
    session=LocalSession()
    try:
        existing=session.get(Account,account_data.account_id)
        if existing:
            raise HTTPException(status_code=400,detail="Account already exists")

        customer=session.get(Customer,account_data.customer_id)
        if customer is None:
            raise HTTPException(status_code=400,detail="Customer does not exist")

        account=Account(
            account_id=account_data.account_id,
            customer_id=account_data.customer_id,
            account_type=account_data.account_type,
            branch_id=account_data.branch_id,
            balance=account_data.balance,
            opening_date=account_data.opening_date,
            account_status=account_data.account_status
        )
        session.add(account)
        session.commit()
        session.refresh(account)
        logger.info(f"Created account: {account_data.account_id}")
        return account
    except HTTPException:
        raise
    except Exception as e:
        session.rollback()
        logger.error(f"Error creating account: {e}")
        raise HTTPException(status_code=500,detail=str(e))
    finally:
        session.close()


@router.put("/{account_id}",response_model=AccountResponse)
def update_account(account_id:str,account_data:AccountUpdate):
    session=LocalSession()
    try:
        account=session.get(Account,account_id)
        if account is None:
            raise HTTPException(status_code=404,detail="Account not found")

        if account_data.account_type is not None:
            account.account_type=account_data.account_type
        if account_data.balance is not None:
            account.balance=account_data.balance
        if account_data.account_status is not None:
            account.account_status=account_data.account_status

        session.commit()
        session.refresh(account)
        logger.info(f"Updated account: {account_id}")
        return account
    except HTTPException:
        raise
    except Exception as e:
        session.rollback()
        logger.error(f"Error updating account: {e}")
        raise HTTPException(status_code=500,detail=str(e))
    finally:
        session.close()

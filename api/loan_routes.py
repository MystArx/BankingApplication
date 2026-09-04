from fastapi import APIRouter,HTTPException
from database.database_connection import LocalSession
from models.models import Loan
from schemas.schemas import LoanResponse
from config.logger_config import logger

router=APIRouter(prefix="/api/loans",tags=["Loans"])


@router.get("/",response_model=list[LoanResponse])
def get_all_loans():
    session=LocalSession()
    try:
        loans=session.query(Loan).all()
        return loans
    except Exception as e:
        logger.error(f"Error fetching loans: {e}")
        raise HTTPException(status_code=500,detail=str(e))
    finally:
        session.close()


@router.get("/{loan_id}",response_model=LoanResponse)
def get_loan_by_id(loan_id:str):
    session=LocalSession()
    try:
        loan=session.get(Loan,loan_id)
        if loan is None:
            raise HTTPException(status_code=404,detail="Loan not found")
        return loan
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error fetching loan: {e}")
        raise HTTPException(status_code=500,detail=str(e))
    finally:
        session.close()


@router.get("/customer/{customer_id}",response_model=list[LoanResponse])
def get_loans_by_customer(customer_id:str):
    session=LocalSession()
    try:
        loans=session.query(Loan).filter(Loan.customer_id==customer_id).all()
        return loans
    except Exception as e:
        logger.error(f"Error fetching loans by customer: {e}")
        raise HTTPException(status_code=500,detail=str(e))
    finally:
        session.close()

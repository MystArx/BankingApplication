from fastapi import APIRouter,HTTPException
from database.database_connection import LocalSession
from models.models import Transaction,Account,Customer,Loan
from sqlalchemy import func
from config.logger_config import logger

router=APIRouter(prefix="/api/analytics",tags=["Analytics"])


@router.get("/branch-transactions")
def get_branch_transactions():
    session=LocalSession()
    try:
        from models.models import Branch
        results=session.query(
            Branch.branch_name,
            func.sum(Transaction.transaction_amount).label("total_amount"),
            func.count(Transaction.transaction_id).label("transaction_count")
        ).join(Account,Account.branch_id==Branch.branch_id)\
         .join(Transaction,Transaction.account_id==Account.account_id)\
         .group_by(Branch.branch_name)\
         .order_by(func.sum(Transaction.transaction_amount).desc())\
         .all()

        return [{"branch_name":r[0],"total_amount":float(r[1]),"transaction_count":int(r[2])} for r in results]
    except Exception as e:
        logger.error(f"Error in branch-transactions analytics: {e}")
        raise HTTPException(status_code=500,detail=str(e))
    finally:
        session.close()


@router.get("/transaction-modes")
def get_transaction_modes():
    session=LocalSession()
    try:
        results=session.query(
            Transaction.transaction_mode,
            func.count(Transaction.transaction_id).label("count"),
            func.sum(Transaction.transaction_amount).label("total_amount")
        ).group_by(Transaction.transaction_mode)\
         .order_by(func.count(Transaction.transaction_id).desc())\
         .all()

        return [{"transaction_mode":r[0],"count":int(r[1]),"total_amount":float(r[2])} for r in results]
    except Exception as e:
        logger.error(f"Error in transaction-modes analytics: {e}")
        raise HTTPException(status_code=500,detail=str(e))
    finally:
        session.close()


@router.get("/top-customers")
def get_top_customers():
    session=LocalSession()
    try:
        results=session.query(
            Customer.customer_id,
            Customer.customer_name,
            func.sum(Transaction.transaction_amount).label("total_amount"),
            func.count(Transaction.transaction_id).label("transaction_count")
        ).join(Account,Account.customer_id==Customer.customer_id)\
         .join(Transaction,Transaction.account_id==Account.account_id)\
         .group_by(Customer.customer_id,Customer.customer_name)\
         .order_by(func.sum(Transaction.transaction_amount).desc())\
         .limit(20)\
         .all()

        return [{"customer_id":r[0],"customer_name":r[1],"total_amount":float(r[2]),"transaction_count":int(r[3])} for r in results]
    except Exception as e:
        logger.error(f"Error in top-customers analytics: {e}")
        raise HTTPException(status_code=500,detail=str(e))
    finally:
        session.close()


@router.get("/city-transactions")
def get_city_transactions():
    session=LocalSession()
    try:
        from models.models import Branch
        results=session.query(
            Branch.city,
            func.sum(Transaction.transaction_amount).label("total_amount"),
            func.count(Transaction.transaction_id).label("transaction_count")
        ).join(Account,Account.branch_id==Branch.branch_id)\
         .join(Transaction,Transaction.account_id==Account.account_id)\
         .group_by(Branch.city)\
         .order_by(func.sum(Transaction.transaction_amount).desc())\
         .all()

        return [{"city":r[0],"total_amount":float(r[1]),"transaction_count":int(r[2])} for r in results]
    except Exception as e:
        logger.error(f"Error in city-transactions analytics: {e}")
        raise HTTPException(status_code=500,detail=str(e))
    finally:
        session.close()


@router.get("/monthly-transactions")
def get_monthly_transactions():
    session=LocalSession()
    try:
        results=session.query(
            func.date_format(Transaction.transaction_date,"%Y-%m").label("month"),
            func.sum(Transaction.transaction_amount).label("total_amount"),
            func.count(Transaction.transaction_id).label("transaction_count")
        ).group_by(func.date_format(Transaction.transaction_date,"%Y-%m"))\
         .order_by(func.date_format(Transaction.transaction_date,"%Y-%m"))\
         .all()

        return [{"month":r[0],"total_amount":float(r[1]),"transaction_count":int(r[2])} for r in results]
    except Exception as e:
        logger.error(f"Error in monthly-transactions analytics: {e}")
        raise HTTPException(status_code=500,detail=str(e))
    finally:
        session.close()


@router.get("/loan-portfolio")
def get_loan_portfolio():
    session=LocalSession()
    try:
        results=session.query(
            Loan.loan_type,
            func.sum(Loan.loan_amount).label("total_amount"),
            func.count(Loan.loan_id).label("loan_count")
        ).group_by(Loan.loan_type)\
         .order_by(func.sum(Loan.loan_amount).desc())\
         .all()

        return [{"loan_type":r[0],"total_amount":float(r[1]),"loan_count":int(r[2])} for r in results]
    except Exception as e:
        logger.error(f"Error in loan-portfolio analytics: {e}")
        raise HTTPException(status_code=500,detail=str(e))
    finally:
        session.close()


@router.get("/risk-summary")
def get_risk_summary():
    session=LocalSession()
    try:
        results=session.query(
            Transaction.risk_status,
            func.count(Transaction.transaction_id).label("count"),
            func.sum(Transaction.transaction_amount).label("total_amount")
        ).group_by(Transaction.risk_status)\
         .all()

        return [{"risk_status":r[0],"count":int(r[1]),"total_amount":float(r[2])} for r in results]
    except Exception as e:
        logger.error(f"Error in risk-summary analytics: {e}")
        raise HTTPException(status_code=500,detail=str(e))
    finally:
        session.close()

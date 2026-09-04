from database.database_connection import LocalSession
from models.models import Transaction,Account,Customer,Branch,Loan
from sqlalchemy import func
from config.logger_config import logger


def get_branch_transaction_data():
    session=LocalSession()
    try:
        results=session.query(
            Branch.branch_name,
            func.sum(Transaction.transaction_amount).label("total_amount")
        ).join(Account,Account.branch_id==Branch.branch_id)\
         .join(Transaction,Transaction.account_id==Account.account_id)\
         .group_by(Branch.branch_name)\
         .order_by(func.sum(Transaction.transaction_amount).desc())\
         .limit(15)\
         .all()
        return [(r[0],float(r[1])) for r in results]
    except Exception as e:
        logger.error(f"Error in analytics: {e}")
        return []
    finally:
        session.close()


def get_transaction_mode_data():
    session=LocalSession()
    try:
        results=session.query(
            Transaction.transaction_mode,
            func.count(Transaction.transaction_id).label("count")
        ).group_by(Transaction.transaction_mode).all()
        return [(r[0],int(r[1])) for r in results]
    except Exception as e:
        logger.error(f"Error in analytics: {e}")
        return []
    finally:
        session.close()


def get_daily_transaction_data():
    session=LocalSession()
    try:
        results=session.query(
            Transaction.transaction_date,
            func.sum(Transaction.transaction_amount).label("total_amount")
        ).group_by(Transaction.transaction_date)\
         .order_by(Transaction.transaction_date)\
         .all()
        return [(str(r[0]),float(r[1])) for r in results]
    except Exception as e:
        logger.error(f"Error in analytics: {e}")
        return []
    finally:
        session.close()


def get_loan_distribution_data():
    session=LocalSession()
    try:
        results=session.query(
            Loan.loan_type,
            func.sum(Loan.loan_amount).label("total_amount")
        ).group_by(Loan.loan_type)\
         .order_by(func.sum(Loan.loan_amount).desc())\
         .all()
        return [(r[0],float(r[1])) for r in results]
    except Exception as e:
        logger.error(f"Error in analytics: {e}")
        return []
    finally:
        session.close()


def get_risk_analysis_data():
    session=LocalSession()
    try:
        results=session.query(
            Transaction.risk_status,
            func.count(Transaction.transaction_id).label("count")
        ).group_by(Transaction.risk_status).all()
        return [(r[0],int(r[1])) for r in results]
    except Exception as e:
        logger.error(f"Error in analytics: {e}")
        return []
    finally:
        session.close()

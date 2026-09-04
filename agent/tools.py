import requests
import json
from langchain_core.tools import tool
from database.database_connection import LocalSession
from models.models import Customer, Account, Branch, Transaction, Loan
from sqlalchemy import func

BASE_URL = "http://127.0.0.1:8000"


@tool
def get_all_customers(limit: int = 10) -> str:
    """List banking customers from the platform (up to specified limit)."""
    try:
        res = requests.get(f"{BASE_URL}/api/customers", timeout=3)
        if res.status_code == 200:
            return json.dumps(res.json()[:limit])
    except Exception:
        pass

    session = LocalSession()
    try:
        customers = session.query(Customer).limit(limit).all()
        return json.dumps([{
            "customer_id": c.customer_id,
            "customer_name": c.customer_name,
            "city": c.city,
            "customer_type": c.customer_type,
            "status": c.status
        } for c in customers])
    finally:
        session.close()


@tool
def get_customer_details(customer_id: str) -> str:
    """Fetch profile details for a specific customer by customer_id (e.g. C0001)."""
    try:
        res = requests.get(f"{BASE_URL}/api/customers/{customer_id}", timeout=3)
        if res.status_code == 200:
            return json.dumps(res.json())
    except Exception:
        pass

    session = LocalSession()
    try:
        customer = session.get(Customer, customer_id)
        if customer:
            return json.dumps({
                "customer_id": customer.customer_id,
                "customer_name": customer.customer_name,
                "email": customer.email,
                "mobile": customer.mobile,
                "city": customer.city,
                "customer_type": customer.customer_type,
                "status": customer.status
            })
        return f"Customer {customer_id} not found."
    finally:
        session.close()


@tool
def get_all_accounts(limit: int = 10) -> str:
    """List bank accounts from the platform (up to specified limit)."""
    try:
        res = requests.get(f"{BASE_URL}/api/accounts", timeout=3)
        if res.status_code == 200:
            return json.dumps(res.json()[:limit])
    except Exception:
        pass

    session = LocalSession()
    try:
        accounts = session.query(Account).limit(limit).all()
        return json.dumps([{
            "account_id": a.account_id,
            "customer_id": a.customer_id,
            "account_type": a.account_type,
            "balance": a.balance,
            "account_status": a.account_status
        } for a in accounts])
    finally:
        session.close()


@tool
def get_customer_accounts(customer_id: str) -> str:
    """Get all bank accounts belonging to a specific customer_id (e.g. C0001)."""
    try:
        res = requests.get(f"{BASE_URL}/api/accounts/customer/{customer_id}", timeout=3)
        if res.status_code == 200:
            return json.dumps(res.json())
    except Exception:
        pass

    session = LocalSession()
    try:
        accounts = session.query(Account).filter(Account.customer_id == customer_id).all()
        return json.dumps([{
            "account_id": a.account_id,
            "account_type": a.account_type,
            "balance": a.balance,
            "account_status": a.account_status,
            "branch_id": a.branch_id
        } for a in accounts])
    finally:
        session.close()


@tool
def get_all_branches() -> str:
    """List all bank branches across all cities."""
    try:
        res = requests.get(f"{BASE_URL}/api/branches", timeout=3)
        if res.status_code == 200:
            return json.dumps(res.json()[:15])
    except Exception:
        pass

    session = LocalSession()
    try:
        branches = session.query(Branch).limit(15).all()
        return json.dumps([{
            "branch_id": b.branch_id,
            "branch_name": b.branch_name,
            "city": b.city,
            "ifsc_code": b.ifsc_code
        } for b in branches])
    finally:
        session.close()


@tool
def get_suspicious_transactions(limit: int = 10) -> str:
    """Fetch high risk and suspicious transactions flagged by fraud analytics rules."""
    try:
        res = requests.get(f"{BASE_URL}/api/transactions/suspicious", timeout=3)
        if res.status_code == 200:
            return json.dumps(res.json()[:limit])
    except Exception:
        pass

    session = LocalSession()
    try:
        txns = session.query(Transaction).filter(Transaction.risk_status.in_(["HIGH RISK", "MEDIUM RISK"])).limit(limit).all()
        return json.dumps([{
            "transaction_id": t.transaction_id,
            "account_id": t.account_id,
            "amount": t.transaction_amount,
            "type": t.transaction_type,
            "mode": t.transaction_mode,
            "risk_status": t.risk_status
        } for t in txns])
    finally:
        session.close()


@tool
def get_branch_performance_summary() -> str:
    """Get branch-wise transaction totals and counts across all banking branches."""
    try:
        res = requests.get(f"{BASE_URL}/api/analytics/branch-transactions", timeout=3)
        if res.status_code == 200:
            return json.dumps(res.json()[:10])
    except Exception:
        pass

    session = LocalSession()
    try:
        results = session.query(
            Branch.branch_name,
            func.sum(Transaction.transaction_amount).label("total_amount"),
            func.count(Transaction.transaction_id).label("count")
        ).join(Account, Account.branch_id == Branch.branch_id)\
         .join(Transaction, Transaction.account_id == Account.account_id)\
         .group_by(Branch.branch_name)\
         .order_by(func.sum(Transaction.transaction_amount).desc())\
         .limit(10).all()

        return json.dumps([{
            "branch_name": r[0],
            "total_amount": float(r[1]),
            "transaction_count": int(r[2])
        } for r in results])
    finally:
        session.close()


@tool
def get_rejected_records_summary() -> str:
    """Get summary count and reasons for rejected records across customers, accounts, branches, transactions, and loans."""
    summary = {}
    for entity in ["customers", "accounts", "branches", "transactions", "loans"]:
        try:
            res = requests.get(f"{BASE_URL}/api/rejected/{entity}", timeout=3)
            if res.status_code == 200:
                data = res.json()
                summary[entity] = {
                    "total_rejected": data.get("total_rejected", 0),
                    "sample_reasons": [r.get("rejection_reason") for r in data.get("records", [])[:3] if r.get("rejection_reason")]
                }
        except Exception:
            pass

    if summary:
        return json.dumps(summary)

    return json.dumps({"status": "Rejected CSVs stored in data/rejected/."})


@tool
def trigger_data_pipeline() -> str:
    """Trigger an execution of the Enterprise Banking ETL Data Pipeline."""
    try:
        res = requests.post(f"{BASE_URL}/api/pipeline/run", timeout=15)
        if res.status_code == 200:
            return json.dumps(res.json())
    except Exception:
        pass

    from pipeline.run_pipeline import run_pipeline
    summary = run_pipeline()
    return json.dumps(summary)


ALL_TOOLS = [
    get_all_customers,
    get_customer_details,
    get_all_accounts,
    get_customer_accounts,
    get_all_branches,
    get_suspicious_transactions,
    get_branch_performance_summary,
    get_rejected_records_summary,
    trigger_data_pipeline
]

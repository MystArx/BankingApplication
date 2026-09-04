import uuid
import json
from datetime import datetime

from pipeline.extract import extract_customers,extract_accounts,extract_branches,extract_transactions,extract_loans

from pipeline.load import load_customers,load_accounts,load_branches,load_transactions,load_loans

from pipeline.transform import transform_transactions

from pipeline.validate import validate_customers,validate_branches,validate_accounts,validate_transactions,validate_loans

from config.logger_config import logger

from database.database_connection import LocalSession
from models.models import PipelineExecution


def run_pipeline():
    pipeline_run_id=str(uuid.uuid4())[:8]
    started_at=datetime.now()

    logger.info(f"Pipeline started - Run ID: {pipeline_run_id}")
    print("="*60)
    print(f"Banking Data Pipeline - Run ID: {pipeline_run_id}")
    print("="*60)

    # ─── Extract ─────────────────────────────────────────────
    print("Extracting...")
    logger.info("Extracting Customers")
    customers_df=extract_customers()

    logger.info("Extracting Branches")
    branches_df=extract_branches()

    logger.info("Extracting Accounts")
    accounts_df=extract_accounts()

    logger.info("Extracting Transactions")
    transactions_df=extract_transactions()

    logger.info("Extracting Loans")
    loans_df=extract_loans()

    # ─── Validate ────────────────────────────────────────────
    print("Validating...")
    logger.info("Validating Customers")
    valid_customers_df,cust_received,cust_loaded,cust_rejected=validate_customers(customers_df,pipeline_run_id)

    valid_customer_ids=set(valid_customers_df["customer_id"].astype(str).str.strip().tolist())

    logger.info("Validating Branches")
    valid_branches_df,branch_received,branch_loaded,branch_rejected=validate_branches(branches_df,pipeline_run_id)

    valid_branch_ids=set(valid_branches_df["branch_id"].astype(str).str.strip().tolist())

    logger.info("Validating Accounts")
    valid_accounts_df,acct_received,acct_loaded,acct_rejected=validate_accounts(accounts_df,valid_customer_ids,valid_branch_ids,pipeline_run_id)


    valid_account_ids=set(valid_accounts_df["account_id"].astype(str).str.strip().tolist())

    # Build account balance map for transaction validation
    account_balances={}
    for i in range(len(valid_accounts_df)):
        row=valid_accounts_df.iloc[i]
        account_balances[str(row["account_id"]).strip()]=float(row["balance"])

    logger.info("Validating Transactions")
    valid_transactions_df,txn_received,txn_loaded,txn_rejected=validate_transactions(transactions_df,valid_account_ids,account_balances,pipeline_run_id)

    logger.info("Validating Loans")
    valid_loans_df,loan_received,loan_loaded,loan_rejected=validate_loans(loans_df,valid_customer_ids,pipeline_run_id)

    # ─── Transform ───────────────────────────────────────────
    print("Transforming...")
    logger.info("Transforming Transactions")
    final_transactions_df=transform_transactions(valid_transactions_df,valid_accounts_df,valid_customers_df,valid_branches_df)

    # ─── Load ────────────────────────────────────────────────
    print("Loading...")
    logger.info("Loading Customers")
    load_customers(valid_customers_df)

    logger.info("Loading Branches")
    load_branches(valid_branches_df)

    logger.info("Loading Accounts")
    load_accounts(valid_accounts_df)

    logger.info("Loading Transactions")
    load_transactions(final_transactions_df)

    logger.info("Loading Loans")
    load_loans(valid_loans_df)

    # ─── Pipeline Summary ────────────────────────────────────
    completed_at=datetime.now()

    summary={
        "status":"SUCCESS",
        "pipeline_run_id":pipeline_run_id,
        "customers_received":int(cust_received),
        "customers_loaded":int(cust_loaded),
        "customers_rejected":int(cust_rejected),
        "accounts_received":int(acct_received),
        "accounts_loaded":int(acct_loaded),
        "accounts_rejected":int(acct_rejected),
        "branches_received":int(branch_received),
        "branches_loaded":int(branch_loaded),
        "branches_rejected":int(branch_rejected),
        "transactions_received":int(txn_received),
        "transactions_loaded":int(txn_loaded),
        "transactions_rejected":int(txn_rejected),
        "loans_received":int(loan_received),
        "loans_loaded":int(loan_loaded),
        "loans_rejected":int(loan_rejected),
        "status_message":"Banking Data Pipeline completed successfully"
    }

    # Save pipeline execution record
    try:
        session=LocalSession()
        execution=PipelineExecution(
            run_id=pipeline_run_id,
            started_at=started_at,
            completed_at=completed_at,
            status="SUCCESS",
            summary_json=json.dumps(summary)
        )
        session.add(execution)
        session.commit()
        session.close()
    except Exception as e:
        logger.error(f"Error saving pipeline execution: {e}")

    print("="*60)
    print(json.dumps(summary,indent=4))
    print("="*60)
    logger.info("Pipeline completed successfully")

    return summary


if __name__=="__main__":
    from database.create_tables import create_tables
    create_tables()
    run_pipeline()

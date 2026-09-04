from database.database_connection import LocalSession

from models.models import Customer,Account,Branch,Transaction,Loan,RejectedRecord

from config.logger_config import logger

import pandas as pd


def load_customers(customers_df):
    session=LocalSession()
    try:
        for i in range(len(customers_df)):
            row=customers_df.iloc[i]
            customer_id=str(row["customer_id"]).strip()
            existing=session.get(Customer,customer_id)

            if existing is None:
                customer=Customer(
                    customer_id=customer_id,
                    customer_name=str(row["customer_name"]),
                    email=str(row["email"]),
                    mobile=str(row["mobile"]),
                    city=str(row["city"]),
                    customer_type=str(row["customer_type"]),
                    registration_date=pd.to_datetime(row["registration_date"]).date() if not pd.isna(row["registration_date"]) else None,
                    status=str(row["status"]) if not pd.isna(row["status"]) else "Active"
                )
                session.add(customer)

        session.commit()
        logger.info("Loaded customers")

    except Exception as e:
        session.rollback()
        logger.error(f"Error loading customers: {e}")

    finally:
        session.close()


def load_branches(branches_df):
    session=LocalSession()
    try:
        for i in range(len(branches_df)):
            row=branches_df.iloc[i]
            branch_id=str(row["branch_id"]).strip()
            existing=session.get(Branch,branch_id)

            if existing is None:
                branch=Branch(
                    branch_id=branch_id,
                    branch_name=str(row["branch_name"]),
                    city=str(row["city"]),
                    state=str(row["state"]),
                    manager_name=str(row["manager_name"]),
                    ifsc_code=str(row["ifsc_code"]),
                    status=str(row["status"]) if not pd.isna(row["status"]) else "Active"
                )
                session.add(branch)

        session.commit()
        logger.info("Loaded branches")

    except Exception as e:
        session.rollback()
        logger.error(f"Error loading branches: {e}")

    finally:
        session.close()


def load_accounts(accounts_df):
    session=LocalSession()
    try:
        for i in range(len(accounts_df)):
            row=accounts_df.iloc[i]
            account_id=str(row["account_id"]).strip()
            existing=session.get(Account,account_id)

            if existing is None:
                account=Account(
                    account_id=account_id,
                    customer_id=str(row["customer_id"]).strip(),
                    account_type=str(row["account_type"]),
                    branch_id=str(row["branch_id"]).strip(),
                    balance=float(row["balance"]),
                    opening_date=pd.to_datetime(row["opening_date"]).date() if not pd.isna(row["opening_date"]) else None,
                    account_status=str(row["account_status"]) if not pd.isna(row["account_status"]) else "Active"
                )
                session.add(account)

        session.commit()
        logger.info("Loaded accounts")

    except Exception as e:
        session.rollback()
        logger.error(f"Error loading accounts: {e}")

    finally:
        session.close()


def load_transactions(transactions_df):
    session=LocalSession()
    try:
        for i in range(len(transactions_df)):
            row=transactions_df.iloc[i]
            transaction_id=str(row["transaction_id"]).strip()
            existing=session.get(Transaction,transaction_id)

            if existing is None:
                transaction=Transaction(
                    transaction_id=transaction_id,
                    account_id=str(row["account_id"]).strip(),
                    transaction_type=str(row["transaction_type"]),
                    transaction_amount=float(row["transaction_amount"]),
                    transaction_date=pd.to_datetime(row["transaction_date"]).date(),
                    transaction_mode=str(row["transaction_mode"]),
                    merchant_category=str(row["merchant_category"]) if not pd.isna(row.get("merchant_category")) else None,
                    transaction_category=str(row["transaction_category"]) if "transaction_category" in row and not pd.isna(row["transaction_category"]) else None,
                    risk_status=str(row["risk_status"]) if "risk_status" in row and not pd.isna(row["risk_status"]) else None
                )
                session.add(transaction)

        session.commit()
        logger.info("Loaded transactions")

    except Exception as e:
        session.rollback()
        logger.error(f"Error loading transactions: {e}")

    finally:
        session.close()


def load_loans(loans_df):
    session=LocalSession()
    try:
        for i in range(len(loans_df)):
            row=loans_df.iloc[i]
            loan_id=str(row["loan_id"]).strip()
            existing=session.get(Loan,loan_id)

            if existing is None:
                loan=Loan(
                    loan_id=loan_id,
                    customer_id=str(row["customer_id"]).strip(),
                    loan_type=str(row["loan_type"]),
                    loan_amount=float(row["loan_amount"]),
                    interest_rate=float(row["interest_rate"]),
                    loan_start_date=pd.to_datetime(row["loan_start_date"]).date() if not pd.isna(row["loan_start_date"]) else None,
                    loan_status=str(row["loan_status"]) if not pd.isna(row["loan_status"]) else "Active"
                )
                session.add(loan)

        session.commit()
        logger.info("Loaded loans")

    except Exception as e:
        session.rollback()
        logger.error(f"Error loading loans: {e}")

    finally:
        session.close()

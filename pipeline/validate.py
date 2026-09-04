import pandas as pd
import re
from datetime import datetime

from config.settings import REJECTED_CUSTOMERS_FILE,REJECTED_ACCOUNTS_FILE,REJECTED_BRANCHES_FILE,REJECTED_TRANSACTIONS_FILE,REJECTED_LOANS_FILE

from config.logger_config import logger

def validate_branches(branches_df,pipeline_run_id="default"):
    logger.info("Starting branch validation")
    valid_records=[]
    invalid_records=[]
    seen_ids=set()

    ifsc_pattern=re.compile(r"^[A-Z]{4}0[A-Z0-9]{6}$")

    for i in range(len(branches_df)):
        row=branches_df.iloc[i]
        reasons=[]

        if pd.isna(row["branch_id"]) or str(row["branch_id"]).strip()=="":
            reasons.append("branch_id missing")

        bid=str(row["branch_id"]).strip()
        if bid in seen_ids and bid!="":
            reasons.append("duplicate branch_id")
        seen_ids.add(bid)

        if pd.isna(row["branch_name"]) or str(row["branch_name"]).strip()=="":
            reasons.append("branch_name missing")

        if pd.isna(row["city"]) or str(row["city"]).strip()=="":
            reasons.append("city missing")

        ifsc_val=str(row["ifsc_code"]).strip() if not pd.isna(row["ifsc_code"]) else ""
        if not ifsc_pattern.match(ifsc_val):
            reasons.append("invalid IFSC")

        if pd.isna(row["manager_name"]) or str(row["manager_name"]).strip()=="":
            reasons.append("manager name missing")

        if reasons:
            record=row.to_dict()
            record["rejection_reason"]="; ".join(reasons)
            record["rejected_at"]=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            record["pipeline_run_id"]=pipeline_run_id
            invalid_records.append(record)
        else:
            valid_records.append(row.to_dict())

    valid_df=pd.DataFrame(valid_records) if valid_records else pd.DataFrame(columns=branches_df.columns)
    invalid_df=pd.DataFrame(invalid_records) if invalid_records else pd.DataFrame()

    if not invalid_df.empty:
        invalid_df.to_csv(REJECTED_BRANCHES_FILE,index=False)

    logger.info(f"Valid Branches : {len(valid_df)}")
    logger.info(f"Invalid Branches : {len(invalid_df)}")
    logger.info("Branch Validation Complete")

    return valid_df,len(branches_df),len(valid_df),len(invalid_df)


def validate_customers(customers_df,pipeline_run_id="default"):
    logger.info("Starting customer validation")
    valid_records=[]
    invalid_records=[]
    seen_ids=set()

    email_pattern=re.compile(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$")
    mobile_pattern=re.compile(r"^[1-9]\d{9}$")
    valid_types={"Regular","Premium","Corporate"}

    for i in range(len(customers_df)):
        row=customers_df.iloc[i]
        reasons=[]

        if pd.isna(row["customer_id"]) or str(row["customer_id"]).strip()=="":
            reasons.append("customer_id is missing")

        if pd.isna(row["customer_name"]) or str(row["customer_name"]).strip()=="":
            reasons.append("customer_name is missing")

        cid=str(row["customer_id"]).strip()
        if cid in seen_ids and cid!="":
            reasons.append("duplicate customer_id")
        seen_ids.add(cid)

        email_val=str(row["email"]).strip() if not pd.isna(row["email"]) else ""
        if not email_pattern.match(email_val):
            reasons.append("invalid email")

        mobile_val=str(row["mobile"]).strip() if not pd.isna(row["mobile"]) else ""
        if not mobile_pattern.match(mobile_val):
            reasons.append("invalid mobile number")

        ctype=str(row["customer_type"]).strip() if not pd.isna(row["customer_type"]) else ""
        if ctype not in valid_types:
            reasons.append("invalid customer_type")

        if reasons:
            record=row.to_dict()
            record["rejection_reason"]="; ".join(reasons)
            record["rejected_at"]=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            record["pipeline_run_id"]=pipeline_run_id
            invalid_records.append(record)
        else:
            valid_records.append(row.to_dict())

    valid_df=pd.DataFrame(valid_records) if valid_records else pd.DataFrame(columns=customers_df.columns)
    invalid_df=pd.DataFrame(invalid_records) if invalid_records else pd.DataFrame()

    if not invalid_df.empty:
        invalid_df.to_csv(REJECTED_CUSTOMERS_FILE,index=False)

    logger.info(f"Valid Customers : {len(valid_df)}")
    logger.info(f"Invalid Customers : {len(invalid_df)}")
    logger.info("Customer Validation Complete")

    return valid_df,len(customers_df),len(valid_df),len(invalid_df)




def validate_accounts(accounts_df,valid_customer_ids,valid_branch_ids,pipeline_run_id="default"):
    logger.info("Starting account validation")
    valid_records=[]
    invalid_records=[]
    seen_ids=set()

    valid_account_types={"Savings","Current","Salary","Business"}

    accounts_df["balance"]=pd.to_numeric(accounts_df["balance"],errors="coerce")

    for i in range(len(accounts_df)):
        row=accounts_df.iloc[i]
        reasons=[]

        if pd.isna(row["account_id"]) or str(row["account_id"]).strip()=="":
            reasons.append("account_id missing")

        aid=str(row["account_id"]).strip()
        if aid in seen_ids and aid!="":
            reasons.append("duplicate account_id")
        seen_ids.add(aid)

        if pd.isna(row["customer_id"]) or str(row["customer_id"]).strip()=="":
            reasons.append("customer_id missing")
        else:
            cid=str(row["customer_id"]).strip()
            if cid not in valid_customer_ids:
                reasons.append("customer does not exist")

        if pd.isna(row.get("branch_id")) or str(row.get("branch_id")).strip()=="":
            reasons.append("branch_id missing")
        else:
            bid=str(row.get("branch_id")).strip()
            if bid not in valid_branch_ids:
                reasons.append("branch does not exist")

        if pd.isna(row["balance"]) or row["balance"]<0:
            reasons.append("balance < 0")


        atype=str(row["account_type"]).strip() if not pd.isna(row["account_type"]) else ""
        if atype not in valid_account_types:
            reasons.append("invalid account_type")

        opening_date_val=str(row["opening_date"]).strip() if not pd.isna(row["opening_date"]) else ""
        try:
            if opening_date_val:
                pd.to_datetime(opening_date_val)
        except:
            reasons.append("invalid opening_date")

        if reasons:
            record=row.to_dict()
            record["rejection_reason"]="; ".join(reasons)
            record["rejected_at"]=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            record["pipeline_run_id"]=pipeline_run_id
            invalid_records.append(record)
        else:
            valid_records.append(row.to_dict())

    valid_df=pd.DataFrame(valid_records) if valid_records else pd.DataFrame(columns=accounts_df.columns)
    invalid_df=pd.DataFrame(invalid_records) if invalid_records else pd.DataFrame()

    if not invalid_df.empty:
        invalid_df.to_csv(REJECTED_ACCOUNTS_FILE,index=False)

    logger.info(f"Valid Accounts : {len(valid_df)}")
    logger.info(f"Invalid Accounts : {len(invalid_df)}")
    logger.info("Account Validation Complete")

    return valid_df,len(accounts_df),len(valid_df),len(invalid_df)


def validate_transactions(transactions_df,valid_account_ids,account_balances,pipeline_run_id="default"):
    logger.info("Starting transaction validation")
    valid_records=[]
    invalid_records=[]
    seen_ids=set()

    valid_transaction_types={"CREDIT","DEBIT"}
    valid_transaction_modes={"UPI","ATM","Debit Card","Credit Card","Net Banking","Mobile Banking"}

    transactions_df["transaction_amount"]=pd.to_numeric(transactions_df["transaction_amount"],errors="coerce")

    for i in range(len(transactions_df)):
        row=transactions_df.iloc[i]
        reasons=[]

        if pd.isna(row["transaction_id"]) or str(row["transaction_id"]).strip()=="":
            reasons.append("transaction_id missing")

        tid=str(row["transaction_id"]).strip()
        if tid in seen_ids and tid!="":
            reasons.append("duplicate transaction_id")
        seen_ids.add(tid)

        if pd.isna(row["account_id"]) or str(row["account_id"]).strip()=="":
            reasons.append("account_id missing")
        else:
            aid=str(row["account_id"]).strip()
            if aid not in valid_account_ids:
                reasons.append("account does not exist")

        if pd.isna(row["transaction_amount"]) or row["transaction_amount"]<=0:
            reasons.append("transaction_amount must be greater than zero")

        ttype=str(row["transaction_type"]).strip() if not pd.isna(row["transaction_type"]) else ""
        if ttype not in valid_transaction_types:
            reasons.append("invalid transaction_type")

        tmode=str(row["transaction_mode"]).strip() if not pd.isna(row["transaction_mode"]) else ""
        if tmode not in valid_transaction_modes:
            reasons.append("invalid transaction_mode")

        tdate=str(row["transaction_date"]).strip() if not pd.isna(row["transaction_date"]) else ""
        try:
            if tdate:
                pd.to_datetime(tdate)
        except:
            reasons.append("invalid transaction_date")

        if reasons:
            record=row.to_dict()
            record["rejection_reason"]="; ".join(reasons)
            record["rejected_at"]=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            record["pipeline_run_id"]=pipeline_run_id
            invalid_records.append(record)
        else:
            valid_records.append(row.to_dict())

    valid_df=pd.DataFrame(valid_records) if valid_records else pd.DataFrame(columns=transactions_df.columns)
    invalid_df=pd.DataFrame(invalid_records) if invalid_records else pd.DataFrame()

    if not invalid_df.empty:
        invalid_df.to_csv(REJECTED_TRANSACTIONS_FILE,index=False)

    logger.info(f"Valid Transactions : {len(valid_df)}")
    logger.info(f"Invalid Transactions : {len(invalid_df)}")
    logger.info("Transaction Validation Complete")

    return valid_df,len(transactions_df),len(valid_df),len(invalid_df)


def validate_loans(loans_df,valid_customer_ids,pipeline_run_id="default"):
    logger.info("Starting loan validation")
    valid_records=[]
    invalid_records=[]
    seen_ids=set()

    valid_loan_types={"Home Loan","Personal Loan","Car Loan","Education Loan","Business Loan"}
    valid_loan_statuses={"Active","Closed","Defaulted"}

    loans_df["loan_amount"]=pd.to_numeric(loans_df["loan_amount"],errors="coerce")
    loans_df["interest_rate"]=pd.to_numeric(loans_df["interest_rate"],errors="coerce")

    for i in range(len(loans_df)):
        row=loans_df.iloc[i]
        reasons=[]

        if pd.isna(row["loan_id"]) or str(row["loan_id"]).strip()=="":
            reasons.append("loan_id missing")

        lid=str(row["loan_id"]).strip()
        if lid in seen_ids and lid!="":
            reasons.append("duplicate loan_id")
        seen_ids.add(lid)

        if pd.isna(row["customer_id"]) or str(row["customer_id"]).strip()=="":
            reasons.append("customer_id missing")
        else:
            cid=str(row["customer_id"]).strip()
            if cid not in valid_customer_ids:
                reasons.append("customer does not exist")

        if pd.isna(row["loan_amount"]) or row["loan_amount"]<=0:
            reasons.append("loan_amount <= 0")

        if pd.isna(row["interest_rate"]) or row["interest_rate"]<=0:
            reasons.append("interest_rate <= 0")

        ltype=str(row["loan_type"]).strip() if not pd.isna(row["loan_type"]) else ""
        if ltype not in valid_loan_types:
            reasons.append("invalid loan_type")

        lstatus=str(row["loan_status"]).strip() if not pd.isna(row["loan_status"]) else ""
        if lstatus not in valid_loan_statuses:
            reasons.append("invalid loan_status")

        if reasons:
            record=row.to_dict()
            record["rejection_reason"]="; ".join(reasons)
            record["rejected_at"]=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            record["pipeline_run_id"]=pipeline_run_id
            invalid_records.append(record)
        else:
            valid_records.append(row.to_dict())

    valid_df=pd.DataFrame(valid_records) if valid_records else pd.DataFrame(columns=loans_df.columns)
    invalid_df=pd.DataFrame(invalid_records) if invalid_records else pd.DataFrame()

    if not invalid_df.empty:
        invalid_df.to_csv(REJECTED_LOANS_FILE,index=False)

    logger.info(f"Valid Loans : {len(valid_df)}")
    logger.info(f"Invalid Loans : {len(invalid_df)}")
    logger.info("Loan Validation Complete")

    return valid_df,len(loans_df),len(valid_df),len(invalid_df)

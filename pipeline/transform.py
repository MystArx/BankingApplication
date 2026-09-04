from config.logger_config import logger
import pandas as pd
import numpy as np


def transform_transactions(transactions_df,accounts_df,customers_df,branches_df):
    logger.info("Transaction transformation started!")

    # Join transactions with accounts
    merged_df=transactions_df.merge(accounts_df[["account_id","customer_id","branch_id","account_type"]],on="account_id",how="left")

    # Join with customers
    merged_df=merged_df.merge(customers_df[["customer_id","customer_name","city","customer_type"]],on="customer_id",how="left",suffixes=("","_customer"))

    # Join with branches
    merged_df=merged_df.merge(branches_df[["branch_id","branch_name","city","state"]],on="branch_id",how="left",suffixes=("","_branch"))

    # Derive transaction_category
    merged_df["transaction_category"]=np.where(
        merged_df["transaction_amount"]>=100000,"HIGH VALUE",
        np.where(merged_df["transaction_amount"]>=50000,"MEDIUM VALUE","NORMAL")
    )

    # Derive risk_status
    merged_df["risk_status"]=np.where(
        merged_df["transaction_amount"]>=200000,"HIGH RISK",
        np.where(merged_df["transaction_amount"]>=100000,"MEDIUM RISK","NORMAL")
    )

    logger.info("Transaction transformation complete")

    return merged_df

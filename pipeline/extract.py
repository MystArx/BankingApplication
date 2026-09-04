import pandas as pd

from config.settings import CUSTOMERS_FILE,ACCOUNTS_FILE,BRANCHES_FILE,TRANSACTIONS_FILE,LOANS_FILE

from config.logger_config import logger


def extract_customers():
    logger.info("Reading customers.csv")
    customers_df=pd.read_csv(CUSTOMERS_FILE)
    return customers_df


def extract_accounts():
    logger.info("Reading accounts.csv")
    accounts_df=pd.read_csv(ACCOUNTS_FILE)
    return accounts_df


def extract_branches():
    logger.info("Reading branches.csv")
    branches_df=pd.read_csv(BRANCHES_FILE)
    return branches_df


def extract_transactions():
    logger.info("Reading transactions.csv")
    transactions_df=pd.read_csv(TRANSACTIONS_FILE)
    return transactions_df


def extract_loans():
    logger.info("Reading loans.csv")
    loans_df=pd.read_csv(LOANS_FILE)
    return loans_df

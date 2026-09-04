from database.database_connection import Base
from sqlalchemy import Column,Integer,String,Float,Date,DateTime,ForeignKey,Text,Index
from sqlalchemy.orm import relationship


class Customer(Base):
    __tablename__="customers"

    customer_id=Column(String(20),primary_key=True)

    customer_name=Column(String(100),nullable=False)

    email=Column(String(100),nullable=False)

    mobile=Column(String(15),nullable=False)

    city=Column(String(50),nullable=False)

    customer_type=Column(String(20),nullable=False)

    registration_date=Column(Date,nullable=True)

    status=Column(String(20),nullable=True)

    accounts=relationship("Account",back_populates="customer")

    loans=relationship("Loan",back_populates="customer")


class Branch(Base):
    __tablename__="branches"

    branch_id=Column(String(20),primary_key=True)

    branch_name=Column(String(100),nullable=False)

    city=Column(String(50),nullable=False)

    state=Column(String(50),nullable=False)

    manager_name=Column(String(100),nullable=False)

    ifsc_code=Column(String(20),nullable=False)

    status=Column(String(20),nullable=True)

    accounts=relationship("Account",back_populates="branch")


class Account(Base):
    __tablename__="accounts"

    account_id=Column(String(20),primary_key=True)

    customer_id=Column(String(20),ForeignKey("customers.customer_id"),nullable=False)

    account_type=Column(String(20),nullable=False)

    branch_id=Column(String(20),ForeignKey("branches.branch_id"),nullable=False)

    balance=Column(Float,nullable=False)

    opening_date=Column(Date,nullable=True)

    account_status=Column(String(20),nullable=True)

    customer=relationship("Customer",back_populates="accounts")

    branch=relationship("Branch",back_populates="accounts")

    transactions=relationship("Transaction",back_populates="account")

    __table_args__=(
        Index("idx_account_customer","customer_id"),
        Index("idx_account_branch","branch_id"),
    )


class Transaction(Base):
    __tablename__="transactions"

    transaction_id=Column(String(20),primary_key=True)

    account_id=Column(String(20),ForeignKey("accounts.account_id"),nullable=False)

    transaction_type=Column(String(10),nullable=False)

    transaction_amount=Column(Float,nullable=False)

    transaction_date=Column(Date,nullable=False)

    transaction_mode=Column(String(30),nullable=False)

    merchant_category=Column(String(50),nullable=True)

    transaction_category=Column(String(20),nullable=True)

    risk_status=Column(String(20),nullable=True)

    account=relationship("Account",back_populates="transactions")

    __table_args__=(
        Index("idx_transaction_account","account_id"),
        Index("idx_transaction_date","transaction_date"),
    )


class Loan(Base):
    __tablename__="loans"

    loan_id=Column(String(20),primary_key=True)

    customer_id=Column(String(20),ForeignKey("customers.customer_id"),nullable=False)

    loan_type=Column(String(30),nullable=False)

    loan_amount=Column(Float,nullable=False)

    interest_rate=Column(Float,nullable=False)

    loan_start_date=Column(Date,nullable=True)

    loan_status=Column(String(20),nullable=True)

    customer=relationship("Customer",back_populates="loans")

    __table_args__=(
        Index("idx_loan_customer","customer_id"),
    )


class RejectedRecord(Base):
    __tablename__="rejected_records"

    id=Column(Integer,primary_key=True,autoincrement=True)

    entity_type=Column(String(30),nullable=False)

    record_data=Column(Text,nullable=False)

    rejection_reason=Column(String(255),nullable=False)

    rejected_at=Column(DateTime,nullable=False)

    pipeline_run_id=Column(String(50),nullable=False)


class PipelineExecution(Base):
    __tablename__="pipeline_executions"

    id=Column(Integer,primary_key=True,autoincrement=True)

    run_id=Column(String(50),nullable=False,unique=True)

    started_at=Column(DateTime,nullable=False)

    completed_at=Column(DateTime,nullable=True)

    status=Column(String(20),nullable=False)

    summary_json=Column(Text,nullable=True)

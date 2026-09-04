from fastapi import APIRouter,HTTPException
from database.database_connection import LocalSession
from models.models import Customer
from schemas.schemas import CustomerCreate,CustomerUpdate,CustomerResponse
from config.logger_config import logger

router=APIRouter(prefix="/api/customers",tags=["Customers"])


@router.get("/",response_model=list[CustomerResponse])
def get_all_customers():
    session=LocalSession()
    try:
        customers=session.query(Customer).all()
        return customers
    except Exception as e:
        logger.error(f"Error fetching customers: {e}")
        raise HTTPException(status_code=500,detail=str(e))
    finally:
        session.close()


@router.get("/{customer_id}",response_model=CustomerResponse)
def get_customer_by_id(customer_id:str):
    session=LocalSession()
    try:
        customer=session.get(Customer,customer_id)
        if customer is None:
            raise HTTPException(status_code=404,detail="Customer not found")
        return customer
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error fetching customer: {e}")
        raise HTTPException(status_code=500,detail=str(e))
    finally:
        session.close()


@router.post("/",response_model=CustomerResponse)
def create_customer(customer_data:CustomerCreate):
    session=LocalSession()
    try:
        existing=session.get(Customer,customer_data.customer_id)
        if existing:
            raise HTTPException(status_code=400,detail="Customer already exists")

        customer=Customer(
            customer_id=customer_data.customer_id,
            customer_name=customer_data.customer_name,
            email=customer_data.email,
            mobile=customer_data.mobile,
            city=customer_data.city,
            customer_type=customer_data.customer_type,
            registration_date=customer_data.registration_date,
            status=customer_data.status
        )
        session.add(customer)
        session.commit()
        session.refresh(customer)
        logger.info(f"Created customer: {customer_data.customer_id}")
        return customer
    except HTTPException:
        raise
    except Exception as e:
        session.rollback()
        logger.error(f"Error creating customer: {e}")
        raise HTTPException(status_code=500,detail=str(e))
    finally:
        session.close()


@router.put("/{customer_id}",response_model=CustomerResponse)
def update_customer(customer_id:str,customer_data:CustomerUpdate):
    session=LocalSession()
    try:
        customer=session.get(Customer,customer_id)
        if customer is None:
            raise HTTPException(status_code=404,detail="Customer not found")

        if customer_data.customer_name is not None:
            customer.customer_name=customer_data.customer_name
        if customer_data.email is not None:
            customer.email=customer_data.email
        if customer_data.mobile is not None:
            customer.mobile=customer_data.mobile
        if customer_data.city is not None:
            customer.city=customer_data.city
        if customer_data.customer_type is not None:
            customer.customer_type=customer_data.customer_type
        if customer_data.status is not None:
            customer.status=customer_data.status

        session.commit()
        session.refresh(customer)
        logger.info(f"Updated customer: {customer_id}")
        return customer
    except HTTPException:
        raise
    except Exception as e:
        session.rollback()
        logger.error(f"Error updating customer: {e}")
        raise HTTPException(status_code=500,detail=str(e))
    finally:
        session.close()


@router.delete("/{customer_id}")
def delete_customer(customer_id:str):
    session=LocalSession()
    try:
        customer=session.get(Customer,customer_id)
        if customer is None:
            raise HTTPException(status_code=404,detail="Customer not found")

        session.delete(customer)
        session.commit()
        logger.info(f"Deleted customer: {customer_id}")
        return {"message":f"Customer {customer_id} deleted successfully"}
    except HTTPException:
        raise
    except Exception as e:
        session.rollback()
        logger.error(f"Error deleting customer: {e}")
        raise HTTPException(status_code=500,detail=str(e))
    finally:
        session.close()

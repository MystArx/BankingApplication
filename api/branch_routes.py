from fastapi import APIRouter,HTTPException
from database.database_connection import LocalSession
from models.models import Branch
from schemas.schemas import BranchResponse
from config.logger_config import logger

router=APIRouter(prefix="/api/branches",tags=["Branches"])


@router.get("/",response_model=list[BranchResponse])
def get_all_branches():
    session=LocalSession()
    try:
        branches=session.query(Branch).all()
        return branches
    except Exception as e:
        logger.error(f"Error fetching branches: {e}")
        raise HTTPException(status_code=500,detail=str(e))
    finally:
        session.close()


@router.get("/{branch_id}",response_model=BranchResponse)
def get_branch_by_id(branch_id:str):
    session=LocalSession()
    try:
        branch=session.get(Branch,branch_id)
        if branch is None:
            raise HTTPException(status_code=404,detail="Branch not found")
        return branch
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error fetching branch: {e}")
        raise HTTPException(status_code=500,detail=str(e))
    finally:
        session.close()


@router.get("/city/{city}",response_model=list[BranchResponse])
def get_branches_by_city(city:str):
    session=LocalSession()
    try:
        branches=session.query(Branch).filter(Branch.city==city).all()
        return branches
    except Exception as e:
        logger.error(f"Error fetching branches by city: {e}")
        raise HTTPException(status_code=500,detail=str(e))
    finally:
        session.close()

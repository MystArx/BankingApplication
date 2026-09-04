from fastapi import APIRouter,HTTPException
from config.logger_config import logger
from database.database_connection import LocalSession
from models.models import PipelineExecution
import json


router=APIRouter(prefix="/api/pipeline",tags=["Pipeline"])


@router.post("/run")
def run_pipeline_api():
    try:
        from pipeline.run_pipeline import run_pipeline
        from database.create_tables import create_tables
        create_tables()
        summary=run_pipeline()
        return summary
    except Exception as e:
        logger.error(f"Pipeline execution failed: {e}")
        raise HTTPException(status_code=500,detail=str(e))


@router.get("/status")
def get_pipeline_status():
    session=LocalSession()
    try:
        executions=session.query(PipelineExecution).order_by(PipelineExecution.id.desc()).limit(10).all()
        results=[]
        for ex in executions:
            results.append({
                "run_id":ex.run_id,
                "started_at":str(ex.started_at),
                "completed_at":str(ex.completed_at) if ex.completed_at else None,
                "status":ex.status,
                "summary":json.loads(ex.summary_json) if ex.summary_json else None
            })
        return results
    except Exception as e:
        logger.error(f"Error fetching pipeline status: {e}")
        raise HTTPException(status_code=500,detail=str(e))
    finally:
        session.close()


@router.get("/status/{run_id}")
def get_pipeline_status_by_id(run_id:str):
    session=LocalSession()
    try:
        execution=session.query(PipelineExecution).filter(PipelineExecution.run_id==run_id).first()
        if execution is None:
            raise HTTPException(status_code=404,detail="Pipeline run not found")
        return {
            "run_id":execution.run_id,
            "started_at":str(execution.started_at),
            "completed_at":str(execution.completed_at) if execution.completed_at else None,
            "status":execution.status,
            "summary":json.loads(execution.summary_json) if execution.summary_json else None
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error fetching pipeline status: {e}")
        raise HTTPException(status_code=500,detail=str(e))
    finally:
        session.close()

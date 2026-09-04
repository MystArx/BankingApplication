from fastapi import APIRouter,HTTPException
from fastapi.responses import FileResponse
from config.logger_config import logger
import os

from charts.branch_transaction_chart import generate_branch_transaction_chart
from charts.transaction_mode_chart import generate_transaction_mode_chart
from charts.daily_transaction_chart import generate_daily_transaction_chart
from charts.loan_distribution_chart import generate_loan_distribution_chart
from charts.risk_analysis_chart import generate_risk_analysis_chart

from config.settings import CHART_OUTPUT_DIR

router=APIRouter(prefix="/api/charts",tags=["Charts"])


@router.get("/branch-transactions")
def get_branch_transaction_chart():
    try:
        chart_path=generate_branch_transaction_chart()
        return FileResponse(chart_path,media_type="image/png")
    except Exception as e:
        logger.error(f"Error generating chart: {e}")
        raise HTTPException(status_code=500,detail=str(e))


@router.get("/transaction-modes")
def get_transaction_mode_chart():
    try:
        chart_path=generate_transaction_mode_chart()
        return FileResponse(chart_path,media_type="image/png")
    except Exception as e:
        logger.error(f"Error generating chart: {e}")
        raise HTTPException(status_code=500,detail=str(e))


@router.get("/daily-transactions")
def get_daily_transaction_chart():
    try:
        chart_path=generate_daily_transaction_chart()
        return FileResponse(chart_path,media_type="image/png")
    except Exception as e:
        logger.error(f"Error generating chart: {e}")
        raise HTTPException(status_code=500,detail=str(e))


@router.get("/loan-distribution")
def get_loan_distribution_chart():
    try:
        chart_path=generate_loan_distribution_chart()
        return FileResponse(chart_path,media_type="image/png")
    except Exception as e:
        logger.error(f"Error generating chart: {e}")
        raise HTTPException(status_code=500,detail=str(e))


@router.get("/risk-analysis")
def get_risk_analysis_chart():
    try:
        chart_path=generate_risk_analysis_chart()
        return FileResponse(chart_path,media_type="image/png")
    except Exception as e:
        logger.error(f"Error generating chart: {e}")
        raise HTTPException(status_code=500,detail=str(e))

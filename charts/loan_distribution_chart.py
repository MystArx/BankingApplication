import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import os
from config.settings import CHART_OUTPUT_DIR
from services.analytics_service import get_loan_distribution_data
from config.logger_config import logger


def generate_loan_distribution_chart():
    logger.info("Generating loan distribution chart")
    data=get_loan_distribution_data()

    if not data:
        logger.warning("No data for loan distribution chart")
        return None

    loan_types=[d[0] for d in data]
    amounts=[d[1]/100000 for d in data]

    colors=["#4BC0C0","#FF6384","#36A2EB","#FFCE56","#9966FF"]

    fig,ax=plt.subplots(figsize=(12,7))
    bars=ax.bar(loan_types,amounts,color=colors[:len(loan_types)])

    ax.set_xlabel("Loan Type",fontsize=12)
    ax.set_ylabel("Total Loan Amount (in Lakhs)",fontsize=12)
    ax.set_title("Loan Portfolio Distribution",fontsize=14,fontweight="bold")

    for bar,amount in zip(bars,amounts):
        ax.text(bar.get_x()+bar.get_width()/2,bar.get_height(),f"{amount:.1f}L",ha="center",va="bottom",fontsize=9)

    plt.tight_layout()
    chart_path=os.path.join(CHART_OUTPUT_DIR,"loan_distribution.png")
    plt.savefig(chart_path,dpi=150)
    plt.close()
    logger.info(f"Chart saved to {chart_path}")
    return chart_path

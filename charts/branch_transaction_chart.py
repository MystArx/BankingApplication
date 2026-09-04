import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import os
from config.settings import CHART_OUTPUT_DIR
from services.analytics_service import get_branch_transaction_data
from config.logger_config import logger


def generate_branch_transaction_chart():
    logger.info("Generating branch transaction chart")
    data=get_branch_transaction_data()

    if not data:
        logger.warning("No data for branch transaction chart")
        return None

    branches=[d[0] for d in data]
    amounts=[d[1]/100000 for d in data]

    fig,ax=plt.subplots(figsize=(14,7))
    bars=ax.bar(range(len(branches)),amounts,color=plt.cm.viridis([i/len(branches) for i in range(len(branches))]))

    ax.set_xlabel("Branch",fontsize=12)
    ax.set_ylabel("Total Transaction Amount (in Lakhs)",fontsize=12)
    ax.set_title("Branch-wise Transaction Value",fontsize=14,fontweight="bold")
    ax.set_xticks(range(len(branches)))
    ax.set_xticklabels(branches,rotation=45,ha="right",fontsize=8)

    for bar,amount in zip(bars,amounts):
        ax.text(bar.get_x()+bar.get_width()/2,bar.get_height(),f"{amount:.1f}L",ha="center",va="bottom",fontsize=7)

    plt.tight_layout()
    chart_path=os.path.join(CHART_OUTPUT_DIR,"branch_transactions.png")
    plt.savefig(chart_path,dpi=150)
    plt.close()
    logger.info(f"Chart saved to {chart_path}")
    return chart_path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import os
from config.settings import CHART_OUTPUT_DIR
from services.analytics_service import get_daily_transaction_data
from config.logger_config import logger


def generate_daily_transaction_chart():
    logger.info("Generating daily transaction chart")
    data=get_daily_transaction_data()

    if not data:
        logger.warning("No data for daily transaction chart")
        return None

    dates=[d[0] for d in data]
    amounts=[d[1]/100000 for d in data]

    fig,ax=plt.subplots(figsize=(16,7))
    ax.plot(range(len(dates)),amounts,color="#36A2EB",linewidth=1.5,marker="o",markersize=2)
    ax.fill_between(range(len(dates)),amounts,alpha=0.1,color="#36A2EB")

    ax.set_xlabel("Transaction Date",fontsize=12)
    ax.set_ylabel("Total Transaction Amount (in Lakhs)",fontsize=12)
    ax.set_title("Daily Transaction Trend",fontsize=14,fontweight="bold")

    # Show every Nth label to avoid crowding
    step=max(1,len(dates)//20)
    ax.set_xticks(range(0,len(dates),step))
    ax.set_xticklabels([dates[i] for i in range(0,len(dates),step)],rotation=45,ha="right",fontsize=8)

    ax.grid(True,alpha=0.3)
    plt.tight_layout()
    chart_path=os.path.join(CHART_OUTPUT_DIR,"daily_transactions.png")
    plt.savefig(chart_path,dpi=150)
    plt.close()
    logger.info(f"Chart saved to {chart_path}")
    return chart_path

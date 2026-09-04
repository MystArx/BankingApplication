import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import os
from config.settings import CHART_OUTPUT_DIR
from services.analytics_service import get_transaction_mode_data
from config.logger_config import logger


def generate_transaction_mode_chart():
    logger.info("Generating transaction mode chart")
    data=get_transaction_mode_data()

    if not data:
        logger.warning("No data for transaction mode chart")
        return None

    modes=[d[0] for d in data]
    counts=[d[1] for d in data]

    colors=["#FF6384","#36A2EB","#FFCE56","#4BC0C0","#9966FF","#FF9F40"]

    fig,ax=plt.subplots(figsize=(10,8))
    wedges,texts,autotexts=ax.pie(counts,labels=modes,autopct="%1.1f%%",colors=colors[:len(modes)],startangle=140)

    for text in autotexts:
        text.set_fontsize(9)

    ax.set_title("Transaction Mode Distribution",fontsize=14,fontweight="bold")
    plt.tight_layout()
    chart_path=os.path.join(CHART_OUTPUT_DIR,"transaction_modes.png")
    plt.savefig(chart_path,dpi=150)
    plt.close()
    logger.info(f"Chart saved to {chart_path}")
    return chart_path

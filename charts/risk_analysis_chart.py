import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import os
from config.settings import CHART_OUTPUT_DIR
from services.analytics_service import get_risk_analysis_data
from config.logger_config import logger


def generate_risk_analysis_chart():
    logger.info("Generating risk analysis chart")
    data=get_risk_analysis_data()

    if not data:
        logger.warning("No data for risk analysis chart")
        return None
    
    statuses=[d[0] for d in data]
    counts=[d[1] for d in data]

    color_map={"NORMAL":"#4BC0C0","MEDIUM RISK":"#FFCE56","HIGH RISK":"#FF6384"}
    colors=[color_map.get(s,"#999999") for s in statuses]

    fig,(ax1,ax2)=plt.subplots(1,2,figsize=(16,7))

    # Bar chart
    bars=ax1.bar(statuses,counts,color=colors)
    ax1.set_xlabel("Risk Status",fontsize=12)
    ax1.set_ylabel("Number of Transactions",fontsize=12)
    ax1.set_title("Transaction Risk Analysis (Bar)",fontsize=13,fontweight="bold")

    for bar,count in zip(bars,counts):
        ax1.text(bar.get_x()+bar.get_width()/2,bar.get_height(),str(count),ha="center",va="bottom",fontsize=10)

    # Pie chart
    ax2.pie(counts,labels=statuses,autopct="%1.1f%%",colors=colors,startangle=140)
    ax2.set_title("Transaction Risk Analysis (Pie)",fontsize=13,fontweight="bold")

    plt.tight_layout()
    chart_path=os.path.join(CHART_OUTPUT_DIR,"risk_analysis.png")
    plt.savefig(chart_path,dpi=150)
    plt.close()
    logger.info(f"Chart saved to {chart_path}")
    return chart_path

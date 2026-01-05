from datetime import datetime, timedelta
from typing import List, Dict

def estimate_usd_rate_history(
    current_usd: float,
    days_back: int,
    monthly_growth_rate: float = 0.05
) -> Dict[int, float]:
    """
    نرخ دلار روزهای گذشته را تخمین می‌زند
    """
    today = datetime.today()  # تاریخ امروز
    history = {}              # دیکشنری برای نگهداری نرخ‌ها

    for i in range(days_back + 1):
        date = today - timedelta(days=i)
        date_key = int(date.strftime("%Y%m%d"))
        months_ago = i / 30.0
        rate = current_usd / ((1 + monthly_growth_rate) ** months_ago)
        history[date_key] = rate

    return history

def calculate_dollar_adjusted_sales(
    sales_data: List[Dict],
    usd_history: Dict[int, float]
) -> List[float]:
    """
    فروش‌های ریالی را به دلار تبدیل می‌کند
    """
    usd_sales = []

    for record in sales_data:
        sale_date = record["date"]
        rial_amount = record["sales"]
        usd_rate = usd_history.get(sale_date)

        if usd_rate is None:
            continue

        usd_value = rial_amount / usd_rate
        usd_sales.append(usd_value)

    return usd_sales

def calculate_three_month_target(
    avg_usd_sales: float,
    future_usd_rate: float,
    inflation_rate: float
) -> float:
    """
    هدف فروش 3 ماه آینده با در نظر گرفتن تورم
    """
    monthly_target = avg_usd_sales * future_usd_rate * (1 + inflation_rate)
    return monthly_target * 3

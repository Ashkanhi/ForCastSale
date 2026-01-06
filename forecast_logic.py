# ===============================
# forecast_logic.py
# محاسبات پیش‌بینی فروش
# ===============================

from typing import List
import numpy as np
from sklearn.linear_model import LinearRegression

def calculate_three_month_target(
    avg_daily_sales: float,
    current_usd: float,
    future_usd: float,
    inflation_rate: float,
    days: int = 90
) -> float:
    """
    محاسبه هدف فروش سه ماه آینده
    بر اساس فرمول ساده:
    Target = ((avg_daily_sales / current_usd) * future_usd) * (1+inflation) * days
    """
    sales_power_usd = avg_daily_sales / current_usd
    future_daily_sales = sales_power_usd * future_usd
    future_daily_sales_with_inflation = future_daily_sales * (1 + inflation_rate)
    return future_daily_sales_with_inflation * days


def predict_sales_trend(sales_data: List[float], days_future: int = 90) -> float:
    """
    پیش‌بینی فروش سه ماه آینده با خط روند ساده (Linear Regression)
    sales_data: لیست فروش روزانه گذشته
    days_future: تعداد روزهای آینده
    """

    if len(sales_data) == 0:
        return 0.0

    # شماره روزها به عنوان X
    X = np.arange(len(sales_data)).reshape(-1, 1)
    y = np.array(sales_data)

    model = LinearRegression()
    model.fit(X, y)

    # پیش‌بینی روزهای آینده
    X_future = np.arange(len(sales_data), len(sales_data) + days_future).reshape(-1, 1)
    y_pred = model.predict(X_future)

    # جمع کل پیش‌بینی ۳ ماه آینده
    total_future_sales = max(0, np.sum(y_pred))  # جلوگیری از مقادیر منفی
    return total_future_sales

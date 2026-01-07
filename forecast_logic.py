def forecast_next_3_months_by_usd(
    monthly_sales,
    usd_current,
    usd_future
):
    """
    این تابع فروش ۳ ماه آینده را فقط بر اساس تغییر نرخ دلار
    پیش‌بینی می‌کند (بدون تورم)
    """

    # -----------------------------
    # لیست خروجی پیش‌بینی‌ها
    # -----------------------------
    forecasts = []

    # -----------------------------
    # فروش آخرین ماه واقعی
    # (فرض می‌کنیم آخرین رکورد جدیدترین ماه است)
    # -----------------------------
    last_month_sales = monthly_sales[-1]["sales"]

    # -----------------------------
    # نسبت تغییر دلار
    # مثال: دلار از 50 به 75 → نسبت = 1.5
    # -----------------------------
    usd_ratio = usd_future / usd_current

    # -----------------------------
    # پیش‌بینی ماه +1 ، +2 ، +3
    # -----------------------------
    for i in range(1, 4):

        # فرمول اصلی:
        # Future = LastMonth × (USD_Future / USD_Current)^i
        future_sales = last_month_sales * (usd_ratio ** i)

        forecasts.append(future_sales)

    return forecasts

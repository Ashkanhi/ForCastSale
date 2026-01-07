import pyodbc
# کتابخانه pyodbc برای اتصال پایتون به SQL Server استفاده می‌شود


def fetch_monthly_sales_last_3_months(config):
    """
    این تابع فروش ماهانه ۳ ماه گذشته را
    از View دیتابیس می‌خواند و به پایتون برمی‌گرداند
    """

    # -----------------------------
    # گرفتن connection string از فایل config
    # -----------------------------
    conn_str = config["DATABASE"]["connection_string"]

    # -----------------------------
    # ایجاد اتصال به دیتابیس
    # -----------------------------
    conn = pyodbc.connect(conn_str)

    # -----------------------------
    # ساخت cursor برای اجرای کوئری
    # -----------------------------
    cursor = conn.cursor()

    # -----------------------------
    # اجرای کوئری
    # این View همان ویویی است که خودت ساختی
    # -----------------------------
    cursor.execute("""
        SELECT 
            JalaliMonthName,
            MonthlyNetSales
        FROM vw_AvgDailyNetSales_Last3Months
        ORDER BY YearMonthKey
    """)

    # -----------------------------
    # گرفتن تمام رکوردها
    # -----------------------------
    rows = cursor.fetchall()

    # -----------------------------
    # بستن اتصال دیتابیس (خیلی مهم)
    # -----------------------------
    conn.close()

    # -----------------------------
    # تبدیل خروجی SQL به لیست دیکشنری پایتون
    # -----------------------------
    result = []

    for row in rows:
        result.append({
            "month": row[0],          # نام ماه شمسی (مثلاً آذر)
            "sales": float(row[1])    # مبلغ فروش ماهانه
        })

    return result

# ===============================
# database.py
# اتصال به SQL Server و گرفتن داده‌های فروش
# ===============================

import pyodbc
from datetime import datetime, timedelta
from config_loader import load_config

def get_db_connection(config):
    """
    ایجاد اتصال به دیتابیس SQL Server
    """
    db_config = config['DATABASE']
    server = db_config['server']
    database = db_config['database']
    use_windows_auth = db_config.getboolean('use_windows_auth', fallback=False)

    if use_windows_auth:
        conn_str = (
            f"DRIVER={{ODBC Driver 17 for SQL Server}};"
            f"SERVER={server};DATABASE={database};Trusted_Connection=yes;"
        )
    else:
        username = db_config['username']
        password = db_config['password']
        conn_str = (
            f"DRIVER={{ODBC Driver 17 for SQL Server}};"
            f"SERVER={server};DATABASE={database};UID={username};PWD={password}"
        )

    return pyodbc.connect(conn_str)


def fetch_avg_daily_net_sales_last_3_months(config):
    """
    گرفتن میانگین فروش روزانه ۳ ماه گذشته
    شامل روزهایی که فروش نداشته‌اند (0 لحاظ می‌شوند)
    """

    conn = get_db_connection(config)
    cursor = conn.cursor()

    # نام جدول و ستون‌ها از فایل config.ini
    table = config['DATABASE']['table']
    date_col = config['DATABASE']['date_column']
    sales_col = config['DATABASE']['sales_column']

    # تاریخ ۳ ماه قبل
    start_date = (datetime.today() - timedelta(days=90)).strftime("%Y%m%d")

    # کوئری SQL
    # LEFT JOIN با DimBusinessDate برای لحاظ کردن روزهای بدون فروش
    query = f"""
    WITH DailySales AS (
        SELECT 
            DB.BusinessDay,
            ISNULL(SUM(FS.{sales_col}), 0) AS DailyNetSales
        FROM DimBusinessDate DB
        LEFT JOIN {table} FS
            ON FS.{date_col} = DB.BusinessDay
        WHERE DB.BusinessDayDate >= ?
          AND DB.BusinessDayDate < CAST(GETDATE() AS DATE)
        GROUP BY DB.BusinessDay
    )
    SELECT AVG(DailyNetSales) AS AvgDailyNetSales
    FROM DailySales;
    """

    cursor.execute(query, start_date)
    row = cursor.fetchone()
    conn.close()

    if row and row[0]:
        return float(row[0])
    return 0.0

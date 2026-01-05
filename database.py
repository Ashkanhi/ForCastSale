import pyodbc                          # برای اتصال به SQL Server
from datetime import datetime, timedelta  # برای محاسبات تاریخ
from config_loader import load_config  # برای خواندن تنظیمات

def get_db_connection(config):
    """
    یک اتصال به دیتابیس ایجاد می‌کند
    """
    db_config = config['DATABASE']  # خواندن بخش DATABASE از فایل ini
    server = db_config['server']
    database = db_config['database']
    use_windows_auth = db_config.getboolean('use_windows_auth', fallback=False)
    
    if use_windows_auth:
        # اتصال با اعتبارسنجی ویندوز
        conn_str = f"DRIVER={{ODBC Driver 17 for SQL Server}};" \
                   f"SERVER={server};DATABASE={database};Trusted_Connection=yes;"
    else:
        # اتصال با نام کاربری و رمز عبور
        username = db_config['username']
        password = db_config['password']
        conn_str = f"DRIVER={{ODBC Driver 17 for SQL Server}};" \
                   f"SERVER={server};DATABASE={database};UID={username};PWD={password}"
    
    # برگرداندن اتصال
    return pyodbc.connect(conn_str)

def fetch_sales_data(config, days_back: int = 90):
    """
    داده‌های فروش را برای 'days_back' روز گذشته برمی‌گرداند
    """
    conn = get_db_connection(config)  # ایجاد اتصال

    # نام جدول و ستون‌ها از فایل تنظیمات
    table = config['DATABASE']['table']
    date_col = config['DATABASE']['date_column']
    sales_col = config['DATABASE']['sales_column']

    # محاسبه تاریخ شروع (YYYYMMDD)
    cutoff_date = (datetime.today() - timedelta(days=days_back)).strftime("%Y%m%d")

    # ساخت کوئری SQL
    query = f"""
    SELECT {date_col}, {sales_col}
    FROM {table}
    WHERE {date_col} >= ?
      AND {sales_col} IS NOT NULL
      AND {sales_col} > 0
    ORDER BY {date_col}
    """

    # اجرای کوئری
    cursor = conn.cursor()
    cursor.execute(query, cutoff_date)
    rows = cursor.fetchall()
    conn.close()  # بستن اتصال مهم است

    # تبدیل نتایج به لیستی از دیکشنری‌ها
    data = []
    for row in rows:
        data.append({
            "date": row[0],        # تاریخ فروش
            "sales": float(row[1]) # مقدار فروش
        })

    return data

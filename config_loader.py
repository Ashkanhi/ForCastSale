import configparser  # برای خواندن فایل ini
import os            # برای کار با مسیرها

def load_config(config_path: str = "config.ini"):
    """
    این تابع فایل config.ini را می‌خواند
    و تنظیمات را به شکل یک دیکشنری برمی‌گرداند
    """

    # مسیر فولدری که این فایل داخلش قرار دارد
    base_dir = os.path.dirname(os.path.abspath(__file__))

    # مسیر کامل فایل config.ini
    full_path = os.path.join(base_dir, config_path)

    # اگر فایل وجود نداشت، خطا بده
    if not os.path.exists(full_path):
        raise FileNotFoundError(f"فایل تنظیمات پیدا نشد: {full_path}")

    # ساختار خواندن فایل ini
    config = configparser.ConfigParser()
    config.read(full_path, encoding="utf-8")

    # برگرداندن تنظیمات
    return config

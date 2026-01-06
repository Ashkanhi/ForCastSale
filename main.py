# ===============================
# main.py
# اجرای برنامه با نمودار اصلاح شده
# ===============================

import sys
import matplotlib
matplotlib.use("TkAgg")
import matplotlib.pyplot as plt

import arabic_reshaper
from bidi.algorithm import get_display

from config_loader import load_config
from database import fetch_avg_daily_net_sales_last_3_months
from forecast_logic import calculate_three_month_target

# ===============================
# نمایش فارسی
# ===============================
def fa(text: str) -> str:
    reshaped_text = arabic_reshaper.reshape(text)
    return get_display(reshaped_text)

# ===============================
# رسم نمودار
# ===============================
def plot_sales_comparison(avg_daily_sales, target_three_month):
    months = ["-3","-2","-1","+1","+2","+3"]

    # تبدیل واحد به میلیون تومان برای خوانایی
    avg_monthly_sales = (avg_daily_sales * 30) / 1_000_000
    future_monthly_target = (target_three_month / 3) / 1_000_000

    values = [
        avg_monthly_sales, avg_monthly_sales, avg_monthly_sales,
        future_monthly_target, future_monthly_target, future_monthly_target
    ]

    plt.figure(figsize=(9,5))
    plt.plot(months, values, marker='o', linewidth=2, color='blue')
    plt.title(fa("مقایسه فروش گذشته با هدف فروش سه ماه آینده"))
    plt.xlabel(fa("ماه"))
    plt.ylabel(fa("مبلغ فروش (میلیون تومان)"))
    plt.ylim(0, max(values)*1.2)
    plt.grid(True)

    # نمایش عدد هر نقطه روی نمودار
    for i, v in enumerate(values):
        plt.text(i, v + 0.02*max(values), f"{v:.1f}", ha='center', fontsize=10)

    plt.show(block=True)

# ===============================
# برنامه اصلی
# ===============================
def main():
    config = load_config()

    # ---------------------------
    # گرفتن ورودی‌ها از کاربر
    # ---------------------------
    try:
        current_usd = float(input("نرخ دلار جاری (تومان): ").strip())
        future_usd = float(input("نرخ دلار پیش‌بینی‌شده (تومان): ").strip())
        inflation_rate = float(input("درصد تورم (مثلاً 5): ").strip()) / 100
    except ValueError:
        print("❌ لطفاً فقط عدد وارد کنید")
        sys.exit(1)

    # ---------------------------
    # میانگین فروش روزانه ۳ ماه گذشته
    # ---------------------------
    avg_daily_sales = fetch_avg_daily_net_sales_last_3_months(config)
    if avg_daily_sales == 0:
        print("❌ داده‌ای برای سه ماه اخیر پیدا نشد")
        sys.exit(1)

    # ---------------------------
    # محاسبه هدف فروش ۳ ماه آینده
    # ---------------------------
    target_three_month = calculate_three_month_target(
        avg_daily_sales,
        current_usd,
        future_usd,
        inflation_rate,
        days=90
    )

    # ---------------------------
    # نمایش نتایج عددی
    # ---------------------------
    print("\n✅ نتایج نهایی (فرمول ساده):")
    print(f"میانگین فروش روزانه گذشته: {avg_daily_sales:,.0f} تومان")
    print(f"نرخ دلار آینده: {future_usd:,.0f} تومان")
    print(f"درصد تورم: {inflation_rate*100:.1f} %")
    print(f"🎯 هدف فروش سه ماه آینده: {target_three_month:,.0f} تومان")

    # ---------------------------
    # رسم نمودار
    # ---------------------------
    plot_sales_comparison(avg_daily_sales, target_three_month)

# ===============================
# اجرای برنامه
# ===============================
if __name__ == "__main__":
    main()

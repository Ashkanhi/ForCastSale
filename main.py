import sys
from config_loader import load_config
from database import fetch_sales_data
from forecast_logic import estimate_usd_rate_history, calculate_dollar_adjusted_sales, calculate_three_month_target
import matplotlib.pyplot as plt  # برای رسم نمودار

def main():
    # مرحله 1: خواندن تنظیمات
    config = load_config()

    # مرحله 2: گرفتن نرخ دلار و تورم از کاربر
    try:
        current_usd = float(input("نرخ دلار جاری (تومان): ").strip())
        future_usd = float(input("نرخ دلار پیش‌بینی‌شده برای ماه آینده (تومان): ").strip())
        inflation_rate = float(input("درصد تورم (مثلاً 10): ").strip()) / 100
    except ValueError:
        print("❌ ورودی‌ها باید عدد باشند!")
        sys.exit(1)

    # مرحله 3: گرفتن داده‌های فروش 3 ماه گذشته
    sales_data = fetch_sales_data(config, days_back=90)
    if not sales_data:
        print("❌ داده‌ای برای 3 ماه گذشته پیدا نشد!")
        sys.exit(1)

    # مرحله 4: تخمین نرخ دلار روزهای گذشته
    usd_history = estimate_usd_rate_history(current_usd, days_back=90)

    # مرحله 5: تبدیل فروش‌ها به دلار
    usd_sales = calculate_dollar_adjusted_sales(sales_data, usd_history)
    if not usd_sales:
        print("❌ تبدیل فروش‌ها به دلار موفق نبود!")
        sys.exit(1)

    # مرحله 6: محاسبه میانگین فروش دلاری
    avg_usd_sales = sum(usd_sales) / len(usd_sales)

    # مرحله 7: محاسبه هدف 3 ماه آینده با تورم
    target_rial = calculate_three_month_target(avg_usd_sales, future_usd, inflation_rate)

    # مرحله 8: نمایش نتایج
    print("\n✅ نتایج:")
    print(f"میانگین فروش واقعی (دلاری): {avg_usd_sales:,.2f} $")
    print(f"نرخ دلار پیش‌بینی‌شده: {future_usd:,.0f} تومان")
    print(f"🎯 هدف فروش 3 ماه آینده: {target_rial:,.0f} تومان")

    # مرحله 9: رسم نمودار
    plot_sales_comparison(usd_sales, target_rial)

def plot_sales_comparison(past_sales, future_target):
    """
    رسم نمودار مقایسه فروش گذشته و هدف آینده
    """
    months = ["-3", "-2", "-1", "+1", "+2", "+3"]

    past_avg = sum(past_sales) / len(past_sales)
    future_monthly = future_target / 3

    values = [past_avg, past_avg, past_avg, future_monthly, future_monthly, future_monthly]

    plt.figure(figsize=(8,5))
    plt.plot(months, values, marker='o', color='blue')
    plt.title("مقایسه فروش گذشته و هدف 3 ماه آینده")
    plt.xlabel("ماه")
    plt.ylabel("مبلغ فروش (تومان)")
    plt.grid(True)
    plt.show()

if __name__ == "__main__":
    main()

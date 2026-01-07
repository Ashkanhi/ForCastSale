# ===============================
# main.py - نسخه نهایی با رنگ متفاوت برای پیش‌بینی
# ===============================
import tkinter as tk
from tkinter import messagebox, simpledialog

import matplotlib
matplotlib.use("TkAgg")
import matplotlib.pyplot as plt

import arabic_reshaper
from bidi.algorithm import get_display

from config_loader import load_config
from database import fetch_monthly_sales_last_3_months
from forecast_logic import forecast_next_3_months_by_usd


def fa(text):
    reshaped = arabic_reshaper.reshape(text)
    return get_display(reshaped)


PERSIAN_MONTHS = [
    "فروردین", "اردیبهشت", "خرداد",
    "تیر", "مرداد", "شهریور",
    "مهر", "آبان", "آذر",
    "دی", "بهمن", "اسفند"
]


def get_next_3_persian_month_names(last_month_name):
    current_index = PERSIAN_MONTHS.index(last_month_name)
    next_months = []
    for i in range(1, 4):
        next_index = (current_index + i) % 12
        next_months.append(PERSIAN_MONTHS[next_index])
    return next_months


def get_usd_from_gui():
    root = tk.Tk()
    root.withdraw()

    try:
        current = simpledialog.askfloat("ورودی نرخ دلار", "نرخ دلار فعلی (تومان):", parent=root)
        if current is None:
            return None, None
        future = simpledialog.askfloat("ورودی نرخ دلار", "نرخ دلار پیش‌بینی‌شده (تومان):", parent=root)
        if future is None:
            return None, None
        return current, future
    finally:
        root.destroy()


def main():
    config = load_config()

    usd_current, usd_future = get_usd_from_gui()
    if usd_current is None or usd_future is None:
        messagebox.showerror("خطا", "نرخ دلار وارد نشد.")
        return

    past_sales = fetch_monthly_sales_last_3_months(config)
    if not past_sales:
        messagebox.showerror("خطا", "داده‌ای برای نمایش وجود ندارد.")
        return

    future_sales = forecast_next_3_months_by_usd(past_sales, usd_current, usd_future)

    # آماده‌سازی داده‌های گذشته
    past_months = [item["month"] for item in past_sales]
    past_values = [item["sales"] / 1_000_000 for item in past_sales]
    past_months_display = [fa(m) for m in past_months]

    # آماده‌سازی داده‌های آینده
    last_month = past_months[-1].strip()
    future_months = get_next_3_persian_month_names(last_month)
    future_values = [v / 1_000_000 for v in future_sales]
    future_months_display = [fa(m) for m in future_months]

    # ✨ رسم نمودار با رنگ‌های متفاوت
    plt.figure(figsize=(10, 5))

    # --- بخش 1: داده‌های واقعی (گذشته) ---
    plt.plot(
        past_months_display,
        past_values,
        marker="o",
        color="tab:blue",      # رنگ آبی پیش‌فرض
        label=fa("داده‌های واقعی")
    )

    # --- بخش 2: داده‌های پیش‌بینی‌شده (آینده) ---
    plt.plot(
        future_months_display,
        future_values,
        marker="^",            # مثلث به‌جای دایره
        color="tab:green",     # رنگ سبز برای پیش‌بینی
        linestyle="--",        # خط چین برای تأکید بر پیش‌بینی بودن
        label=fa("پیش‌بینی")
    )

    # اتصال آخرین نقطه واقعی به اولین نقطه پیش‌بینی (خط پیوستگی)
    plt.plot(
        [past_months_display[-1], future_months_display[0]],
        [past_values[-1], future_values[0]],
        color="gray",
        linestyle=":",
        linewidth=1
    )

    # عنوان و برچسب‌ها
    plt.title(fa("پیش‌بینی فروش سه ماه آینده بر اساس نرخ دلار"))
    plt.ylabel(fa("مبلغ فروش (میلیون تومان)"))
    plt.grid(True, linestyle=":")

    # نمایش مقادیر روی نقاط
    for i, v in enumerate(past_values):
        plt.text(i, v, f"{v:,.0f}", ha="center", va="bottom", color="tab:blue")
    for i, v in enumerate(future_values):
        plt.text(
            i + len(past_values),  # موقعیت افقی: بعد از ماه‌های گذشته
            v,
            f"{v:,.0f}",
            ha="center",
            va="bottom",
            color="tab:green"
        )

    # نمایش توضیحات (legend)
    plt.legend()

    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    main()
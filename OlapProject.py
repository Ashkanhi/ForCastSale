from flask import Flask, render_template
import clr
import sys
import os
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
from bidi.algorithm import get_display
import arabic_reshaper

app = Flask(__name__)

# تنظیم فونت فارسی
plt.rcParams['font.family'] = 'Vazirmatn'
plt.rcParams['axes.labelpad'] = 20

def reshape_text(text):
    """اصلاح نمایش حروف فارسی"""
    if isinstance(text, str) and any('\u0600' <= ch <= '\u06FF' for ch in text):
        return get_display(arabic_reshaper.reshape(text))
    return text

@app.route('/')
def show_chart():
    try:
        # مسیر DLL
        dll_path = r"C:\Program Files\Microsoft.NET\ADOMD.NET\160"
        sys.path.append(dll_path)
        clr.AddReference("Microsoft.AnalysisServices.AdomdClient")

        from Microsoft.AnalysisServices.AdomdClient import AdomdConnection, AdomdCommand

        # اتصال به SSAS
        connection_string = "Data Source=localhost;Initial Catalog=RainBI;"
        conn = AdomdConnection(connection_string)
        conn.Open()

        # کوئری MDX
        mdx_query = """
        SELECT 
            {[Measures].[Amount]} ON COLUMNS,
            [Dim Store].[Store ID].Members ON ROWS
        FROM [Rain]
        """

        cmd = AdomdCommand(mdx_query, conn)
        reader = cmd.ExecuteReader()

        # خواندن داده‌ها
        results = []
        while reader.Read():
            row = []
            for i in range(reader.FieldCount):
                value = reader.GetValue(i)
                row.append(str(value) if value is not None else "NULL")
            results.append(row)

        columns = [reader.GetName(i) for i in range(reader.FieldCount)]
        df = pd.DataFrame(results, columns=columns)

        # اصلاح فارسی و پردازش داده‌ها
        store_names = df.iloc[:, 0].astype(str).apply(reshape_text)
        values = pd.to_numeric(df.iloc[:, 1], errors='coerce') / 1e9

        # رسم نمودار با matplotlib
        plt.figure(figsize=(14, 7))
        bars = plt.bar(store_names, values)

        # تنظیمات ظاهری
        plt.title('📊 فروش بر اساس فروشگاه', fontsize=16, fontweight='bold')
        plt.xlabel('فروشگاه', fontsize=14)
        plt.ylabel('مقدار (میلیارد)', fontsize=14)

        # تنظیم فونت برچسب‌ها
        plt.xticks(rotation=45, ha='right', fontsize=10, fontname='Vazirmatn')

        # اعمال فونت برای تمام محورها
        for label in plt.gca().get_xticklabels():
            label.set_fontname('Vazirmatn')
            label.set_rotation(45)
            label.set_ha('right')

        for label in plt.gca().get_yticklabels():
            label.set_fontname('Vazirmatn')

        plt.tight_layout()

        # ذخیره نمودار به صورت تصویر
        img_path = "static/chart.png"
        plt.savefig(img_path, dpi=150, bbox_inches='tight')
        plt.close()

        reader.Close()
        conn.Close()

        return render_template("index.html", chart_img="chart.png")

    except Exception as e:
        return f"<h1>❌ خطا در بارگذاری داده‌ها:</h1><p>{str(e)}</p>"

if __name__ == '__main__':
    print("🚀 وب‌اپلیکیشن در حال اجراست...")
    print("آدرس: http://localhost:5000")
    app.run(debug=True, host='0.0.0.0', port=5000)
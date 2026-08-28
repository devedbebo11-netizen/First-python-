from flask import Flask, render_template_string, request
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import io
import base64

app = Flask(__name__)

# قالب HTML بتصميم بسيط
HTML_TEMPLATE = '''
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <title>موقع تحليل البيانات</title>
    <style>
        body { font-family: Arial, sans-serif; background-color: #f4f4f9; padding: 20px; text-align: center; }
        .container { background: white; padding: 20px; border-radius: 8px; box-shadow: 0 0 10px rgba(0,0,0,0.1); display: inline-block; }
        input, button { padding: 10px; margin: 10px; font-size: 16px; }
        button { background: #007bff; color: white; border: none; border-radius: 4px; cursor: pointer; }
    </style>
</head>
<body>
    <div class="container">
        <h2>أدخل بيانات المبيعات (أرقام مفصولة بفواصل)</h2>
        <form method="POST">
            <input type="text" name="data" placeholder="مثال: 1200, 1900, 1500, 2200" required>
            <br>
            <button type="submit">حلل وارسم</button>
        </form>
        {% if plot_url %}
            <h3>نتيجة التحليل:</h3>
            <img src="data:image/png;base64,{{ plot_url }}" alt="Chart">
        {% endif %}
    </div>
</body>
</html>
'''

@app.route('/', methods=['GET', 'POST'])
def home():
    plot_url = None
    if request.method == 'POST':
        try:
            # استقبال البيانات من المستخدم وتحويلها لأرقام
            raw_data = request.form['data']
            values = [float(x.strip()) for x in raw_data.split(',')]
            months = [f"شهر {i+1}" for i in range(len(values))]

            # عمل التحليل والرسم البياني
            plt.figure(figsize=(6, 4))
            plt.plot(months, values, marker='o', color='green', linewidth=2)
            plt.title('تحليل البيانات التلقائي')
            plt.xlabel('الفترة')
            plt.ylabel('القيمة')
            plt.grid(True)

            # حفظ الرسمة كصورة داخل الذاكرة (Base64) لعرضها مباشرة
            img = io.BytesIO()
            plt.savefig(img, format='png', bbox_inches='tight')
            img.seek(0)
            plot_url = base64.b64encode(img.getvalue()).decode('utf8')
            plt.close()
        except Exception as e:
            pass

    return render_template_string(HTML_TEMPLATE, plot_url=plot_url)

if __name__ == '__main__':
    app.run(debug=True)

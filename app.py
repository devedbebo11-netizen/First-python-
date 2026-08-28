from flask import Flask, render_template_string, request
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import io
import base64

app = Flask(__name__)
application = app

HTML_TEMPLATE = '''
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>موقع تحليل البيانات</title>
    <style>
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background-color: #f4f4f9;
            margin: 0;
            padding: 20px;
            display: flex;
            justify-content: center;
            align-items: center;
            min-height: 100vh;
            box-sizing: border-box;
        }
        .container {
            background: white;
            padding: 30px;
            border-radius: 12px;
            box-shadow: 0 4px 15px rgba(0,0,0,0.1);
            display: flex;
            flex-direction: column;
            align-items: center;
            width: 100%;
            max-width: 600px;
            box-sizing: border-box;
        }
        h2 { margin-top: 0; color: #333; font-size: 22px; text-align: center; }
        form { width: 100%; display: flex; flex-direction: column; align-items: center; }
        input {
            padding: 15px;
            margin: 10px 0;
            font-size: 16px;
            border: 1px solid #ddd;
            border-radius: 6px;
            width: 100%;
            box-sizing: border-box;
        }
        button {
            padding: 15px 30px;
            margin-top: 10px;
            font-size: 16px;
            background: #28a745;
            color: white;
            border: none;
            border-radius: 6px;
            cursor: pointer;
            transition: background 0.3s;
            width: 100%;
        }
        button:hover { background: #218838; }
        h3 { color: #555; margin-top: 25px; font-size: 18px; }
        img {
            max-width: 100%;
            height: auto;
            margin-top: 15px;
            border: 1px solid #eee;
            border-radius: 6px;
        }
    </style>
</head>
<body>
    <div class="container">
        <h2>أدخل بيانات المبيعات (أرقام مفصولة بفواصل)</h2>
        <form method="POST">
            <input type="text" name="data" placeholder="مثال: 1200, 1900, 1500, 2200" required>
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
            raw_data = request.form['data']
            values = [float(x.strip()) for x in raw_data.split(',')]
            months = [f"شهر {i+1}" for i in range(len(values))]

            plt.figure(figsize=(6, 4))
            plt.plot(months, values, marker='o', color='green', linewidth=2)
            plt.title('تحليل البيانات التلقائي')
            plt.xlabel('الفترة')
            plt.ylabel('القيمة')
            plt.grid(True)

            img = io.BytesIO()
            plt.savefig(img, format='png', bbox_inches='tight')
            img.seek(0)
            plot_url = base64.b64encode(img.getvalue()).decode('utf8')
            plt.close()
        except Exception:
            pass

    return render_template_string(HTML_TEMPLATE, plot_url=plot_url)

if __name__ == '__main__':
    app.run(debug=True)

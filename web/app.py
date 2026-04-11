from flask import Flask, send_from_directory
import os

app = Flask(__name__)

REPORTS_DIR = "/app/reports"


@app.route('/')
def index():

    quality_report = ""
    research_results = ""

    if os.path.exists(f"{REPORTS_DIR}/data_quality_report.md"):
        with open(f"{REPORTS_DIR}/data_quality_report.md", "r", encoding="utf-8") as f:
            quality_report = f.read()

    if os.path.exists(f"{REPORTS_DIR}/research_results.txt"):
        with open(f"{REPORTS_DIR}/research_results.txt", "r", encoding="utf-8") as f:
            research_results = f.read()

    return f"""
    <html>
        <head><title>RRO Open Data Analytics</title></head>
        <body style="font-family: sans-serif; padding: 40px; line-height: 1.6;">
            <h1>📊 Аналітика відкритих даних РРО</h1>
            <hr>
            <h2>📝 Звіт про якість даних</h2>
            <pre style="background: #f4f4f4; padding: 15px; border-radius: 5px;">{quality_report}</pre>

            <h2>🔬 Результати дослідження гіпотез</h2>
            <pre style="background: #eef; padding: 15px; border-radius: 5px;">{research_results}</pre>

            <h2>📈 Візуалізація</h2>
            <div style="display: flex; gap: 20px; flex-wrap: wrap;">
                <div>
                    <p><b>Частки ринку:</b></p>
                    <img src="/plots/market_share.png" width="450">
                </div>
                <div>
                    <p><b>Активність оновлень:</b></p>
                    <img src="/plots/top_applicants_activity.png" width="450">
                </div>
            </div>
        </body>
    </html>
    """


@app.route('/plots/<path:filename>')
def plots(filename):
    return send_from_directory(f"{REPORTS_DIR}/figures", filename)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
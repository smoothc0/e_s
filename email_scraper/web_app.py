from flask import Flask, render_template, request, send_from_directory
import os
from main import run_scraper  # Make sure this function exists in main.py

app = Flask(__name__)

OUTPUT_DIR = 'output'

@app.route('/', methods=['GET', 'POST'])
def index():
    emails = None
    keyword = None
    file = None

    if request.method == 'POST':
        keyword = request.form['keyword']
        result = run_scraper(keyword)
        emails = result.get('emails')
        file = os.path.basename(result.get('file')) if result.get('file') else None

    return render_template('index.html', emails=emails, keyword=keyword, file=file)

@app.route('/download/<filename>')
def download_file(filename):
    return send_from_directory(OUTPUT_DIR, filename, as_attachment=True)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))  # Render sets PORT
    app.run(host="0.0.0.0", port=port)         # Bind to all IPs for external access

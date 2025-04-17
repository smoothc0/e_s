from flask import Flask, render_template, request, send_from_directory, redirect, url_for
import os
from main import run_scraper, clear_history

app = Flask(__name__)

OUTPUT_DIR = 'output'

# ✅ Ensure the output directory exists on startup
os.makedirs(OUTPUT_DIR, exist_ok=True)

@app.route('/', methods=['GET', 'POST'])
def index():
    emails = None
    keyword = None
    file = None

    if request.method == 'POST':
        if 'clear' in request.form:
            clear_history()
            return redirect(url_for('index'))

        try:
            keyword = request.form['keyword']
            result = run_scraper(keyword)
            emails = result.get('emails')
            file = os.path.basename(result.get('file')) if result.get('file') else None
        except Exception as e:
            print(f"🔥 ERROR during scraping: {e}")  # ✅ Helpful log
            return "An error occurred while processing your request.", 500

    return render_template('index.html', emails=emails, keyword=keyword, file=file)

@app.route('/download/<filename>')
def download_file(filename):
    filepath = os.path.join(OUTPUT_DIR, filename)
    if not os.path.exists(filepath):
        return "File not found.", 404  # ✅ Avoid crashing if file is missing
    return send_from_directory(OUTPUT_DIR, filename, as_attachment=True)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)

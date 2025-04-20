from flask import Flask, render_template, request, send_from_directory, redirect, url_for
import os
from main import run_scraper, clear_history

app = Flask(__name__)

OUTPUT_DIR = 'output'

@app.route('/', methods=['GET', 'POST'])
def index():
    emails = None
    keyword = None
    file = None

    if request.method == 'POST':
        if 'clear' in request.form:
            clear_history()
            return redirect(url_for('index'))

        keyword = request.form['keyword']
        result = run_scraper(keyword)
        emails = result.get('emails')
        file = os.path.basename(result.get('file')) if result.get('file') else None

    return render_template('index.html', emails=emails, keyword=keyword, file=file)

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/product')
def product():
    return render_template('product.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')  # You’ll want to create templates/contact.html too

@app.route('/download/<filename>')
def download_file(filename):
    return send_from_directory(OUTPUT_DIR, filename, as_attachment=True)

@app.errorhandler(404)
def not_found(e):
    return render_template("404.html"), 404  # Optional, create 404.html if desired

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)

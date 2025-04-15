from flask import Flask, render_template, request, send_from_directory, redirect, url_for, session
import os
from main import run_scraper

app = Flask(__name__)
app.secret_key = 'change_this_secret_to_something_random'

# Optional security configs
app.config['SESSION_COOKIE_SECURE'] = True
app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'

OUTPUT_DIR = 'output'

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/pricing')
def pricing():
    return render_template('pricing.html')

@app.route('/subscribe/<plan>')
def subscribe(plan):
    session['subscribed'] = True
    session['plan'] = plan
    return redirect(url_for('scraper'))

@app.route('/scraper', methods=['GET', 'POST'])
def scraper():
    if not session.get('subscribed'):
        return redirect(url_for('pricing'))

    emails = None
    keyword = None
    file = None

    if request.method == 'POST':
        keyword = request.form['keyword']
        result = run_scraper(keyword)
        emails = result.get('emails')
        file = os.path.basename(result.get('file')) if result.get('file') else None

    return render_template('scraper.html', emails=emails, keyword=keyword, file=file, plan=session.get('plan'))

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/download/<filename>')
def download_file(filename):
    return send_from_directory(OUTPUT_DIR, filename, as_attachment=True)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)

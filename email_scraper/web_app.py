from flask import Flask, render_template, request, send_from_directory, Response, redirect, url_for
import os
from main import run_scraper, run_scraper_streaming, sanitize_filename

app = Flask(__name__, template_folder='templates')

OUTPUT_DIR = 'output'

# Valid plans we accept
VALID_PLANS = ['basic', 'pro', 'business']

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/scraper')
def scraper_interface():
    # Verify plan is valid before showing scraper
    plan = request.args.get('plan', '').lower()
    if plan not in VALID_PLANS:
        return redirect(url_for('index'))
    
    return render_template('scraper.html', plan=plan)

@app.route('/scrape', methods=['POST'])
def scrape_emails():
    # Verify the request comes with a valid plan
    plan = request.args.get('plan', '').lower()
    if plan not in VALID_PLANS:
        return {"error": "Plan required"}, 400
    
    keyword = request.form.get('keyword')
    if not keyword:
        return {"error": "Keyword required"}, 400
    
    # You could add plan-specific limits here
    goal = 20  # Default for all plans
    if plan == 'basic':
        goal = 10
    elif plan == 'pro':
        goal = 20
    elif plan == 'business':
        goal = 50
    
    result = run_scraper(keyword, goal=goal)
    return result

@app.route('/download/<filename>')
def download_file(filename):
    return send_from_directory(OUTPUT_DIR, filename, as_attachment=True)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
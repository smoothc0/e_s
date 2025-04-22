from flask import Flask, render_template, request, send_from_directory, redirect, url_for, jsonify
import os
from main import run_scraper
from utils import sanitize_filename
from pathlib import Path

app = Flask(__name__, template_folder='templates')
app.secret_key = os.environ.get('SECRET_KEY', 'fallback-secret-key')

# Configuration
OUTPUT_DIR = Path('output')
OUTPUT_DIR.mkdir(exist_ok=True)

# Valid plans
VALID_PLANS = ['basic', 'pro', 'business']

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/scraper')
def scraper_interface():
    plan = request.args.get('plan', '').lower()
    if plan not in VALID_PLANS:
        return redirect(url_for('index'))
    return render_template('scraper.html', plan=plan)

@app.route('/scrape', methods=['POST'])
def scrape_emails():
    try:
        plan = request.args.get('plan', '').lower()
        if plan not in VALID_PLANS:
            return jsonify({"error": "Invalid plan"}), 400
        
        keyword = request.form.get('keyword', '').strip()
        if not keyword:
            return jsonify({"error": "Keyword is required"}), 400
        
        # Plan-based limits
        plan_limits = {
            'basic': 10,
            'pro': 20,
            'business': 50
        }
        
        result = run_scraper(keyword, goal=plan_limits.get(plan, 20))
        if not result.get('emails'):
            return jsonify({"error": "No emails found"}), 404
            
        return jsonify(result)
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/download/<filename>')
def download_file(filename):
    try:
        # Security check
        if not filename.endswith('.csv') or '..' in filename or '/' in filename:
            return "Invalid file", 400
            
        filepath = OUTPUT_DIR / filename
        if not filepath.exists():
            return "File not found", 404
            
        return send_from_directory(OUTPUT_DIR, filename, as_attachment=True)
    except Exception as e:
        return str(e), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
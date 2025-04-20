from flask import Flask, render_template, request, redirect, url_for
import os
import csv
from datetime import datetime
from scraper import EmailScraper

app = Flask(__name__)

OUTPUT_DIR = os.path.join(os.path.dirname(__file__), 'output')
if not os.path.exists(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/product')
def product():
    return render_template('product.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/pricing')
def pricing():
    return render_template('pricing.html')

@app.route('/scrape', methods=['GET', 'POST'])
def scrape():
    if request.method == 'POST':
        url = request.form.get('url')
        if not url:
            return render_template('index.html', error="Please enter a valid URL.")

        scraper = EmailScraper(url)
        results = scraper.scrape_with_sources()

        # Save to CSV
        timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
        filename = f"emails_{timestamp}.csv"
        filepath = os.path.join(OUTPUT_DIR, filename)

        with open(filepath, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['Email', 'Source URL'])
            for email, source in results.items():
                writer.writerow([email, source])

        return render_template('results.html', results=results, filename=filename)
    
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)

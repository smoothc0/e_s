from flask import Flask, render_template, request, redirect, url_for
import os
from datetime import datetime
from scraper import scrape_emails

app = Flask(__name__)

# Home
@app.route('/')
def index():
    return render_template('index.html')

# Product Page
@app.route('/product')
def product():
    return render_template('product.html')

# About Page
@app.route('/about')
def about():
    return render_template('about.html')

# Contact Page
@app.route('/contact')
def contact():
    return render_template('contact.html')

# Scraper Page
@app.route('/scrape', methods=['GET', 'POST'])
def scrape():
    if request.method == 'POST':
        keyword = request.form['keyword']
        results = scrape_emails(keyword)

        # Save results to output CSV
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"{keyword.replace(' ', '_')}_{timestamp}.csv"
        filepath = os.path.join('output', filename)
        with open(filepath, 'w') as f:
            f.write("Email\n")
            for email in results:
                f.write(email + "\n")

        return render_template('scrape.html', emails=results, keyword=keyword)

    return render_template('scrape.html', emails=None)

if __name__ == '__main__':
    app.run(debug=True)

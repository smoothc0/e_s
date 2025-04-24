from flask import Flask, render_template, request, send_from_directory, Response, stream_with_context
import os
from main import run_scraper, run_scraper_streaming, sanitize_filename

app = Flask(__name__)

OUTPUT_DIR = 'output'

@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')

@app.route('/download/<filename>')
def download_file(filename):
    return send_from_directory(OUTPUT_DIR, filename, as_attachment=True)

@app.route('/stream')
def stream():
    keyword = request.args.get('keyword')
    if not keyword:
        return "Keyword required.", 400

    def generate():
        yield f"data: START\n\n"

        for update in run_scraper_streaming(keyword):
            yield f"data: {update}\n\n"

        yield f"data: DONE|{sanitize_filename(keyword)}.csv\n\n"

    return Response(stream_with_context(generate()), mimetype='text/event-stream')

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
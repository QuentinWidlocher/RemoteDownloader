from flask import Flask, render_template, request, redirect, url_for
import json
import queue
from threading import Thread
import requests
import os

app = Flask(__name__)
app.config['TEMPLATES_AUTO_RELOAD'] = True
app.config['ENABLE_THREADS'] = True

rows = []

q = queue.Queue()

@app.route('/')
def index():
    return render_template('index.html', rows=rows)


@app.route('/add-url', methods=["POST"])
def add_url():
    url = request.form['url']

    if not url in rows:
        rows.append(url)

    return redirect(url_for('index'))

@app.route('/delete-url', methods=["POST"])
def delete_url():
    url = request.form['url']

    if url in rows:
        rows.remove(url)

    return redirect(url_for('index'))

def process_urls():
    while True:
        if len(rows) > 0:
            url = rows[0]
            filename = os.path.split(url)[1]

            try:
                r = requests.get(url)
            except requests.exceptions.MissingSchema:
                rows.remove(url)
                continue

            with open(f'./download/{filename}', 'wb') as f:
                f.write(r.content)

            rows.remove(url)

if __name__ == '__main__':
    thread = Thread(target=process_urls)
    thread.daemon = True
    thread.start()
    app.run(host='0.0.0.0', port='5000')
    thread.join()

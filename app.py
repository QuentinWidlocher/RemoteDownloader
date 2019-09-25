from flask import Flask, render_template, request, redirect, url_for
import json
from threading import Thread
import requests
import os
import variables as v

app = Flask(__name__)
app.config['TEMPLATES_AUTO_RELOAD'] = True
app.config['ENABLE_THREADS'] = True

# List of queued downloads
downloads = []

# Home page
@app.route('/')
def index():
    return render_template('index.html', downloads=downloads)

# Add an url to the downloads
@app.route('/add-url', methods=["POST"])
def add_url():
    url = request.form['url']

    if not url in downloads:
        downloads.append(url)

    return redirect(url_for('index'))

# Remove an url from the downloads
@app.route('/delete-url', methods=["POST"])
def delete_url():
    url = request.form['url']

    if url in downloads:
        downloads.remove(url)

    return redirect(url_for('index'))

# Thread that indefinitely downloads queued downloads
def process_urls():
    while True:

        # Skip if they are no downloads of course
        if len(downloads) > 0:
            url = downloads[0]

            # Get the filename and the extension
            filename = os.path.split(url)[1]

            try:
                r = requests.get(url)
            except requests.exceptions.MissingSchema:
                downloads.remove(url)
                continue

            with open(f'{v.DOWNLOAD_DIRECTORY}/{filename}', 'wb') as f:
                f.write(r.content)

            # Once downloaded, remove the queued download
            downloads.remove(url)

if __name__ == '__main__':

    # Prepare and run the downloading thread
    thread = Thread(target=process_urls)
    thread.daemon = True
    thread.start()

    # Run the Flask server
    app.run(host='0.0.0.0', port=v.PORT)
    thread.join()

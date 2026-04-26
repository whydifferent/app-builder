from flask import Flask, render_template, request, redirect, url_for
import os
import json

app = Flask(__name__)
UPLOAD_FOLDER = 'static'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate():
    app_name = request.form['app_name']
    app_url = request.form['app_url']

    icon192 = request.files['icon192']
    icon512 = request.files['icon512']

    icon192.save(os.path.join(UPLOAD_FOLDER, 'icon-192.png'))
    icon512.save(os.path.join(UPLOAD_FOLDER, 'icon-512.png'))

    manifest = {
        "name": app_name,
        "short_name": app_name,
        "start_url": app_url,
        "display": "standalone",
        "background_color": "#111111",
        "theme_color": "#000000",
        "orientation": "portrait",
        "scope": "/",
        "icons": [
            {
                "src": "/static/icon-192.png",
                "sizes": "192x192",
                "type": "image/png"
            },
            {
                "src": "/static/icon-512.png",
                "sizes": "512x512",
                "type": "image/png"
            }
        ]
    }

    with open('static/manifest.json', 'w') as f:
        json.dump(manifest, f, indent=2)

    sw = """
self.addEventListener("install", e => self.skipWaiting());
self.addEventListener("activate", e => clients.claim());
self.addEventListener("fetch", e => e.respondWith(fetch(e.request)));
"""

    with open('static/sw.js', 'w') as f:
        f.write(sw)

    return redirect(url_for('preview'))

@app.route('/preview')
def preview():
    return render_template('preview.html')

if __name__ == '__main__':
    app.run(debug=True)

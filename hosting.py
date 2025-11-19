from flask import Flask
from threading import Thread
import os

app = Flask(__name__, static_folder='static', static_url_path='')

@app.route('/')
def home():
    try:
        with open('index.html') as f:
            return f.read(), 200, {'Content-Type': 'text/html'}
    except FileNotFoundError:
        return "Bot is running."

def run_flask():
    app.run(host='0.0.0.0', port=8080, debug=False)

def keep_alive():
    t = Thread(target=run_flask, daemon=True)
    t.start()
from flask import Flask, render_template
from apscheduler.schedulers.background import BackgroundScheduler
from monitor import check_mentions_and_store
import sqlite3
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
DB_PATH = 'db.sqlite3'

# Inicializa o banco de dados
def init_db():
    with sqlite3.connect(DB_PATH) as conn:
        c = conn.cursor()
        c.execute('''
            CREATE TABLE IF NOT EXISTS mentions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                source TEXT,
                title TEXT,
                link TEXT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        conn.commit()

@app.route('/')
def index():
    with sqlite3.connect(DB_PATH) as conn:
        c = conn.cursor()
        c.execute("SELECT title, link, timestamp FROM mentions ORDER BY timestamp DESC LIMIT 20")
        mentions = c.fetchall()
    return render_template('index.html', mentions=mentions)

if __name__ == '__main__':
    init_db()
    scheduler = BackgroundScheduler()
    scheduler.add_job(check_mentions_and_store, 'interval', minutes=30)
    scheduler.start()
    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
import feedparser
import sqlite3
from email_alert import send_alert
from datetime import datetime, timedelta

KEYWORDS = [
    "problema com pix",
    "pix fora do ar",
    "pix não caiu",
    "erro ao fazer pix",
    "falha no pix",
    "golpe no pix"
]

FEED_URL = "https://news.google.com/rss/search?q=pix+problema"
DB_PATH = 'db.sqlite3'

ALERT_THRESHOLD = 3  # Número de menções para enviar alerta


def check_mentions_and_store():
    feed = feedparser.parse(FEED_URL)
    count = 0
    new_mentions = []

    with sqlite3.connect(DB_PATH) as conn:
        c = conn.cursor()

        for entry in feed.entries:
            title = entry.title.lower()
            link = entry.link

            if any(keyword in title for keyword in KEYWORDS):
                # Verifica se já está no banco
                c.execute("SELECT 1 FROM mentions WHERE link = ?", (link,))
                if c.fetchone():
                    continue

                # Armazena nova menção
                c.execute("INSERT INTO mentions (source, title, link) VALUES (?, ?, ?)",
                          ("Google News", entry.title, link))
                new_mentions.append(entry.title)
                count += 1

        conn.commit()

    # Envia alerta se passou do limite
    if count >= ALERT_THRESHOLD:
        send_alert(count, new_mentions)
# utils/telegram_alert.py

import requests
from flask import current_app

# Optional: avoid spamming
last_sent = {}

def send_alert(message, site_id=None,status=None, cooldown=300):
    """Send a Telegram message if cooldown passed."""
    import time
    now = time.time()
    key = (site_id, status)
    if key in last_sent and now - last_sent[key] < cooldown:
        return  # Skip duplicate alert for that status

    last_sent[key] = now
    
    if site_id:
        if site_id in last_sent and now - last_sent[site_id] < cooldown:
            return  # Skip duplicate alert
        last_sent[site_id] = now

    token = current_app.config.get("TELEGRAM_BOT_TOKEN")
    chat_id = current_app.config.get("TELEGRAM_CHAT_ID")
    chat_id2 = current_app.config.get("TELEGRAM_CHAT_ID")

    if not token or not chat_id:
        print("❌ Telegram not configured")
        return

    url = f"https://api.telegram.org/bot{token}/sendMessage"
    payload = {"chat_id": chat_id, "text": message, "parse_mode": "Markdown"} # had to change this as asterics* don't get sent well.
    payload2 = {"chat_id": chat_id2, "text": message, "parse_mode": "Markdown"} # had to change this as asterics* don't get sent well.
    try:
        requests.post(url, json=payload)
        # requests.post(url, json=payload2)
        print(f"✅ Alert sent: {message}")
    except Exception as e:
        print(f"❌ Failed to send alert: {e}")

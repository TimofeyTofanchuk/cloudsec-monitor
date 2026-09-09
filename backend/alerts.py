import os
import requests

def send_telegram_alert(source_ip: str, username: str, event_type: str, details: str):
    bot_token = os.getenv("TELEGRAM_BOT_TOKEN")
    chat_id = os.getenv("TELEGRAM_CHAT_ID")

    if not bot_token or not chat_id:
        print("[WARNING] Telegram credentials not set. Alert skipped.")
        return False

    message = (
        f"🚨 <b>СИСТЕМА БЕЗПЕКИ CLOUDSEC</b> 🚨\n\n"
        f"<b>Подія:</b> <code>{event_type}</code>\n"
        f"<b>Джерело (IP):</b> <code>{source_ip}</code>\n"
        f"<b>Користувач:</b> <code>{username}</code>\n"
        f"<b>Опис:</b> {details}\n"
    )

    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": message,
        "parse_mode": "HTML"
    }

    try:
        response = requests.post(url, json=payload, timeout=5)
        return response.status_code == 200
    except Exception as e:
        print(f"[ERROR] Failed to send alert: {e}")
        return False

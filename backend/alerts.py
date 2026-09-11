import os
import httpx
from pathlib import Path
from dotenv import load_dotenv

env_path = Path(__file__).resolve().parent.parent / ".env"
load_dotenv(dotenv_path=env_path)

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

async def send_telegram_alert(*args, **kwargs) -> bool:
    if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID:
        print("[WARNING] Telegram credentials not set. Alert skipped.")
        return False

    source_ip = kwargs.get("source_ip", "Unknown")
    username = kwargs.get("username", "Unknown")
    event_type = kwargs.get("event_type", "INCIDENT")
    details = kwargs.get("details", "No details")
    timestamp = kwargs.get("timestamp", "Just now")

    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"

    text = (
        f"🚨 <b>CloudSec Alert: {event_type}</b>\n"
        f"━━━━━━━━━━━━━━━━━━\n"
        f"<b>Source IP:</b> <code>{source_ip}</code>\n"
        f"<b>Target User:</b> <code>{username}</code>\n"
        f"<b>Details:</b> {details}\n"
        f"<b>Time:</b> {timestamp}"
    )

    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": text,
        "parse_mode": "HTML"
    }

    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.post(url, json=payload)
            if response.status_code == 200:
                print("[INFO] Telegram alert sent successfully.")
                return True
            else:
                print(f"[ERROR] Telegram API failed: {response.text}")
                return False
    except Exception as e:
        print(f"[ERROR] Connection error: {e}")
        return False

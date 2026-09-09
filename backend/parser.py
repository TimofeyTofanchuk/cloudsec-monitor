import re
from collections import defaultdict
from datetime import datetime, timedelta

# Зберігання невдалих спроб: {ip: [timestamp1, timestamp2]}
failed_attempts = defaultdict(list)
FAILED_THRESHOLD = 3      # Кількість спроб для тригера
TIME_WINDOW_SEC = 60      # Вікно аналізу (секунди)

# Регулярний вираз для невдалих спроб входу по SSH
SSH_FAILED_REGEX = re.compile(r"Failed password for (invalid user )?(?P<user>\S+) from (?P<ip>\d+\.\d+\.\d+\.\d+)")

def process_log_line(line: str):
    match = SSH_FAILED_REGEX.search(line)
    if not match:
        return None

    username = match.group("user")
    ip = match.group("ip")
    now = datetime.now()

    # Очищення застарілих спроб
    failed_attempts[ip] = [t for t in failed_attempts[ip] if now - t < timedelta(seconds=TIME_WINDOW_SEC)]
    failed_attempts[ip].append(now)

    if len(failed_attempts[ip]) >= FAILED_THRESHOLD:
        failed_attempts[ip].clear()  # Скидаємо лічильник після алерту
        return {
            "source_ip": ip,
            "username": username,
            "event_type": "SSH_BRUTE_FORCE",
            "details": f"Фіксація перебору паролів: {FAILED_THRESHOLD} помилок за {TIME_WINDOW_SEC}с."
        }
    return None

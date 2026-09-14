# CloudSec Monitor 🛡️

![Ubuntu](https://img.shields.io/badge/Ubuntu-24.04_LTS-E95420?logo=ubuntu&logoColor=white)
![Python](https://img.shields.io/badge/Python-3.12-3776AB?logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-0.110+-009688?logo=fastapi&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-Compose-2496ED?logo=docker&logoColor=white)
![Loki](https://img.shields.io/badge/Grafana-Loki-F46800?logo=grafana&logoColor=white)

Легковагова система централізованого збору журналів подій та виявлення інцидентів безпеки для корпоративної мережі підприємства (MVP). Проєкт розроблено як тренувальний пєт-проєкт.

---

## Ключові можливості

* Централізація логів: прийом потоків системних журналів (/var/log/auth.log) через агент Promtail у базу часових рядів Grafana Loki.
* REST API бекенд: сервіс на базі FastAPI з типізацією та валідацією моделей через Pydantic.
* Детектування інцидентів: аналіз логів автентифікації на виявлення ознак атак типу SSH brute-force (алгоритм sliding window).
* Сповіщення в реальному часі: оперативна відправка карток інцидентів черговому адміністратору через Telegram Bot API.
* Ресурсоефективність: споживання оперативної пам'яті менше 2 ГБ, збереження даних без ресурсоємного повнотекстового індексування.

---

## Архітектура системи

```
[ Monitored Client ]
  └─ /var/log/auth.log -> [ Promtail ] --(HTTP POST)-->
                                                      |
[ Central Server ]                                    |
  ├─ [ Grafana Loki ] <-------------------------------┘
  ├─ [ FastAPI Core Backend ] <--- (Аналіз потоку логів / REST API)
  │     └─(HTTPS POST)--> [ Telegram Bot API ] --> [ SysAdmin ]
  └─ [ Grafana Web UI ] <--- (Візуалізація метрик)
```

---

## Швидкий запуск на Central Server

1. Клонування репозиторію:
   ```
   git clone https://github.com/TimofeyTofanchuk/cloudsec-monitor.git
   cd cloudsec-monitor
   ```

3. Запуск сховища Loki:
   ```
   docker compose up -d
   ```
   
5. Підготовка оточення та запуск бекенду:
   ```
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   cp .env.example .env
   uvicorn backend.main:app --host 0.0.0.0 --port 8000
   ```

Документація REST API доступна за адресою: http://localhost:8000/docs

---

## Структура проєкту

```
.
├── backend/
│   ├── alerts.py        # Модуль інтеграції з Telegram API
│   ├── main.py          # Точка входу FastAPI, маршрутизація REST API
│   ├── parser.py        # Аналіз логів та детектування атак
│   └── schemas.py       # Валідація моделей Pydantic
├── config/
│   └── loki-config.yaml # Конфігураційний файл Loki
├── docker-compose.yml   # Маніфест контейнерів
├── .env.example         # Приклад конфігурації оточення
├── .gitignore           # Виключення тимчасових файлів з Git
└── README.md            # Технічна документація проєкту
```

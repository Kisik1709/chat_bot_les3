# Support Bots с интеграцией Dialogflow

В проекте реализованы два бота (для Telegram и ВКонтакте), которые используют Google Dialogflow для обработки естественного языка.
Также есть утилита для создания интентов в Dialogflow и система логирования с отправкой логов в отдельного Telegram-бота.

    Возможности
	•	Интеграция с Dialogflow: автоматическое определение интентов и возврат нужных ответов.
	•	Логирование в Telegram: все важные события и ошибки отправляются в отдельного Telegram-бота.

## 📂 Структура проекта
	•	create_intent.py — скрипт для загрузки тренировочных фраз и ответов из questions.json в Dialogflow.
	•	support_tg_bot.py — бот для Telegram, получает сообщения и отвечает через Dialogflow.
	•	support_vk_bot.py — бот для ВКонтакте, получает сообщения и отвечает через Dialogflow.
	•	utils.py — вспомогательный модуль: обработчик логов TelegramLogHandler и функция для настройки логирования.

## 🔧 Установка

1. Склонируйте репозиторий или скопируйте файлы в свою директорию
2. Создайте и активируйте виртуальное окружение:

```bash
python3 -m venv venv
source venv/bin/activate  # для Linux/Mac
venv\Scripts\activate     # для Windows
```

3. Установите зависимости:

```bash
pip install -r requirements.txt
```

4. Создайте файл .env в корне проекта и добавьте в него свои ключи:

```bash
# Telegram-бот для пользователей
TELEGRAM_TOKEN=токен_бота

# VK-бот
VK_TOKEN=токен_бота

# Google Dialogflow
PROJECT_DIALOGFLOW_ID=project_id_из_консоли
GOOGLE_APPLICATION_CREDENTIALS=path/to/credentials.json

# Telegram-бот для логов
TELEGRAM_TOKEN_FOR_LOGGER=токен_логгер_бота
TELEGRAM_CHAT_ID_FOR_LOGGER=ваш_chat_id
```

## ▶️ Использование

1. Создание интентов в Dialogflow
```bash
python create_intent.py
```

2. Запуск Telegram-бота
```bash
python support_tg_bot.py
```

3. Запуск VK-бота
```bash
python support_vk_bot.py
```
После запуска все логи и ошибки будут отправляться в отдельный Telegram-бот для логирования.

## Список библиотек:
	•	python-telegram-bot==13.15
	•	vk-api
	•	google-cloud-dialogflow
	•	python-dotenv

## Цель проекта
Код написан в образовательных целях на онлайн-курсе для веб-разработчиков [dvmn.org](https://dvmn.org).
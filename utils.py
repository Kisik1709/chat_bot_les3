import os
import sys
import logging
import telegram
from dotenv import load_dotenv

load_dotenv()


class TelegramLogHandler(logging.Handler):
    def __init__(self, bot, chat_id):
        super().__init__()
        self.bot = bot
        self.chat_id = chat_id

    def emit(self, record):
        log_entry = self.format(record)
        try:
            self.bot.send_message(chat_id=self.chat_id, text=log_entry)
        except Exception as e:
            print(f"Ошибка отправки лога в Telegram: {e}")


log_bot_token = os.getenv("API_TELEGRAM_LOGGER")
if not log_bot_token:
    sys.exit("Нет Токена")
log_chat_id = os.getenv("LOGGER_CHAT_ID")
if not log_bot_token:
    sys.exit("Не указан chat_id")
log_bot = telegram.Bot(token=log_bot_token)


def setup_logger(name=__name__):
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)

    handler = TelegramLogHandler(log_bot, log_chat_id)
    formatter = logging.Formatter("[%(module)s] %(levelname)s: %(message)s")
    handler.setFormatter(formatter)

    logger.addHandler(handler)

    return logger

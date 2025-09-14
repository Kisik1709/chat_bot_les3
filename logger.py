import logging
import telegram


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


def setup_logger(name, log_bot_token, log_chat_id):
    log_bot = telegram.Bot(token=log_bot_token)

    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)

    handler = TelegramLogHandler(log_bot, log_chat_id)
    formatter = logging.Formatter("[%(module)s] %(levelname)s: %(message)s")
    handler.setFormatter(formatter)

    logger.addHandler(handler)

    return logger

import os
import sys
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from dotenv import load_dotenv


def start(update, context):
    update.message.reply_text("Здраствуйте!")


def echo(update, context):
    update.message.reply_text(update.message.text)


def main():
    load_dotenv()

    tg_token = os.getenv("API_TELEGRAM")
    if not tg_token:
        sys.exit("Нет ключа доступа к TG. Завершение!")

    updater = Updater(token=tg_token)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(MessageHandler(
        Filters.text & ~Filters.command, echo))

    updater.start_polling()
    updater.idle()


if __name__ == "__main__":
    main()

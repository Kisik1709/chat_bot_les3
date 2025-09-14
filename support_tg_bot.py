import os
import sys
from dotenv import load_dotenv
from google.cloud import dialogflow
from telegram.error import TelegramError
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from logger import setup_logger


def start_command(update, context):
    update.message.reply_text("Я бот, который ответит на ваши вопросы!")


def get_dialogflow_response(project_id, session_id, text, lang_code):
    session_client = dialogflow.SessionsClient()
    session = session_client.session_path(project_id, session_id)

    text_input = dialogflow.TextInput(text=text, language_code=lang_code)
    query_input = dialogflow.QueryInput(text=text_input)

    response = session_client.detect_intent(
        request={"session": session, "query_input": query_input})

    return response.query_result.fulfillment_text


def handle_message(update, context):
    logger = context.bot_data["logger"]
    project_id = context.bot_data["project_id"]
    lang_code = context.bot_data["lang_code"]
    user_text = update.message.text
    session_id = update.effective_user.id

    response_text = get_dialogflow_response(
        project_id, session_id, user_text, lang_code)
    try:
        update.message.reply_text(response_text)
    except TelegramError as e:
        logger.exception(f"Ошибка отправки сообщения {e}")


def main():
    load_dotenv()

    log_bot_token = os.getenv("API_TELEGRAM_LOGGER")
    log_chat_id = os.getenv("LOGGER_CHAT_ID")
    if not log_bot_token or not log_chat_id:
        raise RuntimeError("Нет токена или chat_id для логгера")

    logger = setup_logger(__name__, log_bot_token, log_chat_id)

    tg_token = os.getenv("API_TELEGRAM")
    if not tg_token:
        sys.exit("Нет ключа доступа к TG. Завершение!")

    project_id = os.getenv("PROJECT_DIALOGFLOW_ID")
    if not project_id:
        sys.exit("Нет id dialogflow")

    lang_code = "ru"

    updater = Updater(token=tg_token)
    dispatcher = updater.dispatcher
    logger.info("Bot started!")

    dispatcher.bot_data["project_id"] = project_id
    dispatcher.bot_data["lang_code"] = lang_code
    dispatcher.bot_data["logger"] = logger

    dispatcher.add_handler(CommandHandler("start", start_command))
    dispatcher.add_handler(MessageHandler(
        Filters.text & ~Filters.command, handle_message))

    updater.start_polling()
    updater.idle()
    logger.info("bot stop!")


if __name__ == "__main__":
    main()

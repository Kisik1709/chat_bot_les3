import os
import sys
from dotenv import load_dotenv
from google.cloud import dialogflow
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters


def start_command(update, context):
    update.message.reply_text("Я бот!")


def get_dialogflow_response(project_id, session_id, text, lang_code):
    session_client = dialogflow.SessionsClient()
    session = session_client.session_path(project_id, session_id)

    text_input = dialogflow.TextInput(text=text, language_code=lang_code)
    query_input = dialogflow.QueryInput(text=text_input)

    response = session_client.detect_intent(
        request={"session": session, "query_input": query_input})

    return response.query_result.fulfillment_text


def handle_message(update, context):
    project_id = context.bot_data["project_id"]
    lang_code = context.bot_data["lang_code"]
    user_text = update.message.text
    session_id = update.effective_user.id

    response_text = get_dialogflow_response(
        project_id, session_id, user_text, lang_code)
    update.message.reply_text(response_text)


def main():
    load_dotenv()

    tg_token = os.getenv("API_TELEGRAM")
    if not tg_token:
        sys.exit("Нет ключа доступа к TG. Завершение!")

    project_id = os.getenv("PROJECT_DIALOGFLOW_ID")
    if not project_id:
        sys.exit("Нет id dialogflow")

    lang_code = "ru"

    updater = Updater(token=tg_token)
    dispatcher = updater.dispatcher

    dispatcher.bot_data["project_id"] = project_id
    dispatcher.bot_data["lang_code"] = lang_code

    dispatcher.add_handler(CommandHandler("start", start_command))
    dispatcher.add_handler(MessageHandler(
        Filters.text & ~Filters.command, handle_message))

    updater.start_polling()
    updater.idle()


if __name__ == "__main__":
    main()

import os
import sys
import vk_api
import random
from utils import get_dialogflow_response
from dotenv import load_dotenv
from logger import setup_logger
from vk_api.longpoll import VkLongPoll, VkEventType


def handle_message(event, api, project_id, lang_code, logger):
    session_id = event.user_id
    text = event.text
    if not text:
        return
    response_text = get_dialogflow_response(
        project_id, session_id, text, lang_code, allow_fallback=False)
    if response_text:
        try:
            api.messages.send(
                user_id=session_id,
                message=response_text,
                random_id=random.randint(1, 1000)
            )
        except Exception as e:
            logger.exception(f"Ошибка VK API: {e}", file=sys.stderr)


def main():
    load_dotenv()

    log_bot_token = os.getenv("API_TELEGRAM_LOGGER")
    log_chat_id = os.getenv("LOGGER_CHAT_ID")
    if not log_bot_token or not log_chat_id:
        raise RuntimeError("Нет токена или chat_id для логгера")

    logger = setup_logger(__name__, log_bot_token, log_chat_id)

    token = os.getenv("VK_TOKEN")
    if not token:
        sys.exit("Нет vk token")

    project_id = os.getenv("PROJECT_DIALOGFLOW_ID")
    if not project_id:
        sys.exit("Нет id dialogflow")

    lang_code = "ru"

    vk_session = vk_api.VkApi(token=token)
    api = vk_session.get_api()
    logger.info("Bot started!")

    longpoll = VkLongPoll(vk_session)

    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me:
            handle_message(event, api, project_id, lang_code, logger)


if __name__ == "__main__":
    main()
